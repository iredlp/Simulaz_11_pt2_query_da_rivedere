import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        years = self._model.getAllRatings()
        self._view._ddrating1.options.clear()
        self._view._ddrating2.options.clear()
        for y in years:
            self._view._ddrating1.options.append(ft.dropdown.Option(key=str(y), text=str(y)))
            self._view._ddrating2.options.append(ft.dropdown.Option(key=str(y), text=str(y)))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        v1 = self._view._ddrating1.value
        v2 = self._view._ddrating2.value

        self._model.creaGrafo(v1, v2)

        Nodes, Edges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato! Il grafo contiene {Nodes} nodi e {Edges}archi"))

        top5 = self._model.getTop5Archi()
        #self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Archi di peso maggiore", color="green"))
        for arco in top5:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0]}-->{arco[1]} (peso: {arco[2]["weight"]})"))

        numero, largest, details = self._model.getConnessaInfo()
        #self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {numero}componenti connesse", color="orange"))
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa maggiore ha dimensione {len(largest)}"))
        for l in largest:
            self._view.txt_result.controls.append(ft.Text(f"{l}"))
        self._view.txt_result.controls.append(
            ft.Text(f"La componente connessa in ordine decrescente di grado dei nodi"))

        self._view.update_page()

    def handleCammino(self, e):
        pass