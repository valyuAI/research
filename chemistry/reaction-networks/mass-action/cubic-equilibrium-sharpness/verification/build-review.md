# Build and presentation review

Checked 18 October 2026 from the canonical package directory.

- `sh build.sh --regenerate-certificate` passed. The generator reconstructed all 35 prescribed equilibria for `n = 2,...,8`; the independent standard-library checker replayed them and rejected corrupted products, concentrations and rates. Both ran with `python3 -B -O`.
- The default `sh build.sh` also passed. It uses the saved certificate and requires no SymPy installation for its verification step.
- Both author presentations compiled to four pages. Final logs contain no LaTeX or pdfTeX warnings, overfull boxes or underfull boxes.
- All eight final pages were rendered at 90 dpi and visually inspected. Equations, source and product formulas, the three-species table, reproduction commands and bibliography links are legible without clipping or overlap.
- Both checker source files are byte-identical to the independently audited originals. A separate mathematical review checked the all-`n` proof, the published minimality implication, and the open-neighbourhood argument. A separate package and simplification review found no substantive issue.
- The mathematical source is shared between the two author presentations. Curation changed reproduction paths and citation presentation, without altering the theorem or proof.
- The single-author presentation includes the research-assistance statement. After that final addition, all paper pages and journal pages 1-3 were pixel-identical to their inspected versions; the changed journal page 4 was rendered and inspected again. Both final logs remained clean.

No third-party full text, credentials, private service details, search-response dumps or unreviewed extension is included. Finite arithmetic checks and the analytic all-`n` proof remain explicitly distinguished. External peer review and exhaustive historical priority are not claimed.

## Submission-preparation pass, 18 October 2026

The abstract now leads with the precise sharpness and minimality result and states parameter persistence. The single-author version now identifies the coding agents' actual roles in developing the construction and proof, verification code, and manuscript, alongside DeepResearch literature work. No completed human author review is asserted. Separate readiness and author-walkthrough documents record outstanding decisions.

Both exact programs passed again with `python3 -B -O`; the regenerated certificate differs from the saved one only in elapsed time, and the original timing field was retained to avoid a content-free artifact change. `sh build.sh` then rebuilt both four-page PDFs. Final logs contain no warnings or overfull/underfull boxes. All eight final pages were rendered at 100 dpi and visually inspected with no clipping, overlap, broken equation, malformed table or unresolved citation. The all-`n` formulas and checker sources are unchanged.
