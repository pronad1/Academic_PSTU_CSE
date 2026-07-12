from __future__ import annotations

import math
import dataclasses
from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np
import matplotlib

matplotlib.use("Agg")  # safe for headless / script execution
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle


# ---------------------------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------------------------

@dataclass
class WindowConfig:
    """All parameters that define one simulation window."""
    name: str                  # e.g. "Window 1 (5x5)"
    size: float                # window is [0, size] x [0, size]
    n_nodes: int                # number of chase nodes, n_nodes >= 2
    total_minutes: float        # total simulated time for this window
    dt: float                   # FIXED step size for this window (minutes)
    velocities: List[float]     # one fixed speed per node, length n_nodes
    hit_radius: float           # collision distance threshold
    seed: int = 0                # RNG seed (controls zig-zag phase only)
    node_labels: List[str] = field(default_factory=list)

    def __post_init__(self):
        assert len(self.velocities) == self.n_nodes, \
            "velocities must have exactly n_nodes entries"
        if not self.node_labels:
            self.node_labels = [chr(ord("A") + i) for i in range(self.n_nodes)]
        self.steps = int(round(self.total_minutes / self.dt))


@dataclass
class SimulationResult:
    """Everything produced by running one WindowConfig through the simulator."""
    config: WindowConfig
    times: np.ndarray              # shape (steps+1,)
    positions: np.ndarray          # shape (steps+1, n_nodes, 2)
    active: np.ndarray             # shape (steps+1, n_nodes-1) bool, per-link
    collision_events: List[Tuple[float, int, int]]  # (time, chaser_idx, target_idx)
    total_collisions: int
    possible_links: int


# ---------------------------------------------------------------------------
# 2. Core simulation
# ---------------------------------------------------------------------------

def _initial_positions(cfg: WindowConfig) -> np.ndarray:
    """Place nodes evenly around a circle inside the window so they start
    spread apart (generalises the book's 'four corners of a square')."""
    n = cfg.n_nodes
    size = cfg.size
    margin = size * 0.12
    span = size - 2 * margin
    cx = cy = size / 2.0
    r = span / 2.15

    pos = np.zeros((n, 2))
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2
        pos[i, 0] = cx + r * math.cos(angle)
        pos[i, 1] = cy + r * math.sin(angle)
    return pos


def _reflect(value: float, size: float) -> float:
    """Reflect a coordinate back into [0, size] if it has gone past a wall."""
    if value < 0:
        return -value
    if value > size:
        return 2 * size - value
    return value


