import sys

import gym
from elegantrl2.env import PreprocessEnv, PreprocessVecEnv
from elegantrl2.run import Arguments, train_and_evaluate, train_and_evaluate_mp

gym.logger.set_level(40)  # Block warning: 'WARN: Box bound precision lowered by casting to float32'

"""[ElegantRL](https://github.com/AI4Finance-LLC/ElegantRL)"""


def demo_discrete_action_off_policy():
    args = Arguments()
    from elegantrl2.agent import AgentDoubleDQN  # AgentDQN
    args.agent = AgentDoubleDQN()

    '''choose environment'''
    if_train_cart_pole = 0
    if if_train_cart_pole:
        "TotalStep: 5e4, TargetReward: 200, UsedTime: 60s"
        args.env = PreprocessEnv(env='CartPole-v0')
        args.net_dim = 2 ** 7
        args.target_step = args.env.max_step * 2

    if_train_lunar_lander = 1
    if if_train_lunar_lander:
        "TotalStep: 2e5, TargetReturn: 200, UsedTime: 400s, LunarLander-v2, PPO"
        args.env = PreprocessEnv(env=gym.make('LunarLander-v2'))
        args.net_dim = 2 ** 8
        args.batch_size = args.net_dim

    '''train and evaluate'''
    train_and_evaluate(args)


def demo_discrete_action_on_policy():
    args = Arguments(if_on_policy=True)  # hyper-parameters of on-policy is different from off-policy
    from elegantrl2.agent import AgentDiscretePPO
    args.agent = AgentDiscretePPO()

    '''choose environment'''
    if_train_cart_pole = 0
    if if_train_cart_pole:
        "TotalStep: 5e4, TargetReward: 200, UsedTime: 60s"
        args.env = PreprocessEnv(env='CartPole-v0')
        args.net_dim = 2 ** 7
        args.batch_size = args.net_dim * 2
        args.repeat_times = 2 ** 4
        args.target_step = args.env.max_step * 8
        args.if_per_or_gae = True

    if_train_lunar_lander = 1
    if if_train_lunar_lander:
        "TotalStep: 2e5, TargetReturn: 200, UsedTime: 400s, LunarLander-v2, PPO"
        args.env = PreprocessEnv(env=gym.make('LunarLander-v2'))
        args.agent.cri_target = False
        args.reward_scale = 2 ** -1
        args.net_dim = 2 ** 8
        args.batch_size = args.net_dim * 4
        args.target_step = args.env.max_step * 4
        args.repeat_times = 2 ** 5
        args.if_per_or_gae = True

    '''train and evaluate'''
    train_and_evaluate(args)


def demo_continuous_action_off_policy():
    args = Arguments()
    args.gpu_id = sys.argv[-1][-4]

    from elegantrl2.agent import AgentSAC  # AgentDDPG AgentTD3
    args.agent = AgentSAC()

    '''choose environment'''
    if_train_pendulum = 1
    if if_train_pendulum:
        "TotalStep: 4e5, TargetReward: -200, UsedTime: 400s"
        env = gym.make('Pendulum-v0')
        env.target_return = -200  # set target_reward manually for env 'Pendulum-v0'
        args.env = PreprocessEnv(env=env)
        args.reward_scale = 2 ** -3  # RewardRange: -1800 < -200 < -50 < 0
        args.net_dim = 2 ** 7
        args.batch_size = args.net_dim
        args.target_step = args.env.max_step * 4

    if_train_lunar_lander = 0
    if if_train_lunar_lander:
        "TotalStep: 4e5, TargetReward: 200, UsedTime: 900s"
        args.env = PreprocessEnv(env=gym.make('LunarLanderContinuous-v2'))
        args.reward_scale = 2 ** 0  # RewardRange: -800 < -200 < 200 < 302

    if_train_bipedal_walker = 0
    if if_train_bipedal_walker:
        "TotalStep: 8e5, TargetReward: 300, UsedTime: 1800s"
        args.env = PreprocessEnv(env=gym.make('BipedalWalker-v3'))
        args.reward_scale = 2 ** 0  # RewardRange: -200 < -150 < 300 < 334
        args.gamma = 0.97
        args.if_per_or_gae = True

    '''train and evaluate'''
    train_and_evaluate(args)


