import gym
import fh_ac_ai_gym
import pl

# first
pl_cnf = pl.pl()
#Rules Wumpus
pl_cnf.tell("-S11,W12,W21")
pl_cnf.tell("-W12,S11")
pl_cnf.tell("-W21,S11")
#Rules Pit Left
pl_cnf.tell("-B31,P41,P32")
pl_cnf.tell("-P41,B31")
pl_cnf.tell("-P32,B31")


wumpus_env = gym.make('Wumpus-v0')
cartpole_env = gym.make('Fuzzy-CartPole-v0')
obs = wumpus_env.reset()
while True:
    print(obs)
    wumpus_env.render()
    while True:
        tell = input("Tell? (x/exit)  ")
        if tell == "x": break
        pl_cnf.tell(tell)
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

