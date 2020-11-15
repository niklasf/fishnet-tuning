#!/usr/bin/env python

import asyncio
import logging
import io
import os
import time
import chess.pgn
import chess.engine


GAMES = """\
1. d3 d5 2. g3 e6 3. Bg2 Nf6 4. Nf3 Be7 5. O-O O-O 6. Re1 a6 7. e4 c5 8. e5 Nfd7 9. d4 Nb6 10. dxc5 Bxc5 11. Nc3 N8d7 12. a4 Be7 13. a5 Nc4 14. b3 Ncxe5 15. Nxe5 Nxe5 16. Rxe5 Bd6 17. Re1 Bd7 18. Bf4 Bc6 19. Bxd6 Qxd6 20. Na4 Rad8 21. Nb6 Rfe8 22. Ra4 Bxa4 23. bxa4 Qc5 24. Qa1 Qxa5 25. Qd4 Rd6 26. Nc4 Qb4 27. Nxd6 Qxd4 28. Nxe8 Qd2 29. Rb1 Qxc2 30. Rxb7 Qxa4 31. Rb8 Kf8 32. Nd6+ Ke7 33. Nf5+ Kf6 34. Nh4 Qd1+ 35. Bf1 Qd4 36. Kg2 a5 37. Rb7 a4 38. Rxf7+ Kxf7 39. Nf3 Ke7 40. Ne5 Kd6 41. Nf3 Qc4 42. Nd4 Qc3 43. Nf5+ Ke5 44. Ne3 Kf6 45. Nxd5+ exd5 0-1
1. e4 e6 2. Nf3 c5 3. g3 a6 4. Bg2 Nc6 5. O-O d6 6. h3 Be7 7. Nc3 Qc7 8. d4 cxd4 9. Nxd4 Nxd4 10. Qxd4 Bf6 11. Qd1 e5 12. Nd5 Qc6 13. Nxf6+ Nxf6 14. Re1 O-O 15. Bg5 Nd7 16. f4 exf4 17. Bxf4 Ne5 18. Bxe5 dxe5 19. a3 Be6 20. b4 Rad8 21. Qe2 Rd4 22. Rad1 Rfd8 23. Rxd4 Rxd4 24. c3 Rc4 25. Qc2 f6 26. Rd1 Qc7 27. a4 Rxb4 28. Rc1 Rc4 29. Bf1 Rc5 30. c4 Qb6 31. Qd2 Rxc4+ 32. Kh1 Rxc1 33. Qxc1 Qc6 34. Qd1 Qxe4+ 35. Bg2 Qd4 36. Qc1 1-0
1. e4 g6 2. Nf3 Bg7 3. d4 e6 4. Nc3 Ne7 5. Be3 O-O 6. Be2 d6 7. O-O b6 8. Qd2 Bb7 9. Bh6 c5 10. Bxg7 Kxg7 11. dxc5 bxc5 12. Rad1 d5 13. exd5 exd5 14. Rfe1 d4 15. Nb5 a6 16. Na3 Kg8 17. c3 Nbc6 18. cxd4 cxd4 19. Nxd4 Nxd4 20. Qxd4 Qxd4 21. Rxd4 Nc6 22. Rd7 Rab8 23. Red1 Ne5 24. Re7 Nc6 25. Rc7 Nb4 26. Rdd7 Be4 27. Bc4 Bd5 28. Bxd5 Nxd5 29. Rxd5 Rxb2 30. Rc2 Rfb8 31. f3 Rxc2 32. Nxc2 Rb2 33. Rd8+ Kg7 34. Rc8 Rxa2 35. Nb4 Ra4 36. Nd5 Ra1+ 37. Kf2 a5 38. Kg3 a4 39. Ra8 a3 40. Nc3 Rc1 41. Nb5 Rb1 42. Nxa3 Ra1 0-1
1. e4 g6 2. d4 Bg7 3. e5 e6 4. f4 Ne7 5. Nf3 d5 6. Nc3 O-O 7. Be3 Nd7 8. Bd3 b6 9. Nb5 c5 10. Nd6 cxd4 11. Nxd4 Nxe5 12. fxe5 Bxe5 13. Nxc8 Rxc8 14. O-O Nc6 15. Nxc6 Rxc6 16. c3 Bc7 17. Bd4 Qd6 18. Qg4 Qxh2+ 19. Kf2 e5 20. Rh1 Qf4+ 21. Qxf4 exf4 22. Rh6 Re6 23. Rah1 f5 24. Rxh7 Bd8 25. Rh8+ Kf7 26. R1h7+ Ke8 27. Bb5+ Rc6 28. Bxc6# 1-0
1. e4 c5 2. Nf3 Nc6 3. Bc4 Nf6 4. Nc3 e5 5. O-O d6 6. a3 Nd4 7. Nxd4 exd4 8. Nd5 Be6 9. Nxf6+ Qxf6 10. Bxe6 Qxe6 11. c3 d3 12. Qa4+ Ke7 13. e5 d5 14. Re1 c4 15. Qb4+ Kd7 16. Qxb7+ Ke8 17. Qxa8+ Kd7 18. Qxa7+ Kc8 19. b3 Qf5 20. bxc4 dxc4 21. Qa8+ Kc7 22. Rb1 Bc5 23. Rb7+ Kc6 24. Qa6+ Kd5 25. Rf1 Re8 26. Rc7 Rxe5 27. Qc6# 1-0
1. b3 d5 2. Bb2 Nf6 3. g3 e5 4. Bg2 Nc6 5. d3 Be6 6. e3 Qd6 7. Nd2 O-O-O 8. Ne2 g6 9. c4 dxc4 10. bxc4 Bg7 11. O-O Nd7 12. d4 exd4 13. exd4 Nb4 14. Ne4 Qe7 15. d5 Bg4 16. Bxg7 Rhg8 17. Bc3 Bxe2 18. Qxe2 f5 19. Bxb4 Qxb4 20. Rab1 Qa3 21. Nc3 Rde8 22. Qb2 Qa6 23. Qb5 Qa3 24. Qb4 Qa6 25. a4 Nb6 26. Qb5 Qxb5 27. axb5 Nxc4 28. d6 Nd2 29. Bxb7+ Kxb7 30. Rbe1 1-0
1. e4 d5 2. exd5 Qxd5 3. Nc3 Qd8 4. Nf3 Nf6 5. d4 g6 6. Bc4 Bg7 7. Bg5 O-O 8. O-O Be6 9. Bxe6 fxe6 10. Re1 Nc6 11. d5 e5 12. dxc6 1-0
1. e3 e5 2. Nc3 Nf6 3. Bc4 d5 4. Bb3 c5 5. Ba4+ Bd7 6. Bxd7+ Qxd7 7. d4 exd4 8. exd4 cxd4 9. Qxd4 Qe6+ 10. Be3 Ne4 11. Nf3 Nxc3 12. Qxc3 Nc6 13. Nd4 Nxd4 14. Qxd4 a5 15. a3 b5 16. O-O Be7 17. Rad1 O-O 18. Qxd5 Qxd5 19. Rxd5 b4 20. Rd7 Rfe8 21. axb4 Bxb4 22. c3 Be7 23. Rfd1 a4 24. Ra1 h6 25. Rd4 Bf6 26. Rdxa4 Rxa4 27. Rxa4 g5 28. g3 h5 29. Kg2 Kg7 30. h4 gxh4 31. gxh4 Bxh4 32. Rxh4 Kg6 33. b4 Re5 34. Bd4 Rg5+ 35. Kf3 f5 36. c4 Rg4 37. Rxg4+ fxg4+ 38. Kg3 Kg5 39. b5 h4+ 40. Kg2 h3+ 41. Kh2 Kh4 42. Be5 Kg5 43. b6 Kf5 44. Bg3 Ke4 45. b7 Kf3 46. b8=Q Ke2 47. Qd8 Kf1 48. Qd1# 1-0
1. Nf3 f6 2. d3 e5 3. Nbd2 g5 4. e4 g4 5. Ng1 Bb4 6. Qxg4 d5 7. Qh5+ Kf8 8. a3 dxe4 9. axb4 exd3 10. Bxd3 e4 11. Bc4 f5 12. Qf7# 1-0
1. e4 d5 2. exd5 Qxd5 3. Nc3 Qa5 4. b3 c6 5. Bb2 Nf6 6. Be2 Bf5 7. Nf3 e6 8. O-O Nbd7 9. a3 Qc7 10. a4 Bd6 11. d3 Ng4 12. h3 Ngf6 13. Ne4 Nxe4 14. dxe4 Bg6 15. Bd3 f6 16. Nh4 Bf7 17. g3 Qb6 18. Kg2 g5 19. Nf3 h5 20. Nh2 Qc7 21. Qf3 Ne5 22. Qxf6 Nxd3 23. Qxh8+ Kd7 24. Qg7 Nxb2 25. Qxf7+ Kc8 26. Qe8+ Qd8 27. Qxe6+ Kc7 28. Qf7+ Be7 29. Qxh5 Qd2 30. Qf7 Qd6 31. Rfb1 Rf8 32. Qg7 Qf6 33. Qxf6 Bxf6 34. Ra2 c5 35. Raxb2 Bxb2 36. Rxb2 Rd8 37. c4 Rd3 1-0
1. e4 c6 2. e5 d6 3. exd6 exd6 4. d4 g6 5. Bd2 Bg7 6. Bc3 Ne7 7. Bc4 Be6 8. b3 b5 9. Bxe6 fxe6 10. d5 Nxd5 11. Bxg7 Rg8 12. Bh6 Qf6 13. c3 Nd7 14. Qf3 O-O-O 15. Ne2 Qxf3 16. gxf3 Ne5 17. Nd4 Rde8 18. f4 Nd3+ 19. Kf1 Kb7 20. Nd2 N5xf4 21. Bxf4 Nxf4 22. Ne4 Rgf8 23. Nxd6+ Kb6 24. Nxe8 Rxe8 25. Re1 c5 26. Rxe6+ Nxe6 27. Nxe6 Rxe6 28. Rg1 a5 29. Rg4 Kc6 30. Rg5 Kd6 31. Kg2 Re5 32. Rg4 h5 33. Rxg6+ Kd5 34. Ra6 c4 35. Rxa5 Kc6 36. b4 Rg5+ 37. Kf1 Rg8 38. Ra6+ 1-0
1. f4 d5 2. Nf3 Nc6 3. e3 e6 4. Bb5 Nf6 5. d3 Bd7 6. O-O a6 7. Ba4 b5 8. Bb3 Bd6 9. c3 O-O 10. Bc2 h6 11. e4 dxe4 12. dxe4 Be7 13. e5 Nd5 14. Qd3 g6 15. f5 exf5 16. Bxh6 Re8 17. Qxd5 Be6 18. Qxd8 Raxd8 19. Nbd2 Rd5 20. Rae1 Bc5+ 21. Kh1 Red8 22. Nb3 Bb6 23. Bg5 R8d7 24. Bf6 a5 25. Rd1 a4 26. Nc1 Be3 27. Nd3 Na5 28. Nb4 Rxd1 29. Rxd1 Rxd1+ 30. Bxd1 Nc4 31. Nd3 Na5 32. Bd8 Bb6 33. a3 Bc4 34. Nb4 Kf8 35. Nd4 Ke8 36. Bf6 Bxd4 37. cxd4 Kd7 38. d5 Nb7 39. Bf3 Nc5 40. Nc6 Nd3 41. Na5 Nxb2 42. Nxc4 bxc4 43. e6+ fxe6 44. Bxb2 exd5 45. Bxd5 Kd6 46. Bxc4 g5 47. Bb5 c6 48. Bxa4 Kd5 49. Bc2 f4 50. Bc1 Ke5 51. Kg1 c5 52. Kf2 g4 53. g3 f3 54. Be3 Kd5 55. Bf4 c4 56. a4 Kc5 57. Be5 Kb4 58. a5 1-0
1. e4 e5 2. Nc3 Nf6 3. d3 c6 4. f4 exf4 5. Bxf4 d5 6. e5 d4 7. Nce2 Nd5 8. Bd2 c5 9. c4 Ne3 10. Bxe3 dxe3 11. Nf3 Be7 12. Nc3 Bg4 13. Be2 O-O 14. O-O Nc6 15. Nd5 Nd4 16. Nxd4 cxd4 17. Bxg4 Bc5 18. e6 fxe6 19. Bxe6+ Kh8 20. Rxf8+ Qxf8 21. Qf3 Qd6 22. Bf5 Rf8 23. Qe4 g6 24. Bg4 a5 25. Bf3 Ba7 26. a3 Bb8 27. g3 Ba7 28. b4 h5 29. c5 Qd7 30. Qxg6 Qh7 31. Qxh7+ Kxh7 32. Bxh5 Bb8 33. Rf1 Rd8 34. Nf6+ Kh6 35. g4 Kg5 36. Kg2 axb4 37. axb4 Rc8 38. Ne4+ Kh6 39. Rf6+ Kg7 40. g5 Be5 41. Rf7+ Kg8 42. Rxb7 Rf8 43. Bf3 Ra8 44. Ng3 Ra2+ 45. Ne2 Bf4 46. h4 Kf8 47. b5 Rd2 48. c6 Rxd3 49. b6 1-0
1. d4 d5 2. h3 e6 3. a3 Nf6 4. Nf3 b6 5. e3 c5 6. c4 cxd4 7. Qxd4 Nc6 8. Qd1 Be7 9. cxd5 Nxd5 10. Bb5 Bb7 11. Bxc6+ Bxc6 12. e4 Nf6 13. Qxd8+ Rxd8 14. Nc3 O-O 15. e5 Bxf3 16. gxf3 Nd5 17. Nxd5 Rxd5 18. f4 f6 19. Be3 fxe5 20. fxe5 Rxe5 21. O-O-O Bf6 22. Kb1 Rb5 23. Rd2 Rd8 24. Rhd1 Rf8 25. Ka2 a5 26. Rd6 e5 27. b4 axb4 28. axb4 Ra8+ 29. Kb3 Be7 30. Rxb6 Rxb6 31. Bxb6 Rb8 32. Ba5 Rb5 33. Ka4 Rb7 34. Re1 Bd6 35. Rd1 Rd7 36. Rc1 Kf7 37. Rg1 g6 38. h4 Ke6 39. Rg5 Rf7 40. Bb6 Rf4 41. h5 Kf6 42. Rg2 gxh5 43. Ba5 Rg4 44. Rh2 h4 45. f3 Rf4 46. Rh3 Kf5 47. Kb5 e4 48. fxe4+ Kxe4 49. Kc6 Be5 50. b5 Rf6+ 51. Kd7 Rd6+ 52. Ke7 Rd5 53. Rxh4+ Kf3 54. Rb4 Bd6+ 55. Ke6 Bxb4 56. Kxd5 Bxa5 57. Kc6 h5 58. Kb7 h4 59. Ka6 Bd8 60. b6 Bxb6 61. Kxb6 h3 0-1
1. d4 d5 2. c4 c5 3. e3 e6 4. cxd5 cxd4 5. dxe6 dxe3 6. Qxd8+ Kxd8 7. exf7 exf2+ 8. Kxf2 Nf6 9. Bg5 Be6 10. Nf3 Bxf7 11. Nc3 Be7 12. Be2 Nc6 13. Rhd1+ Kc7 14. Bf4+ Kc8 15. Bb5 Bc5+ 16. Kf1 Nb4 17. a3 Nc2 18. Rac1 Ne3+ 19. Bxe3 Bxe3 20. Rc2 a6 21. Re2 axb5 22. Rxe3 Bc4+ 23. Kg1 Re8 24. Rxe8+ Nxe8 25. Ne5 h6 26. Nxc4 bxc4 27. Rd4 b5 28. Nxb5 Kb7 29. Nd6+ Kb6 30. Nxc4+ Kc5 0-1
1. e4 e5 2. Bc4 Qf6 3. d3 Bc5 4. Qf3 d6 5. Nc3 c6 6. Bg5 Qxf3 7. Nxf3 h6 8. Bh4 g5 9. Bg3 Nf6 10. h4 g4 11. Nd2 h5 12. f3 Nbd7 13. fxg4 Nxg4 14. Rf1 Ndf6 15. Nf3 Be6 16. Ng5 Bxc4 17. dxc4 O-O-O 18. Bf2 Nxf2 19. Rxf2 Bxf2+ 20. Kxf2 Ng4+ 21. Kg1 Rdf8 22. Rf1 f6 23. Ne6 Kd7 24. Nxf8+ Rxf8 25. Rf5 Ke6 26. Rxh5 Ne3 27. Rh7 Nxc4 28. b3 Ne3 29. Rxb7 Nxc2 30. Rxa7 Rh8 31. g3 Rg8 32. Kh2 Ne3 33. Ra6 c5 34. Nb5 Rd8 35. h5 Ng4+ 36. Kh3 f5 37. exf5+ Kxf5 38. Rxd6 Rxd6 39. Nxd6+ Kg5 40. a4 Nf6 41. a5 Nd7 42. Ne4+ Kxh5 43. a6 Kg6 44. a7 Nb6 45. Nxc5 Kf5 46. Nd7 e4 47. Nxb6 e3 48. a8=Q e2 49. Qf3+ 1-0
1. e4 c6 2. Bc4 d5 3. exd5 cxd5 4. Bb3 Nf6 5. c3 Nc6 6. d3 e5 7. h3 Bd6 8. Ne2 Be6 9. O-O O-O 10. f4 e4 11. dxe4 Nxe4 12. Nd4 Kh8 13. f5 Nxd4 14. cxd4 Bd7 15. Bxd5 Bc6 16. Bxc6 bxc6 17. Nc3 Nxc3 18. bxc3 c5 19. d5 c4 20. Be3 Re8 21. Bd4 Be5 22. Bxe5 Rxe5 23. Qd4 Qb6 24. Qxb6 axb6 25. d6 Rd5 26. Rf4 b5 27. Rd4 Rxd4 28. cxd4 Rd8 29. Rb1 g6 30. Rxb5 Rxd6 31. fxg6 fxg6 32. Rc5 Rxd4 33. a4 c3 34. a5 Ra4 35. Rxc3 Rxa5 36. g4 Ra2 37. Rc7 h5 38. Rc6 Kg7 39. gxh5 gxh5 40. Rc4 Kg6 41. h4 Kf5 42. Rc5+ Kg4 43. Rc4+ Kg3 44. Re4 Ra1+ 45. Re1 Rxe1# 0-1
1. e4 e5 2. Nf3 Nc6 3. Bb5 Nf6 4. Bxc6 dxc6 5. d3 Bd6 6. O-O O-O 7. Nbd2 b5 8. Qe2 a5 9. h3 Bd7 10. a4 b4 11. b3 c5 12. Nc4 Be7 13. Ncxe5 Be6 14. Bb2 Qc8 15. Rad1 h6 16. Kh2 Re8 17. Ng1 Nh7 18. f4 f6 19. Nef3 Bf7 20. f5 Bd6+ 21. Kh1 c6 22. Bc1 Bc7 23. Qf2 Bh5 24. g4 Bf7 25. Nh4 Ng5 26. Bf4 Bxf4 27. Qxf4 Re7 28. Ng2 Qc7 29. Qxc7 Rxc7 30. h4 Nh7 31. Kh2 Re8 32. Kg3 Rd7 33. Nf4 Nf8 34. Nf3 Red8 35. g5 hxg5 36. hxg5 fxg5 37. Nxg5 Be8 38. Rh1 g6 39. Rh6 Kg7 40. Rdh1 Kf6 41. Nf3 Rg7 42. Kg4 Ke7 43. e5 Kd7 44. f6 Rf7 45. e6+ Kc7 46. exf7 Bxf7 47. Rh7 Rd7 48. Rxf7 Rxf7 49. Kg5 Kd6 50. Ne6 1-0
1. e4 c5 2. Nf3 Nc6 3. d4 cxd4 4. Nxd4 e5 5. Nb3 a6 6. Nc3 b5 7. Nd5 Bb4+ 8. c3 Bf8 9. Be3 Nf6 10. h3 Nxe4 11. Bd3 f5 12. Bxe4 fxe4 13. O-O Be7 14. Bc5 Bxc5 15. Nxc5 d6 16. Nxe4 Be6 17. Ne3 O-O 18. Qxd6 Qxd6 19. Nxd6 e4 20. a3 Ne5 21. Nxe4 Nd3 22. Rad1 Nxb2 23. Rd2 Nc4 24. Nxc4 Bxc4 25. Nd6 Bxf1 26. Kxf1 Rad8 27. Ne4 Rxd2 28. Nxd2 Rc8 29. c4 bxc4 30. Ne4 c3 31. Nd6 c2 32. Ne4 c1=Q+ 33. Ke2 Rc2+ 34. Kf3 0-1
1. d4 b6 2. e4 Bb7 3. Ba6 g6 4. Bxb7 Na6 5. Bxa8 Qxa8 6. Nc3 c6 7. Qe2 b5 8. Nf3 Qb7 9. O-O b4 10. Nd1 c5 11. dxc5 Nxc5 12. c3 Qxe4 13. Qxe4 Nxe4 14. Ne3 bxc3 15. bxc3 Nxc3 16. Bb2 Ne2+ 17. Kh1 f5 18. Rfe1 Nf4 19. g3 Nh5 20. Ng5 Bh6 21. f4 Bxg5 22. fxg5 h6 23. Nd5 hxg5 24. Bxh8 Kf7 25. Bb2 e6 26. Nc3 Ngf6 27. Rad1 Ne4 28. Nxe4 fxe4 29. Rxd7+ Ke8 30. Rxa7 Nxg3+ 31. hxg3 g4 32. Rc1 g5 33. Rc8# 1-0"""


def boards():
    for line in GAMES.splitlines():
        game = chess.pgn.read_game(io.StringIO(line))
        board = game.board()
        yield board
        for move in game.mainline_moves():
            board.push(move)
            yield board


async def thread(producer):
    _, engine = await chess.engine.popen_uci("stockfish")
    await engine.configure({"Use NNUE": False})

    nodes = 0

    while True:
        try:
            board = next(producer).copy()
        except StopIteration:
            break

        info = await engine.analyse(board, chess.engine.Limit(nodes=10000), game=object())
        print(".", end="", flush=True)
        nodes += info.get("nodes", 0)

    return nodes


async def main():
    cpus = os.cpu_count()

    print("Threads:", cpus)
    print("Positions:", sum(1 for _ in boards()))
    print("---")

    producer = boards()
    start = time.time()
    nodes = sum(await asyncio.gather(*[thread(producer) for _ in range(cpus)]))
    elapsed = time.time() - start

    print()
    print("---")
    print("Nodes:", nodes)
    print("Elapsed:", elapsed)
    print("Nodes/s:", nodes / elapsed)


if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
