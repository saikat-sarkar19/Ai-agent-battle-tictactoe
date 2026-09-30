"""
game.py - Tic-Tac-Toe Game Engine

This module defines the TicTacToe class which manages the 3x3 board state,
legal move generation, move application, win/draw detection, and terminal state checking.
"""

from typing import List, Tuple, Optional


class TicTacToe:
    """
    Represents a 3x3 Tic-Tac-Toe board and handles game logic.
    """
    EMPTY = ''
    PLAYER_X = 'X'
    PLAYER_O = 'O'

    # Winning combinations (3 rows, 3 columns, 2 diagonals)
    WINNING_COMBOS = [
        # Rows
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        # Columns
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        # Diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    def __init__(self):
        """Initialize an empty 3x3 Tic-Tac-Toe board."""
        self.board: List[List[str]] = [
            [self.EMPTY, self.EMPTY, self.EMPTY],
            [self.EMPTY, self.EMPTY, self.EMPTY],
            [self.EMPTY, self.EMPTY, self.EMPTY]
        ]
        self.move_history: List[Tuple[int, int, str]] = []

    def reset(self) -> None:
        """Reset the board to the initial empty state."""
        self.board = [
            [self.EMPTY, self.EMPTY, self.EMPTY],
            [self.EMPTY, self.EMPTY, self.EMPTY],
            [self.EMPTY, self.EMPTY, self.EMPTY]
        ]
        self.move_history.clear()

    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """
        Return a list of empty cell coordinates (row, col).
        """
        moves = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == self.EMPTY:
                    moves.append((r, c))
        return moves

    def is_valid_move(self, row: int, col: int) -> bool:
        """Check if a given (row, col) position is empty and within board bounds."""
        if 0 <= row < 3 and 0 <= col < 3:
            return self.board[row][col] == self.EMPTY
        return False

    def make_move(self, row: int, col: int, player: str) -> bool:
        """
        Place a player's mark ('X' or 'O') at (row, col) if valid.
        Returns True if successful, False otherwise.
        """
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            self.move_history.append((row, col, player))
            return True
        return False

    def undo_move(self, row: int, col: int) -> None:
        """Undo a move at (row, col) by resetting the cell to empty."""
        if 0 <= row < 3 and 0 <= col < 3:
            self.board[row][col] = self.EMPTY
            if self.move_history and self.move_history[-1][:2] == (row, col):
                self.move_history.pop()

    def check_winner(self) -> Optional[str]:
        """
        Check whether player 'X' or 'O' has won.
        Returns 'X', 'O', or None if there is no winner.
        """
        for combo in self.WINNING_COMBOS:
            c1, c2, c3 = combo
            v1 = self.board[c1[0]][c1[1]]
            v2 = self.board[c2[0]][c2[1]]
            v3 = self.board[c3[0]][c3[1]]

            if v1 != self.EMPTY and v1 == v2 == v3:
                return v1
        return None

    def is_draw(self) -> bool:
        """
        Check if the game ended in a draw (board is full and no winner).
        """
        if self.check_winner() is not None:
            return False
        return len(self.get_valid_moves()) == 0

    def is_terminal(self) -> bool:
        """
        Check whether the game has reached a terminal state (win or draw).
        """
        return self.check_winner() is not None or self.is_draw()

    def display_board(self) -> str:
        """Return a formatted ASCII string representation of the board."""
        lines = []
        lines.append("-------------")
        for r in range(3):
            row_str = "| "
            for c in range(3):
                val = self.board[r][c] if self.board[r][c] != self.EMPTY else " "
                row_str += f"{val} | "
            lines.append(row_str)
            lines.append("-------------")
        return "\n".join(lines)

    def print_board(self) -> None:
        """Print the formatted board to console."""
        print(self.display_board())

    def copy(self) -> 'TicTacToe':
        """Create a deep copy of the current game state."""
        new_game = TicTacToe()
        new_game.board = [row[:] for row in self.board]
        new_game.move_history = list(self.move_history)
        return new_game
