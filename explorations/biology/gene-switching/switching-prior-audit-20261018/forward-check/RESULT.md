# Hunchback observation audit and detector reproduction

18 October 2026. Bounded empirical follow-up.

**The real-data burst detector is now reproduced to numerical precision. The supplied files do not contain calibrated ligand concentrations or directly observed promoter dwell times. A complete four-state forward observation comparison was not run.**

## Verified empirical result

`verify_detector.py` applies the operation from the authors' `ExtractIniPheno.m` to the supplied posterior initiation counts. It processes all **217 allele traces**, **1,000 posterior samples per trace**, and **286 common timepoints**. It reproduces the authors' saved ON-probability curve with:

- maximum absolute error: **6.8834e-15**;
- root mean squared error: **2.0890e-15**.

This is a direct comparison with `OutPr.pn` in the public `BPHENO_hb_MS2_INTRON_Nc14_AP16.mat`, not a simulation compared with its own expected output. Numerical results are in `detector-reproduction.json`; complete compared curves are in `detector-reproduction.csv`.

The checked operation is:

1. For each posterior sample, divide initiation counts in each observed interval by the actual interval duration. The first interval is assigned infinite duration, hence rate zero, matching the source.
2. Use a column-normalized kernel `exp(-((t_i-t_j)/(w/2))^4)` with `w=5/6 minute`, or 50 seconds.
3. Classify the smoothed initiation rate as ON when it is at least `2/w=2.4 initiations/minute`.
4. Average over posterior samples and use the authors' triangular temporal weights to pool irregularly timed traces onto the common 10-second grid.

This validates the detector implementation and its indexing against published data. It does not validate the underlying four-state switch or recover true promoter states. No mean-dwell distortion estimate is reported, because that would require a known latent state path and a corresponding complete observation/inference simulation.

## Actual downloaded data

Files came from the authors' [public GitLab repository](https://gitlab.pasteur.fr/tglab/liveburstrulepaper). URLs, byte counts and SHA-256 hashes are retained in `download-manifest.json`. Total download was approximately 176.2 MB. The [published experimental paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13137155/) and repository README describe the hunchback NC14 test case and link the full Zenodo archive.

| File | Content checked |
|---|---|
| `hb_MS2_INTRON_NC14_OutDS.mat` | MATLAB 5 structure `OutDS`, 35 spatial bins. Includes individual fluorescence traces and ensemble moments. |
| `DECONV_hb_MS2_INTRON_Nc14_AP16.mat` | MATLAB 7.3/HDF5 `OutTr`, 217 allele traces with posterior initiation events/counts and reconstructed fluorescence. |
| `BPHENO_hb_MS2_INTRON_Nc14_AP16.mat` | MATLAB 7.3/HDF5 `OutPr`, pooled time-varying burst summaries, distributions, covariances and uncertainty summaries. |
| `Kernel_hb_MS2_INTRON.mat` | Probe kernel: 25 positions `X`, from 0 to 4464 bp, and contributions `K`, from 1/24 to 1. |
| `MeasNoise2PhotonMS2.mat` | Serialized MATLAB anonymous function referring to fitted coefficients through a captured workspace, not a plain numeric noise-parameter array. |

The detector-only Python environment uses h5py 3.16.0 and NumPy 2.3.3. Source and package-security lookup records remain in the unpublished working archive. No project runtime dependencies were changed.

### Measured trace dictionary

Each `OutDS` bin contains `Traces`, spatial coordinate `AP`, time grid `Ti`, ensemble moments `M1/S2/K3/K4`, embryo-level arrays and `Corr`. Individual measured traces have these fields:

| Field | Checked interpretation / representation |
|---|---|
| `t` | Irregular measurement times, in minutes. |
| `int` | Measured calibrated transcription-spot fluorescence. It can be negative after background correction. |
| `mbg`, `sbg` | Background measurements; exact upstream estimator semantics were not audited. |
| `ap`, `dv` | Time-dependent embryo-position coordinates. |
| `emb`, `nid` | Embryo and nucleus identifiers. |
| `rs`, `A` | Additional measurement metadata; not needed for the reproduced detector and not interpreted here. |

There is **no ligand-concentration field and no true promoter-state field** in the checked trace structures. The AP coordinate is position in an embryo, not a calibrated free-TF dose.

The filename's `AP16` means the sixteenth bin **after the code filters for sufficient signal and trace count**. It corresponds to original `OutDS` bin 21, at `AP=0.4301882286`, with 217 traces. It is not original bin 16. This indexing was reproduced from `MainDeconvolution.m` and is saved in `ap-bin-mapping.json`.