def demo_continuous_action_on_policy():
    args = Arguments(if_on_policy=True)  # hyper-parameters of on-policy is different from off-policy
    from elegantrl2.agent import AgentPPO
    args.agent = AgentPPO()
    args.agent.cri_target = True

    '''choose environment'''
    if_train_pendulum = 0
    if if_train_pendulum:
        "TotalStep: 4e5, TargetReward: -200, UsedTime: 400s"
        env = gym.make('Pendulum-v0')
        env.target_return = -200  # set target_reward manually for env 'Pendulum-v0'
        args.env = PreprocessEnv(env=env)
        args.reward_scale = 2 ** -3  # RewardRange: -1800 < -200 < -50 < 0
        args.net_dim = 2 ** 7
        args.batch_size = args.net_dim * 2
        args.target_step = args.env.max_step * 16

    if_train_lunar_lander = 0
    if if_train_lunar_lander:
        "TotalStep: 4e5, TargetReward: 200, UsedTime: 900s"
        args.env = PreprocessEnv(env=gym.make('LunarLanderContinuous-v2'))
        args.reward_scale = 2 ** 0  # RewardRange: -800 < -200 < 200 < 302

    if_train_bipedal_walker = 1
    if if_train_bipedal_walker:
        "TotalStep: 8e5, TargetReward: 300, UsedTime: 1800s"
        args.env = PreprocessEnv(env=gym.make('BipedalWalker-v3'))
        args.reward_scale = 2 ** 0  # RewardRange: -200 < -150 < 300 < 334
        args.gamma = 0.97
        args.if_per_or_gae = True
        # args.agent.lambda_entropy = 0.05

    '''train and evaluate'''
    train_and_evaluate(args)


