import argparse
from types import SimpleNamespace

import pytest

import random_walk.main as main_mod
from random_walk import parser as parser_mod


class DummyParser:
    def __init__(self, args):
        self._args = args

    def parse_args(self):
        return self._args


def test_non_negative_int_validation() -> None:
    assert parser_mod._non_negative_int("0") == 0
    assert parser_mod._non_negative_int("5") == 5
    with pytest.raises(argparse.ArgumentTypeError):
        parser_mod._non_negative_int("-1")
    with pytest.raises(argparse.ArgumentTypeError):
        parser_mod._non_negative_int("abc")


def test_positive_int_validation() -> None:
    assert parser_mod._positive_int("1") == 1
    assert parser_mod._positive_int("9") == 9
    with pytest.raises(argparse.ArgumentTypeError):
        parser_mod._positive_int("0")
    with pytest.raises(argparse.ArgumentTypeError):
        parser_mod._positive_int("-3")
    with pytest.raises(argparse.ArgumentTypeError):
        parser_mod._positive_int("nope")


def test_main_text_writes_output(tmp_path, monkeypatch) -> None:
    output = tmp_path / "walk.txt"
    args = SimpleNamespace(
        seed=123,
        pattern="grid4",
        walkers=1,
        fps=24,
        steps=2,
        display="text",
        output=str(output),
        verbose=2,
    )
    monkeypatch.setattr(main_mod, "build_parser", lambda: DummyParser(args))

    main_mod.main()

    lines = output.read_text().strip().splitlines()
    assert lines[0] == "# Walker 0"
    assert len(lines) == args.steps + 2
    for line in lines[1:]:
        x_str, y_str = line.split()
        float(x_str)
        float(y_str)


def test_main_unknown_pattern_raises(tmp_path, monkeypatch) -> None:
    args = SimpleNamespace(
        seed=1,
        pattern="unknown",
        walkers=1,
        fps=24,
        steps=1,
        display="text",
        output=str(tmp_path / "ignored.txt"),
        verbose=0,
    )
    monkeypatch.setattr(main_mod, "build_parser", lambda: DummyParser(args))

    with pytest.raises(ValueError, match="Unknown pattern"):
        main_mod.main()
