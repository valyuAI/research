#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>

struct Counts {
  uint64_t wins[2] = {};
  uint64_t unresolved = 0;
  uint64_t byEnd[2][11] = {};
};

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  std::ofstream output(argv[1]);
  const std::array<std::array<int, 3>, 6> patterns = {{{1,2,3}, {1,3,2}, {2,1,3},
                                                    {2,3,1}, {3,1,2}, {3,2,1}}};
  for (int horizon = 8; horizon <= 10; ++horizon) {
    Counts counts[6];
    std::vector<int> permutation(horizon);
    std::iota(permutation.begin(), permutation.end(), 1);
    uint64_t examined = 0;
    do {
      int winner[6] = {-1,-1,-1,-1,-1,-1};
      int remaining = 6;
      for (int start = 0; start + 2 < horizon && remaining; ++start) {
        int x = permutation[start], y = permutation[start + 1], z = permutation[start + 2];
        int code = 100 * (1 + (x > y) + (x > z))
                   + 10 * (1 + (y > x) + (y > z)) + (1 + (z > x) + (z > y));
        for (int j = 0; j < 6; ++j) {
          if (winner[j] >= 0) continue;
          const auto &a = patterns[j];
          int aCode = 100 * a[0] + 10 * a[1] + a[2];
          int bCode = 100 * a[2] + 10 * a[0] + a[1];
          if (code == aCode || code == bCode) {
            int label = code == aCode ? 0 : 1;
            winner[j] = label;
            --remaining;
            ++counts[j].wins[label];
            ++counts[j].byEnd[label][start + 3];
          }
        }
      }
      for (int j = 0; j < 6; ++j) if (winner[j] < 0) ++counts[j].unresolved;
      ++examined;
      if (examined % 500000 == 0) {
        std::cout << "Direct k=3, horizon=" << horizon << ", examined=" << examined << "\n" << std::flush;
      }
    } while (std::next_permutation(permutation.begin(), permutation.end()));
    for (int j = 0; j < 6; ++j) {
      output << "{\"horizon\":" << horizon << ",\"pattern\":["
             << patterns[j][0] << ',' << patterns[j][1] << ',' << patterns[j][2]
             << "],\"winsA\":" << counts[j].wins[0] << ",\"winsB\":" << counts[j].wins[1]
             << ",\"unresolved\":" << counts[j].unresolved << ",\"byEnd\":[";
      for (int label = 0; label < 2; ++label) {
        output << (label ? ",[" : "[");
        for (int n = 0; n <= horizon; ++n) output << (n ? "," : "") << counts[j].byEnd[label][n];
        output << ']';
      }
      output << "]}\n";
    }
    output.flush();
    std::cout << "Direct k=3, horizon=" << horizon << ", all six races, " << examined << " permutations COMPLETE\n" << std::flush;
  }
}
