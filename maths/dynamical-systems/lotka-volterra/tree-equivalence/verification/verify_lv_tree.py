"""Exact-arithmetic checks of the LV tree reconstruction lemmas, not a proof by testing."""

from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

import networkx as nx

OUT = Path(__file__).resolve().parent


def dependent_triple(a, b, c):
    # Distinct projective points in this collection are never proportional.
    pivot = next(
        (i, j)
        for i, j in itertools.combinations(range(len(a)), 2)
        if a[i] * b[j] != a[j] * b[i]
    )
    i, j = pivot
    for k in range(len(a)):
        determinant = (
            a[i] * (b[j] * c[k] - b[k] * c[j])
            - a[j] * (b[i] * c[k] - b[k] * c[i])
            + a[k] * (b[i] * c[j] - b[j] * c[i])
        )
        if determinant:
            return False
    return True


def forms(tree):
    n = len(tree)
    result = [tuple(int(i == j) for i in range(n)) for j in range(n)]
    for u, v in sorted(tree.edges()):
        vector = [0] * n
        vector[u], vector[v] = 2 * u + 3, -(2 * v + 5)
        result.append(tuple(vector))
    return result


def reconstruction(tree):
    vectors = forms(tree)
    triples = [
        indices
        for indices in itertools.combinations(range(len(vectors)), 3)
        if dependent_triple(*(vectors[i] for i in indices))
    ]
    n = len(tree)
    expected = {
        tuple(sorted([u, v, n + k])) for k, (u, v) in enumerate(sorted(tree.edges()))
    }
    assert set(triples) == expected
    occurrence = Counter(point for triple in triples for point in triple)
    shared = {point for point, count in occurrence.items() if count >= 2}
    recovered = nx.Graph()
    recovered.add_nodes_from(shared)
    nextLeaf = 2 * n
    for triple in triples:
        endpoints = [point for point in triple if point in shared]
        while len(endpoints) < 2:
            endpoints.append(nextLeaf)
            nextLeaf += 1
        assert len(endpoints) == 2
        recovered.add_edge(*endpoints)
    assert nx.is_isomorphic(tree, recovered)
    return len(triples)


def generic_matrix(tree):
    n = len(tree)
    matrix = [[0] * n for _ in range(n)]
    for j in range(n):
        matrix[j][j] = -((n + 1) ** 2) - j
        removed = tree.copy()
        removed.remove_node(j)
        components = sorted(
            (sorted(component) for component in nx.connected_components(removed)),
            key=lambda component: component[0],
        )
        for k, component in enumerate(components, 1):
            for i in component:
                matrix[i][j] = k
    return matrix


def admitted_support(matrix, support):
    n = len(matrix)
    outside = set(range(n)) - set(support)
    root = support[0]
    if any(matrix[i][j] != matrix[root][j] for i in support for j in outside):
        return False
    coefficients = {root: Fraction(1)}
    for j in support[1:]:
        coefficients[j] = Fraction(
            matrix[j][j] - matrix[root][j], matrix[j][root] - matrix[root][root]
        )
    return all(
        coefficients[i] * (matrix[j][j] - matrix[i][j])
        == coefficients[j] * (matrix[j][i] - matrix[i][i])
        for i, j in itertools.combinations(support, 2)
    )


def completeness(tree):
    n = len(tree)
    matrix = generic_matrix(tree)
    supports = set()
    for size in range(1, n + 1):
        for support in itertools.combinations(range(n), size):
            if admitted_support(matrix, support):
                supports.add(support)
    expected = {(i,) for i in range(n)} | {tuple(sorted(edge)) for edge in tree.edges()}
    assert supports == expected
    return len(supports)


def main():
    rows = []
    totalTrees, totalCompleteness = 0, 0
    for n in range(2, 13):
        count = 0
        for tree in nx.nonisomorphic_trees(n):
            tree = nx.convert_node_labels_to_integers(tree)
            assert reconstruction(tree) == n - 1
            if n <= 10:
                assert completeness(tree) == 2 * n - 1
                totalCompleteness += 1
            count += 1
        totalTrees += count
        rows.append(
            {
                "n": n,
                "unlabelled_trees": count,
                "exact_dependent_triples_and_reconstruction": "pass",
                "complete_support_enumeration": "pass" if n <= 10 else "not_run",
            }
        )
        print(
            f"n={n}: all {count} unlabelled trees pass exact triad/reconstruction checks; support enumeration {'passed' if n <= 10 else 'not run'}",
            flush=True,
        )
    result = {
        "status": "all_checks_pass",
        "arithmetic": "Python integers and rational fractions",
        "all_order_proof_is_separate": True,
        "triad_reconstruction_trees": totalTrees,
        "support_enumeration_trees": totalCompleteness,
        "rows": rows,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (OUT / "lv_tree_exact_checks.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
