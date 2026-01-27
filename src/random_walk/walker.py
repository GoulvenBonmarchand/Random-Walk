class Walker:
    def __init__(self) -> None:
        self._x = 0
        self._y = 0
    
    @property
    def position(self) -> tuple[int, int]:
        return (self._x, self._y)
    
    def walk(self, step_model) -> None:
        """
        Fait un pas : selon le modèle aléatoire choisi, met à jour la position du marcheur.
        """
        dx, dy = step_model.next_step()
        self._x += dx
        self._y += dy


