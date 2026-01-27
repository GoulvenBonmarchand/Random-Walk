from walk_paterns import seed, Grid4, Grid8, Continuous
from world import World
from parser import build_parser

def main() -> None:
    print("In development...")
    args = build_parser().parse_args()
    seed(args.seed)