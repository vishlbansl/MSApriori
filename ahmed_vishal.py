import sys
import os
from itertools import chain, combinations
from collections import defaultdict, OrderedDict
from optparse import OptionParser
import operator


def readInputFile(inputfile):
    "read inputfile"
    a = list()
    with open(inputfile, 'r') as file_iter:
        for line in file_iter:
            line = line.replace(" ", "")
            line = line.replace("}", "")
            line = line.replace("{", "")
            line = line.strip()
            record = set(line.split(','))
            a.append(record)
    return a


def readParamFile(paramFile):
    "Read the parameter file"
    param = OrderedDict()
    sdc = 0

    file_iter = open(paramFile, 'r')
    for line in file_iter:
        line = line.replace(" ", "")
        line = line.replace("'", "")
        line = line.strip()
        if 'MIS' in line:
            # print(line)
            key = line[line.find("(") + 1:line.find(")")]
            value = line[line.find("=") + 1:]
            param[key] = float(value)
        elif 'SDC' in line:
            # print(line)
            sdc = float(line[line.find("=") + 1:])
        elif 'cannot_be_together' in line:
            cannot = line[line.find(":") + 1:]
            tmp1 = cannot.replace("},{", "_")
            tmp2 = tmp1.replace("{","")
            tmp3 = tmp2.replace("}","")
            tmp4 = tmp3.split("_")

            s=[]
            for i in tmp4:
                tmp = i.split(",")
                ss = set()
                for j in tmp:
                    #print("j=", j)
                    ss.add(str(j))
                s.append(frozenset(ss))
            cannot = s

        elif "must-have" in line:
            tmp = line.replace("or", ",")
            must = tmp[tmp.find(":") + 1:]
            must = must.split(",")

    return param, sdc, cannot, must


def getItemSetTransactionList(data_iterator):
    "read extract the transactionList and 1-itemSet"
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = set(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(item)              # Generate 1-itemSets
    return itemSet, transactionList




def joinSet(itemSet, length):
    """Join a set with itself and returns the n-element itemsets"""
    return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])



def level2_cand_gen(FF, param, sdc, count, maxMIS, transSize):
    "generate cadidates for the 2-itemset"
    s = set(frozenset(w.split()) for w in FF)
    s2 = joinSet(s, 2)

    Cand = []
    for e in s2:
        minSup = 1
        maxSup = 0

        for r in e:
            if count[r]/float(transSize) < minSup:
                minSup = count[r]/float(transSize)
            if count[r]/float(transSize) > maxSup:
                maxSup = count[r]/float(transSize)

        if maxSup-minSup <= sdc:
            Cand.append(e)



    ## get the lowest MIS (done)
    minMIS = dict()

    for i in Cand:
        min = 1
        max = 0
        maxMISItem = 0
        for j in i:
            if param[j] < min:
                min = param[j]
            if param[j] > max:
                max = param[j]
                maxMISItem = count[j]
        minMIS[i] = min
        maxMIS[i] = maxMISItem

    return Cand, minMIS



def level_k_cand_gen(FF, param, sdc, k, count, maxMIS):
    s2 = joinSet(FF, k)

    Cand = []
    for e in s2:
        minSup = 1
        maxSup = 0
        for r in e:
            if param[r] < minSup:
                minSup = param[r]
            if param[r] > maxSup:
                maxSup = param[r]
        if maxSup-minSup <= sdc:
            Cand.append(e)


    ## get the lowest MIS
    minMIS = dict()
    for i in Cand:
        min = 1
        max = 0
        maxMISItem = 0
        for j in i:
            # print(j)
            if param[j] < min:
                min = param[j]
            if param[j] > max:
                max = param[j]
                maxMISItem = count[j]
        minMIS[i] = min
        maxMIS[i] = maxMISItem

    return Cand, minMIS




