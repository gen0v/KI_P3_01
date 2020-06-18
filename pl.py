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

    # function to check if there a literal has a complementary in the sentence
    def isComplementaryLiteral(self, literal, sentence):
        nl = self.negate(literal).pop()
        for l in sentence:
            if nl in sentence:
                # print("Contradiction")
                return True
        return False

    def addRules(self,breeze):
        # breeze should always be positive in this scenario
        if breeze[0] == "S": char = "W"
        elif breeze[0] == "W": char = "S"
        elif breeze[0] == "P": char = "B"
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
            res.append(breeze+","+"-"+i)
            r1 += ","+i
        res.append(r1)
        print("Adding rules: " + str(res))
        for rule in res:
            self.tell(rule)

    # resolve algorithm
    def pl_resolve(self,pair):
        # print("Pair: " + str(pair))
        flag = False
        l1 = pair[0].split(",")
        l2 = pair[1].split(",")
        s = list(set(l1+l2))
        # print(s)
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
        elif flag == False:
            tempset = set()
            tempset.add(pair[0])
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
                # print(resolvents)
                if " " in resolvents: return True
                # print(resolvents)
                new = new.union(resolvents)
            if new.issubset(clauses): return False
            # print("Adding: ")
            # print(new)
            clauses = clauses.union(new)

#######################################################3
# CNF and pl-res as inference mechanism
# pl_cnf = pl()
# pl_cnf.tell("-B11,P12,P21")
# pl_cnf.tell("-P12,B11")
# pl_cnf.tell("-P21,B11")
# pl_cnf.tell("-B11")
# print(pl_cnf.getKB())
# print("---RESOLUTION---")
# print(pl_cnf.ask("-P12"))
#######################################################3
# CNF and pl-res as inference mechanism
# pl_cnf = pl()

# pl_cnf.tell("-B12")
# pl_cnf.tell("-P12")
# pl_cnf.tell("-B14")
# pl_cnf.tell("-P14")
# # pl_cnf.tell("-B34")
# # pl_cnf.tell("-P34")
# # pl_cnf.tell("-B32")
# # pl_cnf.tell("-P32")

# pl_cnf.tell("B13")
# pl_cnf.tell("-P13")
# # pl_cnf.tell("B24")
# # pl_cnf.tell("-P24")
# # pl_cnf.tell("B22")
# # pl_cnf.tell("-P22")
# # pl_cnf.tell("B33")
# # pl_cnf.tell("-P33")

# pl_cnf.addRules("B13")
# # pl_cnf.addRules("B24")
# # pl_cnf.addRules("B33")
# # pl_cnf.addRules("B22")

# print(pl_cnf.getKB())
# print("---RESOLUTION---")
# print(pl_cnf.ask("P23"))
