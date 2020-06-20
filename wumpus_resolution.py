import gym
import fh_ac_ai_gym
import pl

# first
pl_cnf = pl.pl()

wumpus_env = gym.make('Wumpus-v0')
cartpole_env = gym.make('Fuzzy-CartPole-v0')
obs = wumpus_env.reset()
while True:
    print(obs)
    wumpus_env.render()
    while True:
        tell = input("Tell? (x/exit)(r/rules) ")
        if tell == "x": break
        elif tell == "r":
            rules = input("Rule? ")
            pl_cnf.addRules(rules)
        else: pl_cnf.tell(tell)
    while True:
        ask = input("Ask? (x/exit)  ")
        if ask == "x": break
        print(pl_cnf.ask(ask))
    while True:
        wumpus_env.render()
        ac = input("Which action? (x/exit) ")
        if ac == "x": break
        obs, reward,done, info = wumpus_env.step(int(ac))
    if done : break
print(reward)

