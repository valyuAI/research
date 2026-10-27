// Exhaustive DFS over all placements of congruence classes with moduli 2^i d (d | 45, 2^i d >= 6, i <= 2)
// looking for level-2 states that survive every price vector in a family F, i.e. sum_cols phi_rho < R_rho.
// Usage: dfs2 famfile [maxsurv] [orbit]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "phi.h"
#define MAXF 64
static int NF; static int F[MAXF][6]; static int RF[MAXF];
static u64 CLS[6][45]; static int NCLS[6]; // type index k: d=1,3,5,9,15,45
static const int DSV[6]={1,3,5,9,15,45};
static void cls_init(void){
  for(int k=0;k<6;k++){ int d=DSV[k]; NCLS[k]=0;
    for(int c=0;c<d;c++){ u64 m=0;
      for(int u=0;u<9;u++) for(int v=0;v<5;v++){ int ok=1;
        if(d%9==0) ok&=(u==c%9); else if(d%3==0) ok&=(u%3==c%3);
        if(d%5==0) ok&=(v==c%5);
        if(ok) m|=1ULL<<(5*u+v); }
      int dup=0; for(int j=0;j<NCLS[k];j++) if(CLS[k][j]==m) dup=1;
      if(!dup) CLS[k][NCLS[k]++]=m; }
  }
}
// items: (level, type index); level-1 items act on cols 2*x1, 2*x1+1; level-2 items on one col
typedef struct { int lev, k; } Item;
static Item IT[10]; static int NIT;
static u64 col[4];
static long long nodes=0, surv=0, maxsurv=1;
static int rem[MAXF]; // remaining impact per rho
static time_t t0;
static FILE *out;
static int bound_ok(void){ // returns 1 if may still survive (no rho proves dead)
  for(int f=0;f<NF;f++){
    int q=0; for(int j=0;j<4;j++) q+=phi(col[j],F[f]);
    if(q-rem[f]>=RF[f]) return 0;
  }
  return 1;
}
static int same_pair(u64 a,u64 b,u64 c,u64 d){ return (a==c&&b==d)||(a==d&&b==c); }
static void dfs(int t){
  nodes++;
  if((nodes&0xFFFFF)==0){ fprintf(stderr,"[%lds] nodes %lld surv %lld\n",(long)(time(NULL)-t0),nodes,surv); }
  if(!bound_ok()) return;
  if(t==NIT){
    surv++;
    fprintf(out,"%llu %llu %llu %llu\n",(unsigned long long)col[0],(unsigned long long)col[1],(unsigned long long)col[2],(unsigned long long)col[3]);
    fflush(out);
    if(surv>=maxsurv){ fprintf(stderr,"max survivors reached\n"); exit(0);} 
    return;
  }
  int lev=IT[t].lev, k=IT[t].k;
  for(int f=0;f<NF;f++) rem[f]-= (lev==1?2:1)*F[f][k];
  // skip branch (also covers residues that hit nothing)
  dfs(t+1);
  int sym01=same_pair(col[0],col[1],col[2],col[3]);
  if(lev==1){
    for(int x1=0;x1<2;x1++){
      if(x1==1&&sym01) break;
      u64 a=col[2*x1], b=col[2*x1+1];
      for(int c=0;c<NCLS[k];c++){ u64 m=CLS[k][c];
        if(!((a|b)&m)) continue;
        col[2*x1]=a&~m; col[2*x1+1]=b&~m;
        dfs(t+1);
        col[2*x1]=a; col[2*x1+1]=b; }
    }
  } else {
    for(int j=0;j<4;j++){
      int x1=j>>1;
      if(x1==1&&sym01) break;
      if((j&1)&&col[j-1]==col[j]) continue;
      u64 a=col[j];
      for(int c=0;c<NCLS[k];c++){ u64 m=CLS[k][c];
        if(!(a&m)) continue;
        col[j]=a&~m; dfs(t+1); col[j]=a; }
    }
  }
  for(int f=0;f<NF;f++) rem[f]+= (lev==1?2:1)*F[f][k];
}
int main(int argc,char**argv){
  phi_init(); cls_init(); t0=time(NULL);
  FILE*ff=fopen(argv[1],"r"); NF=0;
  while(NF<MAXF && fscanf(ff,"%d %d %d %d %d %d",&F[NF][0],&F[NF][1],&F[NF][2],&F[NF][3],&F[NF][4],&F[NF][5])==6){
    RF[NF]=0; for(int k=0;k<6;k++) RF[NF]+=F[NF][k]; NF++; }
  fclose(ff);
  if(argc>2) maxsurv=atoll(argv[2]);
  int orbit=-1; if(argc>3) orbit=atoi(argv[3]);
  out=fopen(argc>4?argv[4]:"surv.txt","w");
  // item order by typical impact
  int ord[10][2]={{1,1},{1,2},{2,1},{1,3},{1,4},{2,2},{2,3},{1,5},{2,4},{2,5}};
  NIT=10; for(int i=0;i<10;i++){ IT[i].lev=ord[i][0]; IT[i].k=ord[i][1]; }
  // level-0 orbits: c9 = u-column u=0; c15 = (block beta, v=0); c45 = (u2,v2)
  int reps[14][4]; int nr=0;
  // beta=0: u2 in {0,3,1}, v2 in {0,1}; beta=1: u2 in {0,3,1,2}, v2 in {0,1}
  int u2s0[3]={0,3,1}; int u2s1[4]={0,3,1,2};
  for(int i=0;i<3;i++) for(int v2=0;v2<2;v2++){ reps[nr][0]=0; reps[nr][1]=u2s0[i]; reps[nr][2]=v2; nr++; }
  for(int i=0;i<4;i++) for(int v2=0;v2<2;v2++){ reps[nr][0]=1; reps[nr][1]=u2s1[i]; reps[nr][2]=v2; nr++; }
  for(int r=0;r<nr;r++){
    if(orbit>=0&&r!=orbit) continue;
    int beta=reps[r][0], u2=reps[r][1], v2=reps[r][2];
    u64 S=(1ULL<<45)-1;
    for(int v=0;v<5;v++) S&=~(1ULL<<(5*0+v));
    for(int u=beta;u<9;u+=3) S&=~(1ULL<<(5*u+0));
    S&=~(1ULL<<(5*u2+v2));
    for(int j=0;j<4;j++) col[j]=S;
    for(int f=0;f<NF;f++) rem[f]=0;
    // add impacts of all items to rem (subtracted as they are processed): rem = sum over items not yet processed
    for(int i=0;i<NIT;i++) for(int f=0;f<NF;f++) rem[f]+=(IT[i].lev==1?2:1)*F[f][IT[i].k];
    long long n0=nodes, s0=surv;
    dfs(0);
    fprintf(stderr,"orbit %d (beta=%d u2=%d v2=%d |S0|=%d): nodes %lld survivors %lld [%lds]\n",r,beta,u2,v2,popc(S),nodes-n0,surv-s0,(long)(time(NULL)-t0));
  }
  fprintf(stderr,"TOTAL nodes %lld survivors %lld\n",nodes,surv);
}
