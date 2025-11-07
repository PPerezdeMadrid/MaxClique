import unittest
import os
from parser import parse_dimacs_graph
from search import search_max_clique
from search2 import search_max_clique as search2_max_clique
from search3 import search_max_clique as search3_max_clique
from search4 import search_max_clique as search4_max_clique

DIMACS_FOLDER = "../DIMACS"
TEST_FILE_1 = "johnson8-2-4.clq"  # Smallest instance
SOL_MAX_CLIQUE_SIZE_1 = 4         # Known max clique size for this graph
TEST_FILE_2 = "p_hat300-1.clq"
SOL_MAX_CLIQUE_SIZE_2 = 8
TEST_FILE_3 = "brock200_2.clq"
SOL_MAX_CLIQUE_SIZE_3 = 12


def build_graph(filename):
    path = os.path.join(DIMACS_FOLDER, filename)
    num_vertices, edges = parse_dimacs_graph(path)
    graph = {i: set() for i in range(1, num_vertices + 1)}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    return graph


class Test(unittest.TestCase):
    """Unit tests for all search versions on multiple DIMACS instances."""

    def test_johnson_search(self):
        print(f"Testing {TEST_FILE_1} with search.py")
        graph = build_graph(TEST_FILE_1)
        result = search_max_clique(graph)
        self.assertEqual(len(result), SOL_MAX_CLIQUE_SIZE_1)

    def test_johnson_search2(self):
        print(f"Testing {TEST_FILE_1} with search2.py")
        graph = build_graph(TEST_FILE_1)
        result = search2_max_clique(graph)
        self.assertEqual(len(result), SOL_MAX_CLIQUE_SIZE_1)

    def test_johnson_search3(self):
        print(f"Testing {TEST_FILE_1} with search3.py")
        graph = build_graph(TEST_FILE_1)
        result = search3_max_clique(graph)
        self.assertEqual(len(result), SOL_MAX_CLIQUE_SIZE_1)

    def test_johnson_search4(self):
        print(f"Testing {TEST_FILE_1} with search4.py")
        graph = build_graph(TEST_FILE_1)
        result = search4_max_clique(graph)
        self.assertEqual(len(result), SOL_MAX_CLIQUE_SIZE_1)


    def test_phat_search(self):
        print(f"Testing {TEST_FILE_2} with search.py")
        graph = build_graph(TEST_FILE_2)
        result = search_max_clique(graph)
        self.assertEqual(len(result), SOL_MAX_CLIQUE_SIZE_2)

    def test_phat_search2(self):
        print(f"Testing {TEST_FILE_2} with search2.py")
        graph = build_graph(TEST_FILE_2)
        result = search2_max_clique(graph)
        self.assertEqual(len(result), SOL_MAX_CLIQUE_SIZE_2)

    def test_phat_search3(self):
        print(f"Testing {TEST_FILE_2} with search3.py")
        graph = build_graph(TEST_FILE_2)
        result = search3_max_clique(graph)
        self.assertEqual(len(result), SOL_MAX_CLIQUE_SIZE_2)

    def test_phat_search4(self):
        print(f"Testing {TEST_FILE_2} with search4.py")
        graph = build_graph(TEST_FILE_2)
        result = search4_max_clique(graph)
        self.assertEqual(len(result), SOL_MAX_CLIQUE_SIZE_2)


    def test_brook_search(self):
        print(f"Testing {TEST_FILE_3} with search.py")
        graph = build_graph(TEST_FILE_3)
        result = search_max_clique(graph)
        self.assertEqual(len(result), SOL_MAX_CLIQUE_SIZE_3)

    def test_brook_search2(self):
        print(f"Testing {TEST_FILE_3} with search2.py")
        graph = build_graph(TEST_FILE_3)
        result = search2_max_clique(graph)
        self.assertEqual(len(result), SOL_MAX_CLIQUE_SIZE_3)


    def test_brook_search3(self):
        print(f"Testing {TEST_FILE_3} with search3.py")
        graph = build_graph(TEST_FILE_3)
        result = search3_max_clique(graph)
        self.assertEqual(len(result), SOL_MAX_CLIQUE_SIZE_3)

    def test_brook_search4(self):
        print(f"Testing {TEST_FILE_3} with search4.py")
        graph = build_graph(TEST_FILE_3)
        result = search4_max_clique(graph)
        self.assertEqual(len(result), SOL_MAX_CLIQUE_SIZE_3)
    

if __name__ == "__main__":
    unittest.main()