The first stored deconvolution input intensity vector is exactly the float32 conversion of the corresponding measured intensity after the code's 2.5-to-50-minute crop. The largest difference before float32 conversion is 1.82e-6 intensity units. Posterior grid timestamps differ by at most 0.4963 seconds because measurements are mapped to the one-second internal grid. See `measured-posterior-match.json`.

### Posterior initiation dictionary

The HDF5 dimensions below appear reversed relative to MATLAB's ordinary array orientation.

| `OutTr` field | Example trace, HDF5 shape | Meaning from the inspected source |
|---|---:|---|
| `tt` | 2842 x 1 | Internal one-second grid, here 2.6337 to 49.9837 minutes. |
| `I` | 2842 x 1 | Mask selecting measurement-aligned positions on that grid. |
| `int` | 286 x 1 | Observed fluorescence input. |
| `Rs` | 2842 x 1000 | Posterior initiation-event configurations, binary. **These are initiation events, not promoter ON/OFF states.** |
| `Gs` | 286 x 1000 | Posterior initiation counts between measurement frames; first trace ranges from 0 to 9. |
| `R` | 2842 x 1 | Mean posterior initiation occupancy. |
| `G` | 286 x 2 | Mean and standard deviation of interval initiation counts. |
| `S` | 286 x 2 | Mean and standard deviation of reconstructed fluorescence. |
| `Ss` | 286 x 10 | Ten example reconstructed fluorescence samples. |

`OutPr.pn`, `tn`, `kn` and related arrays are time-dependent ensemble summaries. They do not provide a list of independent, complete physical state dwells. The detector derives episode calls from initiation posteriors; initial/final observation boundaries are finite, and the saved summaries use the paper's pooling and boundary conventions. They cannot simply be treated as the singleton exponential samples assumed by the proposed state-count test.

Full machine-readable dictionaries are in `mat-dictionary-initial.json`, `hdf5-dictionary.json`, `posterior-trace-example.json` and `measured-trace-bins.json`.

## Why a faithful four-state forward check stops here

The missing stage is substantial and concretely identified: **fluorescence generation followed by the original Bayesian deconvolution**, not just state discretization or smoothing of a latent promoter bit.

The inspected `DeconvSampling.m` uses a 60-bp polymerase footprint and 1800-bp/min elongation rate, giving a one-second combined-copy grid. It uses 3,500 MCMC samples, discards 500 as burn-in, and saves 1,000 selected initiation configurations. Proposals are adapted during sampling. The prior initiation probabilities depend on the measured time-varying ensemble signal `M1`. Likelihood evaluation uses the serialized MATLAB noise function.

Neither MATLAB nor Octave is installed. A replacement implementation would need to reproduce the probe convolution, captured noise fit, initiation prior, adaptive proposal, interpolation behavior and posterior diagnostics. The exact detector match above does not certify that larger port. Exact original MATLAB files for `ExtractIniPheno.m`, `DeconvSampling.m` and `MainDeconvolution.m` were recovered through the repository's immutable blob API using Valyu and decoded locally into `author-source/` in the unpublished working archive. Their blob IDs and hashes are in `exact-code-manifest.json`. These preserve runnable source bytes, unlike normalized web text extractions.

No surrogate simulation was used to manufacture a mean-dwell error estimate. A detector applied directly to sampled latent ON/OFF states would omit the actual measured variable and would not answer the scientific question.

## Next experiment specification

1. Run the recovered source with its helper functions and the MATLAB noise closure, or validate a Python deconvolution port against the supplied fluorescence/posterior test case. Preserve the exact `AP16` mapping above.
2. Add the four-state generator to the authors' simulation interface so it produces initiation events and latent states in the same format as their existing `GenTraceCycle` simulations. Include the same number of gene copies and explicitly set per-copy initiation rate.
3. Convolve initiations with the checked probe kernel, sample at the actual acquisition timestamps, and add the calibrated measurement noise. Keep latent states only as simulation truth.
4. Apply the same deconvolution and the now-validated detector. Use simulated ensemble means for the simulated-data prior; evaluate any data-dependent prior consistently when constructing held-out comparisons.
5. Report separately: latent mean dwells, observed called mean dwells, inferred activity, integrated/fit covariance times, boundary-censored event fractions and false-state transitions. Compare both the reversible witness and telegraph/cycle alternatives under identical observation conditions.
6. For a finite-dose state-count experiment, obtain externally calibrated free ligand concentrations and controlled stationarity. This hunchback dataset alone cannot supply those premises. Its immediate role is testing the observation model and predictive differences, not a calibrated three-dose certificate.

This follow-up ends with a reproducible real-data detector check and an explicit prerequisite for the full forward comparison. Confidence in the detector reproduction and data-format conclusions: **high**. Biological discrimination between the switching models remains **unassessed**.
