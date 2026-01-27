import random

def seed(seed: int | None = None) -> None:
    random.seed(seed)

class StepModel:
    def next_step(self) -> tuple[float, float]:
        raise NotImplementedError

class Grid4(StepModel):
    def next_step(self) -> tuple[float, float]:
        # N, S, E, W
        dx, dy = random.choice([(1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)])
        return (dx, dy)

class Grid8(StepModel):
    def next_step(self) -> tuple[float, float]:
        # N, S, E, W, NE, NW, SE, SW
        dx, dy = random.choice(
            [
                (1.0, 0.0),
                (-1.0, 0.0),
                (0.0, 1.0),
                (0.0, -1.0),
                (1.0, 1.0),
                (1.0, -1.0),
                (-1.0, 1.0),
                (-1.0, -1.0),
            ]
        )
        return (dx, dy)
