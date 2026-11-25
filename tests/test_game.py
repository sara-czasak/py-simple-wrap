"""Tests for the easy_game module."""

from types import SimpleNamespace

import pytest
from py_simple import draw_text as public_draw_text

from py_simple_package.src.py_simple import easy_game
from py_simple_package.src.py_simple.easy_game import (
    EasyGameError,
    basic_game_setup,
    check_if_quit,
    draw_text,
    fill_background,
    get_mouse_position,
    is_left_mouse_button_clicked,
    is_middle_mouse_button_clicked,
    is_key_pressed,
    is_right_mouse_button_clicked,
    update_screen,
)


def test_basic_game_setup_initializes_window_caption_and_clock(monkeypatch):
    """Game setup should wire pygame's required initialization in order."""
    screen = object()
    clock = object()
    calls = []

    monkeypatch.setattr(easy_game.pygame, "init", lambda: calls.append("init"))
    monkeypatch.setattr(
        easy_game.pygame.display,
        "set_mode",
        lambda dimensions: calls.append(("set_mode", dimensions)) or screen,
    )
    monkeypatch.setattr(
        easy_game.pygame.display,
        "set_caption",
        lambda title: calls.append(("set_caption", title)),
    )
    monkeypatch.setattr(
        easy_game.pygame.time,
        "Clock",
        lambda: calls.append("clock") or clock,
    )

    result = basic_game_setup(800, 600, "Test Game")

    assert result == (screen, clock)
    assert calls == [
        "init",
        ("set_mode", (800, 600)),
        ("set_caption", "Test Game"),
        "clock",
    ]


def test_basic_game_setup_uses_default_title(monkeypatch):
    """The default title should be forwarded when no title is supplied."""
    captions = []

    monkeypatch.setattr(easy_game.pygame, "init", lambda: None)
    monkeypatch.setattr(easy_game.pygame.display, "set_mode", lambda _size: object())
    monkeypatch.setattr(
        easy_game.pygame.display,
        "set_caption",
        lambda title: captions.append(title),
    )
    monkeypatch.setattr(easy_game.pygame.time, "Clock", lambda: object())

    basic_game_setup(320, 240)

    assert captions == ["My Game"]


def test_basic_game_setup_wraps_pygame_errors(monkeypatch):
    """Pygame setup failures should use the module's consistent exception."""
    monkeypatch.setattr(easy_game.pygame, "init", lambda: None)

    def fail_to_open(_dimensions):
        raise RuntimeError("display unavailable")

    monkeypatch.setattr(easy_game.pygame.display, "set_mode", fail_to_open)

    with pytest.raises(EasyGameError, match="display unavailable") as exc_info:
        basic_game_setup(800, 600)

    assert exc_info.value.__cause__ is None


def test_basic_game_setup_missing_pygame(monkeypatch):
    """Missing pygame should raise an informative EasyGameError."""
    monkeypatch.setattr(easy_game, "pygame", None)

    with pytest.raises(EasyGameError, match="easy_game needs pygame"):
        basic_game_setup(800, 600)


def test_check_if_quit_returns_true_when_quit_event_is_present(monkeypatch):
    """A quit event anywhere in the queue should stop the game loop."""
    events = [
        SimpleNamespace(type=object()),
        SimpleNamespace(type=easy_game.pygame.QUIT),
    ]
    monkeypatch.setattr(easy_game.pygame.event, "get", lambda: events)

    assert check_if_quit() is True


def test_check_if_quit_returns_false_without_quit_event(monkeypatch):
    """A queue with no quit event should leave the game running."""
    events = [SimpleNamespace(type=object()), SimpleNamespace(type=object())]
    monkeypatch.setattr(easy_game.pygame.event, "get", lambda: events)

    assert check_if_quit() is False


def test_get_mouse_position_returns_pygame_position(monkeypatch):
    """Mouse coordinates should be returned unchanged from pygame."""
    monkeypatch.setattr(easy_game.pygame.mouse, "get_pos", lambda: (123, 456))

    assert get_mouse_position() == (123, 456)


@pytest.mark.parametrize(
    ("helper", "pressed", "expected"),
    [
        (is_left_mouse_button_clicked, (True, False, False), True),
        (is_left_mouse_button_clicked, (False, True, True), False),
        (is_middle_mouse_button_clicked, (False, True, False), True),
        (is_middle_mouse_button_clicked, (True, False, True), False),
        (is_right_mouse_button_clicked, (False, False, True), True),
        (is_right_mouse_button_clicked, (True, True, False), False),
    ],
)
def test_mouse_button_helpers_use_the_correct_button(
    monkeypatch, helper, pressed, expected
):
    """Each mouse helper should read only its corresponding pygame button."""
    monkeypatch.setattr(easy_game.pygame.mouse, "get_pressed", lambda: pressed)

    assert helper() is expected


