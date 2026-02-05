class Walker:
    def __init__(self, step_model) -> None:
        self._x = 0.0
        self._y = 0.0
        self._chemin = [(self._x, self._y)]
        self._model = step_model()
    
    @property
    def position(self) -> tuple[float, float]:
        return (self._x, self._y)

    @property
    def chemin(self) -> list[tuple[float, float]]:
        return self._chemin

    def walk(self) -> None:
        """
        Fait un pas : selon le modèle aléatoire choisi, met à jour la position du marcheur.
        """
        dx, dy = self._model.next_step()
        self._x += dx
        self._y += dy
        self._chemin.append((self._x, self._y))