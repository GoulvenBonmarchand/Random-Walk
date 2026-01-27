import argparse

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="random-walk-2d",
        description="Simulation d'une marche aléatoire 2D (POO) avec affichage.",
    )

    p.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Graine pour l'initialisation du générateur de nombres aléatoires.",
    )
    p.add_argument(
        "--steps",
        type=int,
        default=1000,
        help="Nombre de pas de la marche aléatoire.",
    )
    p.add_argument(
        "--walkers",
        type=int,
        default=1,
        help="Nombre de marcheurs à simuler.",
    )
    p.add_argument( 
        "--pattern", 
        type=str, 
        choices=["grid4", "grid8"], 
        default="grid4", 
        help="Modèle de marche aléatoire à utiliser." )
    return p