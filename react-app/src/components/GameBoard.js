import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom';
import {getGame, makeMove} from '../services/gameApi';
import './GameBoard.css'

function GameBoard(props) {
  const [grid, setGrid] = useState([[null, null, null, null, null], [null, null, null, null, null], [null, null, null, null, null], [null, null, null, null, null]]);
  const { gameId } = useParams();
  // const [column, setColumn] = useState()

  useEffect(function () {
    if (localStorage.getItem(`currentPlayer[${gameId}]`)) {
      props.setCurrentPlayer(localStorage.getItem(`currentPlayer[${gameId}]`));
    }
  }, []);

  // update game board
  useEffect(function () {
    async function getGameUpdates() {
      let {game} = await getGame(gameId);
      setGrid(game.board);
      props.setPlayer1(game.player1);
      props.setPlayer2(game.player2);
    }
    const intervalHandler = setInterval(() => getGameUpdates(), 1000);

    return () => clearInterval(intervalHandler);
  }, [props, gameId]);

  function handleClick(e, col_id) {
    e.preventDefault()
    e.stopPropagation()
      makeMove(gameId, props.currentPlayer, col_id);
  }

  function buildRow(row_id) {
    return grid.map((col, col_id) => <div onMouseDown={e => handleClick(e, col_id)} key={`${row_id}${col_id}`} data-row={row_id} data-column={col_id} >{col[row_id]}</div>);
  }


  function otherPlayer() {
    if (!props.currentPlayer) return '';
    if (props.player1 === props.currentPlayer) {
      if (props.player2) {
        return props.player2;
      } else {
        return "Awaiting Opponent";
      }
    } else {
      return props.player1;
    }
  }

  return (
    <>
      <h3>Play The Game {gameId}</h3>
      <b>You: {props.currentPlayer}</b> |<b>Opponent: {otherPlayer()}</b>
      <div className="game-board">
        {[0, 1, 2, 3, 4].map((i) => buildRow(i)).reverse()}
      </div>
    </>
  );
}

export default GameBoard;
