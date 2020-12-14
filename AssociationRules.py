import random
import datetime

N = 25  # no. of attributes
MINSUP = 0.1


# Creates a file named filename containing m sorted itemsets of items 0..N-1
def createfile(m, filename):
    f = open(filename, "w")
    for line in range(m):
        itemset = []
        for i in range(random.randrange(N) + 1):
            item = random.randrange(N)  # random integer 0..N-1
            if item not in itemset:
                itemset += [item]
        itemset.sort()
        for i in range(len(itemset)):
            f.write(str(itemset[i]) + " ")
        f.write("\n")
    f.close()


# Returns true iff all of smallitemset items are in bigitemset (the itemsets are sorted lists)
def is_in(smallitemset, bigitemset):
    s = b = 0  # s = index of smallitemset, b = index of bigitemset
    while s < len(smallitemset) and b < len(bigitemset):
        if smallitemset[s] > bigitemset[b]:
            b += 1
        elif smallitemset[s] < bigitemset[b]:
            return False
        else:
            s += 1
            b += 1
    return s == len(smallitemset)


# Returns a list of itemsets (from the list itemsets) that are frequent
# in the itemsets in filename
def frequent_itemsets(filename, itemsets , isRemove):
    #print("itemsets",itemsets)
    f = open(filename, "r")
    filelength = 0  # filelength is the no. of itemsets in the file. we
    # use it to calculate the support of an itemset
    count = [0] * len(itemsets)  # creates a list of counters
    line = f.readline()
    while line != "":
        filelength += 1
        line = line.split()  # splits line to separate strings
        for i in range(len(line)):
            line[i] = int(line[i])  # converts line to integers
        for i in range(len(itemsets)):
            if is_in(itemsets[i], line):
                count[i] += 1
        line = f.readline()
    f.close()
    freqitemsets = []
    for i in range(len(itemsets)):
        if count[i] >= MINSUP * filelength or isRemove == False:
            freqitemsets += [[itemsets[i], count[i]/filelength]]
    #print("ret ",freqitemsets)
    return freqitemsets


# function to reduce items from k+1 itemsets, by checking support of k sub-items from k+1 items
def reduceFrom_K_Plus_1_Itemsets(kitemsets, kplus1_itemsets, filename):
    ret = []
    for k_plus_1_item in kplus1_itemsets:
        temp_k_itemsets = []
        #print("kitemsets1: ",kitemsets)
        for k_item in kitemsets:
            #print(k_item)
            if set(k_item[0]) <= set(k_plus_1_item):
                temp_k_itemsets += [k_item]
        isAdd =True
        #print(temp_k_itemsets)
        for temp in temp_k_itemsets:
            #nt("temp: ",temp)
            if temp[1] <= MINSUP:
                isAdd = False
                #print("brake")
                break
        #if len(temp_k_itemsets) == len(frequent_itemsets(filename, temp_k_itemsets)): # the frequent_itemsets will remove itmes
            # that not pass the minSupp
        if isAdd:
            ret += [k_plus_1_item]
    #print(ret)  #################
    return ret


def create_kplus1_itemsets(kitemsets, kitemsetOriginal, filename, isImprove):
    kplus1_itemsets = []
    for i in range(len(kitemsets) - 1):
        j = i + 1  # j is an index
        # compares all pairs, without the last item, (note that the lists are sorted)
        # and if they are equal than adds the last item of kitemsets[j] to kitemsets[i]
        # in order to create k+1 itemset
        #print("kitemsets: ", kitemsets)
        while j < len(kitemsets) and kitemsets[i][0][:-1] == kitemsets[j][0][:-1]:
            kplus1_itemsets += [kitemsets[i][0] + [kitemsets[j][0][-1]]]
            j += 1
    #print(kplus1_itemsets) #################
    kplus1_itemsetsOriginal = kplus1_itemsets
    if isImprove == True:
        kplus1_itemsets = reduceFrom_K_Plus_1_Itemsets(kitemsetOriginal, kplus1_itemsets, filename)
    #(frequent_itemsets(filename, kplus1_itemsets), kplus1_itemsets)  #################
    # checks which of the k+1 itemsets are frequent
    return frequent_itemsets(filename, kplus1_itemsets, True), frequent_itemsets(filename, kplus1_itemsets, False)


def create_1itemsets(filename):
    it = []
    for i in range(N):
        it += [[i]]
    return frequent_itemsets(filename, it, True), frequent_itemsets(filename, it, False)  # return frequent itemsets of it, and original it


def minsup_itemsets(filename , isImprove):
    kitemsets, kitemsetOriginal = create_1itemsets(filename)
    minsupsets = kitemsets
    while kitemsets != []:
        kitemsets, kitemsetOriginal = create_kplus1_itemsets(kitemsets, kitemsetOriginal, filename , isImprove)
        minsupsets += kitemsets
    return minsupsets


createfile(10000, "itemsets.txt")


t3 = datetime.datetime.now()

print(minsup_itemsets("itemsets.txt" ,True))

t4 = datetime.datetime.now()
print("True", t4-t3)


t1 = datetime.datetime.now()

print(minsup_itemsets("itemsets.txt" ,False))

t2 = datetime.datetime.now()
print("False",t2-t1)














