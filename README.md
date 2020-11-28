Fishnet tuning
==============

Hash size
---------

Setup: In reproducible analysis, Stockfish uses 1 thread and the hashtable is
cleared after every move. A fixed number of nodes (1M) is searched at
each position. Hardware is irrelevant. Playing each position from
`noob_3moves_sample.epd` with rematch with reversed colors. No adjudication.

```
HASH(1): 335
draw: 1305
HASH(512): 360
```

Elo diff estimate: -4

```
HASH(16): 334
draw: 1316
HASH(512): 350
```

Elo diff estimate: -3

Forgetfulness
-------------

Setup: A fixed number of nodes (1M) is searched at each position. Both
engines have 512M hash, but FORGET clears its hashtable after every move.

```
FORGET: 88
draw: 862
REMEMBER: 1050
```

Elo diff estimate: -182

CPU comparisons
---------------

https://docs.google.com/spreadsheets/d/1RjL0xcZC94qFtkgd_lDN2jgwHF5rkf6FcOF2rEM4I7I/edit?usp=sharing

NNUE nodes vs classical nodes
-----------------------------

```
Rank Name                                       Elo     +/-   Games   Score    Draw
   1 stockfish-12-dev-nodes-4000000             101      53      60   64.2%   61.7%
   2 stockfish-12-dev-nodes-3000000              47      56      60   56.7%   60.0%
   3 stockfish-12-dev-nodes-3500000              17      38      60   52.5%   81.7%
   4 stockfish-fishnet-20200613-nodes-4000000  -176      61      60   26.7%   50.0%
120 of 120 games finished.
```

```
Score of stockfish-fishnet-20200613-nodes-4000000 vs stockfish-12-dev-nodes-2500000: 4 - 23 - 23 [0.310]
...      stockfish-fishnet-20200613-nodes-4000000 playing White: 4 - 7 - 14  [0.440] 25
...      stockfish-fishnet-20200613-nodes-4000000 playing Black: 0 - 16 - 9  [0.180] 25
...      White vs Black: 20 - 7 - 23  [0.630] 50
Elo difference: -139.0 +/- 72.2, LOS: 0.0 %, DrawRatio: 46.0 %
50 of 50 games finished.
```

```
Score of stockfish-fishnet-20200613-nodes-4000000 vs stockfish-12-plus-nodes-2000000: 1 - 25 - 24 [0.260]
...      stockfish-fishnet-20200613-nodes-4000000 playing White: 1 - 7 - 17  [0.380] 25
...      stockfish-fishnet-20200613-nodes-4000000 playing Black: 0 - 18 - 7  [0.140] 25
...      White vs Black: 19 - 7 - 24  [0.620] 50
Elo difference: -181.7 +/- 68.7, LOS: 0.0 %, DrawRatio: 48.0 %
50 of 50 games finished.
```
