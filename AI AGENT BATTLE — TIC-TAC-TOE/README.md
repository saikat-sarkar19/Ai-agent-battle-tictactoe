# AI Agent Battle — Tic-Tac-Toe Laboratory

**Course**: B.Tech. 5th Semester — AI/ML Laboratory  
**Assignment**: X_02 — AI Agent Battle: Tic-Tac-Toe  
**Language**: Python 3.13  

---

## 📌 Project Overview

This project implements an autonomous AI-vs-AI Tic-Tac-Toe system. Rather than building a program for human gameplay, two intelligent AI agents—**NEXUS** and **TITAN**—compete against each other. Both agents utilize the **Minimax search algorithm with Alpha-Beta pruning**, but employ distinct **heuristic evaluation functions** and configurable **search depth limits**.

The system collects empirical metrics across multiple game parameters to answer three core questions:
1. **Does thinking deeper make an AI better?**
2. **How does the way an AI evaluates a position affect its decisions?**
3. **What is the computational cost of making an AI think more?**

---

## 🏗️ System Architecture & File Structure

The project strictly follows a modular Object-Oriented Programming (OOP) design as required by Part 14 & Part 16 of the specification:

```
ai-agent-battle/
├── game.py                 # Board representation (3x3), move logic, win/draw checking
├── minimax.py              # Minimax search engine with Alpha-Beta pruning & tie-breaking
├── heuristic.py            # Heuristic functions H1 (NEXUS) and H2 (TITAN)
├── agents.py               # Agent base class, NexusAgent, and TitanAgent implementations
├── experiment.py           # Experiment runner for 10-game battle & depth benchmarks
├── main.py                 # Command-line interface (CLI) entry point
├── results/
│   ├── results.csv         # 10-game tournament records
│   ├── depth_experiment.csv# Search depth benchmarking metrics
│   └── summary.json        # Aggregate performance summary statistics
├── README.md               # Quick-start guide & architectural overview
└── REPORT.md               # Detailed experimental analysis & laboratory report
```

---

## 🤖 Agent Profiles

| Agent Name | Search Algorithm | Search Depth | Heuristic Strategy | Key Focus |
| :--- | :--- | :--- | :--- | :--- |
| **NEXUS** | Minimax + Alpha-Beta | Configurable (Default: 3) | **H1 (Positional & Line Opportunity)** | Center/Corner control, open winning line development, balanced positional pressure. |
| **TITAN** | Minimax + Alpha-Beta | Configurable (Default: 3) | **H2 (Threat Defense & Fork Detection)** | Aggressive blocking of opponent 2-in-a-row threats, multi-threat (fork) creation. |

---

## 🚀 How to Run the System

### Prerequisites
- Python 3.8+ (No external third-party dependencies required; uses Python standard library).

### Quick Execution Commands

1. **Run Full Benchmark Suite (Depth Experiment + 10-Game Battle)**:
   ```bash
   python main.py --mode all
   ```

2. **Run 10-Game AI Battle Only**:
   ```bash
   python main.py --mode battle --nexus-depth 3 --titan-depth 3
   ```

3. **Run Search Depth Sensitivity Experiment Only**:
   ```bash
   python main.py --mode depth
   ```

4. **Launch Interactive CLI Menu & Human vs AI Mode**:
   ```bash
   python main.py --mode interactive
   ```

---

## 📊 Summary of Experimental Results

### Experiment 1: Search Depth Benchmarking (TEST_AI vs REF_AI)

| Search Depth | Outcome | Nodes Evaluated | Nodes Pruned | Execution Time (s) | Pruning Efficiency |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | TEST_AI Win | 24 | 0 | 0.00041s | 0.0% |
| **2** | Draw | 92 | 73 | 0.00043s | 44.2% |
| **3** | Draw | 381 | 193 | 0.00164s | 33.6% |
| **4** | Draw | 1,016 | 828 | 0.00448s | 44.9% |
| **5** | TEST_AI Win | 3,567 | 1,803 | 0.01429s | 33.6% |
| **9** (Full) | Draw | 22,639 | 8,239 | 0.05666s | 26.7% |

### Experiment 2: AI Agent Battle (NEXUS Depth=3 vs TITAN Depth=3)

- **Total Games Played**: 10 (Alternating starting player: Games 1,3,5,7,9 = NEXUS starts; Games 2,4,6,8,10 = TITAN starts)
- **NEXUS Wins**: 1 (Game 9)
- **TITAN Wins**: 1 (Game 5)
- **Draws**: 8
- **Average Moves per Game**: 8.8
- **Average Nodes Evaluated**: NEXUS = **305.2**, TITAN = **316.5**
- **Average Nodes Pruned**: NEXUS = **141.6**, TITAN = **141.7**
- **Average Game Execution Time**: **0.0030 seconds**

---

## 💡 Key Observations & Findings

1. **Impact of Depth**: Increasing search depth exponentially increases node evaluations and execution time. At depth $\ge 3$, both agents achieve near-optimal defensive play in Tic-Tac-Toe, leading to a high proportion of draws (80%).
2. **Alpha-Beta Efficiency**: Alpha-Beta pruning reduces node evaluation count by **30% to 45%**, significantly accelerating tree search without altering the optimal move choices.
3. **Heuristic Influence**: NEXUS (H1) favors strategic center/corner positioning, whereas TITAN (H2) prioritizes threat blocking. In equal-depth matches, neither agent dominates, resulting in a balanced 1-1 win record and 8 draws.

---

## 📄 Documentation Deliverables

For an in-depth evaluation answering all 10 laboratory questions, detailed tables, time complexity proofs, and complete analysis, please consult [REPORT.md](file:///c:/Users/sarka/Documents/AI-ML%20ASSIGNMENTS/AI%20AGENT%20BATTLE%20%E2%80%94%20TIC-TAC-TOE/REPORT.md).
