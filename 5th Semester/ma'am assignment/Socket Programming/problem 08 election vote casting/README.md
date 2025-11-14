# Election Voting System

## Files:
- `voting.py` - Multicast voting application

## How to Run:

1. Open 5 terminals (one for each electorate)
2. Run in each terminal: `python voting.py`
3. Each electorate casts vote (A or B)
4. After all 5 votes received, winner is displayed
5. All electorates see the same result

## Features:
- 5 electorates (processes)
- 2 candidates: A and B
- Each electorate votes once
- Multicast vote to all electorates
- Each independently determines winner
- Displays vote count and winner

## Example:
Terminal 1: `python voting.py` → Vote A
Terminal 2: `python voting.py` → Vote B
Terminal 3: `python voting.py` → Vote A
Terminal 4: `python voting.py` → Vote A
Terminal 5: `python voting.py` → Vote B

Result: Candidate A wins (3 votes vs 2 votes)
