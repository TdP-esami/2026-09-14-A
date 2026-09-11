import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._actors = []
        self._bestGroup = []
        self._bestNumMovies = 0

    def buildGraph(self, val_min, val_max):
        self._graph.clear()

        self._actors = DAO.getActorsInRatingRange(val_min, val_max)

        for actor in self._actors:
            DAO.getMoviesForActorInRange(actor, val_min, val_max)

        self._graph.add_nodes_from(self._actors)

        for i in range(len(self._actors)):
            for j in range(i + 1, len(self._actors)):
                a1 = self._actors[i]
                a2 = self._actors[j]

                common_movies = a1.get_movie_ids() & a2.get_movie_ids()
                if common_movies:
                    peso = len(common_movies)
                    self._graph.add_edge(a1, a2, weight=peso)

    def getActorWithMaxDegree(self):
        if len(self._graph.nodes) == 0:
            return None, 0

        max_degree = -1
        best_actor = None
        for node, degree in self._graph.degree():
            if degree > max_degree:
                max_degree = degree
                best_actor = node
        return best_actor, max_degree

    def getActorWithMaxWeightSum(self):
        if len(self._graph.nodes) == 0:
            return None, 0

        max_sum = -1
        best_actor = None
        for node in self._graph.nodes:
            weight_sum = sum(
                self._graph[node][neighbor]["weight"]
                for neighbor in self._graph.neighbors(node)
            )
            if weight_sum > max_sum:
                max_sum = weight_sum
                best_actor = node
        return best_actor, max_sum

    def getYoungestActor(self):
        candidates = [a for a in self._graph.nodes if a.DateOfBirth is not None]
        if not candidates:
            return None
        return max(candidates, key=lambda a: a.DateOfBirth)

    def getOldestActor(self):
        candidates = [a for a in self._graph.nodes if a.DateOfBirth is not None]
        if not candidates:
            return None
        return min(candidates, key=lambda a: a.DateOfBirth)

    def getTop5Edges(self):
        if len(self._graph.edges) == 0:
            return []

        edges_with_weights = [
            (u, v, self._graph[u][v]["weight"])
            for u, v in self._graph.edges
        ]

        edges_sorted = sorted(
            edges_with_weights,
            key=lambda x: (-x[2], x[0].Name, x[1].Name)
        )

        return edges_sorted[:5]

    def getBestGroup(self, starting_actor, N):
        if starting_actor not in self._graph.nodes:
            return [], 0

        self._bestGroup = []
        self._bestNumMovies = 0

        parziale = [starting_actor]
        self._ricorsione(parziale, N)

        return self._bestGroup, self._bestNumMovies

    def _ricorsione(self, parziale, N):
        # condizione di terminazione: parziale lunga N
        if len(parziale) == N:
            total_movies = self._getTotalMovies(parziale)
            if total_movies > self._bestNumMovies:
                self._bestNumMovies = total_movies
                self._bestGroup = copy.deepcopy(parziale)
            return

        for candidate in self._graph.nodes:
            if candidate in parziale:
                # l'attore è già stato selezionato, salto
                continue

            # il candidato deve essere adiacente ad esattamente un attore già in parziale
            num_adjacent = sum(
                1 for existing in parziale if self._graph.has_edge(candidate, existing)
            )
            if num_adjacent != 1:
                continue

            parziale.append(candidate)
            self._ricorsione(parziale, N)
            parziale.pop()

    def _getTotalMovies(self, actors):
        return sum(a.get_num_movies() for a in actors)

    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getAllActors(self):
        return self._graph.nodes
