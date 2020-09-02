import sys
import os
import re
import multiprocessing.dummy
import time
import subprocess
import gzip

#=====================================================================
#
# FORM output parsing, variable replacement and FORM input generation
#
#=====================================================================

def splitExpressions(filename):
    ''' Read and store the expressions from a FORM output file.

    The return value is a list of dictionaries, one for each expression.
    "name" is the name of the expression (the LHS of the expression).
    "value" is a list of two-component lists. Each item in the main list
    is one term in the FORM expression (separated in the file by two
    newlines). The first item of the sublist for a term is what's
    bracketed (in the FORM sense), and the second item is the rest.
    '''
    print 'Splitting',filename
    with open(filename, 'r') as file:
        lines = []
        exprline = ""
        for line in file:
            if "FORM" in line  or "#" in line  or "~"  in line or "off statistics" in line or ".sort" in line or "argument" in line or "endargument" in line:
                continue
            exprline += line.strip(' ')
            if ";" in line:
                lines.append(exprline.strip())
                exprline = ""

    expressions = []
    for line in lines:
        expr = line.split('=')
        if len(expr)<2:
            print expr
            sys.exit()
        expr[0] = expr[0].replace('\n','').replace("\\", '').replace('l ','')
        subexpr = expr[1].split('\n\n')
        bres = []
        for sexpr in subexpr:
            sexpr = sexpr.replace('\n','').replace(';','').strip()
            brackets = sexpr.split("* ")
            brackets[0] = brackets[0].strip("+ ")
            bres.append(brackets)
        expressions.append({"name":expr[0], "value":bres})

    return expressions

def unique(seq, fun=None):
    ''' Return a list of unique members of the list seq.

    "fun" is an optional function which can be specified to be used to
    assign a simple marker to be used to identify more complicated objects.
    It does not appear to be used ever.
    '''
    if fun is None:
        def fun(x): return x
    seen = {} # Why not just use a set?
    result = []
    for item in seq:
        marker = fun(item)
        if marker in seen: continue
        seen[marker]=1
        result.append(item)
    return result

def findVariables(expr, prefix):
    ''' Return a list of variables in expr containing prefix. '''
    x = expr.replace('(',',');
    x = x.replace(')',',');
    x = x.split(',');
    return unique([i for i in x if i.find(prefix) != -1])

def replaceVariable(expr, prefix, ignorepattern = None, 
                    repsuffix = None, repprefix = None, continuous = False):
    if repsuffix is not None:
        if len(repsuffix) != len(prefix):
            raise ValueError("Error: wrong repsuffix")
    else:
        repsuffix = ["" for x in prefix]

    if repprefix is not None:
        if len(repprefix) != len(prefix):
            raise ValueError("Error: wrong repprefix")
    else:
        repprefix = prefix

    count = 0
    for p in range(len(prefix)):
        x = findVariables(expr, prefix[p])
        if ignorepattern is not None:
            x = [i for i in x if i.find(ignorepattern) == -1]
        rep = {x[i]:("TMP"+repprefix[p]+"TMP"+str(count+i)+"TMP"+repsuffix[p]) for i in range(len(x))}
        for k,v in rep.iteritems():
            expr = re.sub(k + r'/?', v, expr)
            #expr = expr.replace(k + r'?', v)
        expr = expr.replace("TMP","")
        if continuous:
            count += len(x)
    return expr

def varToFormPattern(expr, prefix, ignorepattern = None):
    for p in prefix:
        x = findVariables(expr, p)
        if ignorepattern is not None:
            x = [i for i in x if i.find(ignorepattern) == -1]
# Change by Seth: add exclusion set to FORM pattern. By convention this 
# must be named prefix+ignorepattern
        rep = {i:i + "?!" + p + ignorepattern for i in x}
        for k,v in rep.iteritems():
            expr = re.sub(r'' + k +r'([^'+ignorepattern+'])', v + r'\1', expr)
    return expr


def varToForm(expr, prefix, ignorepattern = None):
    for p in prefix:
        x = findVariables(expr, p)
        if ignorepattern is not None:
            x = [i for i in x if i.find(ignorepattern) == -1]
        rep = {i:i for i in x}
        for k,v in rep.iteritems():
            expr = re.sub(r'' + k +r'([^'+ignorepattern+'])', v + r'\1', expr)
    return expr

# This seems to be unused
#def FormExprsToIDs(infile, outfile):
#    infileh = open(infile,'r')
#    tmpfileh = open(infile+".tmp", 'w')
#    for line in infileh:
#        if line.startswith("~") or "sec" in line or "FORM" in line or "#-" in line:
#             continue
#        tmpfileh.write(line);
#    tmpfileh.close();
#    infileh.close();
#    input = splitExpressions(tmpfilename)
#    outfileh = open(outfile, 'w')
#    for expr in input:
#        outfileh.write("id %s = %s;\n\n" % (expr['name'].replace("[","").replace("]",""), 
#                                   expr['value'][0][0]))
#    outfileh.close();

