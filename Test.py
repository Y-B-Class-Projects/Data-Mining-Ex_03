import datetime

import OurAssociationRules
import OriginalAssociationRules

OriginalAssociationRules.createfile(1000, "itemsets.txt")
print("itemsets file created\n")

t1 = datetime.datetime.now()


res1 = OurAssociationRules.minsup_itemsets("itemsets.txt", True)
t2 = datetime.datetime.now()

print([r[0] for r in res1])

Our = t2-t1
print("Our: ",Our)


t1 = datetime.datetime.now()
res2 = OriginalAssociationRules.minsup_itemsets("itemsets.txt")
t2 = datetime.datetime.now()

print(res2)

source = t2-t1
print("source: ",source)

if [r[0] for r in res1] == res2:
    print ("\nThe lists are identical")
else :
    print ("\nThe lists are not identical")

