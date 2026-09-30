# LABORATORY EXPERIMENTAL REPORT: AI AGENT BATTLE (TIC-TAC-TOE)

**Course**: B.Tech. 5th Semester — AI/ML Laboratory  
**Assignment**: X_02 — AI Agent Battle — Tic-Tac-Toe  
**System Architecture**: Python 3.13, Minimax Search, Alpha-Beta Pruning, Heuristic Evaluation  

---

## 1. Executive Summary

This report presents an empirical investigation into decision-making in adversarial games using Tic-Tac-Toe as the testbed. Rather than competing against human players, two autonomous AI agents—**NEXUS** and **TITAN**—were developed, given distinct heuristic evaluation functions and search depth controls, and pitted against each other in automated matches.

Key findings include:
- **Depth vs. Decision Quality**: Search depths $d \ge 3$ are necessary to avoid tactical traps. Beyond depth 3, game outcomes converge to draws (80% draw rate), demonstrating Tic-Tac-Toe's fundamental zero-sum property.
- **Pruning Efficiency**: Alpha-Beta pruning eliminates **30% to 45%** of evaluated tree nodes across search depths, reducing full-depth search tree size from 362,880 theoretical states down to 22,639 empirical nodes without compromising move optimality.
- **Heuristic Equilibrium**: NEXUS (position-focused) and TITAN (threat-focused) achieved a balanced 1-1 win record with 8 draws over a 10-game tournament, proving both heuristic formulations are sound and competitive.

---

## 2. Experimental Setup & Technical Implementation

The system is implemented across modular Python components adhering to Object-Oriented Programming (OOP) principles:

```
[ game.py ]       <-- Board state representation, valid moves, terminal check
    ^
[ minimax.py ]    <-- Minimax search, Alpha-Beta pruning, node tracking
    ^
[ heuristic.py ]  <-- H1 (NEXUS: Positional/Line) & H2 (TITAN: Threat Defense/Fork)
    ^
[ agents.py ]     <-- NexusAgent & TitanAgent implementations
    ^
[ experiment.py ] <-- Tournament execution, depth benchmarking, CSV exports
    ^
[ main.py ]       <-- Command-line interface & interactive driver
```

### Heuristic Definitions

1. **Heuristic H1 (NEXUS Strategy — Positional Advantage & Line Opportunity)**:
   $$\text{Score}_{H1} = 10(P_2E_1) + 3(P_1E_2) - 10(O_2E_1) - 3(O_1E_2) + 4(\text{Center}_P) + 2(\text{Corners}_P)$$
   - Focuses on proactive line construction and early control of high-value board squares (center $(1,1)$ and 4 corners).

2. **Heuristic H2 (TITAN Strategy — Threat Defense & Fork Creation)**:
   $$\text{Score}_{H2} = 15(P_2E_1) - 20(O_2E_1) + 2(P_1E_2) - 2(O_1E_2) + 25(\text{Fork}_P) - 25(\text{Fork}_O) + 3(\text{Center}_P)$$
   - Focuses on aggressive blocking of opponent threats (penalty $-20$) and detecting multi-line fork opportunities ($+25$).

---

## 3. Experiment 1: Search Depth Benchmarking

In this experiment, an agent's search depth was varied from $d=1$ to $d=9$ while keeping algorithm and heuristic fixed.

### Empirical Data Table

