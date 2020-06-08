import gym
import fh_ac_ai_gym

wumpus_env = gym.make('Wumpus-v0')
cartpole_env = gym.make('Fuzzy-CartPole-v0')

wumpus_env.render()