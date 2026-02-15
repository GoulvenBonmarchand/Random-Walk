import math
import pathlib
import random
import tempfile
import unittest

from random_walk.walk_paterns import seed, Grid4, Grid8, Continuous
from random_walk.walker import Walker
from random_walk.world import World
from random_walk.parser import build_parser


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


class TestWalkPaterns(unittest.TestCase):
    def test_grid4_reproducible_with_seed(self) -> None:
        seed(123)
        m1 = Grid4()
        steps1 = [m1.next_step() for _ in range(6)]

        seed(123)
        m2 = Grid4()
        steps2 = [m2.next_step() for _ in range(6)]

        self.assertEqual(steps1, steps2)
        for dx, dy in steps1:
            self.assertIn((dx, dy), [(1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)])

    def test_grid8_reproducible_with_seed(self) -> None:
        seed(999)
        m1 = Grid8()
        steps1 = [m1.next_step() for _ in range(8)]

        seed(999)
        m2 = Grid8()
        steps2 = [m2.next_step() for _ in range(8)]

        self.assertEqual(steps1, steps2)
        for dx, dy in steps1:
            self.assertIn(
                (dx, dy),
                [
                    (1.0, 0.0),
                    (-1.0, 0.0),
                    (0.0, 1.0),
                    (0.0, -1.0),
                    (1.0, 1.0),
                    (1.0, -1.0),
                    (-1.0, 1.0),
                    (-1.0, -1.0),
                ],
            )

    def test_continuous_stays_within_radius(self) -> None:
        model = Continuous(radius=2.5)
        rng = random.Random(42)
        for _ in range(50):
            dx, dy = model.sample_delta(rng)
            dist = math.hypot(dx, dy)
            self.assertLessEqual(dist, 2.5 + 1e-12)

    def test_continuous_zero_radius(self) -> None:
        model = Continuous(radius=0.0)
        dx, dy = model.next_step()
        self.assertEqual((dx, dy), (0.0, 0.0))


class TestWalker(unittest.TestCase):
    def test_walker_initial_state(self) -> None:
        walker = Walker(FixedStepModel)
        self.assertEqual(walker.position, (0.0, 0.0))
        self.assertEqual(walker.chemin, [(0.0, 0.0)])

    def test_walker_walk_updates_position_and_path(self) -> None:
        walker = Walker(FixedStepModel)
        walker.walk()
        self.assertEqual(walker.position, (1.0, -1.0))
        self.assertEqual(walker.chemin, [(0.0, 0.0), (1.0, -1.0)])

    def test_walker_accumulates_multiple_steps(self) -> None:
        walker = Walker(SequenceStepModel)
        walker.walk()
        walker.walk()
        walker.walk()
        self.assertEqual(walker.position, (-2.0, 2.5))
        self.assertEqual(
            walker.chemin,
            [(0.0, 0.0), (1.0, 0.0), (1.0, 2.0), (-2.0, 2.5)],
        )


class TestWorld(unittest.TestCase):
    def test_world_step_moves_all_walkers(self) -> None:
        world = World(FixedStepModel, 2)
        world.step()
        positions = [w.position for w in world._walkers]
        self.assertEqual(positions, [(1.0, -1.0), (1.0, -1.0)])

    def test_world_simulate_advances_steps(self) -> None:
        world = World(FixedStepModel, 1)
        world.simulate(3)
        walker = world._walkers[0]
        self.assertEqual(walker.position, (3.0, -3.0))
        self.assertEqual(len(walker.chemin), 4)

    def test_world_add_walker(self) -> None:
        world = World(FixedStepModel, 1)
        world.add_walker(Walker(FixedStepModel))
        self.assertEqual(len(world._walkers), 2)

    def test_world_to_file_output(self) -> None:
        world = World(FixedStepModel, 1)
        world.simulate(2)
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "walk.txt"
            world.to_file(str(path))
            content = path.read_text().strip().splitlines()

        self.assertEqual(content[0], "# Walker 0")
        self.assertEqual(content[1], "0.0 0.0")
        self.assertEqual(content[2], "1.0 -1.0")
        self.assertEqual(content[3], "2.0 -2.0")


class TestParser(unittest.TestCase):
    def test_parser_defaults(self) -> None:
        parser = build_parser()
        args = parser.parse_args([])
        self.assertIsNone(args.seed)
        self.assertEqual(args.steps, 1000)
        self.assertEqual(args.walkers, 1)
        self.assertEqual(args.pattern, "grid4")

    def test_parser_custom_args(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--seed", "5", "--steps", "10", "--walkers", "3", "--pattern", "grid8"])
        self.assertEqual(args.seed, 5)
        self.assertEqual(args.steps, 10)
        self.assertEqual(args.walkers, 3)
        self.assertEqual(args.pattern, "grid8")


if __name__ == "__main__":
    unittest.main()
