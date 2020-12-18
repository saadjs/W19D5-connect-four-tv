import React, { useState } from "react";
import { Redirect } from "react-router-dom";
import { addPlayer } from "../services/gameApi";

const JoinGameForm = ({ setPlayer2, setCurrentPlayer }) => {
	const [gameId, setGameId] = useState("");
	const [playerName, setPlayerName] = useState("");
	const [redirect, setRedirect] = useState(null);

	const submit = async (e) => {
		e.preventDefault();
		const response = await addPlayer(parseInt(gameId), playerName);
		console.log(response);

		if (response.game) {
			setPlayer2(playerName);
			localStorage.setItem(`player2[${gameId}]`, playerName);
			setCurrentPlayer(playerName);
			setRedirect(<Redirect to={`/game/${gameId}`} />);
		}
	};

	return (
		<>
			{redirect}
			<form>
				<input
					onChange={(e) => setGameId(e.target.value)}
					value={gameId}
					placeholder="Game ID"
				></input>
				<input
					onChange={(e) => setPlayerName(e.target.value)}
					value={playerName}
					placeholder="Player Name"
				></input>
				<button onClick={submit}>Join Game</button>
			</form>
		</>
	);
};

export default JoinGameForm;
