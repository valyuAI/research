// Exact weighted set cover of a fiber set S (45-bit) by classes; class types d in {1,3,5,9,15,45}.
// Each fiber lies in exactly one class of each type.  Prices rho[6] (integers).
#include <stdint.h>
typedef uint64_t u64;
static u64 FIBCLS[45][6]; // class mask of type k containing fiber y
static void wsc_init(void){
  int DSW[6]={1,3,5,9,15,45};
  for(int y=0;y<45;y++){ int u=y/5, v=y%5;
    for(int k=0;k<6;k++){ int d=DSW[k]; u64 m=0;
      for(int u2=0;u2<9;u2++)for(int v2=0;v2<5;v2++){ int ok=1;
        if(d%9==0) ok&=(u2==u); else if(d%3==0) ok&=(u2%3==u%3);
        if(d%5==0) ok&=(v2==v);
        if(ok) m|=((u64)1)<<(5*u2+v2);}
      FIBCLS[y][k]=m; } }
}
static int wsc_best; static const int *wsc_rho;
static void wsc_rec(u64 S,int cost){
  if(cost>=wsc_best) return;
  if(!S){ wsc_best=cost; return; }
  // choose uncovered fiber whose classes cover least (heuristic: lowest bit)
  int y=__builtin_ctzll(S);
  // simple lower bound: cheapest price among classes containing y
  for(int k=0;k<6;k++){ u64 m=FIBCLS[y][k]; wsc_rec(S&~m,cost+wsc_rho[k]); }
}
static int wsc(u64 S,const int*rho){
  wsc_rho=rho; wsc_best=rho[0]; // Y covers everything
  if(!S) return 0;
  // order: try greedy-ish by recursion
  wsc_rec(S,0);
  return wsc_best;
}
