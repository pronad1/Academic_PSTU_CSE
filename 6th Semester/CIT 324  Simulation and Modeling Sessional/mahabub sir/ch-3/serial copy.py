import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---------- প্যারামিটার ----------
N = 10                 # মোট কণা
K = 10.0               # মোট সময় (মিনিট)
DT = 0.1               # সময়ের ধাপ
STEP_SIZE = 0.5        # প্রতি ধাপে সরণ
COLLISION_RADIUS = 0.3 # সংঘর্ষের ব্যাসার্ধ

WINDOWS = [
    (5.0, 5.0),
    (10.0, 10.0),
    (15.0, 15.0),
    (20.0, 20.0),
    (25.0, 25.0),
]

n_steps = int(K / DT)
seed = 42

# ১০টি কণার জন্য আলাদা রং (tab10 কালারম্যাপ)
particle_colors = plt.cm.tab10(np.linspace(0, 1, N))

# ---------- সিমুলেশন ফাংশন (শুধু এলোমেলো চলন) ----------
def simulate(width, height, n_particles, n_steps, step_size,
             collision_radius, seed=None, record_history=False):
    if seed is not None:
        np.random.seed(seed)

    positions = np.random.uniform(0, [width, height], size=(n_particles, 2))
    cumulative = []
    collision_count = 0

    history = [] if record_history else None
    collision_points = [] if record_history else None

    for _ in range(n_steps):
        new_pos = positions.copy()

        for i in range(n_particles):
            angle = np.random.uniform(0, 2 * np.pi)
            displacement = step_size * np.array([np.cos(angle), np.sin(angle)])
            new_pos[i] = positions[i] + displacement

        # সীমানা প্রতিফলন
        mask = new_pos[:, 0] < 0
        new_pos[mask, 0] = -new_pos[mask, 0]
        mask = new_pos[:, 0] > width
        new_pos[mask, 0] = 2 * width - new_pos[mask, 0]
        mask = new_pos[:, 1] < 0
        new_pos[mask, 1] = -new_pos[mask, 1]
        mask = new_pos[:, 1] > height
        new_pos[mask, 1] = 2 * height - new_pos[mask, 1]

        positions = new_pos

        if record_history:
            history.append(positions.copy())
            for i in range(n_particles):
                for j in range(i+1, n_particles):
                    if np.linalg.norm(positions[i] - positions[j]) < collision_radius:
                        collision_points.append((positions[i].copy(), positions[j].copy()))

        for i in range(n_particles):
            for j in range(i+1, n_particles):
                if np.linalg.norm(positions[i] - positions[j]) < collision_radius:
                    collision_count += 1
        cumulative.append(collision_count)

    if record_history:
        return collision_count, cumulative, history, collision_points
    else:
        return collision_count, cumulative

# ---------- সিমুলেশন চালানো (সব উইন্ডোর জন্য) ----------
results = {}
for idx, (w, h) in enumerate(WINDOWS, start=1):
    total, cum, history, collision_points = simulate(
        w, h, N, n_steps, STEP_SIZE, COLLISION_RADIUS,
        seed=seed, record_history=True
    )
    results[f'Window {idx} ({w:.1f}x{h:.1f})'] = {
        'total': total,
        'cumulative': cum,
        'history': history,
        'collision_points': collision_points,
        'area': w*h,
        'dims': (w,h)
    }

# ---------- প্লট ১: ক্রমযোজিত সংঘর্ষ ----------
fig1, ax1 = plt.subplots(figsize=(10,6))
time = np.arange(n_steps)*DT
colors = plt.cm.viridis(np.linspace(0,1,len(WINDOWS)))
for (label, data), color in zip(results.items(), colors):
    ax1.plot(time, data['cumulative'], label=label, lw=2, color=color)
ax1.set_xlabel('Time (minutes)')
ax1.set_ylabel('Cumulative collisions')
ax1.set_title('Collision buildup for all windows')
ax1.legend()
ax1.grid(True, alpha=0.3)
fig1.tight_layout()

