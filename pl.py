import itertools

# Propositional Logic 

class pl:
    def __init__(self, kb):
        self.kb = kb

    def negate(self, s: str):
        l = s.split(",")
        res = set()
        for i in l:
            if "-" in i:
                r = i.replace("-","")
            else:
                r = "-" + i
            res.add(r)
        return res
            
    def ask(self, alpha):
        return not self.pl_resolution(self.kb, alpha)

    # there needs to be a complementary literal so something can be derived
    def pl_resolve(self,pair):
        check = False
        print("Pair: " + str(pair))
        l1 = pair[0].split(",")
        l2 = pair[1].split(",")
        s = list(set((pair[0] + "," + pair[1]).split(",")))
        # work with sentence
        for i1 in l1:
            for i2 in l2:
                # print(set(i1) + " == " + self.negate(i2))
                if(i1 == self.negate(i2).pop()):
                    s.remove(i1)
                    s.remove(i2)
                    check = True
                    print("Contradiction")
        # create new result set
        # print(",".join(s))
        # if check fails then there was no contradiction and thus
        # nothing can be derived so we return a duplicate which will
        # be deleted because of the type set
        if(not check):
            tempset = set()
            tempset.add(pair[0])
        elif(s != []):
            s = ",".join(s)
            if s[0] == ",": s=s[1:]
            tempset = set()
            tempset.add(s)
        else:
            tempset = set(" ")
        
        print(tempset)
        print("----")
        return tempset
    
    # inputs:
    # kb = the knowledge base, a sentence in prop. logic
    # alpha = the query, a sentence in prop. logic
    def pl_resolution(self, kb, alpha) -> bool:
        clauses = kb.union(self.negate(alpha))
        new = set()
        while True:
            for pair in itertools.combinations(clauses,2):
                resolvents = self.pl_resolve(pair)
                # print(resolvents)
                if " " in resolvents: return True
                print(resolvents)
                new = new.union(resolvents)
            if new.issubset(clauses): return False
            print("Adding: ")
            print(new)
            clauses = clauses.union(new)


kb = {"-B11,P12,P21","-P12,B11","-P21,B11","B11"}
pl = pl(kb)
# no pit in 1 2
a = "-P12"
print(a)
print(kb)

print("---RESOLUTION---")
print(pl.ask(a))
