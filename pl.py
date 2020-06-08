import itertools

# Propositional Logic 

class pl:
    def __init__(self, kb = set()):
        self.kb = kb

    def getKB(self):
        return self.kb

    # function to negate a sentence/literal
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

    # function to add new information to the kb
    # the sentence needs to be in cnf as we dont parse it yet
    def tell(self, sentence):
        self.kb.add(sentence)

    def ask(self, alpha):
        return self.pl_resolution(self.kb, alpha)

    def ask_horn(self, alpha):
        return self.pl_fc_entails(self.kb, alpha)

    # function to check if there a literal has a complementary in the sentence
    def isComplementaryLiteral(self, literal, sentence):
        nl = self.negate(literal).pop()
        for l in sentence:
            if nl in sentence:
                print("Contradiction")
                return True
        return False

    # resolve algorithm
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


# CNF and pl-res as inference mechanism
pl_cnf = pl()
pl_cnf.tell("-B11,P12,P21")
pl_cnf.tell("-P12,B11")
pl_cnf.tell("-P21,B11")
pl_cnf.tell("-B11")
print(pl_cnf.getKB())
print("---RESOLUTION---")
print(pl_cnf.ask("-P12"))
