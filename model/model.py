import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapA = {}
        self._attori = []


    def getAllRatings(self):
        return DAO.getAllRatings()

    def creaGrafo(self, voto1, voto2):
        # nodes = DAO.getAllNodes(anno1, anno2)
        self._graph.clear()
        self._idMapA.clear()

        votoMin = min(voto1, voto2)
        votoMax = max(voto1, voto2)

        # Ottenimento di tutti i circuiti
        self._attori = DAO.getAllNodes(votoMin,votoMax)
        #  Dettaglio risultati per nodo e aggiunta al grafo
        for c in  self._attori:
            #c.risultati = DAO.getRisultatiPerCircuito(c.circuitId, min_year, max_year)
            self._idMapA[c.id] = c
            self._graph.add_node(c)

        edges = DAO.getAllEdges(votoMin,votoMax, self._idMapA)

        for e in edges:
            peso_film = e.get_peso_numerico()
            # Se hanno già un arco (un altro film in comune), somma il nuovo incasso
            if self._graph.has_edge(e.a1, e.a2):
                self._graph[e.a1][e.a2]["weight"] += peso_film
            else:
                self._graph.add_edge(e.a1, e.a2, weight=peso_film)


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop5Archi(self):
        return sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:5]

    def getConnessaInfo(self):
        components=list(nx.connected_components(self._graph)) #TROVO LE COMP CONNESSE e ci faccio una lista
        largest=max(components, key=len) #trova la + grande
        #subgraph=self._graph.subgraph(largest).copy()
        #subgraph = self._graph.subgraph
        #ordered_nodes=sorted(subgraph.nodes(), key=lambda n:self._graph.degree(n), reverse=True)
        ordered_nodes = sorted(largest, key=lambda n: self._graph.degree(n), reverse=True)
        details=[(n,self._graph.degree(n)) for n in ordered_nodes]
        return len(components), largest, details

    def getPercorsoOttimo(self, ):
        # 1. Trovo la componente connessa più grande
        components = list(nx.connected_components(self._graph))
        if not components:
            return [], 0
        #largest_cc = max(components, key=len)


        # 3. Inizializzo le variabili per memorizzare il risultato migliore
        self._best_sol = []
        self._best_score = 0.0

        # 4. Lancio la ricorsione
        for nodo in self._graph.nodes:
            self._ricorsione([nodo])

        return self._best_sol, self._best_score

    def _ricorsione(self, parziale):
        # --- CASO TERMINALE --

        # 1)VERIFICA LE LA SOLUZIONE ATTUALE è MIGLIORE DEL BEST- CONDIZ DI OTTIMALITà
        if self._score(parziale) > self._best_score:
            # salvo la nuova soluz ottima
            self._best_weight = self._score(parziale)
            self._best_path = list(parziale)

        ultimo = parziale[-1]
        for vicino in self._graph.neighbors(ultimo):
            # Vincolo: vertice visitato una volta sola
            if vicino not in parziale:
               # peso_arco = self._graph[ultimo][vicino]["weight"]
                # Vincolo: peso strettamente decrescente rispetto all'arco precedente!!!
                if vicino.eta < ultimo.eta:
                    # Passo in avanti
                    parziale.append(vicino)



    def _score(self, parziale):
        #esplora la soluz parzila ed aggiunge i pesi
        score=0
        for i in range(0, len(parziale)-1):
            score+=self._graph[parziale[i]][parziale[i+1]]["weight"]
        return score

