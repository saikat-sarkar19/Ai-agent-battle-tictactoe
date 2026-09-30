"""
heuristic.py - Heuristic Evaluation Functions for Non-Terminal Board Positions

This module implements heuristic evaluation functions for Tic-Tac-Toe positions
when search reaches the maximum depth limit.

Two distinct and reasonable heuristics are provided:
  - H1 (NEXUS Strategy): Focuses on line opportunities and strategic positional control (center & corners).
  - H2 (TITAN Strategy): Focuses on aggressive threat defense/blocking and multi-threat (fork) creation.
"""

from game import TicTacToe


def get_line_contents(board: TicTacToe):
    """Retrieve contents of all 8 winning lines (3 rows, 3 cols, 2 diagonals)."""
    lines = []
    # Rows & Cols
    for i in range(3):
        row = [board.board[i][c] for c in range(3)]
        col = [board.board[r][i] for r in range(3)]
        lines.append(row)
        lines.append(col)
    # Diagonals
    diag1 = [board.board[i][i] for i in range(3)]
    diag2 = [board.board[i][2 - i] for i in range(3)]
    lines.append(diag1)
    lines.append(diag2)
    return lines


def heuristic_h1_nexus(board: TicTacToe, player: str, opponent: str) -> float:
    """
    Heuristic H1 (NEXUS Strategy): Positional Advantage & Line Opportunity.
    
    Evaluates:
      - 2 player marks + 1 empty: +10
      - 1 player mark + 2 empty: +3
      - 2 opponent marks + 1 empty: -10
      - 1 opponent mark + 2 empty: -3
      - Center control (1, 1): +4 for player, -4 for opponent
      - Corner control: +2 per corner for player, -2 for opponent
    """
    score = 0.0
    lines = get_line_contents(board)

    for line in lines:
        p_count = line.count(player)
        o_count = line.count(opponent)
        e_count = line.count(TicTacToe.EMPTY)

        if p_count == 2 and e_count == 1:
            score += 10.0
        elif p_count == 1 and e_count == 2:
            score += 3.0

        if o_count == 2 and e_count == 1:
            score -= 10.0
        elif o_count == 1 and e_count == 2:
            score -= 3.0

    # Positional evaluation: Center control
    if board.board[1][1] == player:
        score += 4.0
    elif board.board[1][1] == opponent:
        score -= 4.0

    # Positional evaluation: Corner control
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for r, c in corners:
        if board.board[r][c] == player:
            score += 2.0
        elif board.board[r][c] == opponent:
            score -= 2.0

    return score


def heuristic_h2_titan(board: TicTacToe, player: str, opponent: str) -> float:
    """
    Heuristic H2 (TITAN Strategy): Threat Defense & Fork Detection.
    
    Evaluates:
      - 2 player marks + 1 empty: +15
      - 2 opponent marks + 1 empty: -20 (higher defensive urgency to block wins)
      - 1 player mark + 2 empty: +2
      - 1 opponent mark + 2 empty: -2
      - Fork detection (multiple 2-in-a-row threats): +25 for player, -25 for opponent
      - Center control (1, 1): +3 for player, -3 for opponent
      - Corner control: +1 per corner for player, -1 for opponent
    """
    score = 0.0
    lines = get_line_contents(board)

    player_threats = 0
    opponent_threats = 0

    for line in lines:
        p_count = line.count(player)
        o_count = line.count(opponent)
        e_count = line.count(TicTacToe.EMPTY)

        if p_count == 2 and e_count == 1:
            score += 15.0
            player_threats += 1
        elif p_count == 1 and e_count == 2:
            score += 2.0

        if o_count == 2 and e_count == 1:
            score -= 20.0
            opponent_threats += 1
        elif o_count == 1 and e_count == 2:
            score -= 2.0

    # Fork bonus / penalty
    if player_threats >= 2:
        score += 25.0
    if opponent_threats >= 2:
        score -= 25.0

    # Center control
    if board.board[1][1] == player:
        score += 3.0
    elif board.board[1][1] == opponent:
        score -= 3.0

    # Corner control
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for r, c in corners:
        if board.board[r][c] == player:
            score += 1.0
        elif board.board[r][c] == opponent:
            score -= 1.0

    return score


def get_heuristic_by_name(name: str):
    """Factory helper to select heuristic function by string name."""
    name_upper = name.upper()
    if name_upper in ["H1", "NEXUS", "H1_NEXUS"]:
        return heuristic_h1_nexus
    elif name_upper in ["H2", "TITAN", "H2_TITAN"]:
        return heuristic_h2_titan
    else:
        raise ValueError(f"Unknown heuristic name: {name}")
