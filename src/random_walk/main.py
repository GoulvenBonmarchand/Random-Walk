"""Program entry point for the random walk simulation."""

import logging

from .walk_paterns import seed, Grid4, Grid8, Continuous
from .world import World
from .parser import build_parser


def main() -> None:
    """
    Run the CLI entry point and start the simulation.

    Args:
        None.

    Returns:
        None.

    Raises:
        ValueError: If an unknown pattern is provided.
    """
    args = build_parser().parse_args()

    log_level = logging.WARNING
    if args.verbose == 1:
        log_level = logging.INFO
    elif args.verbose >= 2:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level, format="%(levelname)s:%(name)s:%(message)s")
    logger = logging.getLogger(__name__)

    logger.info("Demarrage de la simulation")
    seed(args.seed)
    logger.info(
        "Seed=%s, pattern=%s, walkers=%s, fps=%s, steps=%s, display=%s",
        args.seed,
        args.pattern,
        args.walkers,
        args.fps,
        args.steps,
        args.display,
    )

    if args.pattern == "grid4":
        step_model = Grid4
    elif args.pattern == "grid8":
        step_model = Grid8
    elif args.pattern == "continuous":
        step_model = Continuous
    else:
        raise ValueError(f"Unknown pattern: {args.pattern}")

    world = World(step_model, args.walkers)
    if args.display == "screen":
        from .screen import Screen

        screen = Screen(world, simulation_fps=args.fps, max_steps=args.steps)
        logger.info("Interface lancee")
        screen.main_menue()
    else:
        world.simulate(args.steps)
        world.to_file(args.output)
        logger.info("Trajectoires ecrites dans %s", args.output)
