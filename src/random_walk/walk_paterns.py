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

class Continuous(StepModel):
    def __init__(self, radius=2.0:float) -> None:
        self.radius = radius
    def sample_delta(self, rng) -> tuple[float, float]:
        u = rng.random()                 # U ~ Uniform(0,1)
        theta = rng.uniform(0.0, 2 * math.pi)
        r = self.radius * math.sqrt(u)   # correction d'aire
        dx = r * math.cos(theta)
        dy = r * math.sin(theta)
        return dx, dy