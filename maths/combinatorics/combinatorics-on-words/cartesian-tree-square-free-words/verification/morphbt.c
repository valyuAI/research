// Backtracking generator of q-uniform morphisms tau:{a,b,c}->{0,1,2}^q (or {0,1}^q) such that
// tau(f) is l+-CT-square-free for all 7/4+-free ternary f of length <= n0.
// Usage: morphbt s l q n0 maxsol
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int s, L, q, n0, maxsol, nsol;
static int ok_ext(const int *w, int n){ for (int p=1;p<n;p++){int Lr=p; while(Lr<n && w[n-1-Lr]==w[n-1-Lr+p]) Lr++; if(4*Lr>7*p) return 0;} return 1; }
// base words grouped by the set of letters used; we store all 7/4+-free words of length 2..n0
static int nbw; static int bw[200000][32]; static int bwl[200000]; static int bwmask[200000];
static void gen(int *w, int n){
  if (n >= 2){ memcpy(bw[nbw], w, sizeof(int)*n); bwl[nbw]=n; int mk=0; for(int i=0;i<n;i++) mk|=1<<w[i]; bwmask[nbw]=mk; nbw++; }
  if (n == n0) return;
  for (int c=0;c<3;c++){ w[n]=c; if (ok_ext(w,n+1)) gen(w,n+1); }
}
static int img[3][64];
static int ctfree(const int *x, int n){
  int g[2048];
  for (int i=0;i<n;i++){ int j=i-1; while(j>=0 && x[j]>x[i]) j=g[j]; g[i]=j; }
  for (int m=L; 2*m<=n; m++) for (int p=0;p+2*m<=n;p++){
    int t; for (t=0;t<m;t++){ int a = g[p+t]>=p ? p+t-g[p+t] : 0; int b = g[p+m+t]>=p+m ? p+m+t-g[p+m+t] : 0; if (a!=b) break; }
    if (t==m) return 0; }
  return 1;
}
static int test_mask(int need){ // test all base words whose letter set is within 'need' and uses the newest letter
  int x[2048];
  for (int k=0;k<nbw;k++){ if ((bwmask[k] & ~need) || !(bwmask[k] & (need ^ (need>>1)) & ~(need>>1) )) {}
    if ((bwmask[k] & ~need)) continue;
    int n=0; for (int i=0;i<bwl[k];i++) for (int t=0;t<q;t++) x[n++]=img[bw[k][i]][t];
    if (!ctfree(x,n)) return 0; }
  return 1;
}
static int cand[600000][16]; static int ncand;
static void gencand(int *v, int n){
  if (n==q){ if (ctfree(v,q)) { memcpy(cand[ncand++], v, sizeof(int)*q); } return; }
  for (int c=0;c<s;c++){ v[n]=c; // prune: prefix must be CT-free
    if (ctfree(v,n+1)) gencand(v,n+1); }
}
static int sync_ok(int upto){ // synchronizing among letters < upto
  for (int a=0;a<upto;a++) for (int b=0;b<upto;b++) for (int c=0;c<upto;c++) for (int off=1;off<q;off++){
    int eq=1; for (int t=0;t<q;t++){ int pos=off+t; int ch = pos<q? img[a][pos]:img[b][pos-q]; if(ch!=img[c][t]){eq=0;break;} } if(eq) return 0; }
  return 1;
}
int main(int argc,char**argv){
  s=atoi(argv[1]); L=atoi(argv[2]); q=atoi(argv[3]); n0=atoi(argv[4]); maxsol=atoi(argv[5]);
  int w[64]; nbw=0; gen(w,0);
  int v[64]; ncand=0; gencand(v,0);
  fprintf(stderr,"base words %d, candidate blocks %d\n", nbw, ncand);
  for (int i=0;i<ncand;i++){ memcpy(img[0],cand[i],sizeof(int)*q);
    if (!test_mask(1)) continue;
    for (int j=i+1;j<ncand;j++){ memcpy(img[1],cand[j],sizeof(int)*q);
      if (!test_mask(3)) continue;
      for (int k=j+1;k<ncand;k++){ memcpy(img[2],cand[k],sizeof(int)*q);
        if (!sync_ok(3)) continue;
        if (!test_mask(7)) continue;
        nsol++; printf("SOL q=%d:",q); for(int a=0;a<3;a++){printf(" ");for(int t=0;t<q;t++)printf("%d",img[a][t]);} printf("\n"); fflush(stdout);
        if (nsol>=maxsol) return 0;
      }
    }
    if (i % 200 == 0) { fprintf(stderr, "progress %d/%d sols %d\n", i, ncand, nsol); }
  }
  fprintf(stderr,"done sols %d\n",nsol);
  return 0;
}