# ---------- প্লট ২: স্তম্ভচিত্র (মোট সংঘর্ষ) ----------
fig2, ax2 = plt.subplots(figsize=(10,6))
labels = list(results.keys())
totals = [data['total'] for data in results.values()]
bars = ax2.bar(labels, totals, color=colors)
ax2.set_ylabel('Total collisions')
ax2.set_title('Final collision count')
ax2.tick_params(axis='x', rotation=20)
for bar in bars:
    h = bar.get_height()
    ax2.text(bar.get_x()+bar.get_width()/2., h+0.5, f'{int(h)}', ha='center', va='bottom')
ax2.grid(True, alpha=0.3, axis='y')
fig2.tight_layout()

# ---------- প্লট ৩: কণার গতিপথ (সব উইন্ডো) প্রতিটি কণার জন্য আলাদা রং ----------
fig3, axes = plt.subplots(2, 3, figsize=(15,10))
axes_flat = axes.flatten()

for ax, (label, data) in zip(axes_flat, results.items()):
    w, h = data['dims']
    history = data['history']
    collision_points = data['collision_points']

    positions_array = np.array(history)
    for p in range(N):
        x = positions_array[:, p, 0]
        y = positions_array[:, p, 1]
        ax.plot(x, y, color=particle_colors[p], alpha=0.5, linewidth=0.8)

    if collision_points:
        all_pts = []
        for p1, p2 in collision_points:
            all_pts.append(p1)
            all_pts.append(p2)
        all_pts = np.array(all_pts)
        ax.scatter(all_pts[:,0], all_pts[:,1], color='red', s=15,
                   label=f'{len(collision_points)} collisions')
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'No collisions', transform=ax.transAxes,
                ha='center', va='center')

    ax.set_title(f'{label}  (total {data["total"]} coll.)')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_aspect('equal')
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.grid(True, alpha=0.2)

axes_flat[-1].set_visible(False)
fig3.tight_layout()

# ---------- অ্যানিমেশন (প্রথম উইন্ডো: ৫x৫) প্রতিটি কণার জন্য আলাদা রং ----------
first_key = list(results.keys())[0]
data1 = results[first_key]
w1, h1 = data1['dims']
history1 = np.array(data1['history'])          # (n_steps, N, 2)
collision_pts = data1['collision_points']      # list of tuples

fig_anim, ax_anim = plt.subplots(figsize=(6,6))
ax_anim.set_xlim(0, w1)
ax_anim.set_ylim(0, h1)
ax_anim.set_aspect('equal')
ax_anim.set_title(f'Animation: {first_key}')
ax_anim.grid(True, alpha=0.3)

# প্রথম ফ্রেমের অবস্থান দিয়ে স্ক্যাটার তৈরি করি (যাতে x,y-এর সাইজ N হয়)
init_pos = history1[0]  # (N,2)
scat_all = ax_anim.scatter(init_pos[:,0], init_pos[:,1], 
                           s=30, c=particle_colors, alpha=0.7, label='Random walkers')
# সংঘর্ষ বিন্দু (লাল তারকা)
scat_coll = ax_anim.scatter([], [], s=80, color='red', marker='*', label='Collision')
ax_anim.legend()

def update(frame):
    positions = history1[frame]          # (N,2)
    scat_all.set_offsets(positions)      # অবস্থান আপডেট, রং অপরিবর্তিত

    # সংঘর্ষ বিন্দু (সবগুলো একসাথে দেখানো হচ্ছে)
    if collision_pts:
        pts = np.array([p1 for p1, _ in collision_pts] + [p2 for _, p2 in collision_pts])
        scat_coll.set_offsets(pts)
    else:
        scat_coll.set_offsets([])
    return [scat_all, scat_coll]

ani = FuncAnimation(fig_anim, update, frames=n_steps, interval=50, blit=True)

plt.show()