// Exact minimum-cost cover of a set S of fibres y=(u,v) in Z/9 x Z/5 (bit 5u+v) by residue classes of
// types d=1,3,5,9,15,45 with integer prices rho[0..5], using the product structure of the classes.
#include <stdint.h>
typedef uint64_t u64;
static inline int popc(u64 x){ return __builtin_popcountll(x); }
// row mask: all fibres with given v; block-row mask: u in block b, given v
static u64 ROWV[5], BLKV[3][5], UCOL[9];
static void phi_init(void){
  for(int v=0;v<5;v++){ ROWV[v]=0; for(int u=0;u<9;u++) ROWV[v]|=1ULL<<(5*u+v); }
  for(int b=0;b<3;b++) for(int v=0;v<5;v++){ BLKV[b][v]=0; for(int u=b;u<9;u+=3) BLKV[b][v]|=1ULL<<(5*u+v); }
  for(int u=0;u<9;u++){ UCOL[u]=0; for(int v=0;v<5;v++) UCOL[u]|=1ULL<<(5*u+v); }
}
static inline int imin(int a,int b){ return a<b?a:b; }
static int phi(u64 S, const int *rho){
  if(!S) return 0;
  int best=rho[0];
  // per block b, per subset U of the 3 u's in the block, per v: count of points of S in (b\U, v)
  int cnt[3][8][5];
  for(int b=0;b<3;b++) for(int U=0;U<8;U++) for(int v=0;v<5;v++){
    int c=0; for(int j=0;j<3;j++) if(!(U>>j&1)){ int u=b+3*j; if(S>>(5*u+v)&1) c++; }
    cnt[b][U][v]=c; }
  for(int V=0;V<32;V++){
    int cost=rho[2]*popc(V);
    if(cost>=best) continue;
    for(int b=0;b<3&&cost<best;b++){
      int cb=rho[1];
      for(int U=0;U<8;U++){
        int c=rho[3]*popc(U);
        for(int v=0;v<5;v++) if(!(V>>v&1)){ int k=cnt[b][U][v]; if(k) c+=imin(rho[4],rho[5]*k); }
        if(c<cb) cb=c;
      }
      cost+=cb;
    }
    if(cost<best) best=cost;
  }
  return best;
}
