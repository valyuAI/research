#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

// Independent enumeration of ordered variable words; no SAT code is used.
int main(int argc, char** argv) {
  if (argc != 2) return 2;
  std::ifstream input(argv[1]);
  if (!input) return 3;
  std::vector<unsigned char> blue(1u << 24, 0);
  std::string row;
  unsigned histograms = 0;
  while (std::getline(input, row)) {
    std::stringstream fields(row);
    std::string token;
    unsigned key = 0, sum = 0, symbol = 0;
    while (std::getline(fields, token, ',')) {
      unsigned count = std::stoul(token);
      if (count > 7 || symbol >= 8) return 4;
      key |= count << (3 * symbol++);
      sum += count;
    }
    if (symbol != 8 || sum != 7 || blue[key]) return 5;
    blue[key] = 1;
    ++histograms;
  }
  std::uint64_t lines = 0, redViolations = 0, blueViolations = 0;
  std::uint64_t ruleDisagreements = 0, bluePoints = 0;
  constexpr unsigned variableWords = 4782969; // 9^7
  for (unsigned encoded = 0; encoded < variableWords; ++encoded) {
    std::array<unsigned, 8> counts{};
    unsigned value = encoded, variableCount = 0, weight = 0;
    for (unsigned position = 0; position < 7; ++position) {
      unsigned digit = value % 9;
      value /= 9;
      if (digit == 8) ++variableCount;
      else { ++counts[digit]; weight += digit; }
    }
    unsigned key = 0;
    for (unsigned symbol = 0; symbol < 8; ++symbol) key |= counts[symbol] << (3 * symbol);
    if (variableCount == 0) {
      const bool rule = counts[0] == 7 || (weight % 7 == 1 && !(counts[0] == 6 && counts[1] == 1));
      ruleDisagreements += (rule != bool(blue[key]));
      bluePoints += blue[key];
      continue;
    }
    bool anyBlue = false, previousBlue = false;
    for (unsigned symbol = 0; symbol < 8; ++symbol) {
      bool current = blue[key + (variableCount << (3 * symbol))];
      anyBlue |= current;
      blueViolations += current && previousBlue;
      previousBlue = current;
    }
    redViolations += !anyBlue;
    ++lines;
    if (lines % 500000 == 0) std::cerr << "Checked " << lines << " ordered variable words\n" << std::flush;
  }
  std::cout << "{\"histograms\":" << histograms << ",\"ordered_variable_words\":" << lines
            << ",\"blue_points\":" << bluePoints << ",\"red_line_violations\":" << redViolations
            << ",\"blue_adjacent_pair_violations\":" << blueViolations
            << ",\"compact_rule_disagreements\":" << ruleDisagreements << "}\n";
  return redViolations || blueViolations || ruleDisagreements || lines != 2685817;
}
