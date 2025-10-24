**Checkers-AI**

This project explores strategic AI agents in an extended 16x16 Checkers game with unique rule modifications.

**Key Features**

🧩 **Multiple AI Algorithms:**

Minimax, Alpha-Beta Pruning, and Reinforcement Learning via Q-Learning.

♟️ **Special Rules:**

To make the gameplay more dynamic and challenging for the AI agents, we added several custom rules:
- All pieces can move forward and backward
- King promotion after 2 captures (not necessarily in one turn)
- Kings can move up to 4 diagonal steps
- Turn skipped after 30 seconds of inactivity
- Pieces can skip 1–2 diagonal blocks if valid

🎮 **Game Modes**

The project includes multiple playable modes, each defined in a separate Python file:
| File Name  | Description                    |
| ---------- | ------------------------------ |
| `main.py`  | Human vs Minimax AI            |
| `main2.py` | Human vs Alpha-Beta AI         |
| `main3.py` | Human vs Q-Learning AI         |
| `main4.py` | Minimax AI vs Alpha-Beta AI    |
| `main5.py` | Alpha-Beta AI vs Q-Learning AI |