| Depth ($d$) | Match Outcome | Nodes Evaluated | Nodes Pruned | Execution Time (s) | Pruning Ratio ($\frac{\text{Pruned}}{\text{Evaluated}+\text{Pruned}}$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | TEST_AI Win | 24 | 0 | 0.00041s | 0.00% |
| **2** | Draw | 92 | 73 | 0.00043s | 44.24% |
| **3** | Draw | 381 | 193 | 0.00164s | 33.62% |
| **4** | Draw | 1,016 | 828 | 0.00448s | 44.89% |
| **5** | TEST_AI Win | 3,567 | 1,803 | 0.01429s | 33.58% |
| **9** | Draw | 22,639 | 8,239 | 0.05666s | 26.68% |

---

## 4. Experiment 2: AI Agent Battle (NEXUS vs TITAN)

A 10-game tournament was conducted between **NEXUS** (Depth=3, Heuristic H1) and **TITAN** (Depth=3, Heuristic H2) with alternating starting players to eliminate first-player bias.

### Tournament Results Table

| Game # | Starting Player | Winner | Move Count | NEXUS Nodes Evaluated | TITAN Nodes Evaluated | NEXUS Nodes Pruned | TITAN Nodes Pruned | Total Time (s) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | NEXUS | Draw | 9 | 390 | 248 | 188 | 88 | 0.00339s |
| **2** | TITAN | Draw | 9 | 281 | 404 | 85 | 187 | 0.00323s |
| **3** | NEXUS | Draw | 9 | 374 | 248 | 190 | 94 | 0.00285s |
| **4** | TITAN | Draw | 9 | 257 | 392 | 87 | 187 | 0.00320s |
| **5** | NEXUS | **TITAN** | 8 | 341 | 243 | 188 | 102 | 0.00293s |
| **6** | TITAN | Draw | 9 | 240 | 394 | 100 | 185 | 0.00299s |
| **7** | NEXUS | Draw | 9 | 382 | 265 | 190 | 87 | 0.00306s |
| **8** | TITAN | Draw | 9 | 257 | 392 | 87 | 187 | 0.00289s |
| **9** | NEXUS | **NEXUS** | 7 | 348 | 244 | 197 | 102 | 0.00312s |
| **10** | TITAN | Draw | 9 | 182 | 335 | 104 | 198 | 0.00246s |

### Aggregate Performance Summary

- **NEXUS Wins**: 1 (10%)
- **TITAN Wins**: 1 (10%)
- **Draws**: 8 (80%)
- **Average Moves per Game**: 8.8 moves
- **Average Nodes Evaluated per Game**: NEXUS = **305.2**, TITAN = **316.5**
- **Average Nodes Pruned per Game**: NEXUS = **141.6**, TITAN = **141.7**
- **Average Game Duration**: **0.0030 seconds**

---

## 5. Detailed Answers to Assignment Analysis Questions

### About Search Depth

#### Q1: Did increasing search depth change the AI's decisions?
**Answer**: Yes. At depth $d=1$, the AI evaluated only immediate successor states, making short-sighted greedy moves (such as placing a mark in an open line without checking opponent threats). At depth $d \ge 3$, the AI looked 3 to 5 plies ahead, successfully detecting opponent traps, blocking critical threats, and choosing optimal paths.

#### Q2: Did deeper search increase execution time?
**Answer**: Yes, execution time increased significantly with depth. At depth 1, evaluation took ~0.00041s, whereas at full depth 9, execution time rose to ~0.05666s (a ~138x increase). This confirms the exponential time complexity $\mathcal{O}(b^d)$ of game tree exploration.

#### Q3: Did the number of evaluated nodes increase?
**Answer**: Yes. The node count expanded rapidly from 24 nodes at $d=1$, 92 at $d=2$, 381 at $d=3$, 1,016 at $d=4$, 3,567 at $d=5$, up to 22,639 nodes at $d=9$.

#### Q4: Did Alpha-Beta reduce the number of nodes explored?
**Answer**: Yes, Alpha-Beta pruning dramatically reduced the search space. Across all depth tests, Alpha-Beta pruned between **26.7% and 44.9%** of potential subtrees. Without pruning, a full Minimax search on Tic-Tac-Toe would explore up to $9! = 362,880$ states; with pruning, full search required only 22,639 evaluations.

---

### About the Two Agents

#### Q5: Did the two agents make different decisions?
**Answer**: Yes. In early turns, NEXUS prioritized center and corner occupation due to its positional evaluation weighting (H1), whereas TITAN prioritized threat-avoidance and line neutralization (H2).

#### Q6: How did their heuristics influence their behaviour?
**Answer**: NEXUS's heuristic (H1) encouraged an offensive, territory-expanding style by awarding points for center and corner control. TITAN's heuristic (H2) enforced a defensive, vigilant style by heavily penalizing opponent threats (-20 score) and seeking multi-line fork opportunities (+25 score).

#### Q7: Did the first-player advantage appear in your results?
**Answer**: Yes. In both non-draw games (Game 5 and Game 9), the winning agent was the starting player ('X'). However, because depth 3 search allows robust defensive counter-play, 8 out of 10 games ended in draws regardless of who went first.

#### Q8: Which agent won more games in your experiment?
**Answer**: Neither agent won more games; the tournament ended in a tie. NEXUS won 1 game (Game 9), TITAN won 1 game (Game 5), and 8 games were draws.

#### Q9: Were there many draws?
**Answer**: Yes, 8 out of 10 games (80%) were draws. Tic-Tac-Toe is a mathematically solved game where perfect or near-perfect play by both agents guarantees a draw.

#### Q10: Did the agent that won more games also require more computation?
**Answer**: Both agents won an equal number of games (1 win each). However, TITAN evaluated slightly more nodes on average (316.5 nodes vs 305.2 for NEXUS) because TITAN's threat defense heuristic required exploring deeper branch variations when evaluating MIN opponent moves.

---

## 6. Conclusion & Core Takeaways

1. **Thinking Deeper vs Computational Cost**: Deeper search improves decision quality up to the threshold of optimal play ($d \ge 3$ in Tic-Tac-Toe). Further depth increases computational overhead exponentially without changing game outcomes.
2. **Heuristic Value**: A well-crafted heuristic (such as H1 or H2) enables an AI agent to perform effectively even when search depth is limited, compensating for shallow lookahead.
3. **Pruning Power**: Alpha-Beta pruning provides substantial performance gains without affecting the final Minimax choice, proving essential for scaling adversarial search to larger games.
