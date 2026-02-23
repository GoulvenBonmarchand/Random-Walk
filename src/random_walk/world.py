"""World container for multiple walkers and simulation helpers."""

import logging

from .walker import Walker

logger = logging.getLogger(__name__)


class World:
    """
    Collection of walkers and batch simulation utilities.

    Args:
        step_model (type): Callable returning a step model instance.
        nmb_walkers (int): Number of walkers to create.
    """

    def __init__(self, step_model, nmb_walkers: int) -> None:
        """
        Create a world with a given number of walkers.

        Args:
            step_model (type): Callable returning a step model instance.
            nmb_walkers (int): Number of walkers to create.

        Returns:
            None.
        """
        # Initialise une population de marcheurs independants.
        self._walkers = [Walker(step_model) for _ in range(nmb_walkers)]
        logger.debug("World cree avec %s marcheurs", nmb_walkers)

    def add_walker(self, walker: Walker) -> None:
        """
        Add an existing walker to the world.

        Args:
            walker (Walker): Walker instance to add.

        Returns:
            None.
        """
        self._walkers.append(walker)
        logger.info("Ajout d'un marcheur. Total=%s", len(self._walkers))

    def step(self) -> None:
        """
        Advance all walkers by one step.

        Args:
            None.

        Returns:
            None.
        """
        # Applique un pas a tous les marcheurs.
        for walker in self._walkers:
            walker.walk()

    def simulate(self, nmb_steps: int) -> None:
        """
        Run multiple steps of the simulation.

        Args:
            nmb_steps (int): Number of steps to run.

        Returns:
            None.
        """
        logger.debug("Simulation en mode batch: %s pas", nmb_steps)
        # Boucle de simulation simple, sans interface graphique.
        for _ in range(nmb_steps):
            self.step()

    def to_file(self, filename: str) -> None:
        """
        Write all walker paths to a text file.

        Args:
            filename (str): Path to the output file.

        Returns:
            None.
        """
        # Export texte: un bloc par marcheur, puis les points du trajet.
        with open(filename, "w") as f:
            for i, walker in enumerate(self._walkers):
                f.write(f"# Walker {i}\n")
                for x, y in walker.chemin:
                    f.write(f"{x} {y}\n")
                f.write("\n")
        logger.info("Trajectoires ecrites dans %s", filename)
