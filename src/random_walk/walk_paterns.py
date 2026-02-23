"""Step models for 2D random walks."""

import math
import random


def seed(seed: int | None = None) -> None:
    """
    Seed the global random generator used by step models.

    Args:
        seed (int | None): Seed value for the RNG.

    Returns:
        None.
    """
    random.seed(seed)


class StepModel:
    """
    Interface for step models.

    Methods:
        next_step: Return the next step delta.
    """

    def next_step(self) -> tuple[float, float]:
        """
        Return the next (dx, dy) step.

        Args:
            None.

        Returns:
            tuple[float, float]: Delta step.

        Raises:
            NotImplementedError: Always, must be implemented by subclasses.
        """
        raise NotImplementedError


class Grid4(StepModel):
    """
    Random step on a 4-neighbor grid.

    Returns steps to N, S, E, or W.
    """

    def next_step(self) -> tuple[float, float]:
        """
        Return a step to N, S, E, or W.

        Args:
            None.

        Returns:
            tuple[float, float]: Delta step.
        """
        # Tirage uniforme parmi les 4 directions cardinales.
        dx, dy = random.choice([(1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)])
        return (dx, dy)


class Grid8(StepModel):
    """
    Random step on a 8-neighbor grid (including diagonals).

    Returns steps to N, S, E, W, NE, NW, SE, or SW.
    """

    def next_step(self) -> tuple[float, float]:
        """
        Return a step to the 8 grid neighbors.

        Args:
            None.

        Returns:
            tuple[float, float]: Delta step.
        """
        # Tirage uniforme parmi les 8 directions (incluant diagonales).
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
    """
    Random step uniformly sampled in a disk of given radius.

    Args:
        radius (float): Maximum step radius.

    Attributes:
        radius (float): Maximum step radius.
    """

    def __init__(self, radius: float = 2.0) -> None:
        """
        Create a continuous step model with a max radius.

        Args:
            radius (float): Maximum step radius.

        Returns:
            None.
        """
        self.radius = radius

    def sample_delta(self, rng) -> tuple[float, float]:
        """
        Sample a delta using the provided RNG.

        Args:
            rng (random.Random): Random number generator to sample from.

        Returns:
            tuple[float, float]: Delta step.
        """
        # Echantillonnage uniforme dans un disque de rayon fixe.
        u = rng.random()  # U ~ Uniform(0,1)
        theta = rng.uniform(0.0, 2 * math.pi)
        r = self.radius * math.sqrt(u)
        dx = r * math.cos(theta)
        dy = r * math.sin(theta)
        return dx, dy

    def next_step(self) -> tuple[float, float]:
        """
        Return a step sampled from the global RNG.

        Args:
            None.

        Returns:
            tuple[float, float]: Delta step.
        """
        return self.sample_delta(random)