# '''old'''
#
#
# def demo2_continuous_action_off_policy():
#     args = Arguments(if_on_policy=False)
#     args.random_seed = 564217
#
#     '''choose an DRL algorithm'''
#     from elegantrl2.agent import AgentModSAC  # AgentSAC, AgentTD3, AgentDDPG
#     args.agent = AgentModSAC()
#
#     '''choose environment'''
#     "TotalStep: 3e4, TargetReturn: -200, UsedTime: 300s, Pendulum-v0, TD3"
#     "TotalStep: 2e4, TargetReturn: -200, UsedTime: 200s, Pendulum-v0, ModSAC "
#     "1   4.72e+04   -200.00 | -182.72    153.37        432  ########"
#     # env = gym.make('Pendulum-v0')
#     # env.target_return = -200  # set target_return manually for env 'Pendulum-v0'
#     # args.env = PreprocessEnv(env=env)
#     #
#     # args.reward_scale = 2 ** -3  # RewardRange: -1800 < -200 < -50 < 0
#     # args.net_dim = 2 ** 7
#     # args.batch_size = 2 ** 7
#     # args.target_step = args.env.max_step * 4
#     # args.eval_gap = 2 ** 6
#     # args.eval_times1 = 2 ** 4
#     # args.eval_times2 = 2 ** 5
#     # args.break_step = int(2e5)
#     # args.if_allow_break = False
#
#     "TD3    TotalStep:  9e4, TargetReturn: 100, UsedTime: 3ks, LunarLanderContinuous-v2"
#     "TD3    TotalStep: 20e4, TargetReturn: 200, UsedTime: 5ks, LunarLanderContinuous-v2"
#     "SAC    TotalStep:  9e4, TargetReturn: 200, UsedTime: 3ks, LunarLanderContinuous-v2"
#     "ModSAC TotalStep:  5e4, TargetReturn: 200, UsedTime: 1ks, LunarLanderContinuous-v2"
#     # args.env = PreprocessEnv(env=gym.make('LunarLanderContinuous-v2'))
#     # args.reward_scale = 2 ** 0  # RewardRange: -800 < -200 < 200 < 302
#     # args.eval_times2 = 2 ** 4  # set a large eval_times to get a precise learning curve
#
#     "ModSAC TotalStep: 2e5, TargetReturn: 300, UsedTime: 5000s, BipedalWalker-v3"
#     # 1   8.28e+05    300.00 |  319.08      0.42       2448  ########
#     args.env = PreprocessEnv(env=gym.make('BipedalWalker-v3'))
#     args.env.max_step = 2 ** 10
#     args.agent.if_use_dn = True
#
#     args.reward_scale = 2 ** 0  # RewardRange: -200 < -150 < 300 < 334
#     args.net_dim = 2 ** 8
#     args.target_step = args.env.max_step
#     args.if_allow_break = True  # allow break training when reach goal (early termination)
#     args.rollout_num = 1
#     args.gpu_ids = [2, 3]  # todo beta3
#     # args.gpu_ids = [0, 1]
#     # args.gpu_ids = [0, 1, 2, 3]
#     args.break_step = int(2e5 * 8) * len(args.gpu_ids)  # break training after 'total_step > break_step'
#     args.eval_gap = 2 ** 7
#
#     '''train and evaluate'''
#     # train_and_evaluate(args)
#     train_and_evaluate_mp(args)
#
#     "TotalStep:  3e5, TargetReward: 1500, UsedTime:  4ks, AntBulletEnv-v0 ModSAC"
#     "TotalStep:  4e5, TargetReward: 2500, UsedTime:  6ks, AntBulletEnv-v0 ModSAC"
#     "TotalStep: 16e5, TargetReward: 3247, UsedTime: 90ks, AntBulletEnv-v0 ModSAC"
#     "TotalStep:  3e5, TargetReward: 1500, UsedTime:  4ks, AntBulletEnv-v0 ModSAC"
#     "TotalStep:  5e5, TargetReward: 2500, UsedTime: 12ks, AntBulletEnv-v0 ModSAC"
#     "TotalStep: 16e5, TargetReward: 3150, UsedTime:130ks, AntBulletEnv-v0 ModSAC sample_times = 2"
#     # import pybullet_envs
#     # dir(pybullet_envs)
#     # args.env = PreprocessEnv(env=gym.make('AntBulletEnv-v0'))
#     # args.break_step = int(6e5 * 8)  # (5e5) 1e6, UsedTime: (15,000s) 30,000s
#     # args.if_allow_break = False
#     # args.reward_scale = 2 ** -2  # RewardRange: -50 < 0 < 2500 < 3340
#     # args.max_memo = 2 ** 21
#     # args.batch_size = 2 ** 9
#     # args.target_step = args.env.max_step
#     # args.repeat_times = 2 ** 1
#     # args.eval_gap = 2 ** 9  # for Recorder
#     # args.eva_size1 = 2 ** 1  # for Recorder
#     # args.eva_size2 = 2 ** 3  # for Recorder
#     # # args.gpu_ids = [2, 3]
#     # # args.gpu_ids = [0, 1]
#     # args.gpu_ids = [0, 1, 2, 3]
#     #
#     # # train_and_evaluate(args)
#     # args.rollout_num = 2
#     # train_and_evaluate_mp(args)
#
#
# def demo2_continuous_action_on_policy():
#     args = Arguments(if_on_policy=True)  # hyper-parameters of on-policy is different from off-policy
#     args.random_seed = 1943
#
#     '''choose an DRL algorithm'''
#     from elegantrl2.agent import AgentPPO  # AgentPPO AgentSharedPPO
#     args.agent = AgentPPO()
#     args.agent.if_use_gae = True
#     args.agent.learning_rate = 1e-5
#
#     '''choose environment'''
#     "TotalStep: 2e5, TargetReturn: -200, UsedTime: 300s, PPO"
#     # env = PreprocessEnv(env=gym.make('Pendulum-v0'))
#     # env.target_return = -200  # set target_return manually for env 'Pendulum-v0'
#     # args.env = env
#     #
#     # args.net_dim = 2 ** 8
#     # args.batch_size = args.net_dim * 2
#     # args.target_step = args.env.max_step * 16  # max_step=200
#     # args.repeat_times = 2 ** 4
#     # args.reward_scale = 2 ** -4
#     #
#     # args.eval_gap = 2 ** 4
#     # args.eval_times1 = 2 ** 3
#     # args.eval_times2 = 2 ** 5
#     # args.break_step = int(4e4 * 8)
#
#     "PPO    TotalStep: 8e5, TargetReturn: 300, UsedTime: 1800s, BipedalWalker-v3"
#     args.env = PreprocessEnv(env=gym.make('BipedalWalker-v3'))
#     args.reward_scale = 2 ** 0  # RewardRange: -200 < -150 < 300 < 334
#     args.gamma = 0.96
#     args.gpu_ids = [0, 1, 2, 3]
#     args.gpu_ids = [0, 1]
#     # 2   2.23e+06    295.94 |  290.09      1.67      -0.59      0.26 |  1091    26
#     # | SavedDir: ./AgentPPO/BipedalWalker-v3_3
#     # | UsedTime: 3365
#     args.target_step = args.env.max_step * 4
#     args.break_step = int(8e5 * 16 * len(args.gpu_ids))
#
#     '''train and evaluate'''
#     # train_and_evaluate(args)
#     args.rollout_num = 2
#     train_and_evaluate_mp(args)


