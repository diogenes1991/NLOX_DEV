#-

off Statistics;

CF Den,Num;
auto s x;
auto s n;
Table PBifurcation(1);
Table NBifurcation(1);
Table PLadder(1);
Table NLadder(1);
Table RSolution(1);
auto s r,q;

#define VERBOSE "0"
#define POSTPROCESS "0"
#define NEWCODE "0"

#procedure OmmitRoot(DOLLAR,SYMB,ROOT)

    .sort 
    g GLOBAL = xORM*replace_(`SYMB',xOR)*(`DOLLAR');
    id xOR = (xOR+``ROOT'');
    $xmax = -1;
    .sort
    
    if ( count(xOR,1) > $xmax ) $xmax = count_(xOR,1);
    .sort
    
    id xORM*xOR^n? = xORM*xOR^(`$xmax'-n);
    .sort 
    
    $TOS = (`SYMB'-``ROOT'');
    $xmin = -1;
    .sort
    if ( count(xOR,1) > $xmin ) $xmin = count_(xOR,1);
    .sort
    
    #message Cancelling a Polynomial prefactor of (`$TOS')^{`$xmax'-`$xmin'}
    
    $POW = {`$xmax'-`$xmin'};
    id xORM*xOR^n? = (`SYMB'-``ROOT'')^(`$xmin'-n);
    .sort
    
    `DOLLAR' = GLOBAL;
    .sort 
    g GLOBAL = 0 ;
    .sort

#endprocedure

#procedure SpongeFactors(DOLLAR)

    .sort
    $PRE = factorin_(`DOLLAR');
    .sort 
    #message Cancelling a Numerical prefactor of `$PRE'
    `DOLLAR' = (`$PRE')^-1*(``DOLLAR'');
    .sort 
   
#endprocedure 


#procedure Derivative(DOLLAR,SYMB)

*    #message Enter >> ``DOLLAR''
    
    `DOLLAR' = replace_(`SYMB',xDE)*(``DOLLAR'');
    .sort
    #if (`NEWCODE'==1)
    l LOCAL = ``DOLLAR'';
    $xmax = -1;
    .sort
    if ( count(xDE,1) > $xmax ) $xmax = count_(xDE,1);
    .sort
    l LOCAL = 0;
*    #message >> Bracketing done (`TIME_'s)
*    #message >> Stored = ``DOLLAR''
    
    #do i=0,{`$xmax'}
*        #message Derivative: {`i'+1}/{`$xmax'+1}
*        #message Applying >> `SYMB'^{`$xmax'-`i'} = {`$xmax'-`i'}*`SYMB'^{`$xmax'-`i'-1};
        #inside `DOLLAR'
*        id xDE^(`$xmax'-`i') = (`$xmax'-`i')*`SYMB'^(`$xmax'-`i'-1);
        id xDE^{`$xmax'-`i'} = {`$xmax'-`i'}*`SYMB'^{`$xmax'-`i'-1};
        #endinside
    #enddo
    
    
*    #message >> Stored = ``DOLLAR''
*    `DOLLAR' = LOCAL;
*** This line is a bottleneck $VAR = LOCAL is slow... you should avoid this ***
    #write<Definitions.h>"`DOLLAR'=%$;",`DOLLAR'
*    #write<Definitions.h>".sort"
    `DOLLAR' = 0;
    .sort
    
    #else 
        l LOCAL = xDER*(``DOLLAR'');
        id xDER*`SYMB'^n? = n*`SYMB'^(n-1);
        .sort 
        `DOLLAR' = LOCAL;
        .sort
        l LOCAL = 0;
    #endif
    
    
*    #message Exit >> ``DOLLAR''
    
#endprocedure

#procedure HighestPower(DOLLAR,SYMB,POW)

    .sort
    l LOCAL = replace_(`SYMB',xCI)*(`DOLLAR');
    $xmax = -1;
    .sort
        
    if ( count(xCI,1) > $xmax ) $xmax = count_(xCI,1);
    .sort
    
    `POW' = `$xmax';
    
    .sort
    l LOCAL = 0;

#endprocedure


#procedure CreateID(DOLLAR,SYMB,LHSID,RHSID,POW,NUM)
    
*    #message >> We will create an ID for ``DOLLAR'' = 0 wtrt `SYMB'
    
    .sort
    g GLOBAL = replace_(`SYMB',xCI)*(`DOLLAR');
    .sort 
    
    $xmax = -1;
    $xmin = 100;
*    #$TOSHOW = GLOBAL;
    .sort
    
*    #message Stored expression = `$TOSHOW'
    
    if ( count(xCI,1) > $xmax ) $xmax = count_(xCI,1);
    .sort

    if ( count(xCI,1) <= $xmin ) $xmin = count_(xCI,1);
    .sort
    
*    #message `$xmin' --> `$xmax'
    
    id xCI^`$xmax' = xCI3;
    .sort
    #message >> An ID for the {`$xmax'-`$xmin'}th power will be built
    
    $Num = replace_(xCI,xCI0)*replace_(xCI3,0)*GLOBAL;
    $Den = xCI23*replace_(xCI3,xCI23)*GLOBAL;
    .sort 
        
    g GLOBAL = Num(`$Num')*Den(`$Den');
    l LOCAL = Num(`$Den');
    .sort 
    
    argument;
    id xCI23^2 = -1;
    id xCI23 = 0;
    endargument;
    
    .sort
    $NUM = LOCAL;
    
    id Num(x?) = x;
*    id Den(x?) = x^-1;

    
*    #message >> `$NUM'
    
    
    id xCI0 = `SYMB';
    .sort
    `RHSID' = GLOBAL*(x^{-`$xmin'});
    `LHSID' = `SYMB'^{`$xmax'-`$xmin'};
    `POW' = {`$xmax'-`$xmin'};
    `NUM' = `$NUM';
    .sort

*    #message Created identity id ``LHSID'' == ``RHSID''
    
    g GLOBAL = 0;
    l LOCAL = 0;
    
#endprocedure

#procedure ApplyID(DOLLAR,SYMB,LHSID,RHSID,POW,NUM)

    .sort
    g GLOBAL = replace_(`SYMB',xAID)*(`DOLLAR');
    `LHSID' = replace_(`SYMB',xAID)*(``LHSID'');
    `RHSID' = replace_(`SYMB',xAID)*(``RHSID'');

    $xmax = -1;
    if ( count(xAID,1) > $xmax ) $xmax = count_(xAID,1);
*    #call HighestPower(`DOLLAR',`SYMB',$xmax)
    .sort 
    
*    #message >> Applying ID to ``DOLLAR''
    
    #message >> We need to apply an ID of degree ``POW'' to a `$xmax'-degree polynomial:
*    #message >> We will apply id ``LHSID'' = ``RHSID'';
*    #message We assume that the roots of ``NUM'' are not the solution

    #do j=0,{`$xmax'-``POW''}
        #message >> Applying id on: `SYMB'^{`$xmax'-`j'} (`TIME_'s)
        $IterId = (xAID^{`$xmax'-`j'-``POW''})*(``RHSID'');
        .sort
        g GLOBAL = (`$NUM')*(GLOBAL);
        .sort
        id xAID^{`$xmax'-`j'} = `$IterId';
        id Num(x?)*Den(x?) = 1;
        id Num(x?) = x;
        .sort
    #enddo
    
    id xAID = `SYMB';
    .sort
    
    `DOLLAR' = GLOBAL;
    .sort
    #call SpongeFactors(`DOLLAR')
    g GLOBAL = 0;
    .sort

#endprocedure


#procedure CompoundLogistic(DOLLAR,SYMB)
    $DOLLAR = replace_(`SYMB',(r)*`SYMB'*(1-`SYMB'))*(`DOLLAR');
    .sort 
    `DOLLAR' = `$DOLLAR';
    .sort
#endprocedure


#procedure LogisticBifurcaions(B,N)

    $M = {`B'*2^{`N'}/2};
    .sort 
    
    g [NBifurcation(`$M')] = 0;
    g [PBifurcation(`$M')] = 0;

    #message -----------------------------------------------------
    #message Finding the defining equations for 
    #message the {`B'*2^{`N'}/2} --> {`B'*{2^`N'}} Bifurcation
    
    
    $Base = x;
    $NDefinition = x;
    $PDefinition = x;
    $Constraint = x;
    $Redundant  = x;
    .sort
    
    #redefine NEWCODE "1"
    
    #do i=1,{`B'*2^`N'}
        #message Now on step `i'/{`B'*2^`N'} of building (`TIME_'s)
        #call CompoundLogistic($Base,x)
    #if ( `i' == {`B'*2^{`N'}/2} )
        $NDefinition = `$Base'+x;
        $Constraint = `$Base'-x;
        .sort
    #endif
    #if (`N'>=1)
    #if ((`i'=={2^{`N'}*`B'/4}))
        $Redundant = `$Base';
        .sort
    #endif
    #endif
    #enddo
    
    $PDefinition = `$Base'-x;
    $Redundant = `$Redundant'-x;    
    .sort 
    
    #message Base definition built (`TIME_')
    

    #message Deriving 1/2 
    #call Derivative($PDefinition,x)
    #message (`TIME_'s)
    #message Deriving 2/2
    #call Derivative($NDefinition,x)
    #message (`TIME_'s)
    .sort 
    
    
    
    #message Definitions and constraint built (`TIME_'s)
    
    #if(`N'>=1)
        $TOID = div_(`$Constraint',`$Redundant');
    #else
        $TOID = `$Constraint';
    #endif
    .sort 
    
    #include Definitions.h
    $LHSID = 0;
    $RHSID = 0;
    $POW = 0;
    $NUM = 0;
    .sort
    
*    #message $PDefinition = `$PDefinition'
*    #message $NDefinition = `$NDefinition'
    
    #redefine POSTPROCESS "1"
    #if (`POSTPROCESS')
    
    #call CreateID($TOID,x,$LHSID,$RHSID,$POW,$NUM)
    #call ApplyID($NDefinition,x,$LHSID,$RHSID,$POW,$NUM)
    #call ApplyID($PDefinition,x,$LHSID,$RHSID,$POW,$NUM)
        
    g [NBifurcation(`$M')] = `$NDefinition';
    g [PBifurcation(`$M')] = `$PDefinition';
    .sort

    
    
    
    #message Building of defining equations done (`TIME_'s)
    #message -----------------------------------------------------

*    
*    ------------  BUILDING P-N DEFINITIONS DONE -----------------
*    ------------      BUILDING LADDERS NOW      -----------------
*
   
   #message Reducing positive definition
    
    g [PLadder(`$M')] = 0;
    $TOID = [NBifurcation(`$M')];
    .sort
    
    #call HighestPower($TOID,x,$POW)
    
    #do i=1,{`$POW'-{`B'*2^{`N'}/2}}
        $EXPR = [PBifurcation(`$M')];
        .sort
        #call HighestPower($TOID,x,$POW)
        #if( `$POW' <= {`B'*2^{`N'}/2} )
            #message Reduction of positive definition done (`TIME_'s)
            #message ------------------------------------------------
            #breakdo
        #else
            #call CreateID($TOID,x,$LHSID,$RHSID,$POW,$NUM)
            #call ApplyID($EXPR,x,$LHSID,$RHSID,$POW,$NUM)
            $VALUE = -2;
            #call OmmitRoot($EXPR,r,$VALUE)
            $VALUE = 2;
            #call OmmitRoot($EXPR,r,$VALUE)
            $VALUE = 4;
            #call OmmitRoot($EXPR,r,$VALUE)
            $TOID = $EXPR;
            .sort 
        #endif
    #enddo
    
    g [PLadder(`$M')] = `$TOID';
    .sort    

*
*----------------------------------------------------------
*

    #message Reducing negative definition
    
    g [NLadder(`$M')] = 0;
    $TOID = [PBifurcation(`$M')];
    .sort
    
    #call HighestPower($TOID,x,$POW)
    
    #do i=1,{`$POW'-{`B'*2^{`N'}/2}}
        $EXPR = [NBifurcation(`$M')];
        .sort
        #call HighestPower($TOID,x,$POW)
        #if( `$POW' <= {`B'*2^{`N'}/2} )
            #message Reduction of negative definition done (`TIME_'s)
            #message ------------------------------------------------
            #breakdo
        #else
            #call CreateID($TOID,x,$LHSID,$RHSID,$POW,$NUM)
            #call ApplyID($EXPR,x,$LHSID,$RHSID,$POW,$NUM)
            $VALUE = -2;
            #call OmmitRoot($EXPR,r,$VALUE)
            $VALUE = 2;
            #call OmmitRoot($EXPR,r,$VALUE)
            $VALUE = 4;
            #call OmmitRoot($EXPR,r,$VALUE)
            $TOID = $EXPR;
            .sort 
        #endif
    #enddo
    
    g [NLadder(`$M')] = `$TOID';
    .sort  

*
*    --------------   LADDERS BUILT    --------------------
*    -------------  SOLVING FOR R NOW  --------------------
*

    $PDefinition = replace_(x,xSR)*[PLadder(`$M')];
    $NDefinition = replace_(x,xSR)*[NLadder(`$M')];
    .sort 
    
    #call HighestPower($PDefinition,xSR,$POW)
    
    #do i=0,`$POW'
        .sort
        l CP`i' = `$PDefinition';
        l CN`i' = `$NDefinition';
        .sort
        id xSR^{`$POW'-`i'+1} = 1;
        id xSR = 0;
        .sort 
    #enddo
    
    #if (`$POW'>0)
    #do i=0,{`$POW'-1}
        .sort
        l CR`i' = (CP`i')*(CN`$POW') - (CN`i')*(CP`$POW');
        .sort
        #if(`i'>0)
        g [RSolution(`$M')] = gcd_([RSolution(`$M')],CR`i');
        #else
        g [RSolution(`$M')] = CR`i';
        #endif
        .sort
    #enddo
    #else 
        g [RSolution(`$M')] = gcd_([PLadder(`$M')],[NLadder(`$M')]);
    #endif
    
    $EXPR = [RSolution(`$M')];
    #call SpongeFactors($EXPR)
    $VALUE = 2;
    #call OmmitRoot($EXPR,r,$VALUE)
    $VALUE = 4;
    #call OmmitRoot($EXPR,r,$VALUE)
    $VALUE = -2;
    #call OmmitRoot($EXPR,r,$VALUE)
    g [RSolution(`$M')] = `$EXPR';
    .sort
 
 
*    ------------  R SOLVING FOR DONE  --------------------
*    ------------  SOLVING FOR X NOW   --------------------
*
*
*    $TOID = [RSolution(`$M')];
*    $EXPR = [PLadder(`$M')];
*    .sort
*    #call CreateID($TOID,r,$LHSID,$RHSID,$POW,$NUM)
*    #call ApplyID($EXPR,r,$LHSID,$RHSID,$POW,$NUM)
*    #call SpongeFactors($EXPR)
*    $VALUE = 2;
*    #call OmmitRoot($EXPR,r,$VALUE)
*    $VALUE = 4;
*    #call OmmitRoot($EXPR,r,$VALUE)
*    $VALUE = -2;
*    #call OmmitRoot($EXPR,r,$VALUE)
*    
*    g PXSolution = `$EXPR';
*    .sort
*    
*    $TOID = [RSolution(`$M')];
*    $EXPR = [NLadder(`$M')];
*    .sort
*    #call CreateID($TOID,r,$LHSID,$RHSID,$POW,$NUM)
*    #call ApplyID($EXPR,r,$LHSID,$RHSID,$POW,$NUM)
*    #call SpongeFactors($EXPR)
*    $VALUE = 2;
*    #call OmmitRoot($EXPR,r,$VALUE)
*    $VALUE = 4;
*    #call OmmitRoot($EXPR,r,$VALUE)
*    $VALUE = -2;
*    #call OmmitRoot($EXPR,r,$VALUE)
*    
*    g NXSolution = `$EXPR';

*    id r = 1+sqrt_(q);
*    id sqrt_(q)^2 = q;

*    g GLOBAL =0;
    .sort

    #endif
    #message Solution to the {`B'*2^{`N'-1}} --> {`B'*2^`N'} Bifurcation done
    #message All the r that produce this are roots of [RSolution(`$M')] = 0
    #message -------------------------------------------------------------
    

#endprocedure

*** This line is required to 
*** have an active expression from 
*** the start...

g GLOBAL = 1;

*#call LogisticBifurcaions(0)
*#call LogisticBifurcaions(2,1)
*#call LogisticBifurcaions(3,1)
*#call LogisticBifurcaions(5,1)
#call LogisticBifurcaions(2,1)
*#call LogisticBifurcaions(2)
*#call LogisticBifurcaions(3)

.sort 



*** The statement #if (`i'=={2^{`N'-1}}...) hangs the preprocessor if `N'==0 !!

******************************************
******       OLD CODE      ***************


*************************************************************************************************

print;
.end
