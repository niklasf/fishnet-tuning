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
