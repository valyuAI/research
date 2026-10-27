# Search logs

Original search runs (26 October 2026). These are evidence from the search programs, not proofs; the proofs are the replayed certificates.

| Log | Program | Content |
|---|---|---|
| `hexmb_5_L6_centre.log` | `src/hexmb.c` (plain walk search) | Blue wins $\mathrm{Hex}(5,6)$ from the centre |
| `d6_8.log`, `d6_9.log` | `src/hexmb2.c` (walk search, null-move pruning) | Red holds $\mathrm{Hex}_8(6)$, $\mathrm{Hex}_9(6)$ after all 18 opening classes |
| `h3_d6_9.log`, `h3_d6_10.log` | `src/hexmb3.c` | $\mathrm{Hex}_9(6)$: Red for all classes; $\mathrm{Hex}_{10}(6)$: Blue only from $(3,4)$ |
| `h3_l6_7.log`, `h3_l6_8.log` | `src/hexmb3.c` | $\mathrm{Hex}(6,7)$: Red for all classes; $\mathrm{Hex}(6,8)$: Blue only from $(3,4)$ (2.9e9 positions); basis of Proposition 1.3 |
| `cert_n6D9.log`, `cert_n6D10.log` | `src/hexmb3.c` with `CERT` | generation of the 6x6 $\delta$ certificates (byte-identical when regenerated with `src/hexmb4.c`) |
| `strict_r_5_6.log` | `src/hexstrict.c` run with `BLUEREL=1` (exact (Blue, Red) keys; Blue restricted to live cells, Red unrestricted) | Blue succeeds in $\mathrm{Hex}^*(5,6)$ from the centre |
| `strict2c_5_6.log` | `src/hexstrict2.c` with `CERT` | same result, with certificate |
| `table5_raw.txt` | `src/hexmb3.c` | every 5x5 opening for bounds 5 to 13 in both modes (source of Figure 1, now certified by `table5.sh`) |

Openings are 1-based (row, column); "18 opening classes" means one opening per half-turn pair.
