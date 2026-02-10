from .walk_paterns import seed, Grid4, Grid8, Continuous
from .world import World
from .parser import build_parser
from .screen import Screen

def main() -> None:
    args = build_parser().parse_args()
    seed(args.seed)
    
    if args.pattern == "grid4":
        step_model = Grid4
    elif args.pattern == "grid8":
        step_model = Grid8
    elif args.pattern == "continuous":
        step_model = Continuous
    else:
        raise ValueError(f"Unknown pattern: {args.pattern}")
    
    world = World(step_model, args.walkers)
    screen = Screen(world)
    screen.main_menue()
    
