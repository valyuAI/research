# Published detector reproduction

The Python implementation matches the published hunchback ON-probability
summary to maximum absolute error `6.8834e-15`, across 217 real traces and
1,000 posterior initiation samples per trace. This verifies a detector stage;
it does not validate a biological switching mechanism or rerun fluorescence
deconvolution. See [the complete result](RESULT.md).

To reproduce, obtain the first two files in [download-manifest.json](download-manifest.json):
`DECONV_hb_MS2_INTRON_Nc14_AP16.mat` and
`BPHENO_hb_MS2_INTRON_Nc14_AP16.mat`. These are approximately 67 MB of public
scientific data. Verify their SHA-256 hashes and place them beside the script.
With NumPy and h5py available, run:

```bash
OPENBLAS_NUM_THREADS=1 python3 -u verify_detector.py
```

The checked environment used NumPy 2.3.3 and h5py 3.16.0. The script reports
progress and writes a JSON error summary and the complete compared curves.
Raw data and third-party MATLAB sources remain in the unpublished working archive;
their URLs and immutable source-blob hashes are retained here.

The downloaded fluorescence data do not supply calibrated ligand doses or
directly observed promoter dwell times. Applying the ideal complete-episode
state-count test directly to these summaries would violate its assumptions.
