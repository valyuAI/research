#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <string>
#include <unordered_map>
#include <vector>

using Wide = __int128_t;
using Mask = uint32_t;

std::string decimal(Wide x) {
  if (x == 0) return "0";
  bool negative = x < 0;
  if (negative) x = -x;
  std::string result;
  while (x) {
    result.push_back('0' + x % 10);
    x /= 10;
  }
  if (negative) result.push_back('-');
  std::reverse(result.begin(), result.end());
  return result;
}

struct State {
  std::vector<Mask> successors;
  int label;
  bool operator<(const State &other) const {
    if (label != other.label) return label < other.label;
    return successors < other.successors;
  }
};

bool appendOccurrence(const std::vector<Mask> &old, const std::vector<int> &p,
                      int offset, std::vector<Mask> &out) {
  int n = offset + p.size();
  out = old;
  out.resize(n, 0);
  for (int i = 0; i < int(p.size()); ++i) {
    for (int j = 0; j < int(p.size()); ++j) {
      if (p[i] < p[j]) out[offset + i] |= Mask(1) << (offset + j);
    }
  }
  for (int middle = 0; middle < n; ++middle) {
    for (int i = 0; i < n; ++i) {
      if (out[i] & (Mask(1) << middle)) out[i] |= out[middle];
    }
  }
  for (int i = 0; i < n; ++i) {
    if (out[i] & (Mask(1) << i)) return false;
  }
  return true;
}

uint64_t extensions(const std::vector<Mask> &successors) {
  std::unordered_map<Mask, uint64_t> memo;
  auto count = [&](auto &&self, Mask remaining) -> uint64_t {
    if (!remaining) return 1;
    auto found = memo.find(remaining);
    if (found != memo.end()) return found->second;
    uint64_t total = 0;
    for (Mask bits = remaining; bits; bits &= bits - 1) {
      int i = __builtin_ctz(bits);
      if (!(successors[i] & remaining)) total += self(self, remaining ^ (Mask(1) << i));
    }
    memo.emplace(remaining, total);
    return total;
  };
  return count(count, (Mask(1) << successors.size()) - 1);
}

bool overlap(const std::vector<int> &a, const std::vector<int> &b, int shift) {
  int length = a.size() - shift;
  for (int i = 0; i < length; ++i) {
    for (int j = i + 1; j < length; ++j) {
      if ((a[shift + i] < a[shift + j]) != (b[i] < b[j])) return false;
    }
  }
  return true;
}

int main(int argc, char **argv) {
  if (argc != 4) {
    std::cerr << "usage: clusters_independent K CUTOFF OUTPUT\n";
    return 2;
  }
  int k = std::stoi(argv[1]), cutoff = std::stoi(argv[2]);
  if (k < 3 || k + cutoff > 19) return 2;
  std::ofstream output(argv[3]);
  std::vector<int> a(k);
  std::iota(a.begin(), a.end(), 1);
  size_t patternIndex = 0;
  auto started = std::chrono::steady_clock::now();
  do {
    std::vector<int> complement(k);
    for (int i = 0; i < k; ++i) complement[i] = k + 1 - a[i];
    if (complement < a) continue;
    std::vector<int> p[2] = {a, a};
    std::rotate(p[1].begin(), p[1].end() - 1, p[1].end());
    bool compatible[2][2][20] = {};
    for (int i = 0; i < 2; ++i) {
      for (int j = 0; j < 2; ++j) {
        for (int d = 1; d < k; ++d) compatible[i][j][d] = overlap(p[i], p[j], d);
      }
    }
    std::vector<std::map<State, Wide>> states(cutoff + 1);
    for (int i = 0; i < 2; ++i) {
      std::vector<Mask> successors;
      appendOccurrence({}, p[i], 0, successors);
      states[0][{successors, i}] = -1;
    }
    std::vector<Wide> coefficients[2] = {std::vector<Wide>(cutoff + 1), std::vector<Wide>(cutoff + 1)};
    for (int span = 0; span <= cutoff; ++span) {
      for (const auto &[state, weight] : states[span]) {
        if (!weight) continue;
        coefficients[state.label][span] += weight * extensions(state.successors);
        for (int d = 1; d < k && span + d <= cutoff; ++d) {
          for (int label = 0; label < 2; ++label) {
            if (!compatible[state.label][label][d]) continue;
            std::vector<Mask> next;
            if (appendOccurrence(state.successors, p[label], span + d, next)) {
              states[span + d][{next, label}] -= weight;
            }
          }
        }
      }
      states[span].clear();
    }
    output << "{\"pattern\":[";
    for (int i = 0; i < k; ++i) output << (i ? "," : "") << a[i];
    output << "],\"cutoff\":" << cutoff << ",\"coefficients\":[";
    for (int label = 0; label < 2; ++label) {
      output << (label ? ",[" : "[");
      for (int s = 0; s <= cutoff; ++s) output << (s ? "," : "") << decimal(coefficients[label][s]);
      output << "]";
    }
    output << "]}\n";
    output.flush();
    ++patternIndex;
    if (patternIndex % (k == 7 ? 500 : 20) == 0 || k == 4) {
      double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
      std::cout << "k=" << k << ", checked=" << patternIndex << ", elapsed=" << elapsed << "s\n" << std::flush;
    }
  } while (std::next_permutation(a.begin(), a.end()));
  std::cout << "complete: k=" << k << ", patterns=" << patternIndex << "\n" << std::flush;
}
