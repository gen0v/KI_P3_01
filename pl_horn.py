import itertools
import copy
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

    def addRules(self,breeze):
        # breeze should always be positive in this scenario
        if breeze[0] == "S": char = "W"
        else: char = "P"
        t = [(0,-1),(-1,0),(1,0),(0,1)]
        x = int(breeze[1])
        y = int(breeze[2])
        temp,res = [],[]
        # calc the couldbe pits
        for i in t:
            new_x = i[0] + x
            new_y = i[1] + y
            if new_x >= 1 and new_x <= 4 and new_y >= 1 and new_y <= 4:
                temp.append(char + str(new_x) + str(new_y))
        r1 = "-"+breeze
        for i in temp:
            res.append(breeze+"=>"+i)
            r1 += ","+i
        print("Adding rules: " + str(res))
        for rule in res:
            self.tell(rule)

    # function to add new information to the kb
    # the sentence needs to be in cnf as we dont parse it yet
    def tell(self, sentence):
        if sentence[0] == "-" and len(sentence) == 4:
            #negative fact -> delete all rules where the fact is in the head\conclusion
            kbcopy = copy.copy(self.kb)
            for s in kbcopy:
                print(sentence[1:])
                print(self.getClauseHead(s))
                if sentence[1:] in self.getClauseHead(s):
                    print("Removing : " + s)
                    self.kb.remove(s)
        else:
            self.kb.add(sentence)

    def ask(self, alpha):
        return self.pl_fc_entails(self.kb, alpha)

 

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
                    ### ERROR here ?
                    #if len(c_premise) == 1: continue
                    
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


# Propositional Horn clauses and forward chaining to compute entailment
# pl_horn = pl()
# pl_horn.tell("B11=>P12,P21")
# pl_horn.tell("P12,P21=>B11")

# pl_horn.tell("P12=>B11")
# pl_horn.tell("P21=>B11")
# pl_horn.tell("B22,B13,B11=>P12")
# pl_horn.tell("B22,B31,B11=>P21")
# pl_horn.tell("B11")
# pl_horn.tell("B13")
# pl_horn.tell("B22")

######
# pl_horn.tell("S11=>W12")
# pl_horn.tell("S11=>W21")
# pl_horn.tell("S11")
# pl_horn.tell("-W12")
# pl_horn.tell("S21")

######


# pl_horn.tell("S11=>W12,W21")
# pl_horn.tell("S11=>W12")
# pl_horn.tell("S11=>W21")
# pl_horn.tell("W12=>S11")
# pl_horn.tell("W21=>S11")
# pl_horn.tell("S11")


# print(pl_horn.getKB())
# print("---RESOLUTION---")
# # print(pl_horn.ask("P12"))

# print(pl_horn.ask("W21"))
