
f PochammerSymbol;
f HarmonicNumber;
f Factorial;
f Summmation;

#define REPEATCODE "0"

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
    $cache = (replace_(`VAR',0)*(`EXPR'))*PochammerSymbol(nTPCH,0);
    $den = 1;
    if ( count(nTPCH,1) > $xmax ) $xmax = count_(nTPCH,1);
    .sort
    Local EX = 0;
    
    #do i=1,`$xmax'
        
        #call FiniteDifference(`EXPR',`VAR')
        $cache = $cache + (`$den')*(replace_(`VAR',0)*(`EXPR'))*PochammerSymbol(nTPCH,`i');
        $den = `$den'*({`i'+1})^(-1);
        .sort
        
    #enddo
        
    `EXPR' = replace_(nTPCH,`VAR')*(`$cache');
    .sort


#endprocedure


#procedure EvalPochammer(EXPR,VAR)

    .sort 

    Local EX = replace_(`VAR',nEPCH)*(`EXPR');
    id PochammerSymbol(nEPCH,n?) = nCOUN^n*PochammerSymbol(nEPCH,n);
    $xmax = -1;
    if ( count(nCOUN,1) > $xmax ) $xmax = count_(nCOUN,1);
    id nCOUN = 1;
    .sort

    #if REPEATCODE
    
        #message Using repeat code
        repeat;
        id PochammerSymbol(nEPCH,0) = 1;
        id PochammerSymbol(nEPCH,n?) = (nEPCH+n-1)*PochammerSymbol(nEPCH,n-1);
        endrepeat;
    
    #else   *PREPROCESSOR_CODE 
                
        #do i=0,{`$xmax'-1}
        
            id PochammerSymbol(nEPCH,0) = 1;
            id PochammerSymbol(nEPCH,{`$xmax'-`i'}) = (nEPCH+{`$xmax'-`i'-1})*PochammerSymbol(nEPCH,{`$xmax'-`i'-1});
            .sort
        
        #enddo
    
    #endif
    
    id PochammerSymbol(nEPCH,0) = 1;
    id nEPCH = `VAR';
    
    .sort
    Local EX = 0;
    `EXPR' = EX;
    .sort

#endprocedure



#procedure Sum(EXPR,VAR)

*
*  This procedure is based on a simple 
*  premisse, any polynomial function in 
*  the summation variable can be exactly 
*  summed in terms of Pochammer Symbols
*
    #call EvalPochammer(`EXPR',`VAR')
    #call ToPochammer(`EXPR',`VAR')
    
    #message After casting it into PochammerSymbols = ``EXPR''
        
    Local EX = replace_(`VAR',nSUMM)*(`EXPR');
    
    id PochammerSymbol(nSUMM,n?) = (n+1)^(-1)*PochammerSymbol(nSUMM,n+1);
    
    .sort 
    
    `EXPR' = replace_(nSUMM,`VAR')*(EX);
    
    #call EvalPochammer(`EXPR',`VAR')
    
#endprocedure
