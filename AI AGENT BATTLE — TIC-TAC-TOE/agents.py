"""
agents.py - AI Agent Classes (NEXUS and TITAN)

This module defines the Agent base class and specific named AI agents:
  - NEXUS: Powered by Minimax + Alpha-Beta & Heuristic H1 (Positional Advantage & Line Opportunity)
  - TITAN: Powered by Minimax + Alpha-Beta & Heuristic H2 (Threat Defense & Fork Detection)
"""

from typing import Callable, Tuple, Dict, Any, Optional
from game import TicTacToe
from minimax import MinimaxSearch
from heuristic import heuristic_h1_nexus, heuristic_h2_titan


class Agent:
    """
    Base AI Agent class wrapping Minimax search, search depth,
    heuristic evaluation, identity, and performance tracking.
    """

    def __init__(
        self,
        name: str,
        depth: int = 3,
        heuristic_fn: Optional[Callable[[TicTacToe, str, str], float]] = None,
        heuristic_name: str = "Custom"
    ):
        self.name = name
        self.depth = depth
        self.heuristic_fn = heuristic_fn if heuristic_fn is not None else heuristic_h1_nexus
        self.heuristic_name = heuristic_name
        self.mark: str = TicTacToe.PLAYER_X
        self.search_engine = MinimaxSearch(self.heuristic_fn)

        # Per-game performance counters
        self.total_nodes_evaluated: int = 0
        self.total_nodes_pruned: int = 0
        self.total_execution_time: float = 0.0
        self.total_moves_made: int = 0

    def set_mark(self, mark: str) -> None:
        """Assign player mark ('X' or 'O') to the agent."""
        self.mark = mark

    def get_opponent_mark(self) -> str:
        """Return opponent's mark ('O' if self.mark == 'X' else 'X')."""
        return TicTacToe.PLAYER_O if self.mark == TicTacToe.PLAYER_X else TicTacToe.PLAYER_X

    def reset_stats(self) -> None:
        """Reset per-game metrics counters."""
        self.total_nodes_evaluated = 0
        self.total_nodes_pruned = 0
        self.total_execution_time = 0.0
        self.total_moves_made = 0

    def choose_move(self, board: TicTacToe) -> Tuple[int, int]:
        """
        Choose the best move for current board position using Minimax search.

        Returns:
            (row, col) tuple representing chosen move.
        """
        opponent_mark = self.get_opponent_mark()
        move, score, nodes_eval, nodes_pruned, exec_time = self.search_engine.choose_move(
            board=board,
            player_mark=self.mark,
            opponent_mark=opponent_mark,
            depth=self.depth
        )

        # Update agent counters
        self.total_nodes_evaluated += nodes_eval
        self.total_nodes_pruned += nodes_pruned
        self.total_execution_time += exec_time
        self.total_moves_made += 1

        return move

    def __str__(self) -> str:
        return f"Agent({self.name}, Depth={self.depth}, Heuristic={self.heuristic_name}, Mark={self.mark})"


class NexusAgent(Agent):
    """
    NEXUS AI Agent: Employs Minimax + Alpha-Beta search with Heuristic H1.
    """
    def __init__(self, depth: int = 3):
        super().__init__(
            name="NEXUS",
            depth=depth,
            heuristic_fn=heuristic_h1_nexus,
            heuristic_name="H1_Positional"
        )


class TitanAgent(Agent):
    """
    TITAN AI Agent: Employs Minimax + Alpha-Beta search with Heuristic H2.
    """
    def __init__(self, depth: int = 3):
        super().__init__(
            name="TITAN",
            depth=depth,
            heuristic_fn=heuristic_h2_titan,
            heuristic_name="H2_ThreatDefense"
        )
