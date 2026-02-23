import importlib
import sys
from types import ModuleType, SimpleNamespace

from random_walk.button import Button
from random_walk.world import World


class DummyRect:
    def __init__(self, center=(0, 0), size=(100, 50)) -> None:
        cx, cy = center
        w, h = size
        self.left = int(cx - w / 2)
        self.right = int(cx + w / 2)
        self.top = int(cy - h / 2)
        self.bottom = int(cy + h / 2)


class DummySurface:
    def __init__(self, size=(10, 10)) -> None:
        self._size = size
        self.blit_calls = []

    def get_rect(self, center=None):
        return DummyRect(center=center or (0, 0))

    def fill(self, _color):
        return None

    def blit(self, *args, **kwargs):
        self.blit_calls.append((args, kwargs))

    def get_size(self):
        return self._size


class DummyFont:
    def __init__(self) -> None:
        self.last_text = None
        self.last_color = None

    def render(self, text, _antialias, color):
        self.last_text = text
        self.last_color = color
        return DummySurface()


class FixedStepModel:
    def __init__(self, dx=1.0, dy=0.0) -> None:
        self._dx = dx
        self._dy = dy

    def next_step(self):
        return (self._dx, self._dy)


def make_fake_pygame(mouse_pos=(0, 0)) -> ModuleType:
    fake = ModuleType("pygame")
    fake.QUIT = 256
    fake.MOUSEBUTTONDOWN = 1025
    fake.KEYDOWN = 768
    fake.K_ESCAPE = 27
    fake.K_SPACE = 32
    fake.K_p = ord("p")

    event_queue = []

    def set_events(sequence):
        event_queue.clear()
        event_queue.extend(sequence)

    def get_events():
        if event_queue:
            return event_queue.pop(0)
        return []

    class DummyClock:
        def tick(self, _fps):
            return None

    class FakeColor:
        def __init__(self, *_args, **_kwargs) -> None:
            self.hsva = None

    fake.init = lambda: None
    fake.event = SimpleNamespace(get=get_events)
    fake.mouse = SimpleNamespace(get_pos=lambda: mouse_pos)
    fake.time = SimpleNamespace(Clock=lambda: DummyClock())
    fake.font = SimpleNamespace(SysFont=lambda _name, _size: DummyFont())
    fake.display = SimpleNamespace(
        set_mode=lambda size: DummySurface(size=size),
        set_caption=lambda _caption: None,
        update=lambda: None,
        flip=lambda: None,
    )
    fake.Color = FakeColor
    fake.draw = SimpleNamespace(lines=lambda *_args, **_kwargs: None, circle=lambda *_args, **_kwargs: None)
    fake._set_events = set_events
    return fake


def import_screen(monkeypatch, fake_pygame):
    monkeypatch.setitem(sys.modules, "pygame", fake_pygame)
    if "random_walk.screen" in sys.modules:
        del sys.modules["random_walk.screen"]
    return importlib.import_module("random_walk.screen")


def test_button_hit_testing_and_colors() -> None:
    font = DummyFont()
    screen = DummySurface()
    btn = Button("Go", (10, 10), font, screen, base_color="white", hovering_color="green")

    assert btn.check_for_input((10, 10)) is True
    assert btn.check_for_input((1000, 1000)) is False

    btn.change_color((10, 10))
    assert font.last_color == "green"
    btn.change_color((1000, 1000))
    assert font.last_color == "white"


def test_button_no_label_short_circuits_color_change() -> None:
    font = DummyFont()
    screen = DummySurface()
    surface = DummySurface()
    btn = Button(surface, (5, 5), font, screen)

    font.last_color = None
    btn.change_color((5, 5))
    assert font.last_color is None


def test_button_update_with_image() -> None:
    font = DummyFont()
    screen = DummySurface()
    image = DummySurface()
    btn = Button("Img", (3, 3), font, screen, image=image)

    btn.update()
    assert len(screen.blit_calls) == 2


def test_screen_main_menu_quit_button(monkeypatch) -> None:
    fake = make_fake_pygame(mouse_pos=(640, 500))
    fake._set_events([[SimpleNamespace(type=fake.MOUSEBUTTONDOWN)]])
    screen_mod = import_screen(monkeypatch, fake)

    world = World(FixedStepModel, 1)
    ui = screen_mod.Screen(world, simulation_fps=1, max_steps=1)
    ui.main_menue()


def test_screen_simulation_pause_and_max_steps(monkeypatch) -> None:
    fake = make_fake_pygame()
    fake._set_events(
        [
            [SimpleNamespace(type=fake.KEYDOWN, key=fake.K_SPACE)],
            [SimpleNamespace(type=fake.KEYDOWN, key=fake.K_SPACE)],
        ]
    )
    screen_mod = import_screen(monkeypatch, fake)

    world = World(FixedStepModel, 1)
    ui = screen_mod.Screen(world, simulation_fps=1, max_steps=1)
    ui.simulation()

    assert world._walkers[0].position == (1.0, 0.0)


def test_screen_simulation_quit_event(monkeypatch) -> None:
    fake = make_fake_pygame()
    fake._set_events([[SimpleNamespace(type=fake.QUIT)]])
    screen_mod = import_screen(monkeypatch, fake)

    world = World(FixedStepModel, 1)
    ui = screen_mod.Screen(world, simulation_fps=1, max_steps=None)
    ui.simulation()

    assert world._walkers[0].position == (1.0, 0.0)
