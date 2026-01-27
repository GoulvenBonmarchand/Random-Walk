class World:
    def __init__(self, nmb_walkers = 1, step_model = None) -> None:
        self._walkers = [Walker() for _ in range(nmb_walkers)]

    def add_walker(self, walker : Walker) -> None:
        self._walkers.append(walker)

    @property
    def hwidth(self) -> int:
        return self._hwidth
    
    @property
    def hheight(self) -> int:
        return self._hheight

    def step(self) -> None:
        for walker in self._walkers:
            walker.walk()

    

