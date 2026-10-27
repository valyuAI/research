#include <stdio.h>
#include <stdlib.h>
#include "phi.h"
#include "wsc_brute.h"
int main(){ phi_init(); wsc_init(); srand(7); int bad=0;
  for(int t=0;t<20000;t++){ int rho[6]; for(int k=0;k<6;k++) rho[k]=1+rand()%60;
    u64 S=0; int dens=rand()%100; for(int i=0;i<45;i++) if(rand()%100<dens) S|=1ULL<<i;
    int a=phi(S,rho), b=wsc(S,rho); if(a!=b){ bad++; if(bad<5) printf("mismatch %d %d\n",a,b);} }
  printf("mismatches %d\n",bad); return bad ? 1 : 0; }
