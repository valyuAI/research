"""Write the TikZ figures used in paper.tex (values from the search tables)."""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from tikz_board import board_tikz  # noqa: E402

# per-opening values on 5x5 (1-based rows, '-' = opening loses ordinary Hex)
D5 = ["- - - - 8", "- 8 9 7 10", "- 9 7 9 -", "10 7 9 8 -", "8 - - - -"]
L5 = ["- - - - 7", "- 8 8 7 8", "- 9 6 9 -", "8 7 8 8 -", "7 - - - -"]


def table_board(rows, best):
    nums, blue = {}, []
    for r, line in enumerate(rows):
        for c, t in enumerate(line.split()):
            nums[(r, c)] = "$\\cdot$" if t == "-" else t
            if t == str(best):
                blue.append((r, c))
    return board_tikz(5, blue=blue, numbers=nums, path=blue, scale=0.62)


def line_board(n, moves, path):
    blue = [(x // n, x % n) for p, x in moves if p == "B"]
    red = [(x // n, x % n) for p, x in moves if p == "R"]
    nums = {}
    for i, (p, x) in enumerate(moves):
        nums[(x // n, x % n)] = str(i + 1)
    return board_tikz(n, blue=blue, red=red, numbers=nums, path=path, scale=0.62)


# A game from the certified Hex(5,6) centre strategy in which Red maximises the
# number of Blue stones (verification/py/longest_line.py), 1-based (row, col).
LINE5 = ("B33 R11 B24 R52 B51 R42 B53 R43 B41 R32 B31 R14 B15 R12 B13 R22 B35 R25 B34 R44 "
         "B45 R21 B54")
PATH5 = [(1, 5), (2, 4), (3, 4), (3, 5), (4, 5), (5, 4)]


if __name__ == "__main__":
    out = sys.argv[1]
    with open(out + "/fig_tables5.tex", "w") as fh:
        fh.write(table_board(D5, 7) + "\n\\qquad\n" + table_board(L5, 6) + "\n")
    # 6x6: openings achieving delta(6)=10 and lambda(6)=8 (0-based (2,3) and its rotation (3,2))
    nums = {(2, 3): "$\\ast$", (3, 2): "$\\ast$"}
    with open(out + "/fig_board6.tex", "w") as fh:
        fh.write(board_tikz(6, blue=[(2, 3), (3, 2)], path=[(2, 3), (3, 2)], numbers=nums, scale=0.62) + "\n")
    moves = [(t[0], (int(t[1]) - 1) * 5 + int(t[2]) - 1) for t in LINE5.split()]
    with open(out + "/fig_line5.tex", "w") as fh:
        fh.write(line_board(5, moves, [(r - 1, c - 1) for r, c in PATH5]) + "\n")
    print("figures written to", out)
