# Work in progress

These investigations are separate from the manuscript collection. A checked
calculation is not necessarily new, and a useful simulation is not an observed
biological finding. Each package states what survived review and what remains
unresolved.

- [Four-measurement promoter calibration](biology/promoter-calibration/): a
  frozen panel transferred to 202 nonoverlapping promoters in a second reporter
  library, with modest improvement over random panels and worse mean error
  than full calibration. This is an exploratory benchmark.
- [Gene-switching state tests](biology/gene-switching/): sharp mean-dwell
  certificates, concentration design and an ideal-observation statistical
  test. The underlying equilibrium mechanism was identified as an established
  exclusion process. Originality of the inference results remains open.
  A separate real-data check reproduces the published burst detector to
  numerical precision; the full fluorescence-inference comparison remains open.

## Negative and unresolved results

These outcomes from the 18 October exploration round are recorded so that
they are not mistaken for findings.

- **Promoter calibration.** The same-study transfer is independently checked.
  A later benchmark in a different laboratory's mouse assay weakens
  generalization: the four-point model does not beat a simple fixed-slope
  model and is worse than full calibration. That benchmark is frozen but has
  not had an independent numerical review. The package remains an exploration.
- **Gene switching.** The mechanism is a known exclusion process. The
  singleton-state argument and the gamma, Bonferroni and intersection-union
  machinery are standard. Priority of the sharp three-dose tolerance and
  placement result is unresolved. The published burst detector was
  reproduced; complete fluorescence deconvolution and biological
  discrimination were not performed.
- **Single-cell estimation.** An exact synthetic example and a frozen stress
  test show a sign reversal when a decoder is applied after barycentric
  averaging. The underlying Jensen bias is established prior work. No trained
  biological model or published conclusion was tested, and the empirical
  follow-up was not completed. No package is included.
- **Age clocks.** The recovered coefficients and metadata did not supply the
  purified-cell references or complete array-mapping conventions needed for
  the proposed certificate. This does not establish an artefact. No package
  is included.
