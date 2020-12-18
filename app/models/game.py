from sqlalchemy.orm import relationship
from .db import db

NUM_COLUMNS = 4
COLUMN_HEIGHT = 5

class Game(db.Model):
  __tablename__ = 'games'

  id = db.Column(db.Integer, primary_key = True)
  player1 = db.Column(db.String(40))
  player2 = db.Column(db.String(40))
  moves = relationship('Move', back_populates='game', order_by='asc(Move.id)')

  def board(self, ):
    column_height = [0]*NUM_COLUMNS
    board = [[None]*COLUMN_HEIGHT for i in range(0, NUM_COLUMNS)]
    for move in self.moves:
      board[move.column][column_height[move.column]] = move.player_id
      column_height[move.column] += 1
    return board

  def findWinner(self, board):
    for col in board:
      isWon = self.colIsWon(col) or self.altColIsWon(col)
      if isWon:
        return isWon
    for n in range(5):
      isWon = self.rowIsWon(n, board) or self.checkDiagUp(n, board) or self.checkDiagDown(n, board)
      if isWon:
        return isWon


  def checkDiagUp(self, n, board):
    first = board[0][n]
    for dif in range(1, 4):
      if n+dif >= 4:
        return None
      if board[dif][n+dif] != first:
        return None
    return first

  def checkDiagDown(self, n, board):
    first = board[0][n]
    for dif in range(1, 4):
      if n-dif < 0:
        return None
      if board[dif][n-dif] != first:
        return None
    return first


  def colIsWon(self, col):
    first = col[0]
    for val in col[1:4]:
      if val != first:
        return None
    return first

  def altColIsWon(self, col):
    first = col[1]
    for val in col[2:5]:
      if val != first:
        return None
    return first

  def rowIsWon(self,row, board):
    row = [board[n][row] for n in range(4)]
    first = row[0]
    if first is None:
      return None
    matches = [val == first for val in row]
    if all(matches):
      return first
    return None


  def column_exists(self, column_id):
    if column_id < 0 or column_id > NUM_COLUMNS:
      return False
    return True

  def column_has_room(self, column_id):
    column_count = [move for move in self.moves if move.column == column_id]
    return len(column_count) < COLUMN_HEIGHT

  def to_dict(self):
    board = self.board()
    return {
      "id": self.id,
      "player1": self.player1,
      "player2": self.player2,
      "board": board,
      "winner": self.findWinner(board)
    }