# '''old'''
#
#
# def demo1_discrete_action_space():
#     args = Arguments(agent=None, env=None, gpu_id=None)  # see Arguments() to see hyper-parameters
#
#     '''choose an DRL algorithm'''
#     # from elegantrl2.agent import AgentD3QN  # AgentDQN,AgentDuelDQN, AgentDoubleDQN,
#     # args.agent = AgentD3QN()
#     from elegantrl2.agent import AgentDuelDQN  # AgentDQN,AgentDuelDQN, AgentDoubleDQN,
#     args.agent = AgentDuelDQN()
#
#     '''choose environment'''
#     "TotalStep: 2e3, TargetReturn: 200, UsedTime: 20s, CartPole-v0"
#     "TotalStep: 2e3, TargetReturn: 200, UsedTime: 30s, CartPole-v0 rollout_num = 2"
#     # args.env = PreprocessEnv(env=gym.make('CartPole-v0'))
#     # args.net_dim = 2 ** 7  # change a default hyper-parameters
#     # args.batch_size = 2 ** 7
#     # args.target_step = 2 ** 8
#     # args.eval_gap = 2 ** 0
#
#     "TotalStep: 6e4, TargetReturn: 200, UsedTime: 600s, LunarLander-v2, D3DQN"
#     "TotalStep: 4e4, TargetReturn: 200, UsedTime: 600s, LunarLander-v2, DuelDQN"
#     args.env = PreprocessEnv(env=gym.make('LunarLander-v2'))
#     args.net_dim = 2 ** 8
#     args.batch_size = 2 ** 8
#
#     '''train and evaluate'''
#     train_and_evaluate(args)
#     # args.rollout_num = 2
#     # train_and_evaluate_mp(args)
#
#
# def demo2_continuous_action_space_off_policy():
#     args = Arguments(if_on_policy=False)
#
#     '''choose an DRL algorithm'''
#     from elegantrl2.agent import AgentModSAC  # AgentSAC, AgentTD3, AgentDDPG
#     args.agent = AgentModSAC()
#
#     '''choose environment'''
#     "TotalStep: 3e4, TargetReturn: -200, UsedTime: 300s, Pendulum-v0, TD3"
#     "TotalStep: 2e4, TargetReturn: -200, UsedTime: 200s, Pendulum-v0, ModSAC "
#     env = gym.make('Pendulum-v0')
#     env.target_return = -200  # set target_return manually for env 'Pendulum-v0'
#     args.env = PreprocessEnv(env=env)
#     args.reward_scale = 2 ** -3  # RewardRange: -1800 < -200 < -50 < 0
#
#     "TD3    TotalStep:  9e4, TargetReturn: 100, UsedTime: 3ks, LunarLanderContinuous-v2"
#     "TD3    TotalStep: 20e4, TargetReturn: 200, UsedTime: 5ks, LunarLanderContinuous-v2"
#     "SAC    TotalStep:  9e4, TargetReturn: 200, UsedTime: 3ks, LunarLanderContinuous-v2"
#     "ModSAC TotalStep:  5e4, TargetReturn: 200, UsedTime: 1ks, LunarLanderContinuous-v2"
#     # args.env = PreprocessEnv(env=gym.make('LunarLanderContinuous-v2'))
#     # args.reward_scale = 2 ** 0  # RewardRange: -800 < -200 < 200 < 302
#     # args.eval_times2 = 2 ** 4  # set a large eval_times to get a precise learning curve
#
#     "ModSAC TotalStep: 2e5, TargetReturn: 300, UsedTime: 5000s, BipedalWalker-v3"
#     # args.env = PreprocessEnv(env=gym.make('BipedalWalker-v3'))
#     # args.reward_scale = 2 ** 0  # RewardRange: -200 < -150 < 300 < 334
#     # args.net_dim = 2 ** 8
#     # args.break_step = int(2e5)
#     # args.if_allow_break = True  # allow break training when reach goal (early termination)
#     # args.break_step = int(2e5 * 4)  # break training after 'total_step > break_step'
#
#     '''train and evaluate'''
#     train_and_evaluate(args)
#     # args.rollout_num = 4
#     # train_and_evaluate_mp(args)
#

