// Independent rank-seven exclusion in the basis 1,t,u,tu, with t^2=-d.
// Default u^2=0 gives F_(q^2)[u]/u^2; --split gives u^2=u as a positive control.
// Uses sorted full-matrix residuals and modular arithmetic, not field tables.
// Usage: check_local_rank7 3|5 [--split]
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <stdexcept>
#include <vector>

using Row = std::array<int, 16>;
using Form = std::array<int, 4>;
static int prime, d;
static bool split;

static int mod(int value) {
  value %= prime;
  return value < 0 ? value + prime : value;
}

static int inverse(int value) {
  for (int result = 1; result < prime; ++result) {
    if (value * result % prime == 1) return result;
  }
  throw std::runtime_error("Cannot invert zero");
}

struct Basis {
  std::array<Row, 16> rows{};
  std::array<int, 16> pivots{};
  int size = 0;

  Row reduce(Row value) const {
    for (int i = 0; i < size; ++i) {
      int coefficient = value[pivots[i]];
      if (coefficient) {
        for (int j = 0; j < 16; ++j) {
          value[j] = mod(value[j] - coefficient * rows[i][j]);
        }
      }
    }
    return value;
  }

  bool add(Row value) {
    value = reduce(value);
    int pivot = 0;
    while (pivot < 16 && value[pivot] == 0) ++pivot;
    if (pivot == 16) return false;
    int scale = inverse(value[pivot]);
    for (int &entry : value) entry = entry * scale % prime;
    // Forward elimination suffices: every later row is zero at earlier pivots.
    rows[size] = value;
    pivots[size++] = pivot;
    return true;
  }
};

static std::uint64_t projectiveKey(Row value) {
  int pivot = 0;
  while (pivot < 16 && value[pivot] == 0) ++pivot;
  if (pivot == 16) return 0;
  int scale = inverse(value[pivot]);
  std::uint64_t key = 0;
  for (int entry : value) key = key * prime + entry * scale % prime;
  return key;
}

static Row outer(Form left, Form right) {
  Row result{};
  for (int i = 0; i < 4; ++i) {
    for (int j = 0; j < 4; ++j) result[4 * i + j] = left[i] * right[j] % prime;
  }
  return result;
}

int main(int argc, char **argv) {
  if (argc < 2 || argc > 3 || (std::strcmp(argv[1], "3") && std::strcmp(argv[1], "5")) ||
      (argc == 3 && std::strcmp(argv[2], "--split"))) {
    std::fprintf(stderr, "Usage: check_local_rank7 3|5 [--split]\n");
    return 2;
  }
  prime = argv[1][0] - '0';
  d = prime == 3 ? 1 : 2;
  split = argc == 3;
  std::setvbuf(stdout, nullptr, _IOLBF, 0);
  std::array<Row, 4> slices{};
  // Coordinates i encode t^(i%2) u^(i/2), so multiplication is explicit.
  for (int i = 0; i < 4; ++i) {
    for (int j = 0; j < 4; ++j) {
      int tDegree = i % 2 + j % 2;
      int uDegree = i / 2 + j / 2;
      if (uDegree == 2 && !split) continue;
      if (uDegree == 2) uDegree = 1;
      int coefficient = tDegree == 2 ? prime - d : 1;
      slices[tDegree % 2 + 2 * uDegree][4 * i + j] = coefficient;
    }
  }
  Basis sliceBasis;
  for (Row row : slices) sliceBasis.add(row);
  if (sliceBasis.size != 4) throw std::runtime_error("Slice dimension is not four");

  std::vector<Form> forms;
  for (int code = 1; code < prime * prime * prime * prime; ++code) {
    Form form{};
    int rest = code, first = 0;
    for (int &entry : form) {
      entry = rest % prime;
      rest /= prime;
      if (!first && entry) first = entry;
    }
    if (first == 1) forms.push_back(form);
  }
  std::vector<Row> matrices, images;
  for (Form left : forms) {
    for (Form right : forms) {
      Row row = outer(left, right);
      matrices.push_back(row);
      images.push_back(sliceBasis.reduce(row));
    }
  }
  // For the local algebra, units have two orbits on projective functionals:
  // those vanishing on (u), and those not vanishing there. The two chosen
  // coordinate forms represent them. Transpose identifies the mixed pair.
  // A split-control success needs no exhaustive orbit coverage.
  Form constant{1, 0, 0, 0}, nilpotent{0, 0, 1, 0};
  std::array<Row, 3> firstForms{
    outer(constant, constant), outer(constant, nilpotent), outer(nilpotent, nilpotent)
  };
  std::vector<std::pair<std::uint64_t, int>> sorted(matrices.size());
  std::uint64_t prefixes = 0, candidates = 0;
  auto start = std::chrono::steady_clock::now();
  std::printf("q=%d basis=1,t,u,tu u^2=%s forms=%zu rank-ones=%zu\n",
              prime, split ? "u" : "0", forms.size(), matrices.size());
  for (int representative = 0; representative < 3; ++representative) {
    Row first = sliceBasis.reduce(firstForms[representative]);
    for (std::size_t second = 0; second < matrices.size(); ++second) {
      Basis prefix;
      if (!prefix.add(first) || !prefix.add(images[second])) continue;
      ++prefixes;
      for (std::size_t i = 0; i < matrices.size(); ++i) {
        sorted[i] = {projectiveKey(prefix.reduce(images[i])), static_cast<int>(i)};
      }
      std::sort(sorted.begin(), sorted.end());
      Basis common;
      std::size_t position = 0;
      while (position < sorted.size() && sorted[position].first == 0) {
        common.add(matrices[sorted[position++].second]);
      }
      while (position < sorted.size()) {
        std::size_t end = position + 1;
        while (end < sorted.size() && sorted[end].first == sorted[position].first) ++end;
        if (end - position >= static_cast<std::size_t>(7 - common.size)) {
          ++candidates;
          Basis candidate = common;
          for (std::size_t i = position; i < end && candidate.size < 7; ++i) {
            candidate.add(matrices[sorted[i].second]);
          }
          if (candidate.size == 7) {
            std::printf("RESULT rank<=7: YES prefixes=%llu candidates=%llu\n",
                        static_cast<unsigned long long>(prefixes), static_cast<unsigned long long>(candidates));
            return 0;
          }
        }
        position = end;
      }
      if (second % 1000 == 0) {
        auto seconds = std::chrono::duration_cast<std::chrono::seconds>(std::chrono::steady_clock::now() - start).count();
        std::printf("rep=%d/3 second=%zu/%zu prefixes=%llu elapsed=%llds\n",
                    representative + 1, second, matrices.size(), static_cast<unsigned long long>(prefixes),
                    static_cast<long long>(seconds));
      }
    }
    std::printf("representative %d/3 complete prefixes=%llu\n", representative + 1,
                static_cast<unsigned long long>(prefixes));
  }
  if (split) throw std::runtime_error("Positive control found no witness");
  std::printf("RESULT rank<=7: NO prefixes=%llu candidates=%llu\n",
              static_cast<unsigned long long>(prefixes), static_cast<unsigned long long>(candidates));
  return 0;
}
