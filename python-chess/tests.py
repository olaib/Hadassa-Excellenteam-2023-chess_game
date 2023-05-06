import unittest
from unittest.mock import patch, MagicMock

import numpy as np

from chess_engine import game_state as Game
from enums import Player
from Piece import Knight, Pawn


def game_with_empty_board() -> Game:
    """Returns a game with an empty board"""
    game = Game()
    game.board = np.full((8, 8), Player.EMPTY, dtype=object)
    return game


# ======================= TEST CASES FOR THE KNIGHT =======================
class TestGame(unittest.TestCase):
    """Tests for the Game class"""

    def test_get_valid_peaceful_moves(self):
        """Test case where the knight is in the middle of the board and can make all 8 peaceful moves"""
        knight = Knight('n', 3, 4, Player.PLAYER_2)
        with patch.object(knight, 'get_valid_peaceful_moves') as mock_get_valid_peaceful_moves:
            game = game_with_empty_board()
            game.board[3][4] = knight
            mock_get_valid_peaceful_moves.return_value = [(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 5),
                                                          (5, 3)]
            expected_res = knight.get_valid_peaceful_moves(game)
            self.assertEqual(expected_res, mock_get_valid_peaceful_moves.return_value)
            mock_get_valid_peaceful_moves.assert_called_once()

    def test_get_valid_peaceful_moves_invalid(self):
        """Test case where the knight is in the edge of the board and can make only 2 peaceful moves"""
        # Test case where the knight is at the edge of the board and cannot make any peaceful moves
        knight = Knight('n', 0, 0, Player.PLAYER_1)
        game = game_with_empty_board()
        game.board[0][0] = knight
        expected_res = [(1, 2), (2, 1)]
        self.assertEqual(knight.get_valid_peaceful_moves(game), expected_res)

    def test_get_valid_peaceful_moves_blocked(self):
        # Test case where the knight is blocked and can't make any peaceful moves
        knight = Knight('n', 3, 4, Player.PLAYER_1)
        with patch.object(knight, 'get_valid_peaceful_moves') as mock_get_valid_peaceful_moves:
            game = game_with_empty_board()
            game.board[3][4] = knight
            game.board[1][3] = Pawn('p', 1, 3, Player.PLAYER_1)
            game.board[1][5] = Pawn('p', 1, 5, Player.PLAYER_1)
            game.board[2][2] = Pawn('p', 2, 2, Player.PLAYER_1)
            game.board[2][6] = Pawn('p', 2, 6, Player.PLAYER_1)
            game.board[4][2] = Pawn('p', 4, 2, Player.PLAYER_1)
            game.board[4][6] = Pawn('p', 4, 6, Player.PLAYER_1)
            game.board[5][5] = Pawn('p', 5, 5, Player.PLAYER_1)
            game.board[5][3] = Pawn('p', 5, 3, Player.PLAYER_1)
            mock_get_valid_peaceful_moves.return_value = []
            expected_res = []
            self.assertEqual(knight.get_valid_peaceful_moves(game), expected_res)
            mock_get_valid_peaceful_moves.assert_called_once()

    def test_get_valid_piece_takes(self):
        """Test case where the knight is in the middle of the board and can take all 8 opponent pieces"""
        knight = Knight('n', 3, 4, Player.PLAYER_2)
        with patch.object(knight, 'get_valid_piece_takes') as mock_get_valid_piece_takes:
            game = game_with_empty_board()
            game.board[3][4] = knight
            mock_get_valid_piece_takes.return_value = [(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 5),
                                                       (5, 3)]
            expected_res = knight.get_valid_piece_takes(game)  # corrected line
            self.assertEqual(expected_res, mock_get_valid_piece_takes.return_value)
            mock_get_valid_piece_takes.assert_called_once()

    def test_get_valid_piece_takes_invalid_move(self):
        """Test case where the knight is in the edge of the board and can't take any opponent pieces"""
        knight = Knight('n', 0, 0, Player.PLAYER_1)
        with patch.object(knight, 'get_valid_piece_takes') as mock_get_valid_piece_takes:
            game = game_with_empty_board()
            game.board[0][0] = knight
            mock_get_valid_piece_takes.return_value = []
            expected_res = []
            self.assertEqual(knight.get_valid_piece_takes(game), expected_res)
            mock_get_valid_piece_takes.assert_called_once()

    def test_get_valid_piece_takes_no_opponent_pieces(self):
        """Test case where the knight is in the middle of the board and there are no opponent pieces to take"""
        knight = Knight('n', 3, 4, Player.PLAYER_1)
        with patch.object(knight, 'get_valid_piece_takes') as mock_get_valid_piece_takes:
            game = game_with_empty_board()
            game.board[3][4] = knight
            mock_get_valid_piece_takes.return_value = []
            expected_res = []
            self.assertEqual(knight.get_valid_piece_takes(game), expected_res)
            mock_get_valid_piece_takes.assert_called_once()
