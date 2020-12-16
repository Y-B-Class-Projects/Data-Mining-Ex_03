import random
import datetime

N = 25  # no. of attributes
MINSUP = 0.15


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
    '''

    :param smallitemset:
    :type smallitemset:
    :param bigitemset:
    :type bigitemset:
    :return:
    :rtype: bool
    '''
    # print("smallitemset: ", smallitemset,"bigitemset: ",bigitemset)
    s = b = 0  # s = index of smallitemset, b = index of bigitemset
    while s < len(smallitemset) and b < len(bigitemset):
        # print("S: ", s, "B: ",b)
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
    # print("itemsets",itemsets)
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
        # print(itemsets)
        for i in range(len(itemsets)):
            if is_in(itemsets[i][0], line):
                count[i] += 1
        line = f.readline()
    f.close()
    freqitemsets = []
    All = []
    for i in range(len(itemsets)):
        if count[i] >= MINSUP * filelength:
            freqitemsets += [[itemsets[i][0], count[i] / filelength]]
        All += [[itemsets[i][0], count[i] / filelength]]
    #print("All ",[r[0] for r in All])
    return freqitemsets, All


# function to reduce items from k+1 itemsets, by checking support of k sub-items from k+1 items
def reduceFrom_K_Plus_1_Itemsets(kitemsets, kplus1_itemsets, filename):
    ret = []
    for k_plus_1_item in kplus1_itemsets:
        isAdd = True

        #print(kitemsets)
        for k_item in kitemsets:
            if is_in(k_item[0], k_plus_1_item[0]):
                if k_item[1] <= MINSUP:
                    print("B")
                    isAdd = False
                    break

        # temp_k_itemsets = [k_item for k_item in kitemsets if is_in(k_item[0], k_plus_1_item[0])]

        if isAdd:
            ret += [k_plus_1_item]

    return ret


def create_kplus1_itemsets(kitemsets, AllKitemset, filename, isImprove):
    kplus1_itemsets = []
    for i in range(len(kitemsets) - 1):
        j = i + 1  # j is an index
        # compares all pairs, without the last item, (note that the lists are sorted)
        # and if they are equal than adds the last item of kitemsets[j] to kitemsets[i]
        # in order to create k+1 itemset
        while j < len(kitemsets) and kitemsets[i][0][:-1] == kitemsets[j][0][:-1]:
            kplus1_itemsets += [[kitemsets[i][0] + [kitemsets[j][0][-1]], None]]
            j += 1
    # print(kplus1_itemsets) #################
    kplus1_itemsetsOriginal = kplus1_itemsets
    if isImprove == True:
        kplus1_itemsets = reduceFrom_K_Plus_1_Itemsets(AllKitemset, kplus1_itemsets, filename)
    # print("after: ",frequent_itemsets(filename, kplus1_itemsets,True), "be..: ", kplus1_itemsets)  #################
    # checks which of the k+1 itemsets are frequent
    return frequent_itemsets(filename, kplus1_itemsets)


def create_1itemsets(filename):
    it = []
    for i in range(N):
        it += [[[i], None]]
    return frequent_itemsets(filename, it)  # return frequent itemsets of it, and original it


def minsup_itemsets(filename, isImprove):
    k = 1
    kitemsets, AllKitemset = create_1itemsets(filename)

    minsupsets = kitemsets
    while kitemsets != []:
        # print(kitemsets)
        kitemsets, AllKitemset = create_kplus1_itemsets(kitemsets, AllKitemset, filename, isImprove)
        minsupsets += kitemsets
    return minsupsets

# createfile(10000, "itemsets.txt")


# t3 = datetime.datetime.now()

# print(minsup_itemsets("itemsets.txt" ,True))

# t4 = datetime.datetime.now()
# print("True", t4-t3)


# t1 = datetime.datetime.now()

# print(minsup_itemsets("itemsets.txt" ,False))

# t2 = datetime.datetime.now()
# print("False",t2-t1)
