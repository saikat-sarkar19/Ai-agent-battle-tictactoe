"""
experiment.py - Experiment Runner & Statistics Collection

This module implements experimental procedures for:
  1. Search Depth Sensitivity Experiment (Depth 1, 2, 3, 4, 5, 9)
  2. 10-Game AI Agent Battle Tournament (NEXUS vs TITAN)
  3. Automatic statistics collection and CSV export to results/ directory.
"""

import os
import csv
import json
import time
from typing import List, Dict, Any, Tuple
from game import TicTacToe
from agents import Agent, NexusAgent, TitanAgent
from heuristic import heuristic_h1_nexus, heuristic_h2_titan


class Experiment:
    """
    Manages match execution, tournament simulations, statistics aggregation,
    and CSV/JSON results export.
    """

    def __init__(self, output_dir: str = "results"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def run_single_game(
        self,
        agent1: Agent,
        agent2: Agent,
        agent1_starts: bool = True,
        verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Run a single AI-vs-AI Tic-Tac-Toe game.

        Args:
            agent1: First agent instance.
            agent2: Second agent instance.
            agent1_starts: If True, agent1 is assigned 'X' and plays first.
            verbose: If True, prints step-by-step board states.

        Returns:
            Dictionary containing game performance metrics.
        """
        board = TicTacToe()
        agent1.reset_stats()
        agent2.reset_stats()

        if agent1_starts:
            first_agent = agent1
            second_agent = agent2
        else:
            first_agent = agent2
            second_agent = agent1

        first_agent.set_mark(TicTacToe.PLAYER_X)
        second_agent.set_mark(TicTacToe.PLAYER_O)

        current_turn = first_agent
        move_count = 0
        game_start_time = time.perf_counter()

        if verbose:
            print(f"\n--- Game Started: {first_agent.name} ('X') vs {second_agent.name} ('O') ---")
            board.print_board()

        while not board.is_terminal():
            move = current_turn.choose_move(board)
            board.make_move(move[0], move[1], current_turn.mark)
            move_count += 1

            if verbose:
                print(f"Move {move_count}: {current_turn.name} ({current_turn.mark}) plays at {move}")
                board.print_board()

            # Switch turns
            current_turn = second_agent if current_turn == first_agent else first_agent

        game_duration = time.perf_counter() - game_start_time
        winner_mark = board.check_winner()

        if winner_mark == agent1.mark:
            winner_name = agent1.name
        elif winner_mark == agent2.mark:
            winner_name = agent2.name
        else:
            winner_name = "Draw"

        if verbose:
            print(f"Game Over! Outcome: {winner_name} in {move_count} moves ({game_duration:.4f}s)")

        return {
            "first_player": first_agent.name,
            "winner": winner_name,
            "moves": move_count,
            "duration_sec": game_duration,
            f"{agent1.name}_nodes_eval": agent1.total_nodes_evaluated,
            f"{agent1.name}_nodes_pruned": agent1.total_nodes_pruned,
            f"{agent1.name}_time_sec": agent1.total_execution_time,
            f"{agent2.name}_nodes_eval": agent2.total_nodes_evaluated,
            f"{agent2.name}_nodes_pruned": agent2.total_nodes_pruned,
            f"{agent2.name}_time_sec": agent2.total_execution_time,
        }

    def run_10_game_battle(
        self,
        nexus_depth: int = 3,
        titan_depth: int = 3,
        csv_filename: str = "results.csv"
    ) -> Dict[str, Any]:
        """
        Run a 10-game tournament between NEXUS and TITAN, alternating starting player.

        Saves detailed match metrics to CSV.
        """
        nexus = NexusAgent(depth=nexus_depth)
        titan = TitanAgent(depth=titan_depth)

        battle_records: List[Dict[str, Any]] = []

        print("\n=======================================================")
        print(f"   STARTING 10-GAME BATTLE: NEXUS (d={nexus_depth}) vs TITAN (d={titan_depth})")
        print("=======================================================")

        header_fmt = "{:<5} {:<10} {:<10} {:<7} {:<13} {:<13} {:<13} {:<13} {:<10}"
        print(header_fmt.format(
            "Game", "First", "Winner", "Moves", "NEXUS Eval", "TITAN Eval", "NEXUS Pruned", "TITAN Pruned", "Time(s)"
        ))
        print("-" * 96)

        for game_num in range(1, 11):
            nexus_starts = (game_num % 2 != 0)  # Alternating starting player
            stats = self.run_single_game(nexus, titan, agent1_starts=nexus_starts, verbose=False)

            row_data = {
                "game": game_num,
                "first": stats["first_player"],
                "winner": stats["winner"],
                "moves": stats["moves"],
                "nexus_nodes_eval": stats["NEXUS_nodes_eval"],
                "titan_nodes_eval": stats["TITAN_nodes_eval"],
                "nexus_nodes_pruned": stats["NEXUS_nodes_pruned"],
                "titan_nodes_pruned": stats["TITAN_nodes_pruned"],
                "execution_time_sec": round(stats["duration_sec"], 5)
            }
            battle_records.append(row_data)

            print(header_fmt.format(
                game_num,
                row_data["first"],
                row_data["winner"],
                row_data["moves"],
                row_data["nexus_nodes_eval"],
                row_data["titan_nodes_eval"],
                row_data["nexus_nodes_pruned"],
                row_data["titan_nodes_pruned"],
                f"{row_data['execution_time_sec']:.4f}"
            ))

        # Save to CSV file
        csv_path = os.path.join(self.output_dir, csv_filename)
        with open(csv_path, mode="w", newline="") as f:
            fieldnames = ["game", "first", "winner", "moves", "nexus_nodes_eval", "titan_nodes_eval", "nexus_nodes_pruned", "titan_nodes_pruned", "execution_time_sec"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(battle_records)

        # Compute summary metrics
        nexus_wins = sum(1 for r in battle_records if r["winner"] == "NEXUS")
        titan_wins = sum(1 for r in battle_records if r["winner"] == "TITAN")
        draws = sum(1 for r in battle_records if r["winner"] == "Draw")
        avg_moves = sum(r["moves"] for r in battle_records) / 10.0
        avg_nexus_eval = sum(r["nexus_nodes_eval"] for r in battle_records) / 10.0
        avg_titan_eval = sum(r["titan_nodes_eval"] for r in battle_records) / 10.0
        avg_nexus_pruned = sum(r["nexus_nodes_pruned"] for r in battle_records) / 10.0
        avg_titan_pruned = sum(r["titan_nodes_pruned"] for r in battle_records) / 10.0
        avg_time = sum(r["execution_time_sec"] for r in battle_records) / 10.0

        summary = {
            "total_games": 10,
            "nexus_wins": nexus_wins,
            "titan_wins": titan_wins,
            "draws": draws,
            "avg_moves": round(avg_moves, 2),
            "avg_nexus_nodes_eval": round(avg_nexus_eval, 2),
            "avg_titan_nodes_eval": round(avg_titan_eval, 2),
            "avg_nexus_nodes_pruned": round(avg_nexus_pruned, 2),
            "avg_titan_nodes_pruned": round(avg_titan_pruned, 2),
            "avg_execution_time_sec": round(avg_time, 5)
        }

        print("-" * 96)
        print(f"SUMMARY RESULT: NEXUS Wins: {nexus_wins} | TITAN Wins: {titan_wins} | Draws: {draws}")
        print(f"AVG NODES EVAL: NEXUS={avg_nexus_eval:.1f}, TITAN={avg_titan_eval:.1f}")
        print(f"AVG NODES PRUNED: NEXUS={avg_nexus_pruned:.1f}, TITAN={avg_titan_pruned:.1f}")
        print(f"AVG TIME PER GAME: {avg_time:.4f}s")
        print(f"Saved battle results to '{csv_path}'\n")

        # Save summary JSON
        summary_path = os.path.join(self.output_dir, "summary.json")
        with open(summary_path, "w") as sf:
            json.dump(summary, sf, indent=4)

        return {"records": battle_records, "summary": summary}

    def run_depth_experiment(
        self,
        depths: List[int] = [1, 2, 3, 4, 5, 9],
        csv_filename: str = "depth_experiment.csv"
    ) -> List[Dict[str, Any]]:
        """
        Run Experiment 1: Investigate the impact of search depth on decision quality,
        node count, pruning efficiency, and execution time.
        """
        print("\n=======================================================")
        print("   STARTING EXPERIMENT 1: SEARCH DEPTH SENSITIVITY")
        print("=======================================================")

        depth_records = []
        header_fmt = "{:<7} {:<10} {:<15} {:<15} {:<12}"
        print(header_fmt.format("Depth", "Result", "Nodes Evaluated", "Nodes Pruned", "Time(s)"))
        print("-" * 65)

        for depth in depths:
            # We pit an agent with `depth` against a reference baseline agent (depth 3)
            # or simulate benchmark game play to evaluate node growth
            test_agent = Agent("TEST_AI", depth=depth, heuristic_fn=heuristic_h1_nexus, heuristic_name="H1")
            ref_agent = Agent("REF_AI", depth=3, heuristic_fn=heuristic_h2_titan, heuristic_name="H2")

            stats = self.run_single_game(test_agent, ref_agent, agent1_starts=True, verbose=False)

            rec = {
                "depth": depth,
                "result": stats["winner"],
                "nodes_evaluated": stats["TEST_AI_nodes_eval"],
                "nodes_pruned": stats["TEST_AI_nodes_pruned"],
                "execution_time_sec": round(stats["TEST_AI_time_sec"], 5)
            }
            depth_records.append(rec)

            print(header_fmt.format(
                rec["depth"],
                rec["result"],
                rec["nodes_evaluated"],
                rec["nodes_pruned"],
                f"{rec['execution_time_sec']:.4f}"
            ))

        # Save to CSV
        csv_path = os.path.join(self.output_dir, csv_filename)
        with open(csv_path, mode="w", newline="") as f:
            fieldnames = ["depth", "result", "nodes_evaluated", "nodes_pruned", "execution_time_sec"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(depth_records)

        print("-" * 65)
        print(f"Saved depth experiment results to '{csv_path}'\n")

        return depth_records
