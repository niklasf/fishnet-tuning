Fishnet tuning
==============

Hash size
---------

Setup: In reproducible analysis, Stockfish uses 1 thread and the hashtable is
cleared after every move. A fixed number of nodes (1M) is searched at
each position. Hardware is irrelevant. Playing each position from
`noob_3moves_sample.epd` with rematch with reversed colors. No adjudication.

Forgetfulness
-------------

Setup: A fixed number of nodes (1M) is searched at each position. Both
engines have 512M hash, but a clears its hashtable after every move.
