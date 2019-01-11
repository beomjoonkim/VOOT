import os
import sys
from multiprocessing.pool import ThreadPool  # dummy is nothing but multiprocessing but wrapper around threading
import argparse


def worker_p(config):
    s = config['sampling_strategy']
    d = config['domain']
    pidx = config['trial']
    w = config['widening_parameter']
    e = config['epsilon']
    mcts_iter = config['mcts_iter']
    c1 = config['c1']

    command = 'python ./test_scripts/test_mcts.py -sampling_strategy ' + s + \
        ' -problem_idx ' + str(pidx) + ' -domain ' + d + ' -epsilon ' + str(e) + ' -widening_parameter ' + str(w) + \
        ' -mcts_iter ' + str(mcts_iter) + ' -c1 '+str(c1)

    print command
    os.system(command)


def worker_wrapper_multi_input(multi_args):
    return worker_p(multi_args)


def main():
    parser = argparse.ArgumentParser(description='MCTS parameters')
    parser.add_argument('-sampling', type=str, default='unif')
    parser.add_argument('-domain', type=str, default='convbelt')
    parser.add_argument('-mcts_iter', type=int, default=50)
    parser.add_argument('-w', nargs='+', type=float)
    parser.add_argument('-c1', nargs='+', type=float)
    parser.add_argument('-epsilon', nargs='+', type=float)

    args = parser.parse_args()

    sampling_strategy = args.sampling
    epsilons = args.epsilon if args.epsilon is not None else [-1]
    domain = args.domain
    widening_parameters = args.w if args.w is not None else [0.8]
    mcts_iter = args.mcts_iter
    c1s = args.c1 if args.c1 is not None else [1]
    trials = range(200)
    configs = []
    for c1 in c1s:
        for e in epsilons:
            for t in trials:
                for widening_parameter in widening_parameters:
                    config = {"widening_parameter": widening_parameter,
                              "epsilon": e, 'trial':t, 'domain':domain,
                              'sampling_strategy':sampling_strategy,
                              'mcts_iter': mcts_iter, 'c1':c1}
                    configs.append(config)

    n_workers = int(30)
    print configs
    pool = ThreadPool(n_workers)
    results = pool.map(worker_wrapper_multi_input, configs)


if __name__ == '__main__':
    main()
