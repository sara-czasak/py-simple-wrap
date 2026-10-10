"""Tests for easy_images module."""

import os
import tempfile

import pytest
from PIL import Image

from py_simple_package.src.py_simple import create_thumbnail as public_create_thumbnail
from py_simple_package.src.py_simple import flip_image as public_flip_image
from py_simple_package.src.py_simple.easy_images import (
    ImageProcessingError,
    convert_image,
    create_thumbnail,
    flip_image,
    get_image_info,
    resize_image,
    rotate_image,
)


@pytest.fixture
def tmp_workdir():
    """Change to a temp directory for file operations, then clean up."""
    original_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        try:
            yield tmpdir
        finally:
            os.chdir(original_cwd)


@pytest.fixture
def sample_png(tmp_workdir):
    """A small opaque red PNG to run the functions against."""
    path = "sample.png"
    Image.new("RGB", (100, 60), color="red").save(path)
    return path


@pytest.fixture
def sample_rgba_png(tmp_workdir):
    """A small PNG with an alpha channel, to test JPEG conversion."""
    path = "sample_rgba.png"
    Image.new("RGBA", (100, 60), color=(255, 0, 0, 128)).save(path)
    return path


class TestResizeImage:
    """Tests for resize_image function."""

    def test_resizes_to_given_dimensions(self, sample_png):
        resize_image(sample_png, "resized.png", 40, 20)
        with Image.open("resized.png") as img:
            assert img.size == (40, 20)

    def test_missing_input_raises(self, tmp_workdir):
        with pytest.raises(ImageProcessingError):
            resize_image("does_not_exist.png", "out.png", 10, 10)


class TestCreateThumbnail:
    """Tests for create_thumbnail function."""

    def test_fits_within_dimensions_and_preserves_aspect_ratio(self, sample_png):
        create_thumbnail(sample_png, "thumbnail.png", 40, 40)
        with Image.open("thumbnail.png") as img:
            assert img.size == (40, 24)

    def test_does_not_enlarge_small_image(self, sample_png):
        create_thumbnail(sample_png, "thumbnail.png", 200, 200)
        with Image.open("thumbnail.png") as img:
            assert img.size == (100, 60)

    @pytest.mark.parametrize(
        "max_width, max_height",
        [(0, 20), (20, -1), (20.5, 20), (True, 20)],
    )
    def test_rejects_invalid_dimensions(self, sample_png, max_width, max_height):
        with pytest.raises(ValueError):
            create_thumbnail(sample_png, "thumbnail.png", max_width, max_height)

    def test_missing_input_raises(self, tmp_workdir):
        with pytest.raises(ImageProcessingError):
            create_thumbnail("does_not_exist.png", "out.png", 20, 20)

    def test_is_available_from_public_api(self):
        assert public_create_thumbnail is create_thumbnail


class TestConvertImage:
    """Tests for convert_image function."""

    def test_converts_png_to_jpg(self, sample_png):
        convert_image(sample_png, "converted.jpg")
        with Image.open("converted.jpg") as img:
            assert img.format == "JPEG"

    def test_converts_rgba_to_jpg_without_error(self, sample_rgba_png):
        # JPEG has no alpha channel; this must not raise.
        convert_image(sample_rgba_png, "converted.jpg")
        with Image.open("converted.jpg") as img:
            assert img.format == "JPEG"
            assert img.mode == "RGB"

    def test_missing_input_raises(self, tmp_workdir):
        with pytest.raises(ImageProcessingError):
            convert_image("does_not_exist.png", "out.jpg")


class TestRotateImage:
    """Tests for rotate_image function."""

    def test_rotate_90_swaps_dimensions(self, sample_png):
        rotate_image(sample_png, "rotated.png", 90)
        with Image.open("rotated.png") as img:
            # A 100x60 image rotated 90 degrees becomes 60x100.
            assert img.size == (60, 100)

    def test_missing_input_raises(self, tmp_workdir):
        with pytest.raises(ImageProcessingError):
            rotate_image("does_not_exist.png", "out.png", 90)


class TestGetImageInfo:
    """Tests for get_image_info function."""

    def test_returns_expected_keys(self, sample_png):
        info = get_image_info(sample_png)
        assert info == {
            "width": 100,
            "height": 60,
            "format": "PNG",
            "mode": "RGB",
        }

    def test_missing_input_raises(self, tmp_workdir):
        with pytest.raises(ImageProcessingError):
            get_image_info("does_not_exist.png")

    def test_unsupported_file_raises(self, tmp_workdir):
        with open("not_an_image.png", "w", encoding="utf-8") as f:
            f.write("this is definitely not image data")
        with pytest.raises(ImageProcessingError):
            get_image_info("not_an_image.png")


class TestFlipImage:
    """Tests for flip_image function."""

    def test_horizontal_flip_mirrors_pixels(self, sample_png):
        Image.new("RGB", (2, 1), color="white").save("wide.png")
        with Image.open("wide.png") as img:
            img.putpixel((0, 0), (255, 0, 0))
            img.putpixel((1, 0), (0, 0, 255))
            img.save("wide.png")

        flip_image("wide.png", "flipped.png", "horizontal")
        with Image.open("flipped.png") as img:
            assert img.getpixel((0, 0)) == (0, 0, 255)
            assert img.getpixel((1, 0)) == (255, 0, 0)

    def test_vertical_flip_mirrors_pixels(self, tmp_workdir):
        Image.new("RGB", (1, 2), color="white").save("tall.png")
        with Image.open("tall.png") as img:
            img.putpixel((0, 0), (255, 0, 0))
            img.putpixel((0, 1), (0, 0, 255))
            img.save("tall.png")

        flip_image("tall.png", "flipped.png", "vertical")
        with Image.open("flipped.png") as img:
            assert img.getpixel((0, 0)) == (0, 0, 255)
            assert img.getpixel((0, 1)) == (255, 0, 0)

    def test_default_direction_is_horizontal(self, sample_png):
        flip_image(sample_png, "flipped.png")
        with Image.open("flipped.png") as img:
            assert img.size == (100, 60)

    def test_invalid_direction_raises(self, sample_png):
        with pytest.raises(ValueError):
            flip_image(sample_png, "flipped.png", "diagonal")

    def test_missing_input_raises(self, tmp_workdir):
        with pytest.raises(ImageProcessingError):
            flip_image("does_not_exist.png", "out.png")

    def test_public_import(self):
        assert public_flip_image is flip_image
