// Generic price-potential search for moduli 2^i d, d | D = 3^B * 5 (B <= 3), 2^i d >= MINMOD, i <= L0.
// Y = Z/D with y <-> (u = y mod 3^B, v = y mod 5).  Exact min-cost cover by DP over the 3-adic tree of u
// with state W = set of v already covered.  Symmetry: identical sibling subtrees of the 3-adic tree,
// identical v-rows, identical 2-adic subtrees are branched only once.  Usage:
//   gen B MINMOD L0 famfile maxsurv outfile
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>
typedef uint64_t u64;
#define NW 4
typedef struct { u64 w[NW]; } Set;
static int B, D, U, MINMOD, L0, P;     // U = 3^B
static inline int sget(const Set*s,int y){ return (s->w[y>>6]>>(y&63))&1; }
static inline void sset(Set*s,int y){ s->w[y>>6]|=1ULL<<(y&63); }
static inline int sempty(const Set*s){ for(int i=0;i<NW;i++) if(s->w[i]) return 0; return 1; }
static inline int seq(const Set*a,const Set*b){ return memcmp(a,b,sizeof(Set))==0; }
static inline int sinter(const Set*a,const Set*b){ for(int i=0;i<NW;i++) if(a->w[i]&b->w[i]) return 1; return 0; }
static inline void sminus(Set*a,const Set*b){ for(int i=0;i<NW;i++) a->w[i]&=~b->w[i]; }
static int YOF[256][5]; // y index of (u,v)
// types: d = 3^i * 5^j, index k = 2*i + j
static int NT, TD[16], TI[16], TJ[16];
static Set *CLS[16]; static int NC[16];
// --- exact cover phi via DP on 3-adic tree.  node (depth i, residue r mod 3^i); subtree u = r mod 3^i
static const int *RHO;
static int pw3_[5]={1,3,9,27,81};
static Set CUR;
static int memo[4][27][32]; static int memoOK;
static int ROWM[4][27];
static int YU[256], YV[256];
static void build_rowm(const Set*S){
  memset(ROWM,0,sizeof(ROWM));
  for(int y=0;y<D;y++) if(sget(S,y)){ int u=YU[y], v=YV[y];
    for(int dd=0;dd<=B;dd++){ ROWM[dd][u%pw3_[dd]]|=1<<v; } }
}
static inline int rowmask(int depth,int r){ return ROWM[depth][r]; }
static int dp(int depth,int r,int W){
  int need=rowmask(depth,r)&~W;
  if(!need) return 0;
  int *mm=&memo[depth][r][W]; if(*mm>=0) return *mm;
  int i=depth;
  int best=RHO[2*i+0];  // class (node, all v): type 3^i
  int cs=RHO[2*i+1];    // class (node, single v): type 3^i*5
  // choose V subset of need (single-v classes here)
  for(int V=need;;V=(V-1)&need){
    int c=cs*__builtin_popcount(V);
    if(c<best){
      if(depth==B){ if((need&~V)==0) best=c; }
      else{ int step=1; for(int t=0;t<depth;t++) step*=3;
        for(int k=0;k<3&&c<best;k++) c+=dp(depth+1,r+k*step,W|V);
        if(c<best) best=c; }
    }
    if(V==0) break;
  }
  *mm=best; return best;
}
static int phi_raw(const Set*S,const int*rho);
#define CACHE (1<<20)
typedef struct { Set s; int f; int val; } CE; static CE *cache;
static int phi_c(const Set*S,int f,const int*rho){
  u64 h=(u64)f*0x9E3779B97F4A7C15ULL; for(int i=0;i<NW;i++){ h^=S->w[i]; h*=0xff51afd7ed558ccdULL; h^=h>>33; }
  CE*e=&cache[h&(CACHE-1)];
  if(e->f==f && seq(&e->s,S)) return e->val;
  int v=phi_raw(S,rho); e->s=*S; e->f=f; e->val=v; return v;
}
static int phi_raw(const Set*S,const int*rho){
  if(sempty(S)) return 0;
  RHO=rho; build_rowm(S); memset(memo,-1,sizeof(memo));
  return dp(0,0,0);
}
// --- family
#define MAXF 64
static int NF, F[MAXF][16], RF[MAXF];
// --- state
static Set col[8];
typedef struct { int lev,k; } Item; static Item IT[64]; static int NIT;
static int rem[MAXF]; static long long nodes=0,surv=0,maxsurv; static FILE*out; static time_t t0;
static int dead(void){
  for(int f=0;f<NF;f++){ int q=0; for(int x=0;x<P;x++) q+=phi_c(&col[x],f,F[f]); if(q-rem[f]>=RF[f]) return 1; }
  return 0;
}
// symmetry helpers
static int pw3[5]={1,3,9,27,81};
static int subtree_equal(int depth,int r1,int r2){ // subtrees of u = r1, r2 mod 3^depth equal in all columns (shift map)
  for(int x=0;x<P;x++) for(int u=r1;u<U;u+=pw3[depth]){ int u2=u-r1+r2; // same higher digits
      for(int v=0;v<5;v++) if(sget(&col[x],YOF[u][v])!=sget(&col[x],YOF[u2][v])) return 0; }
  return 1;
}
static int node_canonical(int depth,int r){ // every ancestor-or-self has no earlier identical sibling
  for(int d=depth;d>=1;d--){ int rr=r%pw3[d]; int parent=rr%pw3[d-1]; int digit=rr/pw3[d-1];
    for(int k=0;k<digit;k++) if(subtree_equal(d,rr,parent+k*pw3[d-1])) return 0; }
  return 1;
}
static int rows_equal(int v1,int v2){
  for(int x=0;x<P;x++) for(int u=0;u<U;u++) if(sget(&col[x],YOF[u][v1])!=sget(&col[x],YOF[u][v2])) return 0;
  return 1;
}
static int v_canonical(int v){ for(int k=0;k<v;k++) if(rows_equal(k,v)) return 0; return 1; }
static int xsub_equal(int lev,int n1,int n2){ // 2-adic: columns x = n1 mod 2^lev vs n2 mod 2^lev, matched by x -> x - n1 + n2
  int nn=1<<lev; for(int x=n1;x<P;x+=nn) if(!seq(&col[x],&col[x-n1+n2])) return 0; return 1;
}
static int x_canonical(int lev,int n){
  for(int d=lev;d>=1;d--){ int nn=n%(1<<d); int parent=nn%(1<<(d-1)); int bit=nn>>(d-1);
    if(bit==1 && xsub_equal(d,nn,parent)) return 0; }
  return 1;
}
static void dfs(int t){
  nodes++;
  if((nodes&0xFFFFF)==0){ fprintf(stderr,"[%lds] nodes %lld surv %lld\n",(long)(time(NULL)-t0),nodes,surv); }
  if(dead()) return;
  if(t==NIT){ surv++;
    for(int x=0;x<P;x++){ for(int y=0;y<D;y++) if(sget(&col[x],y)) fprintf(out,"%d,",y); fprintf(out,";"); }
    fprintf(out,"\n"); fflush(out);
    if(surv>=maxsurv){ fprintf(stderr,"TOTAL nodes %lld survivors %lld (max reached)\n",nodes,surv); exit(0);} return; }
  int lev=IT[t].lev,k=IT[t].k,mult=P>>lev;
  for(int f=0;f<NF;f++) rem[f]-=mult*F[f][k];
  dfs(t+1);
  int nn=1<<lev; int i=TI[k], j=TJ[k];
  for(int n=0;n<nn;n++){
    if(!x_canonical(lev,n)) continue;
    for(int c=0;c<NC[k];c++){
      int r=c% pw3[i]; int v= j? (c%5) : -1;
      // class c of type k: u = r mod 3^i, v = c mod 5 (if j)
      if(!node_canonical(i,r)) continue;
      if(j && !v_canonical(v)) continue;
      Set*m=&CLS[k][c]; int hit=0;
      for(int x=n;x<P;x+=nn) if(sinter(&col[x],m)) hit=1;
      if(!hit) continue;
      Set save[8]; for(int x=n;x<P;x+=nn){ save[x]=col[x]; sminus(&col[x],m); }
      dfs(t+1);
      for(int x=n;x<P;x+=nn) col[x]=save[x];
    }
  }
  for(int f=0;f<NF;f++) rem[f]+=mult*F[f][k];
}
int main(int argc,char**argv){
  B=atoi(argv[1]); MINMOD=atoi(argv[2]); L0=atoi(argv[3]); U=pw3[B]; D=U*5; P=1<<L0;
  cache=calloc(CACHE,sizeof(CE)); for(int i=0;i<CACHE;i++) cache[i].f=-1;
  for(int y=0;y<5*pw3[B];y++){ YU[y]=y%pw3[B]; YV[y]=y%5; }
  for(int u=0;u<U;u++) for(int v=0;v<5;v++){ // y = CRT(u mod 3^B, v mod 5)
    for(int y=0;y<D;y++) if(y%U==u && y%5==v){ YOF[u][v]=y; break; } }
  NT=2*(B+1);
  for(int i=0;i<=B;i++) for(int j=0;j<2;j++){ int k=2*i+j; TI[k]=i; TJ[k]=j; TD[k]=pw3[i]*(j?5:1); NC[k]=TD[k];
      CLS[k]=calloc(TD[k],sizeof(Set));
      for(int c=0;c<TD[k];c++) for(int y=0;y<D;y++) if((y-c)%TD[k]==0) sset(&CLS[k][c],y); }
  // class index c: residue mod d; its u-part c mod 3^i and v-part c mod 5 -- consistent with y = c mod d
  FILE*ff=fopen(argv[4],"r"); NF=0;
  while(NF<MAXF){ int ok=1; for(int k=0;k<NT;k++) if(fscanf(ff,"%d",&F[NF][k])!=1){ ok=0; break; } if(!ok) break;
    RF[NF]=0; for(int k=0;k<NT;k++) RF[NF]+=F[NF][k]; NF++; }
  fclose(ff);
  maxsurv=atoll(argv[5]); out=fopen(argv[6],"w"); t0=time(NULL);
  // items: all (lev,k) with 2^lev * d >= MINMOD and lev <= L0; order by impact (area*columns) desc, level 0 first
  NIT=0;
  for(int lev=0;lev<=L0;lev++) for(int k=0;k<NT;k++) if((TD[k]<<lev)>=MINMOD){ IT[NIT].lev=lev; IT[NIT].k=k; NIT++; }
  // sort: by (P>>lev) * (D/d) descending
  for(int a=0;a<NIT;a++) for(int b=a+1;b<NIT;b++){
    long ia=(long)(P>>IT[a].lev)*(D/TD[IT[a].k]), ib=(long)(P>>IT[b].lev)*(D/TD[IT[b].k]);
    if(ib>ia){ Item tmp=IT[a]; IT[a]=IT[b]; IT[b]=tmp; } }
  fprintf(stderr,"B=%d D=%d MINMOD=%d L0=%d types=%d items=%d fam=%d\n",B,D,MINMOD,L0,NT,NIT,NF);
  for(int a=0;a<NIT;a++) fprintf(stderr," (%d,%d)",IT[a].lev,TD[IT[a].k]); fprintf(stderr,"\n");
  for(int x=0;x<P;x++){ memset(&col[x],0,sizeof(Set)); for(int y=0;y<D;y++) sset(&col[x],y); }
  for(int f=0;f<NF;f++){ rem[f]=0; for(int a=0;a<NIT;a++) rem[f]+=(P>>IT[a].lev)*F[f][IT[a].k]; }
  dfs(0);
  fprintf(stderr,"TOTAL nodes %lld survivors %lld\n",nodes,surv);
}
