/* Independent re-verification of Breaker's win in 7^3 Maker-Breaker tic-tac-toe
   (Cain-Raymond-Kallersjo, arXiv:2509.21494), with every Maker line of play enumerated.

   Case C (Maker opens at the centre 444): the published rule, as in the authors' public
   starting-moves.C: Breaker 555, then 626, then 117 / 771 / 177, then 177 / 711 / 622 / 266
   (or 226 / 662). Maker's 2nd move is restricted to x<=y exactly as in the published
   enumeration (the reflection x<->y fixes 444 and 555).
   Case N (Maker opens elsewhere): Breaker takes 444; Maker's 1st move reduced to the 19
   orbit representatives of the 48-element cube group. For each Maker 2nd move:
     - if some symmetry g maps both Maker moves into x<=4 (paper's WLOG), Breaker plays
       g^-1(555) then g^-1(626) or, if taken, g^-1(717)   [paper rule]
     - otherwise (opposite open octants: the gap in the paper's WLOG) Breaker uses a
       greedy rule: the free cell that eliminates the most surviving lines (lowest index
       on ties), for both of the next two moves                     [repair rule]
   After the prescribed moves, the position must admit a pairing: a matching saturating
   two slots per surviving line into distinct free cells of that line.

   Output: counts of positions checked and failures, per case. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 7
#define NC (N*N*N)
#define MAXL 200
#define MAXDEG 16

static int nlines;
static int lcell[MAXL][N];
static int deg[NC], cl[NC][MAXDEG];

static int idx(int x, int y, int z) { return ((x-1)*N + (y-1))*N + (z-1); }
static void coords(int c, int *x, int *y, int *z) { *x = c/(N*N)+1; *y = (c/N)%N+1; *z = c%N+1; }

static void gen_lines(void) {
  int dirs[13][3], nd = 0;
  for (int a=-1;a<=1;a++) for (int b=-1;b<=1;b++) for (int c=-1;c<=1;c++) {
    if (!a && !b && !c) continue;
    /* canonical sign: first nonzero component positive */
    int f = a ? a : (b ? b : c);
    if (f < 0) continue;
    dirs[nd][0]=a; dirs[nd][1]=b; dirs[nd][2]=c; nd++;
  }
  nlines = 0;
  for (int d=0; d<nd; d++) {
    for (int x=1;x<=N;x++) for (int y=1;y<=N;y++) for (int z=1;z<=N;z++) {
      int s[3]={x,y,z}, ok=1;
      for (int i=0;i<3;i++) {
        if (dirs[d][i]==1 && s[i]!=1) ok=0;
        if (dirs[d][i]==-1 && s[i]!=N) ok=0;
      }
      if (!ok) continue;
      for (int t=0;t<N;t++) lcell[nlines][t] = idx(x+t*dirs[d][0], y+t*dirs[d][1], z+t*dirs[d][2]);
      nlines++;
    }
  }
  memset(deg,0,sizeof deg);
  for (int l=0;l<nlines;l++) for (int t=0;t<N;t++) { int c=lcell[l][t]; cl[c][deg[c]++]=l; }
}

