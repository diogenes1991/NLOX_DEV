
f PochammerSymbol;

auto s n;

#procedure FiniteDifference(EXPR,VAR)
    
        .sort
         Local EX = nFND*(`EXPR');
        id nFND*`VAR'^nE? = `VAR'^nE-(`VAR'-1)^nE;
        .sort 
        `EXPR' = EX;
        .sort
        Local EX = 0;

#endprocedure




#procedure ToPochammer(EXPR,VAR)

    .sort 
*
*  This procedure makes use of
*  Taylor's theorem to express
*  any polynomial in terms of Pochammer
*  symbols to prepare it for summation
*

    Local EX = replace_(`VAR',nTPCH)*(`EXPR');
    $xmax = -1;
    if ( count(nTPCH,1) > $xmax ) $xmax = count_(nTPCH,1);
    .sort
    #message The maximum term has degree = `$xmax'
    
    


#endprocedure








#procedure SumPochammer($EXPR,$VAR)

    .sort 
*
*  This procedure is based on a simple 
*  premisse, any polynomial function in 
*  the summation variable can be exactly 
*  summed in terms of Pochammer Symbols
*
    
    Local EXPR = `EXPR'

#endprocedure
