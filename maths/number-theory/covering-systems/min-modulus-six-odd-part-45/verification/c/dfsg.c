// Generalised check (no tree symmetry, minimal Y-symmetry): moduli 2^i d, d | 45, 2^i d >= MINMOD, i <= L0.
// Level-0 classes are enumerated with only the translations u -> u+t (mod 9) and v -> v+s (mod 5) used:
// the first level-0 class of type 9 (if allowed) is fixed to u=0, and the v-coordinate of the first
// v-dependent level-0 class is fixed to 0.  Columns x in Z/2^L0; a class at level l and node n acts on all
// x with x mod 2^l = n.  Survivor: final sum_x phi_rho(S_x) < R_rho for every rho in the family.
// Usage: dfsg famfile MINMOD L0 maxsurv outfile
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "phi.h"
#define MAXF 64
static int NF, F[MAXF][6], RF[MAXF];
static u64 CLS[6][45]; static int NCLS[6]; static const int DSV[6]={1,3,5,9,15,45};
static int CLSU[6][45], CLSV[6][45]; // representative u (mod d's 9-part) and v of class
static void cls_init(void){
  for(int k=0;k<6;k++){ int d=DSV[k]; NCLS[k]=0;
    for(int c=0;c<d;c++){ u64 m=0;
      for(int u=0;u<9;u++) for(int v=0;v<5;v++){ int ok=1;
        if(d%9==0) ok&=(u==c%9); else if(d%3==0) ok&=(u%3==c%3);
        if(d%5==0) ok&=(v==c%5);
        if(ok) m|=1ULL<<(5*u+v); }
      int dup=0; for(int j=0;j<NCLS[k];j++) if(CLS[k][j]==m) dup=1;
      if(!dup){ CLSU[k][NCLS[k]]=c%9; CLSV[k][NCLS[k]]=c%5; CLS[k][NCLS[k]++]=m; } } }
}
static int MINMOD, L0, P; static u64 col[64];
typedef struct { int lev,k; } Item; static Item IT[64]; static int NIT;
static int rem[MAXF]; static long long nodes=0,surv=0,maxsurv; static FILE*out; static time_t t0;
static int alive(void){
  for(int f=0;f<NF;f++){ int q=0; for(int x=0;x<P;x++) q+=phi(col[x],F[f]); if(q-rem[f]>=RF[f]) return 0; }
  return 1;
}
static int fixu=0, fixv=0; // whether translation normalisation still available at level 0
static void dfs(int t){
  nodes++;
  if((nodes&0xFFFFF)==0) fprintf(stderr,"[%lds] nodes %lld surv %lld\n",(long)(time(NULL)-t0),nodes,surv);
  if(!alive()) return;
  if(t==NIT){ surv++; for(int x=0;x<P;x++) fprintf(out,"%llu ",(unsigned long long)col[x]); fprintf(out,"\n"); fflush(out);
    if(surv>=maxsurv){ fprintf(stderr,"TOTAL nodes %lld survivors %lld (max reached)\n",nodes,surv); exit(0);} return; }
  int lev=IT[t].lev,k=IT[t].k,d=DSV[k],mult=P>>lev;
  for(int f=0;f<NF;f++) rem[f]-=mult*F[f][k];
  dfs(t+1); // skip
  int nn=1<<lev; u64 save[64];
  for(int n=0;n<nn;n++){
    for(int c=0;c<NCLS[k];c++){
      // translation normalisation at level 0
      int su=fixu, sv=fixv;
      if(lev==0){
        if(!fixu && (d%9==0) && CLSU[k][c]!=0) continue;
        if(!fixv && (d%5==0) && fixu && CLSV[k][c]!=0) continue;
      }
      u64 m=CLS[k][c]; int hit=0;
      for(int x=n;x<P;x+=nn) if(col[x]&m) hit=1;
      if(!hit) continue;
      for(int x=n;x<P;x+=nn){ save[x]=col[x]; col[x]&=~m; }
      if(lev==0){ if(d%9==0) fixu=1; if(d%5==0 && su) fixv=1; }
      dfs(t+1);
      fixu=su; fixv=sv;
      for(int x=n;x<P;x+=nn) col[x]=save[x];
    }
  }
  for(int f=0;f<NF;f++) rem[f]+=mult*F[f][k];
}
int main(int argc,char**argv){
  phi_init(); cls_init(); t0=time(NULL);
  FILE*ff=fopen(argv[1],"r"); NF=0;
  while(NF<MAXF&&fscanf(ff,"%d %d %d %d %d %d",&F[NF][0],&F[NF][1],&F[NF][2],&F[NF][3],&F[NF][4],&F[NF][5])==6){ RF[NF]=0; for(int k=0;k<6;k++) RF[NF]+=F[NF][k]; NF++; }
  MINMOD=atoi(argv[2]); L0=atoi(argv[3]); maxsurv=atoll(argv[4]); out=fopen(argv[5],"w"); P=1<<L0;
  // items: level 0 types in order 9,45,15,5,3,1 (type 9 first so u-normalisation applies); then levels 1..L0
  int ord0[6]={3,4,5,2,1,0}; NIT=0;
  for(int i=0;i<6;i++){ int k=ord0[i]; if(DSV[k]>=MINMOD){ IT[NIT].lev=0; IT[NIT].k=k; NIT++; } }
  // note: with type 9 placed first and fixing u=0, the next v-dependent level-0 class gets v=0.
  for(int lev=1;lev<=L0;lev++) for(int k=1;k<6;k++) if((DSV[k]<<lev)>=MINMOD){ IT[NIT].lev=lev; IT[NIT].k=k; NIT++; }
  for(int lev=1;lev<=L0;lev++) if((1<<lev)>=MINMOD){ IT[NIT].lev=lev; IT[NIT].k=0; NIT++; }
  for(int x=0;x<P;x++) col[x]=(1ULL<<45)-1;
  for(int f=0;f<NF;f++){ rem[f]=0; for(int i=0;i<NIT;i++) rem[f]+=(P>>IT[i].lev)*F[f][IT[i].k]; }
  fprintf(stderr,"MINMOD %d L0 %d items %d fam %d\n",MINMOD,L0,NIT,NF);
  dfs(0);
  fprintf(stderr,"TOTAL nodes %lld survivors %lld\n",nodes,surv);
}