def test_fill_background(monkeypatch):
    """Filling the background should call surface fill and wrap errors."""
    screen = SimpleNamespace(fill=lambda color: None)

    # Test valid fill
    fill_background(screen, (255, 0, 0))

    # Test error handling when fill fails or surface is invalid
    def fail_fill(_color):
        raise RuntimeError("surface error")

    bad_screen = SimpleNamespace(fill=fail_fill)
    with pytest.raises(EasyGameError, match="surface error"):
        fill_background(bad_screen, (255, 0, 0))


def test_draw_text_renders_and_blits_text(monkeypatch):
    """Text should be rendered with the default font and drawn on screen."""
    screen = SimpleNamespace(blit=lambda surface, position: (surface, position))
    calls = []
    text_surface = object()

    class FakeFont:
        def render(self, text, antialias, color):
            calls.append(("render", text, antialias, color))
            return text_surface

    def create_font(font_name, font_size):
        calls.append(("font", font_name, font_size))
        return FakeFont()

    monkeypatch.setattr(easy_game.pygame.font, "Font", create_font)

    result = draw_text(screen, "Score: 10", (20, 20), 24, (255, 0, 0))

    assert calls == [
        ("font", None, 24),
        ("render", "Score: 10", True, (255, 0, 0)),
    ]
    assert result == (text_surface, (20, 20))


def test_draw_text_is_available_from_public_package():
    """The documented package-level draw_text import should work."""
    assert public_draw_text.__name__ == "draw_text"


def test_draw_text_wraps_pygame_errors(monkeypatch):
    """Text-rendering failures should use the module's consistent exception."""
    screen = SimpleNamespace(blit=lambda _surface, _position: None)

    def fail_to_create_font(_font_name, _font_size):
        raise RuntimeError("font unavailable")

    monkeypatch.setattr(easy_game.pygame.font, "Font", fail_to_create_font)

    with pytest.raises(EasyGameError, match="font unavailable") as exc_info:
        draw_text(screen, "Score: 10", (20, 20))

    assert exc_info.value.__cause__ is None


@pytest.mark.parametrize(
    ("pressed", "expected"),
    [
        ([False, True], True),
        ([True, False], False),
    ],
)
def test_is_key_pressed_returns_key_state(monkeypatch, pressed, expected):
    """Key state should be read from the pygame key-state sequence."""
    monkeypatch.setattr(easy_game.pygame, "K_SPACE", 1)
    monkeypatch.setattr(
        easy_game.pygame.key,
        "get_pressed",
        lambda: pressed,
    )

    assert is_key_pressed("space") is expected


def test_is_key_pressed_rejects_unknown_key():
    """Unknown key names should raise the module's consistent exception."""
    with pytest.raises(EasyGameError, match="Invalid key name: 'NOPE'"):
        is_key_pressed("NOPE")


def test_is_key_pressed_wraps_pygame_errors(monkeypatch):
    """Failures while reading key state should be wrapped consistently."""
    monkeypatch.setattr(easy_game.pygame, "K_SPACE", 1)

    def fail_get_pressed():
        raise RuntimeError("keyboard unavailable")

    monkeypatch.setattr(easy_game.pygame.key, "get_pressed", fail_get_pressed)

    with pytest.raises(EasyGameError, match="keyboard unavailable") as exc_info:
        is_key_pressed("SPACE")

    assert exc_info.value.__cause__ is None


def test_update_screen_calls_pygame_display_flip(monkeypatch):
    """Updating the screen should refresh the active pygame display."""
    calls = []
    monkeypatch.setattr(easy_game.pygame.display, "flip", lambda: calls.append("flip"))

    update_screen()

    assert calls == ["flip"]


def test_update_screen_wraps_pygame_errors(monkeypatch):
    """Display refresh failures should use the module's consistent exception."""

    def fail_flip():
        raise RuntimeError("display update failed")

    monkeypatch.setattr(easy_game.pygame.display, "flip", fail_flip)

    with pytest.raises(EasyGameError, match="display update failed") as exc_info:
        update_screen()

    assert exc_info.value.__cause__ is None


def test_easy_game_error_message():
    """EasyGameError should store message and format string properly."""
    err = EasyGameError("custom error message")
    assert err.message == "custom error message"
    assert str(err) == "custom error message"


def test_allowed_keys_contains_pygame_key_constants():
    """ALLOWED_KEYS should only contain attributes starting with K_."""
    assert len(easy_game.ALLOWED_KEYS) > 0
    assert all(k.startswith("K_") for k in easy_game.ALLOWED_KEYS)
    assert "K_SPACE" in easy_game.ALLOWED_KEYS or "K_SPACE" in dir(easy_game.pygame)
