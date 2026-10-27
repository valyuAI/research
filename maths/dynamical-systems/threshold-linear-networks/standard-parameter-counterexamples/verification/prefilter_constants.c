/* Print the actual double constants used by the recovered permission filter. */
#include <math.h>
#include <stdio.h>
int main(void) {
  for (int n = 2; n <= 7; n++) {
    double rn = sqrt(1.0 + 9.0 * (n - 1));
    double cinv = n * pow(rn, n - 1) * 1.01;
    printf("%d %a\n", n, cinv);
  }
  return 0;
}
