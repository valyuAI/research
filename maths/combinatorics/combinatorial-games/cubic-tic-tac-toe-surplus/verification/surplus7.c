/* Independent second implementation of the Hall-surplus certificate for 7^3.
   No symmetry reduction. For every configuration it computes the exact surplus
   sigma = min over nonempty slot sets S of |N(S)| - |S|  (capped at CAP), where the slot graph
   has two slots per surviving line joined to that line's free cells. sigma >= d means any d
   further Maker cells leave a pairing.
   Mode 1 (centre): Maker {444}; Breaker one non-centre cell on each of the 4 space diagonals
     (6^4 = 1296 sets). Prints histogram (lines killed, sigma).
   Mode 2 (non-centre): Maker {m1} for all 342 non-centre m1; Breaker {444, a, b} with a, b on
     different space diagonals, not the centre, sharing no line (all such pairs). Prints the
     histogram and any configuration with sigma < 2. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 7
#define NC (N*N*N)
#define MAXL 200
#define CAP 4

static int nlines, lc[MAXL][N], dg[NC], cl[NC][16];
static int id3(int x,int y,int z){return ((x-1)*N+(y-1))*N+(z-1);}

static void gen(void){
  nlines=0;
  for(int a=-1;a<=1;a++)for(int b=-1;b<=1;b++)for(int c=-1;c<=1;c++){
    if(!a&&!b&&!c)continue;
    int f=a?a:(b?b:c); if(f<0)continue;
    int d[3]={a,b,c};
    for(int x=1;x<=N;x++)for(int y=1;y<=N;y++)for(int z=1;z<=N;z++){
      int s[3]={x,y,z},ok=1;
      for(int i=0;i<3;i++){ if(d[i]==1&&s[i]!=1)ok=0; if(d[i]==-1&&s[i]!=N)ok=0; }
      if(!ok)continue;
      for(int t=0;t<N;t++) lc[nlines][t]=id3(x+t*a,y+t*b,z+t*c);
      nlines++;
    }
  }
  for(int l=0;l<nlines;l++)for(int t=0;t<N;t++){int q=lc[l][t];cl[q][dg[q]++]=l;}
}

static int occ[NC], alive[MAXL];
static int nslot, sline[2*MAXL+CAP+2], ms[2*MAXL+CAP+2], mc[NC], vis[NC], stamp;

static int aug(int s){
  int l=sline[s];
  for(int t=0;t<N;t++){int c=lc[l][t]; if(occ[c]||vis[c]==stamp)continue; vis[c]=stamp;
    if(mc[c]<0||aug(mc[c])){mc[c]=s;ms[s]=c;return 1;}}
  return 0;
}

/* returns sigma (capped at CAP), or -1 if no saturating matching; *killed set */
static int sigma(int *killed){
  int k=0; for(int l=0;l<nlines;l++) k+=!alive[l]; *killed=k;
  nslot=0;
  for(int l=0;l<nlines;l++) if(alive[l]){sline[nslot++]=l; sline[nslot++]=l;}
  for(int c=0;c<NC;c++) mc[c]=-1;
  for(int s=0;s<nslot;s++){ms[s]=-1; stamp++; if(!aug(s)) return -1;}
  static int sms[2*MAXL+CAP+2], smc[NC];
  memcpy(sms,ms,sizeof(int)*nslot); memcpy(smc,mc,sizeof mc);
  int best=CAP;
  for(int l=0;l<nlines;l++) if(alive[l]){
    int got=0;
    for(int j=0;j<best;j++){ sline[nslot+j]=l; ms[nslot+j]=-1; stamp++; if(aug(nslot+j)) got++; else break; }
    if(got<best) best=got;
    memcpy(ms,sms,sizeof(int)*nslot); memcpy(mc,smc,sizeof mc);
    if(best==0) break;
  }
  return best;
}

