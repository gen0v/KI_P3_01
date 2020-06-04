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
        return self.pl_resolution(self.kb, alpha)

    def isComplementaryLiteral(self, literal, sentence):
        nl = self.negate(literal).pop()
        for l in sentence:
            if nl in sentence:
                print("Contradiction")
                return True
        return False

    def pl_resolve(self,pair):
        print("Pair: " + str(pair))
        flag = False
        l1 = pair[0].split(",")
        l2 = pair[1].split(",")
        s = list(set(l1+l2))
        print(s)
        for literal in l1:
            # if is complementary literal remove it
            if self.isComplementaryLiteral(literal,l2):
                # if flag is set then this means second complementary literal
                # -> discard
                if flag:
                    tempset = set()
                    tempset.add(pair[0])
                    return tempset
                s.remove(literal)
                s.remove(self.negate(literal).pop())
                flag = True
        if s == []:
            tempset = set(" ")
            print("test")
            return tempset
        else:
            s = ",".join(s)
            if s[0] == ",": s=s[1:]
            tempset = set()
            tempset.add(s)
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
                print(resolvents)
                if " " in resolvents: return True
                print(resolvents)
                new = new.union(resolvents)
            if new.issubset(clauses): return False
            print("Adding: ")
            print(new)
            clauses = clauses.union(new)


kb = {"-B11,P12,P21","-P12,B11","-P21,B11","-B11"}
pl = pl(kb)
# no pit in 1 2
a = "-P12"
print(a)
print(kb)

print("---RESOLUTION---")
print(pl.ask(a))