# def demo2_continuous_action_space_on_policy():
#     args = Arguments(if_on_policy=True)  # hyper-parameters of on-policy is different from off-policy
#     args.random_seed = 1943
#
#     '''choose an DRL algorithm'''
#     from elegantrl2.agent import AgentPPO
#     args.agent = AgentPPO()
#     args.agent.if_use_gae = False
#
#     '''choose environment'''
#     "TotalStep: 2e5, TargetReturn: -200, UsedTime: 300s, Pendulum-v0, PPO"
#     args.env = PreprocessEnv(env=gym.make('Pendulum-v0'))
#     args.env.target_return = -200  # set target_return manually for env 'Pendulum-v0'
#     args.reward_scale = 2 ** -6  # RewardRange: -1800 < -200 < -50 < 0
#     args.net_dim = 2 ** 8
#     args.batch_size = 2 ** 8
#     args.target_step = args.env.max_step * 16  # max_step=200
#     args.repeat_times = 2 ** 4
#     args.eval_gap = 2 ** 4
#
#     "PPO    TotalStep: 8e5, TargetReturn: 200, UsedTime: 1500s, LunarLanderContinuous-v2"
#     # args.env = PreprocessEnv(env=gym.make('LunarLanderContinuous-v2'))
#     # args.reward_scale = 2 ** 0  # RewardRange: -800 < -200 < 200 < 302
#
#     "PPO    TotalStep: 8e5, TargetReturn: 300, UsedTime: 1800s, BipedalWalker-v3"
#     # args.env = PreprocessEnv(env=gym.make('BipedalWalker-v3'))
#     # args.reward_scale = 2 ** 0  # RewardRange: -200 < -150 < 300 < 334
#     # args.gamma = 0.96
#
#     '''train and evaluate'''
#     # train_and_evaluate(args)
#     args.rollout_num = 2
#     train_and_evaluate_mp(args)
#
#
# def demo3_custom_env_fin_rl():
#     from elegantrl2.agent import AgentPPO
#
#     '''choose an DRL algorithm'''
#     args = Arguments(if_on_policy=True)
#     args.agent = AgentPPO()
#     args.agent.if_use_gae = True
#     args.agent.lambda_entropy = 0.04
#
#     "TotalStep: 10e4, TargetReturn: 3.0, UsedTime:  200s, FinanceStock-v1"
#     "TotalStep: 20e4, TargetReturn: 4.0, UsedTime:  400s, FinanceStock-v1"
#     "TotalStep: 30e4, TargetReturn: 4.2, UsedTime:  600s, FinanceStock-v1"
#     from envs.FinRL.StockTrading import StockTradingEnv
#     gamma = 0.995
#     args.env = StockTradingEnv(if_eval=False, gamma=gamma)
#     args.env_eval = StockTradingEnv(if_eval=True, gamma=gamma)
#
#     args.gamma = gamma
#     args.break_step = int(3e5)
#     args.net_dim = 2 ** 9
#     args.max_step = args.env.max_step
#     args.max_memo = args.max_step * 4
#     args.batch_size = 2 ** 10
#     args.repeat_times = 2 ** 3
#     args.eval_gap = 2 ** 4
#     args.eval_times1 = 2 ** 3
#     args.eval_times2 = 2 ** 5
#     args.if_allow_break = False
#
#     '''train and evaluate'''
#     # train_and_evaluate(args)
#     args.rollout_num = 4
#     train_and_evaluate_mp(args)
#
#
# def demo4_bullet_mujoco_off_policy():
#     args = Arguments(if_on_policy=False)
#     args.random_seed = 10086
#
#     from elegantrl2.agent import AgentModSAC  # AgentSAC, AgentTD3, AgentDDPG
#     args.agent = AgentModSAC()  # AgentSAC(), AgentTD3(), AgentDDPG()
#     args.agent.if_use_dn = True
#
#     import pybullet_envs  # for python-bullet-gym
#     dir(pybullet_envs)
#
#     "TotalStep:  5e4, TargetReturn: 18, UsedTime: 1100s, ReacherBulletEnv-v0"
#     "TotalStep: 30e4, TargetReturn: 25, UsedTime:     s, ReacherBulletEnv-v0"
#     args.env = PreprocessEnv(gym.make('ReacherBulletEnv-v0'))
#     args.env.max_step = 2 ** 10  # important, default env.max_step=150
#     args.reward_scale = 2 ** 0  # -80 < -30 < 18 < 28
#     args.gamma = 0.96
#     args.break_step = int(6e4 * 8)  # (4e4) 8e5, UsedTime: (300s) 700s
#     args.eval_times1 = 2 ** 2
#     args.eval_times1 = 2 ** 5
#     args.if_per = True
#
#     train_and_evaluate(args)
#
#     "TotalStep:  3e5, TargetReward: 1500, UsedTime:  4ks, AntBulletEnv-v0 ModSAC"
#     "TotalStep:  4e5, TargetReward: 2500, UsedTime:  6ks, AntBulletEnv-v0 ModSAC"
#     "TotalStep: 16e5, TargetReward: 3247, UsedTime: 90ks, AntBulletEnv-v0 ModSAC"
#     "TotalStep:  3e5, TargetReward: 1500, UsedTime:  4ks, AntBulletEnv-v0 ModSAC"
#     "TotalStep:  5e5, TargetReward: 2500, UsedTime: 12ks, AntBulletEnv-v0 ModSAC"
#     "TotalStep: 16e5, TargetReward: 3150, UsedTime:130ks, AntBulletEnv-v0 ModSAC sample_times = 2"
#     args.agent.sample_times = 2
#
#     args.env = PreprocessEnv(env=gym.make('AntBulletEnv-v0'))
#     args.break_step = int(6e5 * 8)  # (5e5) 1e6, UsedTime: (15,000s) 30,000s
#     args.if_allow_break = False
#     args.reward_scale = 2 ** -2  # RewardRange: -50 < 0 < 2500 < 3340
#     args.max_memo = 2 ** 21
#     args.batch_size = 2 ** 9
#     args.target_step = args.env.max_step
#     args.repeat_times = 2 ** 1
#     args.eval_gap = 2 ** 9  # for Recorder
#     args.eva_size1 = 2 ** 1  # for Recorder
#     args.eva_size2 = 2 ** 3  # for Recorder
#
#     # train_and_evaluate(args)
#     args.rollout_num = 4
#     train_and_evaluate_mp(args)
#
#     "TotalStep: 15e5, TargetReward: 500, UsedTime:   ks, HumanoidBulletEnv-v0 ModSAC"
#     "TotalStep: 20e5, TargetReward:1000, UsedTime:   ks, HumanoidBulletEnv-v0 ModSAC"
#
#     "TotalStep: 17e5, TargetReward: 910, UsedTime:   ks, HumanoidBulletEnv-v0 ModSAC"
#     args.agent = AgentModSAC()  # AgentSAC(), AgentTD3(), AgentDDPG()
#     args.agent.if_use_dn = False
#     args.agent.repeat_times = 8  # todo
#     args.agent.learning_rate = 2e-5  # todo
#
#     args.env = PreprocessEnv(env=gym.make('HumanoidBulletEnv-v0'))  # todo
#     args.break_step = int(8e5 * 8)  # (5e5) 1e6, UsedTime: (15,000s) 30,000s
#     args.if_allow_break = False
#     args.reward_scale = 2 ** -3
#     args.max_memo = 2 ** 20
#     args.batch_size = 2 ** 9
#     args.target_step = args.env.max_step
#     args.repeat_times = 2 ** 0
#     args.eval_gap = 2 ** 9  # for Recorder
#     args.eva_size1 = 2 ** 1  # for Recorder
#     args.eva_size2 = 2 ** 3  # for Recorder
#
#     # train_and_evaluate(args)
#     args.rollout_num = 4
#     train_and_evaluate_mp(args)
#
#
# def demo4_bullet_mujoco_on_policy():
#     args = Arguments(if_on_policy=True)  # hyper-parameters of on-policy is different from off-policy
#
#     import pybullet_envs  # for python-bullet-gym
#     dir(pybullet_envs)
#
#     # "TotalStep: 1e5, TargetReturn: 18, UsedTime:  3ks, ReacherBulletEnv-v0, PPO"
#     # "TotalStep: 1e6, TargetReturn: 18, UsedTime: 30ks, ReacherBulletEnv-v0, PPO"
#     # args.env = PreprocessEnv(gym.make('ReacherBulletEnv-v0'))
#     #
#     # from elegantrl2.agent import AgentPPO
#     # args.agent = AgentPPO()
#     # args.agent.if_use_gae = True
#     #
#     # args.break_step = int(2e5 * 8)
#     # args.reward_scale = 2 ** 0  # RewardRange: -15 < 0 < 18 < 25
#     # args.gamma = 0.96
#     # args.eval_times1 = 2 ** 2
#     # args.eval_times1 = 2 ** 5
#     #
#     # # train_and_evaluate(args)
#     # args.rollout_num = 4
#     # train_and_evaluate_mp(args)
#     #
#     # "TotalStep:  3e6, TargetReturn: 1500, UsedTime:  2ks, AntBulletEnv-v0, PPO"
#     # "TotalStep: 10e6, TargetReturn: 2500, UsedTime:  6ks, AntBulletEnv-v0, PPO"
#     # "TotalStep: 46e6, TargetReturn: 3017, UsedTime: 25ks, AntBulletEnv-v0, PPO"
#     # args.env = PreprocessEnv(env=gym.make('AntBulletEnv-v0'))
#     #
#     # from elegantrl2.agent import AgentPPO
#     # args.agent = AgentPPO()
#     # args.agent.if_use_gae = True
#     # args.agent.lambda_entropy = 0.05
#     # args.agent.lambda_gae_adv = 0.97
#     #
#     # args.if_allow_break = False
#     # args.break_step = int(8e6 * 8)  # (5e5) 1e6, UsedTime: (15,000s) 30,000s
#     # args.reward_scale = 2 ** -2  # (-50) 0 ~ 2500 (3340)
#     # args.max_memo = args.env.max_step * 4
#     # args.batch_size = 2 ** 11  # 10
#     # args.repeat_times = 2 ** 3
#     # args.eval_gap = 2 ** 8  # for Recorder
#     # args.eva_size1 = 2 ** 1  # for Recorder
#     # args.eva_size2 = 2 ** 3  # for Recorder
#     #
#     # # train_and_evaluate(args)
#     # args.rollout_num = 4
#     # train_and_evaluate_mp(args)
#
#     "TotalStep:  3e6, TargetReward: 1500, UsedTime:  3ks, HumanoidBulletEnv-v0 PPO"
#     "TotalStep:  6e6, TargetReward: 2500, UsedTime:  5ks, HumanoidBulletEnv-v0 PPO"
#     "TotalStep: 23e6, TargetReward: 3000, UsedTime: 19ks, HumanoidBulletEnv-v0 PPO"
#     "TotalStep: 30e5, TargetReward: 3139, UsedTime: 25ks, HumanoidBulletEnv-v0 PPO"
#     "TotalStep: 80e5, TargetReward: 3279, UsedTime:   ks, HumanoidBulletEnv-v0 PPO learning rate = 1e-4"
#     "TotalStep:  6e6, TargetReward: 1500, UsedTime:  4ks, HumanoidBulletEnv-v0 PPO"
#     "TotalStep: 25e6, TargetReward: 3000, UsedTime: 11ks, HumanoidBulletEnv-v0 PPO"
#     "TotalStep: 57e5, TargetReward: 3161, UsedTime: 54ks, HumanoidBulletEnv-v0 PPO"
#     args.env = PreprocessEnv(env=gym.make('HumanoidBulletEnv-v0'))
#     args.env.target_return = 2500
#
#     from elegantrl2.agent import AgentPPO
#     args.agent = AgentPPO()
#     args.agent.if_use_gae = True
#     args.agent.lambda_entropy = 0.02
#     args.agent.lambda_gae_adv = 0.97
#     args.agent.learning_rate = 5e-5
#
#     args.if_allow_break = False
#     args.break_step = int(8e6 * 16)
#     args.reward_scale = 2 ** -1
#     args.max_memo = args.env.max_step * 4
#     args.net_dim = 2 ** 9
#     args.batch_size = 2 ** 11
#     args.repeat_times = 2 ** 3
#     args.eval_gap = 2 ** 9  # for Recorder
#     args.eva_size1 = 2 ** 1  # for Recorder
#     args.eva_size2 = 2 ** 3  # for Recorder
#
#     # train_and_evaluate(args)
#     args.rollout_num = 4
#     train_and_evaluate_mp(args)


