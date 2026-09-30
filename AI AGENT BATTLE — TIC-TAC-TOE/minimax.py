"""
minimax.py - Minimax Search Engine with Alpha-Beta Pruning

This module implements the Minimax search algorithm augmented with Alpha-Beta pruning,
configurable search depth, non-terminal heuristic evaluation, statistics collection
(evaluated nodes, pruned nodes, time taken), and random tie-breaking among equal-valued moves.
"""

import math
import random
import time
from typing import Callable, List, Tuple, Dict, Any
from game import TicTacToe


class MinimaxSearch:
    """
    Minimax search engine with Alpha-Beta pruning.
    Tracks search statistics (nodes evaluated, nodes pruned, execution time).
    """

    def __init__(self, heuristic_fn: Callable[[TicTacToe, str, str], float]):
        self.heuristic_fn = heuristic_fn
        self.nodes_evaluated: int = 0
        self.nodes_pruned: int = 0

    def reset_counters(self) -> None:
        """Reset nodes evaluated and pruned counters."""
        self.nodes_evaluated = 0
        self.nodes_pruned = 0

    def minimax_ab(
        self,
        board: TicTacToe,
        depth: int,
        alpha: float,
        beta: float,
        is_maximizing: bool,
        player_mark: str,
        opponent_mark: str
    ) -> float:
        """
        Recursive Minimax search with Alpha-Beta pruning.

        Args:
            board: Current TicTacToe board instance.
            depth: Remaining search depth limit.
            alpha: Alpha threshold for MAX player.
            beta: Beta threshold for MIN player.
            is_maximizing: True if current turn is MAX, False if MIN.
            player_mark: Mark of the AI agent running the search ('X' or 'O').
            opponent_mark: Mark of the opponent ('O' or 'X').

        Returns:
            Evaluated score float for the board position.
        """
        self.nodes_evaluated += 1

        # Check for terminal state
        winner = board.check_winner()
        if winner == player_mark:
            return 100.0 + depth  # Prefer faster wins
        elif winner == opponent_mark:
            return -100.0 - depth # Prefer delaying losses
        elif board.is_draw():
            return 0.0

        # Check search depth limit cutoff
        if depth == 0:
            return float(self.heuristic_fn(board, player_mark, opponent_mark))

        valid_moves = board.get_valid_moves()

        if is_maximizing:
            max_eval = -math.inf
            for idx, (r, c) in enumerate(valid_moves):
                board.board[r][c] = player_mark
                eval_score = self.minimax_ab(
                    board, depth - 1, alpha, beta, False, player_mark, opponent_mark
                )
                board.board[r][c] = TicTacToe.EMPTY

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                # Alpha-Beta Pruning Cutoff
                if beta <= alpha:
                    # Count remaining unsearched branches as pruned
                    pruned_count = len(valid_moves) - (idx + 1)
                    self.nodes_pruned += pruned_count
                    break

            return max_eval
        else:
            min_eval = math.inf
            for idx, (r, c) in enumerate(valid_moves):
                board.board[r][c] = opponent_mark
                eval_score = self.minimax_ab(
                    board, depth - 1, alpha, beta, True, player_mark, opponent_mark
                )
                board.board[r][c] = TicTacToe.EMPTY

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                # Alpha-Beta Pruning Cutoff
                if beta <= alpha:
                    # Count remaining unsearched branches as pruned
                    pruned_count = len(valid_moves) - (idx + 1)
                    self.nodes_pruned += pruned_count
                    break

            return min_eval

    def choose_move(
        self,
        board: TicTacToe,
        player_mark: str,
        opponent_mark: str,
        depth: int
    ) -> Tuple[Tuple[int, int], float, int, int, float]:
        """
        Evaluate all valid moves at root level and choose the optimal move.
        If multiple moves yield the same maximum score, randomly break the tie
        to allow move variation across games.

        Args:
            board: Current TicTacToe board state.
            player_mark: Mark of the AI player ('X' or 'O').
            opponent_mark: Mark of the opponent ('O' or 'X').
            depth: Maximum search depth.

        Returns:
            Tuple of:
              - best_move: (row, col)
              - best_score: float score of best move
              - nodes_evaluated: int count of nodes evaluated in this search
              - nodes_pruned: int count of nodes pruned in this search
              - elapsed_time: float search duration in seconds
        """
        self.reset_counters()
        start_time = time.perf_counter()

        valid_moves = board.get_valid_moves()
        if not valid_moves:
            raise ValueError("No valid moves available on the board.")

        best_score = -math.inf
        move_scores: List[Tuple[Tuple[int, int], float]] = []

        alpha = -math.inf
        beta = math.inf

        for r, c in valid_moves:
            board.board[r][c] = player_mark
            # Next depth step is MIN's turn (is_maximizing=False)
            score = self.minimax_ab(
                board, depth - 1, alpha, beta, False, player_mark, opponent_mark
            )
            board.board[r][c] = TicTacToe.EMPTY

            move_scores.append(((r, c), score))
            if score > best_score:
                best_score = score
            alpha = max(alpha, best_score)

        # Collect all moves that achieve the maximum score
        top_moves = [move for move, score in move_scores if math.isclose(score, best_score, abs_tol=1e-5)]

        # Randomly choose among equal top-scoring moves to ensure varied play
        chosen_move = random.choice(top_moves)

        elapsed_time = time.perf_counter() - start_time

        return chosen_move, best_score, self.nodes_evaluated, self.nodes_pruned, elapsed_time
