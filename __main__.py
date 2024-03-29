import argparse

import tabulate

from vertex_cover_approximations import Algorithm, RunMode
from vertex_cover_approximations import logger
from vertex_cover_approximations.algorithms.exact import exact
from vertex_cover_approximations.algorithms.greedy_2_approx import greedy_2_approx
from vertex_cover_approximations.algorithms.greedy_logn_approx import greedy_logn_approx
from vertex_cover_approximations.algorithms.naive_approx import naive_approx


def run_specific(algorithm, dataset_path, visualize=False, plot_path=None):
    logger.info('run_specific called with algorithm=\'{0}\', dataset_path=\'{1}\', visualize=\'{2}\', plot_path=\'{3}\'.'.format(algorithm, dataset_path, visualize, plot_path))

    # compute vertex cover
    node_set = None
    running_time = None
    if algorithm == Algorithm.EXACT.value[0]:
        node_set, running_time = exact(dataset_path, visualize, plot_path)
    elif algorithm == Algorithm.NAIVE_APPROX.value[0]:
        node_set, running_time = naive_approx(dataset_path, visualize, plot_path)
    elif algorithm == Algorithm.GREEDY_LOGN_APPROX.value[0]:
        node_set, running_time = greedy_logn_approx(dataset_path, visualize, plot_path)
    elif algorithm == Algorithm.GREEDY_2_APPROX.value[0]:
        node_set, running_time = greedy_2_approx(dataset_path, visualize, plot_path)

    print('Computed vertex cover for the graph specified in \'{0}\' consists of {1} nodes. Running time is {2} seconds.'.format(dataset_path, len(node_set), round(running_time, 4)))


def run_all(dataset_path, exclude_exact, visualize=False, plot_path=None):
    logger.info('run_all called with dataset_path=\'{0}\', visualize=\'{1}\', plot_path=\'{2}\'.'.format(dataset_path, visualize, plot_path))

    node_set_exact = set()
    running_time_exact = 0.0
    if not exclude_exact:
        node_set_exact, running_time_exact = exact(dataset_path, visualize, plot_path)
    node_set_naive_approx, running_time_naive_approx = naive_approx(dataset_path, visualize, plot_path)
    node_set_greedy_logn_approx, running_time_greedy_logn_approx = greedy_logn_approx(dataset_path, visualize, plot_path)
    node_set_greedy_2_approx, running_time_greedy_2_approx = greedy_2_approx(dataset_path, visualize, plot_path)

    res_list = [(Algorithm.EXACT.value[1], len(node_set_exact), running_time_exact)] if not exclude_exact else []

    res_list += [
        (Algorithm.NAIVE_APPROX.value[1], len(node_set_naive_approx), round(running_time_naive_approx, 4)),
        (Algorithm.GREEDY_LOGN_APPROX.value[1], len(node_set_greedy_logn_approx), round(running_time_greedy_logn_approx, 4)),
        (Algorithm.GREEDY_2_APPROX.value[1], len(node_set_greedy_2_approx), round(running_time_greedy_2_approx, 4))
    ]

    print(tabulate.tabulate(res_list, headers=('Algorithm', 'Computed Vertex Cover Size', 'Running Time (seconds)')))


if __name__ == '__main__':

    # parse arguments
    parser = argparse.ArgumentParser(prog='sat-reductions')
    subparsers = parser.add_subparsers(help='run all or specific', dest='run_mode', required=True)
    parser_all = subparsers.add_parser(RunMode.ALL.value, help='run all algorithms')
    parser_specific = subparsers.add_parser(RunMode.SPECIFIC.value, help='run specific algorithm')
    for subparser in (parser_all, parser_specific):
        subparser.add_argument('--dataset', type=str, required=True, help='path to the dataset/graph specification to use')
        subparser.add_argument('--visualize', action='store_true', help='visualize the vertex cover or not')
        subparser.add_argument('--plot-path', type=str, default='.', help='path to directory in which to save the visualization plots')
    parser_all.add_argument('--exclude-exact', action='store_true', help='use only approximation algorithms (exclude the exact algorithm)')
    parser_specific.add_argument('--algorithm', type=str, choices=[e.value[0] for e in Algorithm], default=Algorithm.EXACT.value[0], help='algorithm to use')

    args = parser.parse_args()

    if args.run_mode == RunMode.SPECIFIC.value:
        # run specific algorithm
        run_specific(args.algorithm, args.dataset, args.visualize, args.plot_path)
    elif args.run_mode == RunMode.ALL.value:
        # run all algorithms
        run_all(args.dataset, args.exclude_exact, args.visualize, args.plot_path)