# '''DEMO wait for updating'''

# def train__demo():
#     pass
##
#     import pybullet_envs  # for python-bullet-gym
#     dir(pybullet_envs)
#     args.env = decorate_env(gym.make('MinitaurBulletEnv-v0'), if_print=True)
#     args.break_step = int(4e6 * 4)  # (2e6) 4e6
#     args.reward_scale = 2 ** 5  # (-2) 0 ~ 16 (20)
#     args.batch_size = (2 ** 8)
#     args.net_dim = int(2 ** 8)
#     args.max_step = 2 ** 11
#     args.max_memo = 2 ** 20
#     args.eval_times2 = 3  # for Recorder
#     args.eval_times2 = 9  # for Recorder
#     args.show_gap = 2 ** 9  # for Recorder
#     args.init_for_training()
#     train_agent_mp(args)  # train_agent(args)
#     exit()
#
#     args.env = decorate_env(gym.make('BipedalWalkerHardcore-v3'), if_print=True)  # 2020-08-24 plan
#     args.reward_scale = 2 ** 0  # (-200) -150 ~ 300 (334)
#     args.break_step = int(4e6 * 8)  # (2e6) 4e6
#     args.net_dim = int(2 ** 8)  # int(2 ** 8.5) #
#     args.max_memo = int(2 ** 21)
#     args.batch_size = int(2 ** 8)
#     args.eval_times2 = 2 ** 5  # for Recorder
#     args.show_gap = 2 ** 8  # for Recorder
#     args.init_for_training()
#     train_agent_mp(args)  # train_offline_policy(args)
#     exit()
#
#
# def train__continuous_action__on_policy():
#     import AgentZoo as Zoo
#     args = Arguments(rl_agent=None, env=None, gpu_id=None)
#     args.rl_agent = [
#         Zoo.AgentPPO,  # 2018. PPO2 + GAE, slow but quite stable, especially in high-dim
#         Zoo.AgentInterPPO,  # 2019. Integrated Network, useful in pixel-level task (state2D)
#     ][0]
#
#     import gym  # gym of OpenAI is not necessary for ElegantRL (even RL)
#     gym.logger.set_level(40)  # Block warning: 'WARN: Box bound precision lowered by casting to float32'
#     args.if_break_early = True  # break training if reach the target reward (total return of an episode)
#     args.if_remove_history = True  # delete the historical directory
#
#     args.net_dim = 2 ** 8
#     args.max_memo = 2 ** 12
#     args.batch_size = 2 ** 9
#     args.repeat_times = 2 ** 4
#     args.reward_scale = 2 ** 0  # unimportant hyper-parameter in PPO which do normalization on Q value
#     args.gamma = 0.99  # important hyper-parameter, related to episode steps
#
#     import pybullet_envs  # for python-bullet-gym
#     dir(pybullet_envs)
#     args.env = decorate_env(gym.make('MinitaurBulletEnv-v0'), if_print=True)
#     args.break_step = int(1e6 * 8)  # (4e5) 1e6 (8e6)
#     args.reward_scale = 2 ** 4  # (-2) 0 ~ 16 (PPO 34)
#     args.gamma = 0.95  # important hyper-parameter, related to episode steps
#     args.net_dim = 2 ** 8
#     args.max_memo = 2 ** 11
#     args.batch_size = 2 ** 9
#     args.repeat_times = 2 ** 4
#     args.init_for_training()
#     train_agent_mp(args)
#     exit()
#
#     # args.env = decorate_env(gym.make('BipedalWalkerHardcore-v3'), if_print=True)  # 2020-08-24 plan
#     # on-policy (like PPO) is BAD at a environment with so many random factors (like BipedalWalkerHardcore).
#     # exit()
#
#     args.env = fix_car_racing_env(gym.make('CarRacing-v0'))
#     # on-policy (like PPO) is GOOD at learning on a environment with less random factors (like 'CarRacing-v0').
#     # see 'train__car_racing__pixel_level_state2d()'
#
#
# def run__fin_rl():
#     env = FinanceMultiStockEnv()  # 2020-12-24
#
#     from AgentZoo import AgentPPO
#
#     args = Arguments(rl_agent=AgentPPO, env=env)
#     args.eval_times1 = 1
#     args.eval_times2 = 1
#     args.rollout_num = 4
#     args.if_break_early = False
#
#     args.reward_scale = 2 ** 0  # (0) 1.1 ~ 15 (19)
#     args.break_step = int(5e6 * 4)  # 5e6 (15e6) UsedTime: 4,000s (12,000s)
#     args.net_dim = 2 ** 8
#     args.max_step = 1699
#     args.max_memo = 1699 * 16
#     args.batch_size = 2 ** 10
#     args.repeat_times = 2 ** 4
#     args.init_for_training()
#     train_agent_mp(args)  # train_agent(args)
#     exit()
#
#     # from AgentZoo import AgentModSAC
#     #
#     # args = Arguments(rl_agent=AgentModSAC, env=env)  # much slower than on-policy trajectory
#     # args.eval_times1 = 1
#     # args.eval_times2 = 2
#     #
#     # args.break_step = 2 ** 22  # UsedTime:
#     # args.net_dim = 2 ** 7
#     # args.max_memo = 2 ** 18
#     # args.batch_size = 2 ** 8
#     # args.init_for_training()
#     # train_agent_mp(args)  # train_agent(args)
#
#
# def train__car_racing__pixel_level_state2d():
#     from AgentZoo import AgentPPO
#
#     '''DEMO 4: Fix gym Box2D env CarRacing-v0 (pixel-level 2D-state, continuous action) using PPO'''
#     import gym  # gym of OpenAI is not necessary for ElegantRL (even RL)
#     gym.logger.set_level(40)  # Block warning: 'WARN: Box bound precision lowered by casting to float32'
#     env = gym.make('CarRacing-v0')
#     env = fix_car_racing_env(env)
#
#     args = Arguments(rl_agent=AgentPPO, env=env, gpu_id=None)
#     args.if_break_early = True
#     args.eval_times2 = 1
#     args.eval_times2 = 3  # CarRacing Env is so slow. The GPU-util is low while training CarRacing.
#     args.rollout_num = 4  # (num, step, time) (8, 1e5, 1360) (4, 1e4, 1860)
#     args.random_seed += 1943
#
#     args.break_step = int(5e5 * 4)  # (1e5) 2e5 4e5 (8e5) used time (7,000s) 10ks 30ks (60ks)
#     # Sometimes bad luck (5%), it reach 300 score in 5e5 steps and don't increase.
#     # You just need to change the random seed and retrain.
#     args.reward_scale = 2 ** -2  # (-1) 50 ~ 700 ~ 900 (1001)
#     args.max_memo = 2 ** 11
#     args.batch_size = 2 ** 7
#     args.repeat_times = 2 ** 4
#     args.net_dim = 2 ** 7
#     args.max_step = 2 ** 10
#     args.show_gap = 2 ** 8  # for Recorder
#     args.init_for_training()
#     train_agent_mp(args)  # train_agent(args)
#     exit()


if __name__ == '__main__':
    # demo_continuous_action_off_policy()
    demo_continuous_action_on_policy()
