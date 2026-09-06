import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._actorValue = None

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        try:
            val_min = float(self._view._txtRatingMin.value.replace(",", "."))
            val_max = float(self._view._txtRatingMax.value.replace(",", "."))
        except (ValueError, AttributeError):
            self._view.create_alert("Inserisci due valori numerici validi per la valutazione.")
            return

        if val_min < 0 or val_max > 10:
            self._view.create_alert("La valutazione deve essere compresa tra 0 e 10.")
            return
        if val_min > val_max:
            self._view.create_alert("Il valore minimo deve essere minore o uguale al valore massimo.")
            return

        try:
            self._model.buildGraph(val_min, val_max)

            self._view._txt_result.controls.append(
                ft.Text("Grafo correttamente creato.")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero di vertici: {self._model.getNumNodi()}")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero di archi: {self._model.getNumEdges()}")
            )

            self._fillDDActors()
            self._view.update_page()
        except Exception as ex:
            self._view.create_alert(f"Errore nella creazione del grafo: {ex}")
            print(ex)

    def handleStampaInfo(self, e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        try:
            actor_max_degree, max_degree = self._model.getActorWithMaxDegree()
            self._view._txt_result.controls.append(
                ft.Text(f"Attore con grado maggiore: {actor_max_degree} (grado: {max_degree})")
            )

            actor_max_weight, max_weight = self._model.getActorWithMaxWeightSum()
            self._view._txt_result.controls.append(
                ft.Text(f"Attore con somma pesi incidenti massima: {actor_max_weight} (somma: {max_weight})")
            )

            self._view._txt_result.controls.append(ft.Text(""))
            self._view._txt_result.controls.append(ft.Text("Top 5 archi con peso maggiore:"))

            top5 = self._model.getTop5Edges()
            for idx, (a1, a2, peso) in enumerate(top5, start=1):
                self._view._txt_result.controls.append(
                    ft.Text(f"{idx}. {a1} -- {a2} (peso: {peso})")
                )

            self._view.update_page()
        except Exception as ex:
            self._view.create_alert(f"Errore nella stampa delle info: {ex}")

    def handleTrovaGruppo(self, e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        if self._actorValue is None:
            self._view.create_alert("Seleziona un attore dal menu a tendina.")
            return

        try:
            N = int(self._view._txtInN.value)
            if N <= 0:
                self._view.create_alert("Inserisci un numero intero positivo per N.")
                return
        except (ValueError, TypeError):
            self._view.create_alert("Inserisci un valore numerico valido per N.")
            return

        try:
            best_group, best_num_movies = self._model.getBestGroup(self._actorValue, N)

            if not best_group:
                self._view._txt_result.controls.append(
                    ft.Text("Nessun gruppo di attori trovato con i vincoli richiesti.")
                )
                self._view.update_page()
                return

            sorted_group = sorted(best_group, key=lambda a: a.Name)

            self._view._txt_result.controls.append(ft.Text("Lista alfabetica degli attori selezionati:"))
            self._view._txt_result.controls.append(ft.Text(""))

            for actor in sorted_group:
                self._view._txt_result.controls.append(
                    ft.Text(f"  - {actor.Name}: {actor.get_num_movies()} film")
                )

            self._view._txt_result.controls.append(ft.Text(""))
            self._view._txt_result.controls.append(
                ft.Text(f"Numero totale di attori selezionati: {len(best_group)}")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero complessivo di film della soluzione ottima: {best_num_movies}")
            )

            self._view.update_page()
        except Exception as ex:
            self._view.create_alert(f"Errore nella ricerca del gruppo di attori: {ex}")

    def _fillDDActors(self):
        self._view._ddActor.options.clear()
        all_actors = self._model.getAllActors()

        actorOptions = list(
            map(lambda a: ft.dropdown.Option(data=a, key=str(a), on_click=self._choiceActor), all_actors)
        )
        self._view._ddActor.options = actorOptions

        self._view.update_page()

    def _choiceActor(self, e):
        self._actorValue = e.control.data
