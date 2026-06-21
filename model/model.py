import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapP = {}
        self._optListaPilotiOttima = None
        self._minDistAnni = None

    def getAllYears(self):
        return DAO.getAllYears()

    def creaGrafo(self, d1, d2):
        self._grafo.clear()
        self._piloti = DAO.getPiloti(d1, d2)

        for p in self._piloti:
            self._idMapP[p.driverId] = p

        self._grafo.add_nodes_from(self._piloti)

        allEdges = DAO.getAllEdges( d1, d2, self._idMapP)
        for e in allEdges:
            self._grafo.add_edge(e.p1, e.p2, peso=e.peso)

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    #stampare i tre archi maggiori
    def getTop3archi(self):
        return sorted(self._grafo.edges(data=True), key=lambda x: x[2]['peso'], reverse=True)[:3]

    def getConnessaInfo(self):
        componenti = list(nx.connected_components(self._grafo)) #lista di componenti connesse

        maggiore = max(componenti, key=len) #componente connessa di dimensione maggiore

        sottografo = self._grafo.subgraph(maggiore).copy() #sottografo della componente connessa maggiore
        ordinati = sorted(sottografo.nodes(),key=lambda n: self._grafo.degree(n), reverse=True) #ordino la lista di nodi per grado
        dettagli = [(n, self._grafo.degree(n)) for n in ordinati]

        return len(componenti), maggiore, dettagli

    def getListaPilotiOttima(self,k):
        self._optListaPiloti = []
        self._minDistGiorni = 100*365

        componenti =list(nx.connected_components(self._grafo))

        if len(componenti)<k:
            #allora non ho abbastanza componenti connesse da cui pescare
            return None, 0

        parziale = []
        self._ricorsione(componenti, parziale,k, 0)
        return self._optListaPiloti, self._minDistGiorni

    def _ricorsione(self, componenti, parziale,k, indexComponente):
        #condizione di ottimalità
        if len(parziale) == k:
            #ho una soluzione accettabile
            dateDiNascita = [p.dob for p in parziale]
            diffEtaPiloti = (max(dateDiNascita) - min(dateDiNascita)).days
            if diffEtaPiloti < self._minDistGiorni:
                self._optListaPiloti = copy.deepcopy(parziale)
                self._minDistGiorni = diffEtaPiloti
            return

        #condizione di terminazione
        #esco se l'indice che indica quale comp connessa sto considerando a questa iterazione
        #è divetato >= al numeor di componenti connesse totali (ho finito i piloti)
        #oppure se non ho abbastanza componenti
        if indexComponente >= len(componenti) or len(componenti) - indexComponente < (k- len(parziale)):
            return

        #se non sono uscita allora posso aggiungere ancora piloti
        #per questa componente provo a prendere un pilota o a non prendere nessuno

        #caso 1 inserisco un pilota appartenente a questa comp connessa
        componente = componenti[indexComponente]
        for pilota in componente:
            parziale.append(pilota)
            self._ricorsione(componenti, parziale,k, indexComponente+1)
            parziale.pop()

        #caso 2 mi tengo un branch di esplorazione in cui non ho preso nessuno da questa componente
        self._ricorsione(componenti, parziale,k, indexComponente+1)