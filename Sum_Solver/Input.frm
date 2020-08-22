#-

off Statistics;

#include Discrete_Calculus.h


L MyFunction = 2;

$SOME = n^3;
.sort 
#call ToPochammer($SOME,n)
*#call FiniteDifference($SOME,n)

L MyFunction = `$SOME';

print;
.end