def FormExprsToTable(infile, outfile):
    COMPRESS_LEVEL = 1
    infileh = open(infile,'r')
    zipfileh = gzip.open(infile+".gz", 'wb', COMPRESS_LEVEL)
    tmpfilename = infile+".tmp"
    tmpfileh = open(tmpfilename, 'w')
    for line in infileh:
        zipfileh.write(line);
        if line.startswith("~") or "sec" in line or "FORM" in line or "#-" in line:
             continue
        tmpfileh.write(line);
    tmpfileh.close()
    zipfileh.close()
    infileh.close()
    os.remove(infile)
    input = splitExpressions(tmpfilename)
    os.remove(tmpfilename)
    outfileh = open(outfile, 'w')
    for expr in input:
        outfileh.write("fill %s = %s;\n\n" % (expr['name'].replace("[","").replace("]",""), 
                                   expr['value'][0][0]))
    outfileh.close();

#=====================================================================
#
# Extraction of objects
#
#=====================================================================

def uniqueSMEs(filename, smeindex):
    res = splitExpressions(filename)
    if len(res) != 1:
        raise Exception("number of expressions")
    sccs = unique([replaceVariable(x[0], prefix = ['v','cOli'], 
                                         repsuffix = [smeindex, ""],
                                         ignorepattern = 'e') 
                   for x in res[0]['value']])
    sccs = {"SME%s(%i)" % (smeindex, i):sccs[i] for i in range(len(sccs))}
    return sccs

def uniqueColors(filename, index):
    res = splitExpressions(filename)
    if len(res) != 1:
        raise Exception("number of expressions")
    colors = unique([replaceVariable(x[0], prefix = ['cOli'], repsuffix = [index], 
                                     ignorepattern = 'e')
                       for x in res[0]['value']])
    colors = {"col%s(%i)" % (index, i):colors[i] for i in range(len(colors))}

    return colors

def printIDs(filename, dict, ignore = None):
    file = open(filename, 'w')
    for name, expr in dict.iteritems():
        if not expr.isdigit(): #don't attempt to id these!
            file.write("id %s = %s;\n\n" % (varToFormPattern(expr, ['v', 'cOli'], ignorepattern = ignore), name))
    file.close()

def printExpr(filename, dict, ignore = None):
    file = open(filename, 'w')
    for name, expr in dict.iteritems():
        file.write("l [%s] = %s;\n\n" % (name, varToForm(expr, ['v', 'cOli'], ignorepattern = ignore)))
    file.close()


def runColorContractions(filename, exprlist1, exprlist2,
                         frmcmd = 'form', useOldColor = False, extFields = []):

    if useOldColor:
        print "simplifying colors ..."
        header = "#-\n#include declarations.h\noff statistics;\n\n"
        footer = "#call simplifyColor;\nprint;\n.end"
    else:
        # After runColorContractions() has been run (see genAmplitude.py),
        # no unsaturated color indices should be left anymore.
        print "amplitudeTools.py:runColorContractions: simplifying colors " + \
              "on the squared amplitude level ..."
        gExtIdList = []
        adjIdStatements = []
        for x, fld in enumerate(extFields):
            if (fld == "g"):
                print "amplitudeTools.py:runColorContractions: " + \
                      "found gluon with external id " + str(x+1)
                gExtIdList.append(x+1)
                adjIdStatements.append("id cOli"+str(x+1)+"e = cOlaie"+str(x+1)+";\n")
                adjIdStatements.append("id cOlj"+str(x+1)+"e = cOlaje"+str(x+1)+";\n")
        # NLOXSimplifyColorHeader only contains NLOXSimplifyColorDefineObjects,
        # i.e. it only contains the object declarations.
        header = """
            #-\n
            off statistics;\n
            #include NLOXSimplifyColor.h\n
            #call NLOXSimplifyColorHeader\n
            """
        footer = """
            #call NLOXSimplifyColorTranslateIndices\n
            """
        ## We out-commented NLOXSimplifyColorTranslateIndices from
        ## NLOXSimplifyColorHeader, in order to insert a special treatment for
        ## the color-index carrying delta functions, depending on whether they
        ## are adjoint indices coming from external gluons or not. The
        ## corresponding lines (see below) are also out-commented in
        ## NLOXSimplifyColorTranslateIndices, such that
        ## NLOXSimplifyColorTranslateIndices only takes explicitely care of the
        ## color-index carrying f and T matrices, for which the assignment of
        ## which indices are fundamental and which adjoint is unambiguous.
        footer += "argument;\n"
        for x in adjIdStatements:
            footer += x
        footer += "endargument;\n"
        ## Now, since the adjoint indices in the delta functions have been taken
        ## care of, we can take care of the rest of the indices, which should be
        ## only fundamental ones.
