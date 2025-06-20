import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        countries = self._model.get_countries()
        years = [2015, 2016, 2017, 2018]
        for y in years:
            self._view.ddyear.options.append(ft.dropdown.Option(str(y)))
        for c in countries:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))
        self._view.update_page()


    def handle_graph(self, e):
        self._view.txt_result.clean()
        year = self._view.ddyear.value
        if year is None:
            self._view.create_alert("Scegliere un anno")
            return
        year=int(year)

        country = self._view.ddcountry.value
        if country is None:
            self._view.create_alert("Scegliere un anno")
            return
        self.graph = self._model.buildGraph(country, year)
        nNodi, nArchi = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {nNodi} Numero archi: {nArchi}"))
        self._view.btn_volume.disabled = False
        self._view.update_page()


    def handle_volume(self, e):
        self._view.txtOut2.clean()
        list = self._model.volumiVenditaRetailer()
        for l in list:
            self._view.txtOut2.controls.append(ft.Text(f"{l[0]}--> {l[1]}"))
        self._view.update_page()




    def handle_path(self, e):
        print("DEBUG: Bottone cliccato")
        lun = self._view.txtN.value
        if lun is None:
            self._view.create_alert("Inserire un numero")
            return
        try:
            lun = int(lun)
        except ValueError:
            self._view.create_alert("Inserire un numero")
            return
        if lun < 2:
            self._view.create_alert("Inserire un numero maggiore o uguale a 2")
            return

        bestPath, bestScore = self._model.cammino_massimo(lun)
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {bestScore}"))
        for i in range(0, len(bestPath)-1):
            peso = self._model.getPeso(bestPath[i], bestPath[i+1])
            self._view.txtOut3.controls.append(ft.Text(f"{bestPath[i]}-->{bestPath[i+1]}: "
                                                       f"{peso}"))
        self._view.update_page()

