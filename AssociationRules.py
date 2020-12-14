import random

N = 5  # no. of attributes
MINSUP = 0.4


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
def frequent_itemsets(filename, itemsets):
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
        if count[i] >= MINSUP * filelength:
            freqitemsets += [itemsets[i]]
    print(count) ################
    return freqitemsets


# function to reduce items from k+1 itemsets, by checking support of k sub-items from k+1 items
def reduceFrom_K_Plus_1_Itemsets(kitemsets, kplus1_itemsets, filename):
    ret = []
    for k_plus_1_item in kplus1_itemsets:
        temp_k_itemsets = []
        for k_item in kitemsets:
            if set(k_item) <= set(k_plus_1_item):
                temp_k_itemsets += [k_item]
        if len(temp_k_itemsets) == len(frequent_itemsets(filename, temp_k_itemsets)): # the frequent_itemsets will remove itmes
            # that not pass the minSupp
            ret += [k_plus_1_item]
    print(ret)  #################
    return ret


def create_kplus1_itemsets(kitemsets, kitemsetOriginal, filename):
    kplus1_itemsets = []
    for i in range(len(kitemsets) - 1):
        j = i + 1  # j is an index
        # compares all pairs, without the last item, (note that the lists are sorted)
        # and if they are equal than adds the last item of kitemsets[j] to kitemsets[i]
        # in order to create k+1 itemset
        while j < len(kitemsets) and kitemsets[i][:-1] == kitemsets[j][:-1]:
            kplus1_itemsets += [kitemsets[i] + [kitemsets[j][-1]]]
            j += 1
    print(kplus1_itemsets) #################
    kplus1_itemsetsOriginal = kplus1_itemsets
    kplus1_itemsets = reduceFrom_K_Plus_1_Itemsets(kitemsetOriginal, kplus1_itemsets, filename)
    print(frequent_itemsets(filename, kplus1_itemsets), kplus1_itemsets)  #################
    # checks which of the k+1 itemsets are frequent
    return frequent_itemsets(filename, kplus1_itemsets), kplus1_itemsetsOriginal


def create_1itemsets(filename):
    it = []
    for i in range(N):
        it += [[i]]
    return frequent_itemsets(filename, it), it  # return frequent itemsets of it, and original it


def minsup_itemsets(filename):
    minsupsets = kitemsets, kitemsetOriginal = create_1itemsets(filename)
    while kitemsets != []:
        print(kitemsets) #################
        kitemsets, kitemsetOriginal = create_kplus1_itemsets(kitemsets, kitemsetOriginal, filename)
        minsupsets += kitemsets
    return minsupsets


createfile(100, "itemsets.txt")
print(minsup_itemsets("itemsets.txt"))