def run_simulation(cfg: WindowConfig) -> SimulationResult:
    """
    Run one window's serial chase to completion.

    IMPORTANT: the loop always runs for the FULL number of steps
    (cfg.steps), i.e. until cfg.total_minutes has elapsed. A collision
    on one chase link does NOT stop the simulation and does NOT stop the
    other links. It only:
        (a) gets logged once, with its time and which pair collided, and
        (b) marks that one link inactive, so the same pair cannot be
            "re-collided" and double-counted, while still letting the
            chaser node move passively for visualisation purposes? --
            No: once a link is inactive, we freeze that CHASER node in
            place (it has "caught" its target and stops), which matches
            the book's behaviour where a hit ends that particular chase.
    The TOTAL collision count for the window is only meaningful, and only
    reported, once the full time has run out.
    """
    n = cfg.n_nodes
    size = cfg.size
    rng = np.random.default_rng(cfg.seed)

    pos = _initial_positions(cfg)
    last = n - 1

    # zig-zag parameters for the last (evading) node
    zig_period = max(0.6, size / 11.0)
    zig_angle_base = rng.uniform(0, 2 * math.pi)
    zig_turn_rate = 0.55 + rng.uniform(0, 0.25)

    active = np.ones(n - 1, dtype=bool)   # True while link i (chaser i -> target i+1) is still live
    collision_events: List[Tuple[float, int, int]] = []

    steps = cfg.steps
    times = np.zeros(steps + 1)
    positions = np.zeros((steps + 1, n, 2))
    active_history = np.zeros((steps + 1, n - 1), dtype=bool)

    positions[0] = pos
    active_history[0] = active
    t = 0.0

    for s in range(1, steps + 1):
        new_pos = pos.copy()

        # --- last node: zig-zag motion, always moving regardless of anything else
        base_heading = zig_angle_base + t * zig_turn_rate
        sway = math.sin(t * (2 * math.pi / zig_period)) * 1.15
        heading = base_heading + sway
        v_last = cfg.velocities[last]
        new_pos[last, 0] += math.cos(heading) * v_last * cfg.dt
        new_pos[last, 1] += math.sin(heading) * v_last * cfg.dt

        # --- chasers: each one (if its link is still active) steers toward
        #     its target's CURRENT (pre-update) position, exactly like the
        #     book's pure-pursuit rule.
        for i in range(n - 2, -1, -1):
            if not active[i]:
                # this link already collided earlier -- the chaser stays
                # frozen at its catch point; do not move it further.
                continue
            tx, ty = pos[i + 1]
            dx, dy = tx - pos[i, 0], ty - pos[i, 1]
            dist = math.hypot(dx, dy)
            if dist < 1e-9:
                continue
            ux, uy = dx / dist, dy / dist
            v = cfg.velocities[i]
            new_pos[i, 0] += ux * v * cfg.dt
            new_pos[i, 1] += uy * v * cfg.dt

        # --- reflect off walls
        for i in range(n):
            new_pos[i, 0] = _reflect(new_pos[i, 0], size)
            new_pos[i, 1] = _reflect(new_pos[i, 1], size)

        pos = new_pos
        t += cfg.dt

        # --- collision check: only for links still active.
        #     THE SIMULATION DOES NOT STOP HERE. We simply record the hit,
        #     deactivate that one link, and keep looping until s == steps.
        for i in range(n - 1):
            if active[i]:
                d = math.hypot(pos[i, 0] - pos[i + 1, 0], pos[i, 1] - pos[i + 1, 1])
                if d <= cfg.hit_radius:
                    active[i] = False
                    collision_events.append((t, i, i + 1))

        times[s] = t
        positions[s] = pos
        active_history[s] = active

    total_collisions = len(collision_events)  # only counted/reported AFTER full run
    return SimulationResult(
        config=cfg,
        times=times,
        positions=positions,
        active=active_history,
        collision_events=collision_events,
        total_collisions=total_collisions,
        possible_links=n - 1,
    )


# ---------------------------------------------------------------------------
# 3. Window definitions (edit these to change the scenario)
# ---------------------------------------------------------------------------

WINDOWS: List[WindowConfig] = [
    WindowConfig(
        name="Window 1 (5x5)",
        size=5,
        n_nodes=4,
        total_minutes=4,
        dt=0.01,
        velocities=[1.8, 1.6, 1.4, 2.0],
        hit_radius=0.15,
        seed=11,
    ),
    WindowConfig(
        name="Window 2 (9x9)",
        size=9,
        n_nodes=5,
        total_minutes=9,
        dt=0.015,
        velocities=[1.5, 1.3, 1.15, 1.0, 1.7],
        hit_radius=0.18,
        seed=22,
    ),
    WindowConfig(
        name="Window 3 (16x16)",
        size=16,
        n_nodes=8,
        total_minutes=13,
        dt=0.02,
        velocities=[2.2, 2.0, 1.85, 1.7, 1.55, 1.4, 1.25, 2.5],
        hit_radius=0.28,
        seed=33,
    ),
]


# ---------------------------------------------------------------------------
# 4. Reporting
# ---------------------------------------------------------------------------

def print_report(result: SimulationResult) -> None:
    cfg = result.config
    print("=" * 70)
    print(cfg.name)
    print("-" * 70)
    print(f"  window size       : {cfg.size} x {cfg.size}")
    print(f"  nodes             : {cfg.n_nodes}  ({', '.join(cfg.node_labels)})")
    print(f"  chase order       : " +
          " -> ".join(cfg.node_labels[:-1]) +
          f" -> {cfg.node_labels[-1]} (zig-zag, not chased target)")
    print(f"  total run time    : {cfg.total_minutes} min")
    print(f"  fixed step (dt)   : {cfg.dt} min")
    print(f"  speeds            : " +
          ", ".join(f"{lbl}={v}" for lbl, v in zip(cfg.node_labels, cfg.velocities)))
    print(f"  hit radius        : {cfg.hit_radius} units")
    print(f"  steps simulated   : {cfg.steps}  (ran to completion, no early stop)")
    print()
    if result.collision_events:
        print("  Collision log (simulation kept running after each one):")
        for (t, chaser_i, target_i) in result.collision_events:
            print(f"    t = {t:6.3f} min   {cfg.node_labels[chaser_i]} caught "
                  f"{cfg.node_labels[target_i]}")
    else:
        print("  No collisions occurred during this window's full run.")
    print()
    print(f"  TOTAL COLLISIONS FOR THIS WINDOW (after full {cfg.total_minutes} "
          f"min run): {result.total_collisions} / {result.possible_links} "
          f"possible chase links")
    print("=" * 70)
    print()


