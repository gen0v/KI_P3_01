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

    # inputs :
    # kb = knowledge base, a set of propositional definite clauses
    # q = query, a proposition symbol
    def pl_fc_entails(self, kb, q):
        # count, a table where count[c] is the number of symbols in c`s premise
        # inferred, a table where inferred[s] is initially false for all symbols
        # agenda, a queue of symbols, initially symbols known to be true in kb
        count = {}
        agenda = []
        inferred = {}
        for l in kb:
            # if there is no "," or "=>" then it is a fact
            if "," not in l and "=>" not in l: 
                agenda.insert(0,l)
                # add key = false to inferred
                inferred[l] = False
            else:
                for s in self.getClauseHead(l):
                    inferred[s] = False
                for s in self.getClauseBody(l):
                    inferred[s] = False
            # count the symbols in the premise
            count[l] = len((l.split("=>")[0].split(",")))

        while len(agenda) > 0:
            print("--------------")
            print("Count: " + str(count))
            print("Agenda: " + str(agenda))
            print("Inferred: " + str(inferred))
            p = agenda.pop()
            print("P: " + str(p))
            if p == q: return True
            if inferred[p] == False:
                inferred[p] = True
                for c in kb:
                    c_premise = c.split("=>")[0].split(",")
                    if len(c_premise) == 1: continue
                    print("C: " + str(c))
                    if p in c_premise:
                        print("C2: " + str(c))
                        print(count)
                        count[str(c)] -= 1
                        if count[str(c)] == 0: 
                            print("New agenda")
                            agenda += self.getClauseHead(c)
                            print(agenda)
                            print("+++++++++")
        return False

    def getClauseHead(self, clause):
        print(clause)
        if "=>" in clause:
            res = clause.split("=>")
            print(res)
            res = res[1].split(',')
            print(res)
        else:
            res = clause.split(",")
        print(res)
        return res
    
    def getClauseBody(self, clause):
        if "=>" in clause:
            res = clause.split("=>")
            res = res[0].split(',')
        else:
            res = clause.split(",")
        return res
# kb = {"-B11,P12,P21","-P12,B11","-P21,B11","-B11"}
# pl = pl(kb)
# no pit in 1 2
# a = "P12"

# CNF and pl-res as inference mechanism
"""
pl_cnf = pl()
pl_cnf.tell("-B11,P12,P21")
pl_cnf.tell("-P12,B11")
pl_cnf.tell("-P21,B11")
pl_cnf.tell("-B11")
print(pl_cnf.getKB())
print("---RESOLUTION---")
print(pl_cnf.ask("-P12"))
"""

# Propositional Horn clauses and forward chaining to compute entailment
pl_horn = pl()
# pl_horn.tell("B11=>P12,P21")
# pl_horn.tell("P12,P21=>B11")
pl_horn.tell("P12=>B11")
pl_horn.tell("P21=>B11")
pl_horn.tell("B22,B13,B11=>P12")
pl_horn.tell("B22,B31,B11=>P21")
pl_horn.tell("B11")
pl_horn.tell("B13")
pl_horn.tell("B22")

print(pl_horn.getKB())
print("---RESOLUTION---")
print(pl_horn.ask_horn("P12"))
