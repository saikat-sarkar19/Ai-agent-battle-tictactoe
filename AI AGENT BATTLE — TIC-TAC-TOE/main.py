"""
main.py - Main Program Entry Point & CLI Interface

Tic-Tac-Toe AI Agent Battle System
Demonstrates Minimax, Alpha-Beta Pruning, Heuristic Evaluation, and Depth Analysis.
"""

import sys
import argparse
from game import TicTacToe
from agents import Agent, NexusAgent, TitanAgent
from experiment import Experiment
from heuristic import get_heuristic_by_name, heuristic_h1_nexus, heuristic_h2_titan


def print_banner():
    print("==================================================================")
    print("           AI AGENT BATTLE — TIC-TAC-TOE LABORATORY               ")
    print("  Minimax | Alpha-Beta Pruning | Heuristic Search | Depth Analysis ")
    print("==================================================================")


def run_interactive_human_vs_ai():
    """Allows a human player to challenge an AI Agent (NEXUS or TITAN)."""
    print_banner()
    print("\n--- HUMAN VS AI AGENT MATCH ---")
    
    agent_name = input("Select AI Agent (1: NEXUS [H1], 2: TITAN [H2]) [Default: 1]: ").strip()
    depth_str = input("Select AI Search Depth (1 to 9) [Default: 3]: ").strip()
    
    depth = int(depth_str) if depth_str.isdigit() else 3
    if agent_name == "2":
        ai_agent = TitanAgent(depth=depth)
    else:
        ai_agent = NexusAgent(depth=depth)

    human_mark_choice = input("Choose your mark (X starts first, O plays second) [Default: X]: ").strip().upper()
    if human_mark_choice == "O":
        human_mark = TicTacToe.PLAYER_O
        ai_mark = TicTacToe.PLAYER_X
    else:
        human_mark = TicTacToe.PLAYER_X
        ai_mark = TicTacToe.PLAYER_O

    ai_agent.set_mark(ai_mark)
    board = TicTacToe()
    
    print(f"\nGame Starting: You ('{human_mark}') vs {ai_agent.name} ('{ai_mark}') [Depth={depth}]")
    board.print_board()

    turn = TicTacToe.PLAYER_X
    while not board.is_terminal():
        if turn == human_mark:
            print("\nYour Turn!")
            valid_moves = board.get_valid_moves()
            while True:
                try:
                    move_input = input(f"Enter move as 'row col' (0-2) [Valid: {valid_moves}]: ").strip()
                    r_str, c_str = move_input.split()
                    r, c = int(r_str), int(c_str)
                    if (r, c) in valid_moves:
                        board.make_move(r, c, human_mark)
                        break
                    else:
                        print("Invalid cell location. Try again.")
                except Exception:
                    print("Invalid input format. Enter two numbers separated by space (e.g. '1 1').")
        else:
            print(f"\n{ai_agent.name}'s Turn (Thinking with Depth={depth})...")
            move = ai_agent.choose_move(board)
            board.make_move(move[0], move[1], ai_mark)
            print(f"{ai_agent.name} played at position {move}")

        board.print_board()
        turn = TicTacToe.PLAYER_O if turn == TicTacToe.PLAYER_X else TicTacToe.PLAYER_X

    winner = board.check_winner()
    print("\n--------------------------------------------------")
    if winner == human_mark:
        print("CONGRATULATIONS! You won against the AI!")
    elif winner == ai_mark:
        print(f"GAME OVER! {ai_agent.name} won the match!")
    else:
        print("GAME OVER! The match ended in a DRAW.")
    print("--------------------------------------------------")


def interactive_menu():
    """Interactive command-line menu."""
    exp = Experiment()
    while True:
        print_banner()
        print("\nPlease select an option:")
        print("  1. Run 10-Game AI Agent Battle (NEXUS vs TITAN)")
        print("  2. Run Search Depth Sensitivity Experiment (Experiment 1)")
        print("  3. Play Interactive Match against AI Agent")
        print("  4. Run Full Benchmark Suite (Battle + Depth Experiment)")
        print("  5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            d1_str = input("Enter NEXUS search depth [Default 3]: ").strip()
            d2_str = input("Enter TITAN search depth [Default 3]: ").strip()
            d1 = int(d1_str) if d1_str.isdigit() else 3
            d2 = int(d2_str) if d2_str.isdigit() else 3
            exp.run_10_game_battle(nexus_depth=d1, titan_depth=d2)
            input("\nPress Enter to return to menu...")
        elif choice == "2":
            exp.run_depth_experiment(depths=[1, 2, 3, 4, 5, 9])
            input("\nPress Enter to return to menu...")
        elif choice == "3":
            run_interactive_human_vs_ai()
            input("\nPress Enter to return to menu...")
        elif choice == "4":
            exp.run_depth_experiment(depths=[1, 2, 3, 4, 5, 9])
            exp.run_10_game_battle(nexus_depth=3, titan_depth=3)
            input("\nPress Enter to return to menu...")
        elif choice == "5":
            print("\nExiting AI Agent Battle System. Goodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please select 1-5.")


def main():
    parser = argparse.ArgumentParser(description="Tic-Tac-Toe AI Agent Battle System")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["battle", "depth", "all", "interactive"],
        default="all",
        help="Execution mode: battle (10 games), depth (depth benchmark), all (both), interactive (menu)"
    )
    parser.add_argument("--nexus-depth", type=int, default=3, help="Search depth for NEXUS agent")
    parser.add_argument("--titan-depth", type=int, default=3, help="Search depth for TITAN agent")
    parser.add_argument("--outdir", type=str, default="results", help="Directory to store CSV outputs")

    args = parser.parse_args()

    exp = Experiment(output_dir=args.outdir)

    if args.mode == "interactive":
        interactive_menu()
    elif args.mode == "battle":
        exp.run_10_game_battle(nexus_depth=args.nexus_depth, titan_depth=args.titan_depth)
    elif args.mode == "depth":
        exp.run_depth_experiment(depths=[1, 2, 3, 4, 5, 9])
    elif args.mode == "all":
        print_banner()
        exp.run_depth_experiment(depths=[1, 2, 3, 4, 5, 9])
        exp.run_10_game_battle(nexus_depth=args.nexus_depth, titan_depth=args.titan_depth)


if __name__ == "__main__":
    main()
