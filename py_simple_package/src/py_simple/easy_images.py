"""
easy_images is meant to simplify common image processing tasks
(resizing, converting, rotating, and inspecting images) using Pillow.
"""

import os

from PIL import Image, UnidentifiedImageError


class ImageProcessingError(Exception):
    """
    Raised when a py_simple image function fails to complete.

    This covers a missing input file, an unsupported/corrupt image
    format, or any other error that prevents a function from returning
    a real result.

    Args:
        message (str): Description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def _open_image(input_path: str) -> Image.Image:
    """Open an image file, raising ImageProcessingError with a clear
    message instead of letting Pillow's own exceptions leak through."""
    if not os.path.isfile(input_path):
        raise ImageProcessingError(f"\nFile '{input_path}' not found.")
    try:
        return Image.open(input_path)
    except UnidentifiedImageError as error:
        raise ImageProcessingError(
            f"\n'{input_path}' is not a valid or supported image file."
        ) from error


def resize_image(input_path: str, output_path: str, width: int, height: int):
    """
    Resize an image to the given dimensions and save it.

    Args:
        input_path (str): Path of the image to resize.
        output_path (str): Path to save the resized image to.
        width (int): Target width in pixels.
        height (int): Target height in pixels.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import resize_image

            resize_image("photo.jpg", "photo_small.jpg", 320, 240)
            ```

        === "The Traditional Way"
            ```python
            from PIL import Image

            with Image.open("photo.jpg") as img:
                img.resize((320, 240)).save("photo_small.jpg")
            ```
    """
    with _open_image(input_path) as img:
        img.resize((width, height)).save(output_path)


def create_thumbnail(
    input_path: str, output_path: str, max_width: int, max_height: int
):
    """
    Create a thumbnail that fits within the given dimensions.

    The image keeps its original aspect ratio and is never enlarged.

    Args:
        input_path (str): Path of the source image.
        output_path (str): Path to save the thumbnail to.
        max_width (int): Maximum thumbnail width in pixels.
        max_height (int): Maximum thumbnail height in pixels.

    Raises:
        ValueError: If either maximum dimension is not a positive integer.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import create_thumbnail

            create_thumbnail("photo.jpg", "thumbnail.jpg", 320, 320)
            ```

        === "The Traditional Way"
            ```python
            from PIL import Image

            with Image.open("photo.jpg") as img:
                img.thumbnail((320, 320))
                img.save("thumbnail.jpg")
            ```
    """
    dimensions = (max_width, max_height)
    if any(
        not isinstance(value, int) or isinstance(value, bool) or value < 1
        for value in dimensions
    ):
        raise ValueError("Maximum width and height must be positive integers.")

    with _open_image(input_path) as img:
        img.thumbnail((max_width, max_height))
        img.save(output_path)


def convert_image(input_path: str, output_path: str):
    """
    Convert an image to a different format based on the output file's
    extension (e.g. PNG to JPG).

    Args:
        input_path (str): Path of the image to convert.
        output_path (str): Path to save the converted image to. The
            new format is inferred from this path's extension.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import convert_image

            convert_image("photo.png", "photo.jpg")
            ```

        === "The Traditional Way"
            ```python
            from PIL import Image

            with Image.open("photo.png") as img:
                img.convert("RGB").save("photo.jpg")
            ```
    """
    with _open_image(input_path) as img:
        # JPEG has no alpha channel; converting to RGB first avoids Pillow
        # raising on images that have one (e.g. a PNG with transparency).
        if img.mode in ("RGBA", "P") and output_path.lower().endswith(
            (".jpg", ".jpeg")
        ):
            img = img.convert("RGB")
        img.save(output_path)


def rotate_image(input_path: str, output_path: str, angle: float):
    """
    Rotate an image by the given angle (counter-clockwise) and save it.

    Args:
        input_path (str): Path of the image to rotate.
        output_path (str): Path to save the rotated image to.
        angle (float): Degrees to rotate counter-clockwise, e.g. 90.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import rotate_image

            rotate_image("photo.jpg", "photo_rotated.jpg", 90)
            ```

        === "The Traditional Way"
            ```python
            from PIL import Image

            with Image.open("photo.jpg") as img:
                img.rotate(90, expand=True).save("photo_rotated.jpg")
            ```
    """
    with _open_image(input_path) as img:
        img.rotate(angle, expand=True).save(output_path)


def get_image_info(input_path: str) -> dict:
    """
    Get basic information about an image.

    Args:
        input_path (str): Path of the image to inspect.

    Returns:
        dict: With keys "width", "height", "format", and "mode".

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_image_info

            info = get_image_info("photo.jpg")
            # {"width": 1920, "height": 1080, "format": "JPEG", "mode": "RGB"}
            ```

        === "The Traditional Way"
            ```python
            from PIL import Image

            with Image.open("photo.jpg") as img:
                info = {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                    "mode": img.mode,
                }
            ```
    """
    with _open_image(input_path) as img:
        return {
            "width": img.width,
            "height": img.height,
            "format": img.format,
            "mode": img.mode,
        }
