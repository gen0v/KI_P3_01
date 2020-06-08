import gym
import fh_ac_ai_gym

wumpus_env = gym.make('Wumpus-v0')
cartpole_env = gym.make('Fuzzy-CartPole-v0')
obs = wumpus_env.reset()
while True:
    print(obs)
    wumpus_env.render()
    ac = input("Which action?")
    obs, reward,done, info = wumpus_env.step(int(ac))
    # print(reward)
    if done : break