/* cube symmetries: perm p of coords and sign flips s (bit i => coord i -> N+1-coord) */
static int symap[48][NC], syminv[48][NC];
static void gen_syms(void) {
  int perms[6][3]={{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
  int g=0;
  for (int p=0;p<6;p++) for (int s=0;s<8;s++,g++) {
    for (int c=0;c<NC;c++) {
      int v[3]; coords(c,&v[0],&v[1],&v[2]);
      int w[3];
      for (int i=0;i<3;i++) { int u=v[perms[p][i]]; w[i] = (s>>i&1) ? N+1-u : u; }
      int d = idx(w[0],w[1],w[2]);
      symap[g][c]=d; syminv[g][d]=c;
    }
  }
}

/* ---------- position state ---------- */
static int occ[NC];        /* 0 free, 1 maker, 2 breaker */
static int alive[MAXL];    /* line not yet containing a breaker cell */

static void reset_pos(void){ memset(occ,0,sizeof occ); for(int l=0;l<nlines;l++) alive[l]=1; }
static void play(int c, int who){ occ[c]=who; if(who==2) for(int i=0;i<deg[c];i++) alive[cl[c][i]]=0; }

/* ---------- matching: slots (2 per alive line) -> free cells ---------- */
static int nslot, slotline[2*MAXL];
static int mslot[2*MAXL], mcell[NC];
static int vis[NC], stamp;

static int augment(int s) {
  int l = slotline[s];
  for (int t=0;t<N;t++) {
    int c = lcell[l][t];
    if (occ[c] || vis[c]==stamp) continue;
    vis[c]=stamp;
    if (mcell[c]<0 || augment(mcell[c])) { mcell[c]=s; mslot[s]=c; return 1; }
  }
  return 0;
}

/* returns size of maximum matching; pairing exists iff == nslot */
static int full_matching(void) {
  nslot=0;
  for (int l=0;l<nlines;l++) if (alive[l]) { slotline[nslot++]=l; slotline[nslot++]=l; }
  for (int c=0;c<NC;c++) mcell[c]=-1;
  int sz=0;
  for (int s=0;s<nslot;s++) { mslot[s]=-1; stamp++; if (augment(s)) sz++; }
  return sz;
}

/* independent re-check of a found matching (used on every success when CHECK) */
static int verify_matching(void) {
  static int used[NC]; memset(used,0,sizeof used);
  for (int s=0;s<nslot;s++) {
    int c=mslot[s]; if (c<0) return 0;
    if (occ[c]) return 0;
    if (used[c]) return 0; used[c]=1;
    int l=slotline[s], on=0; for(int t=0;t<N;t++) if(lcell[l][t]==c) on=1;
    if(!on) return 0;
    if (!alive[l]) return 0;
  }
  /* every alive line has exactly 2 slots */
  int cnt=0; for(int l=0;l<nlines;l++) if(alive[l]) cnt++;
  return cnt*2==nslot;
}

static int n_alive(void){ int k=0; for(int l=0;l<nlines;l++) k+=alive[l]; return k; }

static long long checked=0, failures=0;
static int verbose_fail=20;

static void check_pos(const char *tag, int *mv, int nm) {
  int sz = full_matching();
  checked++;
  if (sz != nslot || !verify_matching()) {
    failures++;
    if (verbose_fail-- > 0) {
      printf("FAIL %s alive=%d slots=%d matched=%d moves:", tag, n_alive(), nslot, sz);
      for (int i=0;i<nm;i++){int x,y,z; coords(mv[i],&x,&y,&z); printf(" %d%d%d",x,y,z);} printf("\n");
    }
  }
}


/* incremental: current position has a complete matching; test the position obtained by
   additionally giving cell m to Maker (one augmentation), then restore. */
static int savems[2*MAXL], savemc[NC];
static void check_incremental(const char *tag, int m, int *mv, int nm) {
  memcpy(savems,mslot,sizeof(int)*nslot); memcpy(savemc,mcell,sizeof mcell);
  occ[m]=1;
  int ok=1;
  if (mcell[m]>=0) { int s=mcell[m]; mcell[m]=-1; mslot[s]=-1; stamp++; ok=augment(s); }
  checked++;
  if (!ok || !verify_matching()) {
    /* fall back to a full recomputation before declaring failure */
    int sz=full_matching();
    if (sz!=nslot || !verify_matching()) {
      failures++;
      if (verbose_fail-- > 0) {
        printf("FAIL %s alive=%d slots=%d matched=%d moves:", tag, n_alive(), nslot, sz);
        for (int i=0;i<nm;i++){int x,y,z; coords(mv[i],&x,&y,&z); printf(" %d%d%d",x,y,z);}
        {int x,y,z; coords(m,&x,&y,&z); printf(" +M%d%d%d",x,y,z);} printf("\n");
      }
    }
    occ[m]=0; full_matching(); return;
  }
  occ[m]=0;
  memcpy(mslot,savems,sizeof(int)*nslot); memcpy(mcell,savemc,sizeof mcell);
}

/* greedy: free cell eliminating most alive lines, lowest index on ties */
static int greedy_move(void) {
  int best=-1, bv=-1;
  for (int c=0;c<NC;c++) if(!occ[c]) {
    int v=0; for(int i=0;i<deg[c];i++) v+=alive[cl[c][i]];
    if (v>bv){bv=v;best=c;}
  }
  return best;
}

int main(int argc, char **argv) {
  setvbuf(stdout, NULL, _IOLBF, 0);
  if (argc > 2 || (argc == 2 && strcmp(argv[1], "0") && strcmp(argv[1], "1") && strcmp(argv[1], "2"))) {
    fprintf(stderr, "Usage: replicate_published [0|1|2]\n");
    return 2;
  }
  int which = argc>1 ? atoi(argv[1]) : 0; /* 0 both, 1 centre case, 2 non-centre case */
  gen_lines(); gen_syms();
  printf("n=%d lines=%d\n", N, nlines);
  int C444=idx(4,4,4), C555=idx(5,5,5), C626=idx(6,2,6), C717=idx(7,1,7);
  int c117=idx(1,1,7), c771=idx(7,7,1), c177=idx(1,7,7), c711=idx(7,1,1), c622=idx(6,2,2), c266=idx(2,6,6), c226=idx(2,2,6), c662=idx(6,6,2);
  int mv[8];

  if (which==0 || which==1) {
    /* Case C, paper rule, Maker 2nd move with x<=y. */
    long long c0=checked, f0=failures;
    for (int m2=0;m2<NC;m2++) {
      int x,y,z; coords(m2,&x,&y,&z);
      if (x>y || m2==C444 || m2==C555) continue;
      for (int m3=0;m3<NC;m3++) {
        if (m3==C444||m3==C555||m3==m2||m3==C626) continue;
        int b3;
        if ((m2==c117&&m3==c771)||(m2==c771&&m3==c117)) b3=c177;
        else if (m2!=c117 && m3!=c117) b3=c117;
        else b3=c771;
        int list[4]={c177,c711,c622,c266};
        int prim;
        if (b3==c177) prim=c226;
        else { prim=-1; for(int i=0;i<4;i++) if(list[i]!=m2&&list[i]!=m3){prim=list[i];break;} }
        /* base: M4 not yet played, B4 = prim */
        reset_pos();
        mv[0]=C444; mv[1]=C555; mv[2]=m2; mv[3]=C626; mv[4]=m3; mv[5]=b3; mv[6]=prim;
        play(C444,1); play(C555,2); play(m2,1); play(C626,2); play(m3,1); play(b3,2); play(prim,2);
        int sz=full_matching();
        int basefull = (sz==nslot);
        for (int m4=0;m4<NC;m4++) {
          if (m4==C444||m4==C555||m4==m2||m4==C626||m4==m3||m4==b3) continue;
          if (m4==prim) continue;
          if (basefull) check_incremental("C", m4, mv, 7);
          else { occ[m4]=1; check_pos("C", mv, 7); occ[m4]=0; }
        }
        /* M4 = prim: Breaker takes the next cell */
        {
          int m4=prim, b4;
          if (b3==c177) b4=c662;
          else { b4=-1; for(int i=0;i<4;i++) if(list[i]!=m2&&list[i]!=m3&&list[i]!=m4){b4=list[i];break;} }
          reset_pos();
          mv[0]=C444; mv[1]=C555; mv[2]=m2; mv[3]=C626; mv[4]=m3; mv[5]=b3; mv[6]=m4; mv[7]=b4;
          for (int i=0;i<8;i++) play(mv[i], (i%2==0)?1:2);
          check_pos("C", mv, 8);
        }
      }
      fprintf(stderr,"caseC m2=%d checked=%lld fail=%lld\n", m2, checked-c0, failures-f0);
    }
    printf("CASE_C checked=%lld failures=%lld\n", checked-c0, failures-f0);
    fflush(stdout);
  }

  if (which==0 || which==2) {
    long long c0=checked, f0=failures, gapcases=0, gapchecked=0, gapfail=0;
    /* orbit representatives of non-centre cells: centred |a|>=|b|>=|c|, take a,b,c>=0 */
    for (int m1=0;m1<NC;m1++) {
      int x,y,z; coords(m1,&x,&y,&z);
      int a=x-4,b=y-4,c=z-4;
      if (a<0||b<0||c<0||a<b||b<c||m1==C444) continue;
      /* x is largest coordinate >= 4 here; map so that the paper's convention works:
         we do not need x<=4 for M1, the per-M2 symmetry search handles everything */
      for (int m2=0;m2<NC;m2++) {
        if (m2==m1||m2==C444) continue;
        int g=-1;
        for (int h=0;h<48;h++) { int x1,y1,z1,x2,y2,z2; coords(symap[h][m1],&x1,&y1,&z1); coords(symap[h][m2],&x2,&y2,&z2);
          if (x1<=4 && x2<=4){g=h;break;} }
        if (g>=0) {
          int b2=syminv[g][C555], b3a=syminv[g][C626], b3b=syminv[g][C717];
          reset_pos(); play(m1,1); play(C444,2); play(m2,1); play(b2,2); play(b3a,2);
          mv[0]=m1; mv[1]=C444; mv[2]=m2; mv[3]=b2; mv[4]=b3a;
          int sz=full_matching(); int basefull=(sz==nslot);
          for (int m3=0;m3<NC;m3++) {
            if (m3==m1||m3==m2||m3==C444||m3==b2||m3==b3a) continue;
            if (basefull) check_incremental("N", m3, mv, 5);
            else { occ[m3]=1; check_pos("N", mv, 5); occ[m3]=0; }
          }
          reset_pos(); play(m1,1); play(C444,2); play(m2,1); play(b2,2); play(b3a,1); play(b3b,2);
          mv[4]=b3a; mv[5]=b3b; check_pos("N", mv, 6);
        } else {
          gapcases++;
          reset_pos(); play(m1,1); play(C444,2); play(m2,1);
          int b2=greedy_move();
          for (int m3=0;m3<NC;m3++) {
            if (m3==m1||m3==m2||m3==C444||m3==b2) continue;
            reset_pos(); play(m1,1); play(C444,2); play(m2,1); play(b2,2); play(m3,1);
            int b3=greedy_move(); play(b3,2);
            mv[0]=m1; mv[1]=C444; mv[2]=m2; mv[3]=b2; mv[4]=m3; mv[5]=b3;
            long long fb=failures;
            check_pos("GAP", mv, 6);
            gapchecked++; if (failures>fb) gapfail++;
          }
        }
      }
      fprintf(stderr,"caseN m1=%d%d%d checked=%lld fail=%lld\n", x,y,z, checked-c0, failures-f0);
    }
    printf("CASE_N checked=%lld failures=%lld (gap (M1,M2) pairs=%lld, gap positions=%lld, gap failures=%lld)\n",
           checked-c0, failures-f0, gapcases, gapchecked, gapfail);
  }
  printf("TOTAL checked=%lld failures=%lld\n", checked, failures);
  long long expected = which == 1 ? 22163142 : which == 2 ? 2196381 : 24359523;
  if (checked != expected) {
    fprintf(stderr, "FAIL: expected %lld checked positions\n", expected);
    return 1;
  }
  return failures ? 1 : 0;
}
