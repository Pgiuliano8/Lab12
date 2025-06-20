import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._countries = DAO.get_countries()
        self._graph = nx.Graph()
        self._idMap={}

        self.bestPath = []
        self.bestScore = 0

    def get_countries(self):
        return self._countries

    def buildGraph(self, country, year):
        nodes = DAO.getNodes(country)
        for n in nodes:
            self._idMap[n.Retailer_code] = n
        self._graph.add_nodes_from(nodes)

        archi = DAO.getEdges(year, country, self._idMap)
        for a in archi:
            self._graph.add_edge(a.arco1, a.arco2, weight=a.peso)

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def volumiVenditaRetailer(self):
        res = []
        for node in self._graph.nodes():
            vv = 0
            neighbors = self._graph.neighbors(node)
            for n in neighbors:
                vv+=self._graph[node][n]["weight"]
            res.append((node, vv))
        return sorted(res, key=lambda x: x[1], reverse=True)
    
    def cammino_massimo(self, lun):
        self.bestPath = []
        self.bestScore = 0
        
        parziale = []
        rimanenti = self._graph.nodes()
        for n in rimanenti:
            parziale.append(n)
            self.ricorsione(parziale, self.nuovi_rimanenti(parziale), lun)
        return self.bestPath+[self.bestPath[0]], self.bestScore

    def ricorsione(self, parziale, rimanenti, lun):
        if len(parziale) == lun:
            if self._graph.has_edge(parziale[-1], parziale[0]):
                score = self.calcola_score(parziale) + self._graph[parziale[-1]][parziale[0]]["weight"]
                if score > self.bestScore:
                    self.bestScore = score
                    self.bestPath = copy.deepcopy(parziale)
        else:
            for n in rimanenti:
                parziale.append(n)
                nuovi_rimanenti = self.nuovi_rimanenti(parziale)
                self.ricorsione(parziale, nuovi_rimanenti,  lun)
                parziale.pop()

    def nuovi_rimanenti(self, parziale):
        nr = []
        neighbors = self._graph.neighbors(parziale[-1])
        for n in neighbors:
            if n not in parziale:
                nr.append(n)
        return nr


    def calcola_score(self, parziale):
        score = 0
        for i in range(0, len(parziale)-1):
            score += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return score

    def getPeso(self, a1, a2):
        return self._graph[a1][a2]["weight"]