def print_grand_summary(results: List[SimulationResult]) -> None:
    print("#" * 70)
    print("GRAND SUMMARY -- all windows")
    print("#" * 70)
    grand_total = 0
    for r in results:
        grand_total += r.total_collisions
        print(f"  {r.config.name:18s} : {r.total_collisions} / {r.possible_links} "
              f"collisions over {r.config.total_minutes} min "
              f"(dt={r.config.dt}, {r.config.n_nodes} nodes)")
    total_minutes = sum(r.config.total_minutes for r in results)
    print("-" * 70)
    print(f"  TOTAL COLLISIONS ACROSS ALL WINDOWS: {grand_total}")
    print(f"  TOTAL SIMULATED TIME ACROSS ALL WINDOWS: {total_minutes} min")
    print("#" * 70)


# ---------------------------------------------------------------------------
# 5. Static plot: full traced paths + collision markers
# ---------------------------------------------------------------------------

NODE_COLORS = [
    "#3fb6ff", "#3ddc97", "#ffb454", "#ff5d5d",
    "#c792ea", "#5dd5ff", "#ff9f43", "#ff6b9d",
]


def plot_paths(result: SimulationResult, save_path: str) -> None:
    cfg = result.config
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_facecolor("#0a0f15")
    fig.patch.set_facecolor("#0d1117")

    ax.add_patch(Rectangle((0, 0), cfg.size, cfg.size, fill=False,
                            edgecolor="#3a4555", linewidth=2))
    ax.set_xlim(-0.5, cfg.size + 0.5)
    ax.set_ylim(-0.5, cfg.size + 0.5)
    ax.set_aspect("equal")
    ax.grid(True, color="#1c2530", linewidth=0.6)
    ax.tick_params(colors="#8b98a9")
    for spine in ax.spines.values():
        spine.set_color("#2a3441")

    for i in range(cfg.n_nodes):
        color = NODE_COLORS[i % len(NODE_COLORS)]
        xs = result.positions[:, i, 0]
        ys = result.positions[:, i, 1]
        ax.plot(xs, ys, color=color, linewidth=1.4, alpha=0.85,
                 label=cfg.node_labels[i])
        ax.plot(xs[0], ys[0], "o", color=color, markersize=7,
                 markeredgecolor="#0a0f15", markeredgewidth=1.2)
        ax.plot(xs[-1], ys[-1], "s", color=color, markersize=7,
                 markeredgecolor="#0a0f15", markeredgewidth=1.2)

    for (t, chaser_i, target_i) in result.collision_events:
        step_idx = int(round(t / cfg.dt))
        cx, cy = result.positions[step_idx, target_i]
        ax.plot(cx, cy, "x", color="#ff5d5d", markersize=13, markeredgewidth=3)
        ax.annotate(f"t={t:.2f}", (cx, cy), textcoords="offset points",
                     xytext=(6, 6), fontsize=8, color="#ff5d5d")

    ax.set_title(
        f"{cfg.name} -- {result.total_collisions}/{result.possible_links} "
        f"collisions over {cfg.total_minutes} min",
        color="#e6edf3", fontsize=12,
    )
    legend = ax.legend(loc="upper right", fontsize=8, framealpha=0.2)
    for text in legend.get_texts():
        text.set_color("#e6edf3")

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  saved static plot -> {save_path}")


# ---------------------------------------------------------------------------
# 6. Animation: live chase
# ---------------------------------------------------------------------------

