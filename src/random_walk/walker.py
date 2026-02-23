"""Walker state and stepping logic."""


class Walker:
    """
    Stateful random walker with a step model.

    Args:
        step_model (type): Callable returning a step model instance.
    """

    def __init__(self, step_model) -> None:
        """
        Initialize a walker at the origin using the step model factory.

        Args:
            step_model (type): Callable returning a step model instance.

        Returns:
            None.
        """
        self._x = 0.0
        self._y = 0.0
        self._chemin = [(self._x, self._y)]
        self._model = step_model()

    @property
    def position(self) -> tuple[float, float]:
        """
        Current (x, y) position.

        Args:
            None.

        Returns:
            tuple[float, float]: Current position.
        """
        return (self._x, self._y)

    @property
    def chemin(self) -> list[tuple[float, float]]:
        """
        List of positions visited so far.

        Args:
            None.

        Returns:
            list[tuple[float, float]]: Path history.
        """
        return self._chemin

    def walk(self) -> None:
        """
        Advance the walker by one step and update the path.

        Args:
            None.

        Returns:
            None.
        """
        dx, dy = self._model.next_step()
        self._x += dx
        self._y += dy
        self._chemin.append((self._x, self._y))
