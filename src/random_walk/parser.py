"""Argument parser for the random walk CLI."""

import argparse


def _non_negative_int(value: str) -> int:
    """
    Parse a non-negative integer value.

    Args:
        value (str): Input string to parse.

    Returns:
        int: Parsed integer (>= 0).

    Raises:
        argparse.ArgumentTypeError: If the value is not a non-negative integer.
    """
    try:
        ivalue = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("doit être un entier") from exc
    if ivalue < 0:
        raise argparse.ArgumentTypeError("doit être >= 0")
    return ivalue


def _positive_int(value: str) -> int:
    """
    Parse a positive integer value.

    Args:
        value (str): Input string to parse.

    Returns:
        int: Parsed integer (>= 1).

    Raises:
        argparse.ArgumentTypeError: If the value is not a positive integer.
    """
    try:
        ivalue = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("doit être un entier") from exc
    if ivalue < 1:
        raise argparse.ArgumentTypeError("doit être >= 1")
    return ivalue


def build_parser() -> argparse.ArgumentParser:
    """
    Create and return the CLI argument parser.

    Args:
        None.

    Returns:
        argparse.ArgumentParser: Configured argument parser.
    """
    p = argparse.ArgumentParser(
        prog="random-walk-2d",
        description="Simulation d'une marche aléatoire 2D (POO) avec affichage configurable.",
    )

    p.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Graine pour l'initialisation du générateur de nombres aléatoires. Par défaut, une graine aléatoire est utilisée.",
    )
    p.add_argument(
        "--steps",
        type=_non_negative_int,
        default=1000,
        help="Nombre de pas de la marche aléatoire.",
    )
    p.add_argument(
        "--fps",
        type=_positive_int,
        default=24,
        help="Nombre d'images par seconde (FPS) pour la simulation.",
    )
    p.add_argument(
        "--display",
        type=str,
        choices=["screen", "text", "both"],
        default="text",
        help=(
            "Mode d'affichage: screen pour l'interface, text pour ecrire les trajectoires dans un fichier .txt, "
            "both pour lancer l'interface puis ecrire le fichier a la fermeture."
        ),
    )
    p.add_argument(
        "-o",
        "--output",
        type=str,
        default="random_walk.txt",
        help="Fichier de sortie en mode text/both (par defaut: random_walk.txt).",
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Augmente la verbosité des logs (ex: -v, -vv).",
    )
    p.add_argument(
        "--walkers",
        type=_positive_int,
        default=1,
        help="Nombre de marcheurs à simuler.",
    )
    p.add_argument(
        "--pattern",
        type=str,
        choices=["grid4", "grid8", "continuous"],
        default="grid4",
        help="Modèle de marche aléatoire à utiliser parmi grid4, grid8 ou continuous.",
    )
    return p