def animate_window(result: SimulationResult, save_path: str,
                    fps: int = 30, playback_speedup: int = 4) -> None:
    """
    Render an animated view of the chase. `playback_speedup` controls how
    many simulated steps advance per rendered frame, so long simulations
    (thousands of steps) don't produce absurdly long videos.
    """
    cfg = result.config
    n_steps = result.positions.shape[0]
    frame_indices = list(range(0, n_steps, playback_speedup))
    if frame_indices[-1] != n_steps - 1:
        frame_indices.append(n_steps - 1)

    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    ax.set_facecolor("#0a0f15")
    fig.patch.set_facecolor("#0d1117")
    ax.add_patch(Rectangle((0, 0), cfg.size, cfg.size, fill=False,
                            edgecolor="#3a4555", linewidth=2))
    ax.set_xlim(-0.5, cfg.size + 0.5)
    ax.set_ylim(-0.5, cfg.size + 0.5)
    ax.set_aspect("equal")
    ax.grid(True, color="#1c2530", linewidth=0.6)
    ax.tick_params(colors="#8b98a9")
    for spine in ax.spines.values():
        spine.set_color("#2a3441")

    trail_lines = []
    point_markers = []
    labels = []
    for i in range(cfg.n_nodes):
        color = NODE_COLORS[i % len(NODE_COLORS)]
        line, = ax.plot([], [], color=color, linewidth=1.3, alpha=0.7)
        point, = ax.plot([], [], "o", color=color, markersize=9,
                          markeredgecolor="#0a0f15", markeredgewidth=1.4)
        text = ax.text(0, 0, cfg.node_labels[i], color="#e6edf3", fontsize=9,
                        fontweight="bold", ha="center", va="bottom")
        trail_lines.append(line)
        point_markers.append(point)
        labels.append(text)

    title = ax.set_title("", color="#e6edf3", fontsize=11)
    collision_text = ax.text(
        0.02, 0.02, "", transform=ax.transAxes, color="#ff5d5d",
        fontsize=9, va="bottom", ha="left",
    )

    def update(frame_no):
        idx = frame_indices[frame_no]
        t = result.times[idx]
        for i in range(cfg.n_nodes):
            xs = result.positions[: idx + 1, i, 0]
            ys = result.positions[: idx + 1, i, 1]
            trail_lines[i].set_data(xs, ys)
            point_markers[i].set_data([xs[-1]], [ys[-1]])
            labels[i].set_position((xs[-1], ys[-1] + cfg.size * 0.02))
            if i < cfg.n_nodes - 1 and not result.active[idx, i]:
                point_markers[i].set_alpha(0.4)
            else:
                point_markers[i].set_alpha(1.0)

        collisions_so_far = sum(1 for (ct, _, _) in result.collision_events if ct <= t)
        title.set_text(f"{cfg.name} -- t = {t:.2f} / {cfg.total_minutes:.2f} min")
        collision_text.set_text(
            f"collisions so far: {collisions_so_far} / {result.possible_links}"
        )
        return trail_lines + point_markers + labels + [title, collision_text]

    anim = animation.FuncAnimation(
        fig, update, frames=len(frame_indices), interval=1000 / fps, blit=False
    )

    try:
        writer = animation.PillowWriter(fps=fps)
        anim.save(save_path, writer=writer)
        print(f"  saved animation -> {save_path}")
    except Exception as exc:
        print(f"  [warning] could not save animation ({exc}); skipping.")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 7. Main
# ---------------------------------------------------------------------------

def main(make_plots: bool = True, make_animations: bool = True,
         output_dir: str = ".") -> List[SimulationResult]:
    results = []
    for cfg in WINDOWS:
        result = run_simulation(cfg)
        results.append(result)
        print_report(result)

        if make_plots:
            safe_name = cfg.name.lower().replace(" ", "_").replace("(", "").replace(")", "")
            plot_paths(result, f"{output_dir}/{safe_name}_paths.png")

        if make_animations:
            safe_name = cfg.name.lower().replace(" ", "_").replace("(", "").replace(")", "")
            speedup = max(1, cfg.steps // 250)
            animate_window(result, f"{output_dir}/{safe_name}_animation.gif",
                            fps=25, playback_speedup=speedup)

    print_grand_summary(results)
    return results


if __name__ == "__main__":
    main(make_plots=True, make_animations=True, output_dir=".")