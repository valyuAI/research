"""Check the rendered matrix, target polynomials, and minor indices against input.

This reads a restricted expression grammar independently of the Lean generator.
Lean itself checks the resulting determinant identities.
"""

import hashlib
import json
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parent
sys.path.insert(0, str(root.parent))
from verify_certificates import add, coefficient, multiply, parse, variable


def read_expression(text):
  tokens = re.findall(r"Complex\.I|cadd|cmul|cpow|w|-?\d+|[():ℂ]", text)
  if "".join(tokens) != re.sub(r"\s+", "", text):
    raise ValueError("Unexpected expression syntax")
  cursor = 0

  def value():
    nonlocal cursor
    token = tokens[cursor]
    cursor += 1
    if token == "(":
      head = tokens[cursor]
      cursor += 1
      if re.fullmatch(r"-?\d+", head):
        if tokens[cursor:cursor + 3] != [":", "ℂ", ")"]:
          raise ValueError("Unexpected scalar syntax")
        cursor += 3
        return parse(head)
      if head == "w":
        result = variable(int(tokens[cursor]))
        cursor += 1
      elif head in ["cadd", "cmul"]:
        left, right = value(), value()
        result = add(left, right) if head == "cadd" else multiply(left, right)
      elif head == "cpow":
        base = value()
        power = int(tokens[cursor])
        cursor += 1
        result = parse("1")
        for _ in range(power):
          result = multiply(result, base)
      else:
        raise ValueError(f"Unexpected operator: {head}")
      if tokens[cursor] != ")":
        raise ValueError("Missing closing parenthesis")
      cursor += 1
      return result
    if token == "Complex.I":
      return parse("I")
    if re.fullmatch(r"-?\d+", token):
      return parse(token)
    raise ValueError(f"Unexpected atom: {token}")

  result = value()
  if cursor != len(tokens):
    raise ValueError("Unconsumed expression tokens")
  return result


source = json.loads((root.parent / "minor_dimension_certificates.json").read_text())
core = (root / "MinorCore.lean").read_text()
matrix_text = core.split("  !![", 1)[1].split("]\n\n", 1)[0]
matrix = [[read_expression(entry.strip()) for entry in row.split(",")]
  for row in matrix_text.split(";")]
expected_matrix = [[parse(entry) for entry in row] for row in source["matrix"]]
if matrix != expected_matrix:
  raise ValueError("Rendered matrix differs from the certificate input")
text = "\n".join((root / f"MinorBatch{i:02}.lean").read_text() for i in range(1, 22))
targets = re.findall(r"^def (certificate_(\d+)_(\d+)_target) .*? :=\n(.*?)\n\n", text, re.M | re.S)
if len(targets) != 11:
  raise ValueError("Expected exactly eleven target definitions")
for name, rank, target_id, expression in targets:
  original = next(item for item in source["bounds"][rank]["certificates"]
    if item["target_id"] == int(target_id))
  expected = {tuple(term["powers"]): coefficient(term["coefficient"])
    for term in original["polynomial"]}
  if read_expression(expression.strip()) != expected:
    raise ValueError(f"Target mismatch: {name}")
minors = re.findall(r"^def original_minor_(\d+)_(\d+).*? :=\n"
  r"  Matrix.det \(\(normalMatrix w\).submatrix !\[(.*?)\] !\[(.*?)\]\)", text, re.M)
if len(minors) != 237:
  raise ValueError("Expected237 original minor definitions")
for rank, index, rows, columns in minors:
  actual = {"rows": [int(item) for item in rows.split(",")],
    "columns": [int(item) for item in columns.split(",")]}
  if actual != source["bounds"][rank]["independent_minors"][int(index)]:
    raise ValueError(f"Minor descriptor mismatch: {rank}/{index}")
record = {"matrix_entries_verified": 91, "target_polynomials_verified": len(targets),
  "actual_minor_descriptors_verified": len(minors), "passed": True,
  "input_sha256": hashlib.sha256((root.parent / "minor_dimension_certificates.json").read_bytes()).hexdigest()}
if len(sys.argv) > 1:
  Path(sys.argv[1]).write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
