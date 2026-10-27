# Short forced wins in Hex

Audience: GCSE-level; no game theory assumed. 35 short Cedar clips. The actual 23-move game is retained and separately audited in `witness-data.json`. No source paper, checker or certificate was edited or rerun.

| Scene | Clips | Animation and learning step |
|---|---|---|
| TinyStrategy | h01-h05 | Edge adjacency, goal edges, then the 2x2 two-threat strategy. Red takes one completion; Blue visibly chooses the other. Defines adaptive strategy before notation. |
| TwoCosts | h06-h07 | Five rows require at least five path cells. Introduce path budget lambda and all-stones budget delta separately. |
| TheActualGame | h08-h14 | All 23 retained moves appear in order with move numbers. Trace the actual six-cell path; highlight the six extra Blue stones. Two-sided certified bounds combine into lambda(5)=6; a separate delta strategy yields 7. |
| AdaptiveProof | h15-h17 | Red blocks one preselected route, but the 2x2 alternative survives. Animate one-good-choice Blue node and every-reply Red node. |
| Checking | h18-h23 | Search, move table and independent replay. Enumerate reply cells; remove three real target sets hit by Red. Summarise retained 106,826-position replay. Compare both stopping rules; lambda(5)=lambda*(5)=6. |
| SixBySix | h24-h29 | Actual certified opening (3,4), ten Blue plus nine Red moves, all 36 openings for the path lower bound. Summarise 22,780,097 replay positions. Keep certified lower bound and search-only upper bound in distinct labelled statements. Strict6 stays in [8,10]. |
| Evidence | h30-h35 | Campbell, 2026 preprint correction, prior KataHex estimate, negative controls and no Lean claim. Certified recap, unknown larger cases and end card. |

First-view comprehension review: the 2x2 example introduces force and adaptation before lambda/delta; path and stone counts are counted separately in the real branch before universal claims. Game-tree AND/OR logic is explained without requiring Boolean vocabulary. A counter is explicitly a summary of retained records, not live computation. The 23-move branch is never offered as a universal proof. No exact certified lambda(6)=8 or exact strict6 value appears.

Accessibility: Blue/Red roles are spoken and written; actual-game move labels use odd/even parity as well as colour. Caption tracks reproduce the narration. No named creator's voice or brand is imitated.
