import pytest
import random

from algo.topo_sort import Graph

## Test Utilities


# Check that the sort order is viable
def assert_topo_sort(graph, order):
    assert len(order) == len(graph.adj_list)

    g = graph
    for i, v in enumerate(order):
        for x in g.out(v):
            # assert that if x is an outgoing neighbor of v, then it comes
            # after v in the ordering
            assert i < order.index(x)


# check test fails when not topologically sorted
def test_assert_topo_sort():
    with pytest.raises(AssertionError):
        g = Graph([(0, 1)])
        assert_topo_sort(g, [1, 0])


## Test graph generators

# Generates a directed tree with n vertices in the following manner:
# Start with a set of n disconnected vertices
# At each step, pick a random vertex from the vertices in the graph, and a random vertex from the disconnected vertices.
# Add an edge between the graph vertex and the chosen vertex, and remove it from the disconnected set.
# Continue until there are no more disconnected vertices.
#
# As an extension, I feel like you could maybe use a multiset where each
# element has cardinality k for the disconnected vertices to generate a
# k-connected graph if you make sure not to choose repeats. You couldn't use
# this to generate a DAG though, it would probably end up having cycles.
def gen_ditree(n):
    graph = Graph()
    graph_vertices = [0]
    remaining = list(range(1, n))
    while len(remaining) > 0:
        v1 = random.choice(graph_vertices)
        v2 = random.choice(remaining)
        graph.add_edge(v1, v2)
        remaining.remove(v2)
    return graph


# just call to make sure it works
# TODO check vertex degrees and acyclicity
def test_gen_ditree():
    gen_ditree(1)
    gen_ditree(10)
    gen_ditree(100)


## Basic add tests
def test_add_edge_1():
    g = Graph()
    v1 = 0
    v2 = 1

    g.add_edge(v1, v2)
    assert v2 in g.out(v1)
    assert v1 in g.inc(v2)

    assert len(g.inc(v1)) == 0
    assert len(g.out(v2)) == 0


def test_add_edges_2():
    g = Graph()
    v1 = 0
    v2 = 1
    v3 = 2

    g.add_edge(v1, v2)
    g.add_edge(v2, v3)
    assert v2 in g.out(v1)
    assert v1 in g.inc(v2)
    assert v3 in g.out(v2)
    assert v2 in g.inc(v3)

    assert len(g.inc(v1)) == 0
    assert len(g.out(v3)) == 0


## Topological sort tests


def test_one_edge():
    g = Graph([(0, 1)])

    order = g.topo_sort()
    assert order == [0, 1]

    assert_topo_sort(g, order)


def test_two_edges():
    edges = [(0, 1), (1, 2)]
    g = Graph(edges)

    order = g.topo_sort()
    assert order == [0, 1, 2]

    assert_topo_sort(g, order)


def test_dag_1():
    edges = [(0, 1), (0, 2), (1, 2), (2, 3)]
    g = Graph(edges)

    order = g.topo_sort()
    assert_topo_sort(g, order)

    # [0,1,3,2] is also a valid ordering but is not the one produced by this
    # algorithm
    assert order == [0, 1, 2, 3]


def test_random_50():
    # generate 100 random trees with 50 vertices and topologically sort them
    for _ in range(0, 100):
        g = gen_ditree(50)
        order = g.topo_sort()
        assert_topo_sort(g, order)
