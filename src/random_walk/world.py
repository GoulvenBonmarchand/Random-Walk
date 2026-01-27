from walker import Walker

class World:
    def __init__(self, step_model, nmb_walkers = 1) -> None:
        self._walkers = [Walker(step_model) for _ in range(nmb_walkers)]

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

    def simulate(self, nmb_steps : int) -> None:
        for _ in range(nmb_steps):
            self.step()

    