static void setpos(const int *mk,int nm,const int *bk,int nb){
  memset(occ,0,sizeof occ); for(int l=0;l<nlines;l++) alive[l]=1;
  for(int i=0;i<nm;i++) occ[mk[i]]=1;
  for(int i=0;i<nb;i++){ occ[bk[i]]=2; for(int j=0;j<dg[bk[i]];j++) alive[cl[bk[i]][j]]=0; }
}

int main(int argc,char**argv){
  setvbuf(stdout,NULL,_IOLBF,0);
  if(argc>2 || (argc==2 && strcmp(argv[1],"1") && strcmp(argv[1],"2"))){
    fprintf(stderr,"Usage: surplus7 [1|2]\n");
    return 2;
  }
  int mode=argc>1?atoi(argv[1]):1;
  gen(); printf("lines=%d\n",nlines);
  if(nlines!=193){fprintf(stderr,"FAIL: expected 193 lines\n");return 1;}
  int ctr=id3(4,4,4);
  int D[4][6];
  for(int t=1,i=0;t<=N;t++){ if(t==4)continue;
    D[0][i]=id3(t,t,t); D[1][i]=id3(t,8-t,t); D[2][i]=id3(8-t,t,t); D[3][i]=id3(t,t,8-t); i++; }
  static long hist[200][CAP+2];
  memset(hist,0,sizeof hist);
  if(mode==1){
    int mk[1]={ctr};
    for(int a=0;a<6;a++)for(int b=0;b<6;b++)for(int c=0;c<6;c++)for(int d=0;d<6;d++){
      int bk[4]={D[0][a],D[1][b],D[2][c],D[3][d]}, kl;
      setpos(mk,1,bk,4); int s=sigma(&kl);
      hist[kl][s+1]++;
    }
    printf("centre: killed sigma(-1=no pairing) count\n");
    for(int k=0;k<200;k++)for(int s=0;s<CAP+2;s++) if(hist[k][s]) printf("  killed=%d sigma=%d%s count=%ld\n",k,s-1,(s-1==CAP)?"+":"",hist[k][s]);
    if(hist[27][5]!=576 || hist[26][5]!=288 || hist[25][3]!=384 || hist[22][0]!=48){
      fprintf(stderr,"FAIL: central surplus histogram differs from the certificate\n");
      return 1;
    }
  } else {
    int dl[NC]; for(int c=0;c<NC;c++) dl[c]=-1;
    for(int i=0;i<4;i++)for(int j=0;j<6;j++) dl[D[i][j]]=i;
    long cfg=0, bad=0, notThree=0;
    for(int m1=0;m1<NC;m1++){ if(m1==ctr)continue;
      for(int i=0;i<4;i++)for(int j=0;j<6;j++)for(int i2=i+1;i2<4;i2++)for(int j2=0;j2<6;j2++){
        int a=D[i][j], b=D[i2][j2];
        if(a==m1||b==m1)continue;
        int share=0; for(int p=0;p<dg[a];p++)for(int q=0;q<dg[b];q++) if(cl[a][p]==cl[b][q]) share=1;
        if(share)continue;
        int mk[1]={m1}, bk[3]={ctr,a,b}, kl;
        setpos(mk,1,bk,3); int s=sigma(&kl); cfg++;
        if(s!=3)notThree++;
        hist[kl][s+1]++;
        if(s<2){ bad++; if(bad<=30){int x=m1/49+1,y=(m1/7)%7+1,z=m1%7+1; printf("  sigma=%d m1=%d%d%d a=%d b=%d\n",s,x,y,z,a,b);} }
      }
      if(m1%20==0){fprintf(stderr,"m1=%d cfg=%ld bad=%ld\n",m1,cfg,bad);}
    }
    printf("noncentre: configurations=%ld with sigma<2: %ld\n",cfg,bad);
    for(int k=0;k<200;k++)for(int s=0;s<CAP+2;s++) if(hist[k][s]) printf("  killed=%d sigma=%d%s count=%ld\n",k,s-1,(s-1==CAP)?"+":"",hist[k][s]);
    if(cfg!=48960 || bad || notThree){
      fprintf(stderr,"FAIL: expected 48960 configurations all with surplus 3\n");
      return 1;
    }
  }
  return 0;
}
