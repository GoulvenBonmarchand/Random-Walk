from walker import Walker

class World:
    def __init__(self, step_model, nmb_walkers) -> None:
        self._walkers = [Walker(step_model) for _ in range(nmb_walkers)]

    def add_walker(self, walker : Walker) -> None:
        self._walkers.append(walker)

    def step(self) -> None:
        for walker in self._walkers:
            walker.walk()

    def simulate(self, nmb_steps : int) -> None:
        for _ in range(nmb_steps):
            self.step()
        
    def to_file(self, filename : str) -> None:
        with open(filename, "w") as f:
            for i, walker in enumerate(self._walkers):
                f.write(f"# Walker {i}\n")
                for x, y in walker.chemin:
                    f.write(f"{x} {y}\n")
                f.write("\n")

    

