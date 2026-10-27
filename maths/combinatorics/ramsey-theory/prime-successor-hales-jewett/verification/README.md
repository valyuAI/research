# Hales-Jewett: exhaustive finite certificate check

From this directory:

```bash
mkdir -p build
c++ -std=c++17 -O2 -Wall -Wextra verify_hj8.cpp -o build/verify_hj8
./build/verify_hj8 hj8_blue_histograms.csv > hj8_independent_verification.json
```

No external library is required. The CSV records the 490 blue coordinate histograms in the eight-letter, seven-coordinate cube. Every row has eight nonnegative counts summing to seven; coordinate permutations have the same color.

The verifier independently enumerates all 8^7 = 2,097,152 points and all 9^7 - 8^7 = 2,685,817 ordered nonempty variable words. It checks the saved certificate against the compact formula, tests every full line for a blue point, and tests every consecutive pair for the absence of two blue points. Progress goes to standard error; the result JSON goes to standard output. A nonzero exit code indicates a failed check or invalid input.

The saved result has 299,587 blue points and zero violations or formula disagreements. The finite enumeration supports this instance; the general prime-family theorem is proved in the paper and in Lean.
