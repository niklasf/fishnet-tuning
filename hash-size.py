#!/usr/bin/python3

import asyncio
import chess
import chess.engine
import logging


async def play(board, white, black, *, nodes):
    engines = [black, white]

    while True:
        result = board.result(claim_draw=True)
        if result != "*":
            return result

        engine = engines[board.turn]
        m = await engine.play(board, chess.engine.Limit(nodes=nodes), game=object())
        board.push(m.move)


async def main():
    _, a = await chess.engine.popen_uci("./Stockfish/src/stockfish")
    _, b = await chess.engine.popen_uci("./Stockfish/src/stockfish")

    await a.configure({
        "Hash": "1",
    })

    await b.configure({
        "Hash": "512",
    })

    stats = {
        "a": 0,
        "b": 0,
        "draw": 0,
    }

    a_white = {
        "1-0": "a",
        "0-1": "b",
        "1/2-1/2": "draw",
    }

    b_white = {
        "1-0": "b",
        "0-1": "a",
        "1/2-1/2": "draw",
    }

    for i, epd in enumerate(open("noob_3moves_sample.epd")):
        board = chess.Board(epd)

        result_a = await play(board.copy(), a, b, nodes=1000_000)
        stats[a_white[result_a]] += 1

        result_b = await play(board.copy(), b, a, nodes=1000_000)
        stats[b_white[result_b]] += 1

        print(i, board.epd(), result_a, result_b, stats)


if __name__ == "__main__":
    asyncio.run(main())
