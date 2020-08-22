#-

off Statistics;

#include Discrete_Calculus.h


L MyFunction = 2;

$SOME = 3*n^2-3*n+1;
.sort 
*#call ToPochammer($SOME,n)
*#call EvalPochammer($SOME,n)

#call Sum($SOME,n)

L MyFunction = `$SOME';

print;
.end