## Moved to NLOXSimplifyColorFooter; delete when checked
#        footer += """
#            argument;\n
#            #do i = 0, 30\n
#              id cOli`i'e = cOlie`i';\n
#              id cOlj`i'e = cOlje`i';\n
#            #enddo\n
#            endargument;\n
#            .sort\n
#            id delta(?X) = d_(?X);\n
#            id cOlOne = 1;\n
#            .sort\n
#            """
        ## Also, since the new diagram-level color code leaves cOlTr() objects
        ## with cOli`i'l and possibly cOli`i'r indices, etc. we need to trans-
        ## late them first: In cOlTr() all indices are adjoint.
#        footer += """
#            argument cOlTr;\n
#            #do i = 0, 30\n
#              id cOli`i'l = cOlail`i';\n
#              id cOlj`i'l = cOlajl`i';\n
#              id cOli`i'r = cOlair`i';\n
#              id cOlj`i'r = cOlajr`i';\n
#            #enddo\n
#            endargument;\n
#            .sort\n
#            """
        footer += """
            #call NLOXSimplifyColorFooter\n
            """

    file = open(filename+".frm", 'w')
    file.write(header)
    for k1,v1 in exprlist1.iteritems():
        for k2,v2 in exprlist2.iteritems():
            lnr = k1.replace("coll(","").replace(")","")
            rnr = k2.replace("colr(","").replace(")","")
            file.write("l [col(%s,%s)] = (%s)*(%s);\n\n" % (lnr,rnr, v1, v2))
    file.write(footer)
    file.close()
    runForm(filename + ".frm", filename + ".out", False, frmcmd)

def writeSMEContractions(filename,exprlist1, exprlist2):

# change to add Workspace setting by Seth
    header = "#-\n#:Workspace 1G\n#:smallsize 100M\n#:largesize 500M\n#:scratchsize 500M\n#include declarations.h\noff statistics;\n\n"
    footer = "#call computeSCContractions;\nprint;\n.end"

    file = open(filename+".frm", 'w')
    file.write(header)
    for k1,v1 in exprlist1.iteritems():
        for k2,v2 in exprlist2.iteritems():
            lnr = k1.replace("SimpSMEl(","").replace(")","")
            rnr = k2.replace("SimpSMEr(","").replace(")","")
            file.write("l [SME(%s,%s)] = (%s)*(%s);\n\n" % (lnr,rnr, v1, v2))
    file.write(footer)
    file.close()

def parwork(cmd):
    return subprocess.call(cmd, shell=True)

def runFormParallel(filename, parts, procs, defineVar=None, frmcmd = 'form'):
    pool = multiprocessing.dummy.Pool(processes=procs)
    #pool = multiprocessing.Pool(processes=procs)
    commands = []
    print "running FORM on %d parts of %s" % (parts, filename)
    for i in range(parts):
        input = "%s.part%d.frm" % (filename, (i+1))
        output = "%s.part%d.out" % (filename, (i+1))
        if defineVar is None:
            commands.append(frmcmd + " -M %s > %s" % (input, output))
        else:
            commands.append(frmcmd + " -M -d %s=%i %s > %s" % (defineVar, i, input, output))
    results = pool.map_async(parwork, commands)
    tasks = results._number_left
    print "%d parts divided into %d tasks" % (parts, tasks)
    sleepTime = 0.1
    printTime = 10
    cyclesPerPrint = printTime/sleepTime
    cyclesSincePrint = 0
    remaining = results._number_left+1 #+1 forces first print
    while True:
        if (results.ready()): break
        if (results._number_left < remaining):
            remaining = results._number_left
            print
            print "Waiting for", remaining, "/", tasks, "tasks to complete",
            cyclesSincePrint = 0
        elif (cyclesSincePrint >= cyclesPerPrint):
            sys.stdout.write(".")
            sys.stdout.flush()
            cyclesSincePrint = 0
        cyclesSincePrint += 1
        time.sleep(sleepTime)
    pool.close()

def runForm(input, output=None, deleteOnSuccess = False, frmcmd = 'form'):
    print "running FORM on %s" % input
    if output is None:
        output = "/dev/null"
    success = os.system(frmcmd + " %s > %s" % (input, output))
    if success != 0:
        raise RuntimeError("%s failed, check %s.out" % (input, output))
