import math
import random
from pathlib import Path

from random_walk.walk_paterns import Continuous, Grid4, Grid8, seed
from random_walk.parser import build_parser
from random_walk.walker import Walker
from random_walk.world import World


# Modeles deterministes pour tester les trajectoires.
# Ils permettent de verifier des positions exactes sans alea.
class FixedStepModel:
    def __init__(self, dx=1.0, dy=-1.0) -> None:
        self.dx = dx
        self.dy = dy

    def next_step(self):
        return (self.dx, self.dy)


class SequenceStepModel:
    def __init__(self):
        self._steps = [(1.0, 0.0), (0.0, 2.0), (-3.0, 0.5)]
        self._i = 0

    def next_step(self):
        step = self._steps[self._i % len(self._steps)]
        self._i += 1
        return step


def test_grid4_reproducible_with_seed() -> None:
    seed(123)
    m1 = Grid4()
    steps1 = [m1.next_step() for _ in range(6)]

    seed(123)
    m2 = Grid4()
    steps2 = [m2.next_step() for _ in range(6)]

    assert steps1 == steps2
    allowed = {(1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)}
    for dx, dy in steps1:
        assert (dx, dy) in allowed


def test_grid8_reproducible_with_seed() -> None:
    seed(999)
    m1 = Grid8()
    steps1 = [m1.next_step() for _ in range(8)]

    seed(999)
    m2 = Grid8()
    steps2 = [m2.next_step() for _ in range(8)]

    assert steps1 == steps2
    allowed = {
        (1.0, 0.0),
        (-1.0, 0.0),
        (0.0, 1.0),
        (0.0, -1.0),
        (1.0, 1.0),
        (1.0, -1.0),
        (-1.0, 1.0),
        (-1.0, -1.0),
    }
    for dx, dy in steps1:
        assert (dx, dy) in allowed


def test_continuous_stays_within_radius() -> None:
    model = Continuous(radius=2.5)
    rng = random.Random(42)
    for _ in range(50):
        dx, dy = model.sample_delta(rng)
        dist = math.hypot(dx, dy)
        assert dist <= 2.5 + 1e-12


def test_continuous_zero_radius() -> None:
    model = Continuous(radius=0.0)
    dx, dy = model.next_step()
    assert (dx, dy) == (0.0, 0.0)


def test_walker_initial_state() -> None:
    walker = Walker(FixedStepModel)
    assert walker.position == (0.0, 0.0)
    assert walker.chemin == [(0.0, 0.0)]


def test_walker_walk_updates_position_and_path() -> None:
    walker = Walker(FixedStepModel)
    walker.walk()
    assert walker.position == (1.0, -1.0)
    assert walker.chemin == [(0.0, 0.0), (1.0, -1.0)]


def test_walker_accumulates_multiple_steps() -> None:
    walker = Walker(SequenceStepModel)
    walker.walk()
    walker.walk()
    walker.walk()
    assert walker.position == (-2.0, 2.5)
    assert walker.chemin == [(0.0, 0.0), (1.0, 0.0), (1.0, 2.0), (-2.0, 2.5)]


def test_world_step_moves_all_walkers() -> None:
    world = World(FixedStepModel, 2)
    world.step()
    positions = [w.position for w in world._walkers]
    assert positions == [(1.0, -1.0), (1.0, -1.0)]


def test_world_simulate_advances_steps() -> None:
    world = World(FixedStepModel, 1)
    world.simulate(3)
    walker = world._walkers[0]
    assert walker.position == (3.0, -3.0)
    assert len(walker.chemin) == 4


def test_world_add_walker() -> None:
    world = World(FixedStepModel, 1)
    world.add_walker(Walker(FixedStepModel))
    assert len(world._walkers) == 2


def test_world_to_file_output(tmp_path: Path) -> None:
    world = World(FixedStepModel, 1)
    world.simulate(2)
    path = tmp_path / "walk.txt"
    world.to_file(str(path))
    content = path.read_text().strip().splitlines()

    assert content[0] == "# Walker 0"
    assert content[1] == "0.0 0.0"
    assert content[2] == "1.0 -1.0"
    assert content[3] == "2.0 -2.0"


def test_parser_defaults() -> None:
    parser = build_parser()
    args = parser.parse_args([])
    assert args.seed is None
    assert args.steps == 1000
    assert args.fps == 24
    assert args.verbose == 0
    assert args.walkers == 1
    assert args.pattern == "grid4"


def test_parser_custom_args() -> None:
    parser = build_parser()
    args = parser.parse_args(
        ["--seed", "5", "--steps", "10", "--fps", "30", "-vv", "--walkers", "3", "--pattern", "grid8"]
    )
    assert args.seed == 5
    assert args.steps == 10
    assert args.fps == 30
    assert args.verbose == 2
    assert args.walkers == 3
    assert args.pattern == "grid8"
