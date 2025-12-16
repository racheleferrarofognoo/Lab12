import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G = nx.Graph()
        self.id_map = {}
        self.dao = DAO()
        self.grafo_filtrato = nx.Graph()

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        self.G.clear()
        self.id_map.clear()
        rifugi = self.dao.read_rifugi()
        for r in rifugi:
            self.id_map[r["id"]] = r  # dizionario con chiave id del rifugio e valore oggetti Rifugio
        connessioni = self.dao.read_connessioni(year)
        for conn in connessioni:
            id1 = conn["id_rifugio1"]
            id2 = conn["id_rifugio2"]
            if conn["difficolta"] == "facile":
                fattore_difficolta = 1
            elif conn["difficolta"] == "media":
                fattore_difficolta = 1.5
            else:
                fattore_difficolta = 2

            peso = float(conn["distanza"]) * fattore_difficolta

            self.G.add_node(id1)
            self.G.add_node(id2)
            self.G.add_edge(id1, id2, peso = peso)

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        minimo = 100000
        massimo = -10000
        archi = self.G.edges(data=True)
        for u,v,attributo in archi:
            peso = attributo["peso"]
            if peso < minimo:
                minimo = peso
            if peso > massimo:
                massimo = peso

        return minimo,massimo

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        minori_di_soglia = 0
        maggiori_di_soglia = 0
        for u,v,attributo in self.G.edges(data = True):
            if attributo["peso"] < soglia:
                minori_di_soglia +=1
            elif attributo["peso"] > soglia:
                maggiori_di_soglia += 1

        return minori_di_soglia, maggiori_di_soglia


    """Implementare la parte di ricerca del cammino minimo"""
    #NETWORKX
    def cammino_minimo_nx(self,soglia):
        #creo un grafco filtrato con solo i cammini con peso > soglia
        grafo_filtrato = self.grafo_filtrato
        grafo_filtrato.clear()
        for u,v,attr in self.G.edges(data = True):
            if attr["peso"] > soglia:
                grafo_filtrato.add_node(u)
                grafo_filtrato.add_node(v)
                grafo_filtrato.add_edge(u, v, peso = attr["peso"])

        #minimo num di nodi
        if len(self.grafo_filtrato.nodes) < 3:
            return []

        cammino_minimo = []
        peso_minimo = 10000
        nodi = list(grafo_filtrato.nodes)
        for i in range(len(nodi)):
            for j in range(i + 1, len(nodi)):
                percorso = nx.shortest_path(grafo_filtrato, nodi[i], nodi[j], weight = "peso")
                if len(percorso) >= 3: #ovvero se ho almeno 2 archi
                    peso = 0
                    for k in range(len(percorso)-1):
                        peso += grafo_filtrato[percorso[k]][percorso[k+1]]["peso"] #prendo il peso del k-esimo arco
                        if peso < peso_minimo:
                            peso_minimo = peso
                            cammino_minimo = percorso
        return cammino_minimo

    #RICORSIONE
    def cammino_minimo_ricorsione(self, soglia):
        grafo_filtrato = self.grafo_filtrato
        grafo_filtrato.clear()
        for u,v,attr in self.G.edges(data = True):
            if attr["peso"] > soglia:
                grafo_filtrato.add_node(u)
                grafo_filtrato.add_node(v)
                grafo_filtrato.add_edge(u, v, peso = attr["peso"])

        self.cammino_minimo = []
        self.peso_minimo = 10000

        for inizio in grafo_filtrato:
            self.dfs_ricorsiva(grafo_filtrato, inizio, [inizio],0)
        return self.cammino_minimo

    def dfs_ricorsiva(self, grafo, parziale, cammino, peso_attuale):
        #eploro tutti i cammini semplici del grafo filtrato
        for neighbor, peso in self.grafo_filtrato[parziale].items():
            if neighbor not in cammino:
                cammino_nuovo = cammino + [neighbor]
                peso_nuovo = peso_attuale + peso
                #ogni volta che trovo un cammino con almeno 2 rchi e peso minore del peso migliore, aggiorno la sol e continuo
                if len(cammino_nuovo) >= 3 and peso_nuovo < self.peso_minimo:
                    self.cammino_minimo = cammino_nuovo
                    self.peso_minimo = peso_nuovo
                self.dfs_ricorsiva(grafo, neighbor, cammino_nuovo, peso_nuovo)














