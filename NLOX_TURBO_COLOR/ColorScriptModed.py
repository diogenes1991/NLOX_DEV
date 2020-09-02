

import amplitudeTools as aTools


def UniqueChains(seq):
    seen = [] 
    for item in seq:
        chain = item['value'][0][0]
        NewChain = ''
        record = 0
        for i in chain:
            if i == 'C' or i== 'c': record = 1
            if(record==1): NewChain += i
        if NewChain in seen: continue
        if (len(NewChain)): seen.append(NewChain)
    return seen

def UniqueChainsReplaced(RawFile):
    
    aTools.runForm(RawFile,'PreProcColor.out',False,'form')
    OriginalExpressions = aTools.splitExpressions(RawFile)
    
    UniqueChainsFile = "UniqueChains.frm"
    UCF = open(UniqueChainsFile,"w")
    
    ColorProductsUniqueChains = 'ColorProductsUniqueChains.id.frm'
    UCRF = open(ColorProductsUniqueChains,"w")
    
    ### Global Header 
    Header  = '#-\n'+'off statistics;\n'
    Header += '#include TopologicalColor.h\n'
    Header += '#include NLOXSimplifyColor.h\n'
    Header += '#call NLOXSimplifyColorHeader\n'
    Header += '#call DefineTopologies\n'
    UCF.write(Header)
    UCRFHeader = Header
    ###
    
    UCRFBody = ''
    Expressions = aTools.splitExpressions('PreProcColor.out')
    seen = {}
    ChainCount = 0
    for Term in Expressions:
        UCRFBody += 'l '+Term['name'] + ' = '
        Chain = Term['value'][0][0]
        NewChain = ''
        Prefactor = ''
        record = 0
        for i in Chain:
            if i == 'F' or 'T': 
                record = 1
            if(record==1): 
                NewChain += i
            else:
                Prefactor += i
        InvPrefactor = Prefactor.replace('*','')
        if(len(Prefactor)==0):
            InvPrefactor = '1'
        if(InvPrefactor=='- '): InvPrefactor = '-1'
        UCRFBody += Prefactor 
        #UCRF.write(UCRFLine)
        if NewChain in seen.keys():
            UCRFBody += seen[NewChain] + ';\n'
            #UCRF.write(UCRFLine)
            continue
        if (len(NewChain)):
            ChainCount +=1
            res = next((sub for sub in OriginalExpressions if sub['name'] == Term['name']), None)
            UCFLine  = 'l [UC('+str(ChainCount)+')] = ('+res['value'][0][0]+')/('+InvPrefactor+');\n'
            UCFLine += '*l [UC('+str(ChainCount)+')] = '+NewChain+';\n\n'
            UCF.write(UCFLine)
            seen[NewChain] = 'UC('+str(ChainCount)+')'
            
            UCRFBody += seen[NewChain]
            #UCRF.write(UCRFLine)
        #UCRF.write(';\n')
        UCRFBody += ';\n'
    
    print "Color preprocessing has reduced from",len(Expressions),"color expressions to",len(seen)    
    UCRFHeader  += 'Table, sparse, UC(1);\n'
    UCRFHeader  += '#include FillUniqueChains.id\n'
    UCRF.write(UCRFHeader)
    UCRF.write(UCRFBody)
    UCRFLine = '#call NLOXSimplifyColorPrintEnd\n'
    UCRF.write(UCRFLine)
    
    UCFLine = ''
    UCFLine += '#call NLOXSimplifyColorTranslateIndices \n'
    UCFLine += '#call NLOXSimplifyColorFooter \n'
    UCFLine += '#call NLOXSimplifyColorPrintEnd\n'
    UCF.write(UCFLine)
    UCF.close()
    UCRF.close()

UniqueChainsReplaced('ColorProducts.id.frm')
aTools.runForm('UniqueChains.frm','UniqueChains.frm.out',False,'form')
aTools.FormExprsToTable('UniqueChains.frm.out','FillUniqueChains.id')
aTools.runForm('ColorProductsUniqueChains.id.frm','ColorProductsUniqueChains.id.frm.out',False,'form')

