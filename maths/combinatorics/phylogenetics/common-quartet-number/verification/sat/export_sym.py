import json, sys
def newick(adj, n, shift=1):
    def rec(v, p):
        ch = [u for u in adj[v] if u != p]
        if not ch: return str(v + shift)
        return '(' + ','.join(sorted((rec(u, v) for u in ch), key=lambda s: (len(s), s))) + ')'
    r = adj[0][0]
    return '(' + ','.join(sorted((rec(u, r) for u in adj[r]), key=lambda s: (len(s), s))) + ');'
if __name__ == "__main__":
  f = sys.argv[1]; n = int(f.split('_n')[1].split('_')[0])
  for t in json.load(open(f)):
      adj = {int(a): b for a, b in t.items()}
      print(newick(adj, n))
