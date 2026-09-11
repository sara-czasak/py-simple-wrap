"""
easy_game is built on top of pygame to simplify the tricky parts of
building games.
"""

import pygame

ALLOWED_KEYS = [i for i in dir(pygame) if i.startswith("K_")]


class EasyGameError(Exception):
    """
    Raised when a pygame window/game can't be set up.

    Wraps whatever pygame raises internally (bad dimensions, display
    driver issues, etc.) so py_simple functions can fail with one
    consistent, easy-to-read exception instead of a random builtin
    or pygame-specific one.

    Args:
        message (str): Human-readable description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def basic_game_setup(width: int, height: int, title: str = "My Game") -> tuple:
    """
    Sets up a pygame window and clock in one call, handling the
    pygame.init(), display, caption, and clock boilerplate every
    pygame project needs before the game loop can start.

    Args:
        width (int): Width of the game window, in pixels.
        height (int): Height of the game window, in pixels.
        title (str, optional): Text shown in the window's title bar.
            Defaults to `"My Game"`.

    Returns:
        tuple: `(screen, clock)`, where `screen` is the pygame
            `Surface` returned by `pygame.display.set_mode()` and
            `clock` is a `pygame.time.Clock` instance.

    Raises:
        EasyGameError: If pygame fails to initialize or set up the
            window (e.g. invalid width/height, display driver issue).

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import basic_game_setup

            screen, clock = basic_game_setup(800, 600, "My Game")
            ```

        === "The Traditional Way"
            ```python
            import pygame

            pygame.init()
            screen = pygame.display.set_mode((800, 600))
            pygame.display.set_caption("My Game")
            clock = pygame.time.Clock()
            ```
    """
    try:
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        clock = pygame.time.Clock()
        return screen, clock
    except Exception as e:
        raise EasyGameError(str(e)) from None


def check_if_quit() -> bool:
    """
    Checks the pygame event queue for a quit event (e.g. the window's
    close button), saving you from writing the `for event in
    pygame.event.get()` loop yourself every frame.

    Returns:
        bool: `True` if a quit event was found in the queue, `False`
            otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import check_if_quit

            running = True
            while running:
                if check_if_quit():
                    running = False
            ```

        === "The Traditional Way"
            ```python
            import pygame

            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
            ```
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False


def get_mouse_position() -> tuple:
    """
    Gets the current position of the mouse cursor, saving you from
    remembering the exact pygame call.

    Returns:
        tuple: `(x, y)` coordinates of the mouse cursor, in pixels,
            relative to the top-left corner of the window.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_mouse_position

            x, y = get_mouse_position()
            ```

        === "The Traditional Way"
            ```python
            import pygame

            x, y = pygame.mouse.get_pos()
            ```
    """
    return pygame.mouse.get_pos()


def is_left_mouse_button_clicked() -> bool:
    """
    Checks whether the left mouse button is currently held down.

    Returns:
        bool: `True` if the left mouse button is being pressed,
            `False` otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_left_mouse_button_clicked

            if is_left_mouse_button_clicked():
                print("Left click!")
            ```

        === "The Traditional Way"
            ```python
            import pygame

            if pygame.mouse.get_pressed()[0]:
                print("Left click!")
            ```
    """
    return pygame.mouse.get_pressed()[0]


def is_middle_mouse_button_clicked() -> bool:
    """
    Checks whether the middle mouse button (scroll wheel) is
    currently held down.

    Returns:
        bool: `True` if the middle mouse button is being pressed,
            `False` otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_middle_mouse_button_clicked

            if is_middle_mouse_button_clicked():
                print("Middle click!")
            ```

        === "The Traditional Way"
            ```python
            import pygame

            if pygame.mouse.get_pressed()[1]:
                print("Middle click!")
            ```
    """
    return pygame.mouse.get_pressed()[1]


def is_right_mouse_button_clicked() -> bool:
    """
    Checks whether the right mouse button is currently held down.

    Returns:
        bool: `True` if the right mouse button is being pressed,
            `False` otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_right_mouse_button_clicked

            if is_right_mouse_button_clicked():
                print("Right click!")
            ```

        === "The Traditional Way"
            ```python
            import pygame

            if pygame.mouse.get_pressed()[2]:
                print("Right click!")
            ```
    """
    return pygame.mouse.get_pressed()[2]


def fill_background(screen: pygame.Surface, color: tuple = (0, 0, 0)) -> None:
    """
    Fills the entire game screen with a solid background color,
    saving you from writing screen clearing boilerplate every frame.

    Args:
        screen (pygame.Surface): The pygame surface to fill.
        color (tuple, optional): RGB tuple for the background color.
            Defaults to black `(0, 0, 0)`.

    Returns:
        None

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import basic_game_setup, fill_background

            screen, clock = basic_game_setup(800, 600)
            fill_background(screen, (30, 30, 30))
            ```

        === "The Traditional Way"
            ```python
            import pygame

            screen = pygame.display.set_mode((800, 600))
            screen.fill((30, 30, 30))
            ```
    """
    try:
        screen.fill(color)
    except Exception as e:
        raise EasyGameError(str(e)) from None


def is_key_pressed(key_name: str) -> bool:
    """
    Checks whether a specific keyboard key is currently held down,
    saving you from remembering key constant imports and state arrays.

    Args:
        key_name (str): The name of the key (e.g., `"SPACE"`, `"RETURN"`, `"UP"`).

    Returns:
        bool: `True` if the specified key is being pressed, `False` otherwise.

    Raises:
        EasyGameError: If an invalid key name is provided.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_key_pressed

            if is_key_pressed("SPACE"):
                print("Spacebar held down!")
            ```

        === "The Traditional Way"
            ```python
            import pygame

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                print("Spacebar held down!")
            ```
    """
    try:
        full_key_name = f"K_{key_name.upper()}"
        if not hasattr(pygame, full_key_name):
            raise EasyGameError(f"Invalid key name: '{key_name}'")
        key_constant = getattr(pygame, full_key_name)
        return bool(pygame.key.get_pressed()[key_constant])
    except Exception as e:
        if isinstance(e, EasyGameError):
            raise
        raise EasyGameError(str(e)) from None
