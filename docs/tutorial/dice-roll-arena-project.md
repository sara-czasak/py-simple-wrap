# Building a Dice Roll Arena with Easy Random and Easy Game

Combine **Easy Random** and **Easy Game** to build a visual, interactive dice rolling game window with Pygame in just a few lines of Python.

## What we are building

Imagine you want to build a quick tabletop dice roller or mini-game where a player can click the window or press the spacebar to roll dice, rendering live game status on the screen without dealing with Pygame setup boilerplate.

```python
from py_simple import (
    basic_game_setup,
    check_if_quit,
    fill_background,
    draw_text,
    update_screen,
    is_key_pressed,
    is_left_mouse_button_clicked,
    roll_dice,
)

# 1. Initialize a 600x400 window with title and clock
screen, clock = basic_game_setup(600, 400, "Dice Roll Arena")

current_roll = roll_dice(6)
rolling = True
running = True

while running:
    # 2. Check if the user clicked the window's close button
    if check_if_quit():
        running = False

    # 3. Roll a new value when pressing SPACE or clicking the left mouse button
    if is_key_pressed("SPACE") or is_left_mouse_button_clicked():
        if not rolling:
            current_roll = roll_dice(6)
            rolling = True
    else:
        rolling = False

    # 4. Render the background and current dice result
    fill_background(screen, (30, 30, 40))
    draw_text(screen, "Dice Roll Arena", (200, 50), font_size=42, color=(255, 215, 0))
    draw_text(screen, f"You rolled: {current_roll}", (220, 160), font_size=48, color=(255, 255, 255))
    draw_text(screen, "Press SPACE or Click to Roll", (160, 280), font_size=28, color=(180, 180, 180))

    # 5. Flip display buffer and lock framerate
    update_screen()
    clock.tick(30)
```

## What happened?

1. `basic_game_setup(600, 400, "Dice Roll Arena")` initializes the Pygame engine, generates the window surface, sets the caption, and returns the screen and clock instances in a single line.
2. `check_if_quit()` inspects the Pygame event queue so you don't have to write manual event loops.
3. `roll_dice(6)` uses `easy_random` to simulate rolling a standard 6-sided die.
4. `is_key_pressed("SPACE")` and `is_left_mouse_button_clicked()` monitor keyboard and mouse inputs without raw Pygame key constant lookups.
5. `fill_background()` and `draw_text()` paint the background color and text surfaces directly onto the active screen.
6. `update_screen()` handles the display refresh cycle.

## Why use these helpers?

Building even a simple graphic window with raw Pygame usually requires:
- Initializing `pygame.init()` and instantiating `pygame.display.set_mode()`.
- Managing a `for event in pygame.event.get():` loop just to prevent the window from freezing.
- Setting up custom fonts, rendering surfaces, and calling `.blit()` with custom coordinates.

By combining `easy_game` and `easy_random`, all the low-level rendering, event handling, and random number logic are reduced to declarative, readable function calls.