import json
from subprocess import run, PIPE
from typing import Tuple, List


class APSP(object):
    NAIVE_FW = '0'
    CUDA_NAIVE_FW = '1'
    CUDA_BLOCKED_FW = '2'


def execute_algorithm(exec_path: str, algorithm: APSP, data_input: str) -> Tuple:
    """
    Execute specific algorithm and return algorithm result

    :param exec_path: Path to executable
    :param algorithm: Type of algorithm
    :param data_input: Data input for algorithm

    :return: Data output and stderr
    """
    process = run([exec_path, '-a', algorithm],
                  input=data_input, encoding='ascii',
                  stdout=PIPE, stderr=PIPE)
    if process.stderr:
        return {'graph': [], 'predecessors': []}, process.stderr
    data = json.loads(process.stdout)
    return data, ''


def gen_empty_graph(size: int, value: int) -> List:
    """
    Generate graph with

    :param size: size of graph
    :param value: value for each cell
    """
    return [[value] * size for _ in range(size)]


def gen_graph_with_diagonal_zeros(size: int, value: int = -1) -> List:
    """
    Generate graph with zeros in diagonal

    :param size: size of graph
    :param value: value for each cell
    """
    graph = gen_empty_graph(size, value)
    for i in range(size):
        graph[i][i] = 0
    return graph


def gen_k1_graph(size: int) -> List:
    """
    Generate K1 graph

    :param size: size of graph
    """
    graph = gen_graph_with_diagonal_zeros(size)
    for i in range(size // 2):
        graph[2 * i][2 * i + 1] = 1
        graph[2 * i + 1][2 * i] = 1
    return graph


def gen_k1_predecessors(size: int) -> List:
    """
    Generate predecessors for K1 graph

    :param size: size of graph
    """
    graph = gen_empty_graph(size, -1)
    for i in range(size // 2):
        graph[2 * i][2 * i + 1] = 2 * i
        graph[2 * i + 1][2 * i] = 2 * i + 1
    return graph


def gen_kn_predecessors(size: int) -> List:
    """
    Generate predecessors for Kn graph

    :param size: size of graph
    """
    graph = gen_empty_graph(size, -1)
    for i in range(size):
        for j in range(size):
            if i != j:
                graph[i][j] = i
    return graph