def writeOutputFile(outputFile, F, count, maxMIS):
    "Save output in the same format as requested"
    with open(outputFile, 'w') as f:
        k = []
        for key in F:
            k.append(key)
        k = sorted(k)
        for i in k:
            f.write("Frequent %d-itemsets\n\n" % i)
            for j in F[i]:
                if i == 1:
                    tmp = next(iter(j))
                    f.write("\t%d : %s \n" % (count[tmp], j))
                else:
                    f.write("\t%d : %s \n" % (count[j], set(j)))
                    if i != 1:
                        # TODO: extract the correct tail
                        #end = "10"
                        f.write("Tailcount = %d \n" % maxMIS[j])

            f.write("\n\tTotal number of frequent %d-itemsets = %d \n" % (i, len(F[i])))
            f.write("\n\n")




def MSApriori (fileData, parameters, sdc, cannot, must):
    "MSApriori algorithm"
    one, trans = getItemSetTransactionList(fileData)
    sorted_items = sorted(parameters.items(), key=operator.itemgetter(1))
    transSize = len(trans)

    print("Working on 1 itemset ......")
    ## construct the M
    M =[]
    for i in (sorted_items):
        M.append(i[0])



    ## get the count
    count=defaultdict(int)
    for item in M:
        for transaction in trans:
            m=set(item.split(','))
            if m.issubset(transaction):
                count[item] += 1


    ## Initial pass
    L=[]
    start = 0
    pivot = 0
    for i in M:
        if count[i]/float(len(trans)) >= parameters[i] and start == 0:
            L.append(i)
            start = 1
            pivot = parameters[i]
        elif count[i]/float(len(trans))  >= pivot and start == 1:
            L.append(i)

    ## select the 1-frequentset
    F = dict()
    F_local = []
    for i in L:
        if count[i] / float(len(trans))  >= parameters[i]:
            F_local.append(set(i.split()))


    ### Check constrains
    m = []
    for i in must:
        m.append(set(i.split()))

    remain = []
    for i in F_local:
        if i in m:
            remain.append(i)
    F[1] = remain



    ### for the rest of set-size
    k = 2
    maxMIS = dict()
    while(len(F[k-1]) != 0):
        print("Working on",k,"itemset ......")
        if(k==2):
            C, minMIS = level2_cand_gen(L, parameters, sdc, count, maxMIS, transSize)
        else:
            C, minMIS = level_k_cand_gen(F[k - 1], parameters, sdc, k, count, maxMIS)



        ## Get the count
        for item in C:
            for transaction in trans:
                if item.issubset(transaction):
                    count[item] += 1

        ## Select the items fro the k-frequent itemset
        F_local = []
        for item in C:
            if count[item] / float(len(trans))  >= minMIS[item]:#parameters[list(item)[0]]:
                F_local.append(item)


        ##### Check constrains
        remain = []
        for i in F_local:
            trigger = 0
            for j in cannot:
                if j.issubset(i):
                    trigger = 1
                    break
            if trigger == 0:
                remain.append(i)

        ## Save the k-frequent itemset
        F[k] = remain
        k+=1


    del(F[k-1])
    return F, count, maxMIS



if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-i', '--inputFile',
                         dest='input',
                         help='filename containing transactions',
                         default=None)
    optparser.add_option('-p', '--paramFile',
                         dest='param',
                         help='filename containing parameters',
                         default=None)
    optparser.add_option('-o', '--outputFile',
                         dest='out',
                         help='name of the outputfile',
                         default="MSAprioriOutput.txt",
                         type='string')

    (options, args) = optparser.parse_args()

    inputFile = None
    if options.input is not None:
            inputFile = options.input
    else:
            print('No input filename specified, system with exit\n')
            sys.exit('System will exit')

    paramFile = None
    if options.param is not None:
        paramFile = options.param
    else:
        print('No input filename specified, system with exit\n')
        sys.exit('System will exit')

    outFile = options.out

    print("inputFile = ", inputFile, "    paramFile = ", paramFile, "    outFile = ", outFile)
    fileData = readInputFile(inputFile)
    parameters, sdc, cannot, must = readParamFile(paramFile)


    F, count, maxMIS = MSApriori(fileData, parameters, sdc, cannot, must)

    ### Create the outputfile
    writeOutputFile(outFile, F, count, maxMIS)
    print("\n DONE \n")