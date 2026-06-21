import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    #def fillDDYear(self):
        #years = self._model.getAllYears()
        #for y in years:
            #self._view._ddAnno1.options.append(ft.dropdown.Option(y))
            #self._view._ddAnno2.options.append(ft.dropdown.Option(y))
        #self._view.update_page()

    def fillYearsDA(self):
        anni= self._model.getAllYears()
        anniDD = list(
            map(lambda x: ft.dropdown.Option(data=x, key=str(x), on_click=self._annoScelto1), anni))
        self._view._ddAnno1.options = anniDD
        self._view.update_page()

    def fillYearsA(self):
        anni= self._model.getAllYears()
        anniDD = list(
            map(lambda x: ft.dropdown.Option(data=x, key=str(x), on_click=self._annoScelto2), anni))
        self._view._ddAnno2.options = anniDD
        self._view.update_page()

    def _annoScelto1(self, e):
        # salva in una variabile di classe la scelta dell'utente
        self._anno1Value = e.control.data

    def _annoScelto2(self, e):
        # salva in una variabile di classe la scelta dell'utente
        self._anno2Value = e.control.data

    def handleCreaGrafo(self,e):
        #d1 = self._view._ddAnno1.value
        #d2 = self._view._ddAnno2.value
        d1 = self._anno1Value
        d2 = self._anno2Value

        if d1 is None or d2 is None:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("selezionare un anno"))
            self._view.update_page()
            return

        self._model.creaGrafo( d1, d2)

        n, m = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"grafo correttamnete creato, è formato da {n} nodi e {m} archi"))
        self._view.update_page()

    def handleDettagli(self, e):
        top3 = self._model.getTop3archi()
        self._view.txt_result.controls.append( ft.Text(f"archi di peso maggiore:"))
        for arco in top3:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0]} --> {arco[1]} (peso: {arco[2]["peso"]}"))

        numero, maggiore, dettagli = self._model.getConnessaInfo()
        self._view.txt_result.controls.append(ft.Text(f"il grafo contiene {numero} componenti connesse"))

        self._view.txt_result.controls.append(ft.Text(f"il componente connessa maggiore ha dimesione pari a {len(maggiore)} "))
        for m in maggiore:
            self._view.txt_result.controls.append(ft.Text(f"{m}"))

        self._view.txt_result.controls.append(
            ft.Text(f"in ordine decrescente in base ai nodi "))
        for d in dettagli:
            self._view.txt_result.controls.append(ft.Text(f"{d[0]} --> grado:{d[1]}"))

        self._view.update_page()


    def handleCerca(self, e):
        k = self._view._txtInK.value
        #controlli sulla validità di k

        kInt = int(k)
        listPilotiOttima, minDistEta = self._model.getListaPilotiOttima(kInt)

        if listPilotiOttima is None:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text(f"non ci sono abbastanza componenti connesse per trovare {k} che non sono stati compagni di squadra nel range selezionato "))
            return

        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"lista di piloti con scarto di età minimo che non sono mai stati compagni di squadra nel range selezionato "))

        for p in listPilotiOttima:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))

        self._view.txt_result.controls.append(ft.Text(f"differenza di età {minDistEta}"))
        self._view.update_page()



