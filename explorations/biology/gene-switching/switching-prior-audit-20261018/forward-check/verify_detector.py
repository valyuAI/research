"""Reproduce published ON-probability summaries from supplied initiation posteriors.

This checks only ExtractIniPheno's quartic smoothing, threshold and temporal
weighting. It neither observes true promoter states nor reruns deconvolution.
"""

from pathlib import Path
import json
import time

import h5py
import numpy as np


def main():
  folder = Path(__file__).resolve().parent
  targetTimes = np.arange(15, 301, dtype=float) / 6
  weightedOn = np.zeros(targetTimes.size)
  weights = np.zeros(targetTimes.size)
  windowMinutes = 5 / 6
  thresholdPerMinute = 2 / windowMinutes
  started = time.monotonic()
  with h5py.File(folder / 'DECONV_hb_MS2_INTRON_Nc14_AP16.mat', 'r') as source:
    data = source['OutTr']
    nTraces = data['tt'].shape[0]
    for index in range(nTraces):
      timesFine = source[data['tt'][index, 0]][()].ravel().astype(float)
      observed = source[data['I'][index, 0]][()].ravel().astype(bool)
      times = timesFine[observed]
      counts = source[data['Gs'][index, 0]][()].T.astype(float)
      interval = np.concatenate(([np.inf], np.diff(times)))
      rates = counts / interval
      differences = times[:, None] - times[None, :]
      kernel = np.exp(-((differences / (windowMinutes / 2)) ** 4))
      kernel /= kernel.sum(axis=0, keepdims=True)
      calledOn = (rates @ kernel) >= thresholdPerMinute
      posteriorOn = calledOn.mean(axis=0)
      localWeights = np.maximum(0, 1 - np.abs(times[None, :] - targetTimes[:, None]) * 6)
      weightedOn += localWeights @ posteriorOn
      weights += localWeights.sum(axis=1)
      if (index + 1) % 20 == 0 or index + 1 == nTraces:
        print(f'{index + 1}/{nTraces} traces checked, {time.monotonic() - started:.1f}s', flush=True)
  reconstructedOn = weightedOn / weights
  with h5py.File(folder / 'BPHENO_hb_MS2_INTRON_Nc14_AP16.mat', 'r') as source:
    publishedOn = source['OutPr/pn'][()][:, 1]
  discrepancy = reconstructedOn - publishedOn
  result = {
    'scope': 'Detector-stage reproduction on real posterior initiation samples, not a forward model fit',
    'nTraces': nTraces,
    'posteriorSamplesPerTrace': int(counts.shape[0]),
    'nTimepoints': int(targetTimes.size),
    'windowSeconds': 60 * windowMinutes,
    'thresholdInitiationsPerWindow': 2,
    'maximumAbsoluteOnProbabilityDifference': float(np.max(np.abs(discrepancy))),
    'rmsOnProbabilityDifference': float(np.sqrt(np.mean(discrepancy ** 2))),
    'elapsedSeconds': time.monotonic() - started,
    'numpyVersion': np.__version__,
    'h5pyVersion': h5py.__version__,
  }
  (folder / 'detector-reproduction.json').write_text(json.dumps(result, indent=2) + '\n')
  np.savetxt(folder / 'detector-reproduction.csv', np.column_stack((targetTimes, publishedOn, reconstructedOn)), delimiter=',', header='time_minutes,published_on_probability,reconstructed_on_probability', comments='')
  print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
  main()
