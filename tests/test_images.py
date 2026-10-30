"""Tests for easy_images module."""

import os
import tempfile

import pytest
from PIL import Image

from py_simple_package.src.py_simple import (
    adjust_brightness as public_adjust_brightness,
    convert_to_greyscale as public_convert_to_greyscale,
    create_thumbnail as public_create_thumbnail,
    crop_image as public_crop_image,
    flip_image as public_flip_image,
)

from py_simple_package.src.py_simple.easy_images import (
    ImageProcessingError,
    adjust_brightness,
    convert_image,
    convert_to_greyscale,
    create_thumbnail,
    crop_image,
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


class TestConvertToGreyscale:
    """Exercise real image files and decoded pixels, without mocking Pillow."""

    def test_converts_rgb_pixels_and_preserves_source(self, tmp_path):
        source = tmp_path / "colours.png"
        output = tmp_path / "gray.png"
        image = Image.new("RGB", (5, 1))
        image.putdata(
            [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
        )
        image.save(source)
        original_bytes = source.read_bytes()

        assert convert_to_greyscale(str(source), str(output)) is None

        with Image.open(output) as converted:
            assert converted.mode == "LA"
            assert converted.size == (5, 1)
            assert list(converted.getchannel("L").getdata()) == [0, 76, 150, 29, 255]
            assert converted.getchannel("A").getextrema() == (255, 255)
        assert source.read_bytes() == original_bytes

    def test_webp_preserves_transparency(self, tmp_path):
        source = tmp_path / "transparent.png"
        output = tmp_path / "gray.webp"
        image = Image.new("RGBA", (3, 1))
        image.putdata([(255, 0, 0, 0), (0, 255, 0, 128), (0, 0, 255, 255)])
        image.save(source)
        original_bytes = source.read_bytes()

        convert_to_greyscale(str(source), str(output))

        with Image.open(output) as converted:
            assert converted.format == "WEBP"
            assert converted.mode == "RGBA"
            assert converted.size == (3, 1)
            # WebP's default colour compression is lossy; alpha stays exact.
            assert list(converted.getchannel("A").getdata()) == [0, 128, 255]
        assert source.read_bytes() == original_bytes

    @pytest.mark.parametrize(
        ("extension", "format", "mode"),
        [(".png", "PNG", "LA"), (".JPEG", "JPEG", "L"), (".bmp", "BMP", "L")],
    )
    def test_accepts_pathlib_paths(self, tmp_path, extension, format, mode):
        source = tmp_path / "source.png"
        output = tmp_path / ("gray" + extension)
        Image.new("RGBA", (2, 1), (255, 0, 0, 128)).save(source)

        convert_to_greyscale(source, output)

        with Image.open(output) as converted:
            assert converted.format == format
            assert converted.mode == mode
            assert converted.size == (2, 1)
            if mode == "LA":
                assert list(converted.getdata()) == [(76, 128)] * 2
            else:
                assert list(converted.getdata()) == pytest.approx([76, 76], abs=2)

    @pytest.mark.parametrize(
        ("extension", "mode"),
        [(".png", "LA"), (".jpg", "L"), (".bmp", "L"), (".tiff", "LA")],
    )
    def test_saves_requested_format(self, sample_png, extension, mode):
        output = "grayscale" + extension
        convert_to_greyscale(sample_png, output)

        with Image.open(output) as converted:
            assert converted.mode == mode
            assert converted.size == (100, 60)
            assert converted.getchannel("L").getpixel((0, 0)) == 76

    @pytest.mark.parametrize("extension", [".png", ".tiff"])
    def test_rgba_input_preserves_transparency(self, tmp_path, extension):
        source = tmp_path / "transparent.png"
        output = tmp_path / ("gray" + extension)
        image = Image.new("RGBA", (3, 1))
        image.putdata([(255, 0, 0, 0), (0, 255, 0, 128), (0, 0, 255, 255)])
        image.save(source)
        original_bytes = source.read_bytes()

        convert_to_greyscale(str(source), str(output))

        with Image.open(output) as converted:
            assert converted.mode == "LA"
            assert list(converted.getdata()) == [(76, 0), (150, 128), (29, 255)]
        assert source.read_bytes() == original_bytes

    @pytest.mark.parametrize(
        ("extension", "format"), [(".jpg", "JPEG"), (".JPEG", "JPEG"), (".bmp", "BMP")]
    )
    def test_transparent_input_saves_without_alpha(self, tmp_path, extension, format):
        source = tmp_path / "transparent.png"
        output = tmp_path / ("gray" + extension)
        image = Image.new("RGBA", (3, 1))
        image.putdata([(255, 0, 0, 0), (255, 0, 0, 128), (255, 0, 0, 255)])
        image.save(source)

        convert_to_greyscale(str(source), str(output))

        with Image.open(output) as converted:
            assert converted.format == format
            assert converted.mode == "L"
            assert list(converted.getdata()) == pytest.approx([76, 76, 76], abs=2)

    @pytest.mark.parametrize(
        ("transparency", "alpha"),
        [(0, [0, 255, 255]), (bytes([0, 128, 255]), [0, 128, 255])],
    )
    def test_preserves_palette_transparency(self, tmp_path, transparency, alpha):
        source = tmp_path / "transparent-palette.png"
        output = tmp_path / "gray.png"
        image = Image.new("P", (3, 1))
        image.putpalette([255, 255, 255, 254, 255, 255, 255, 0, 0] + [0] * 759)
        image.putdata([0, 1, 2])
        image.save(source, transparency=transparency)

        convert_to_greyscale(str(source), str(output))

        with Image.open(output) as converted:
            assert converted.mode == "LA"
            assert list(converted.getdata()) == list(zip([255, 255, 76], alpha))

    def test_preserves_rgb_colour_key_transparency(self, tmp_path):
        source = tmp_path / "transparent-rgb.png"
        output = tmp_path / "gray.png"
        image = Image.new("RGB", (2, 1))
        image.putdata([(255, 0, 0), (0, 130, 0)])
        image.save(source, transparency=(255, 0, 0))

        convert_to_greyscale(str(source), str(output))

        with Image.open(output) as converted:
            assert converted.mode == "LA"
            assert list(converted.getchannel("A").getdata()) == [0, 255]
            assert converted.getpixel((1, 0)) == (76, 255)

    def test_preserves_existing_grayscale_alpha(self, tmp_path):
        source = tmp_path / "transparent-gray.png"
        output = tmp_path / "gray.png"
        pixels = [(0, 0), (64, 128), (255, 255)]
        image = Image.new("LA", (3, 1))
        image.putdata(pixels)
        image.save(source)

        convert_to_greyscale(str(source), str(output))

        with Image.open(output) as converted:
            assert converted.mode == "LA"
            assert list(converted.getdata()) == pixels

    def test_preserves_existing_grayscale_values(self, tmp_path):
        source = tmp_path / "already-gray.png"
        output = tmp_path / "gray.png"
        image = Image.new("L", (4, 1))
        image.putdata([0, 64, 128, 255])
        image.save(source)

        convert_to_greyscale(str(source), str(output))

        with Image.open(output) as converted:
            assert list(converted.getchannel("L").getdata()) == [0, 64, 128, 255]

    def test_uses_palette_colours(self, tmp_path):
        source = tmp_path / "palette.png"
        output = tmp_path / "gray.png"
        image = Image.new("P", (2, 1))
        image.putpalette([255, 0, 0, 0, 0, 255] + [0] * (768 - 6))
        image.putdata([0, 1])
        image.save(source)

        convert_to_greyscale(str(source), str(output))

        with Image.open(output) as converted:
            assert list(converted.getchannel("L").getdata()) == [76, 29]

    @pytest.mark.parametrize("extension", [".png", ".gif"])
    def test_converts_only_first_frame(self, tmp_path, extension):
        source = tmp_path / "animated.gif"
        output = tmp_path / ("gray" + extension)
        first = Image.new("RGB", (2, 1), "red")
        second = Image.new("RGB", (2, 1), "blue")
        first.save(source, save_all=True, append_images=[second])

        convert_to_greyscale(str(source), str(output))

        with Image.open(output) as converted:
            assert converted.n_frames == 1
            assert list(converted.convert("RGB").getdata()) == [(76, 76, 76)] * 2

    def test_missing_input_raises(self, tmp_path):
        with pytest.raises(ImageProcessingError):
            convert_to_greyscale(
                str(tmp_path / "missing.png"), str(tmp_path / "gray.png")
            )

    def test_unrecognized_input_raises(self, tmp_path):
        source = tmp_path / "broken.png"
        source.write_bytes(b"not an image")

        with pytest.raises(ImageProcessingError):
            convert_to_greyscale(str(source), str(tmp_path / "gray.png"))

    def test_unknown_output_format_raises(self, sample_png):
        with pytest.raises(ValueError, match="unknown file extension"):
            convert_to_greyscale(sample_png, "gray.unknown")

    def test_missing_output_directory_raises(self, sample_png, tmp_path):
        with pytest.raises(OSError):
            convert_to_greyscale(sample_png, str(tmp_path / "missing" / "gray.png"))

    def test_public_import(self):
        assert public_convert_to_greyscale is convert_to_greyscale

class TestAdjustBrightness:
    """Tests for adjust_brightness function."""

    def test_brightens_image(self, tmp_workdir):
        Image.new("RGB", (10, 10), (100, 100, 100)).save("gray.png")

        adjust_brightness("gray.png", "bright.png", 1.5)

        with Image.open("bright.png") as img:
            assert img.getpixel((0, 0)) == (150, 150, 150)

    def test_darkens_image(self, tmp_workdir):
        Image.new("RGB", (10, 10), (100, 100, 100)).save("gray.png")

        adjust_brightness("gray.png", "dark.png", 0.5)

        with Image.open("dark.png") as img:
            assert img.getpixel((0, 0)) == (50, 50, 50)

    def test_zero_produces_black_image(self, tmp_workdir):
        Image.new("RGB", (10, 10), (100, 150, 200)).save("image.png")

        adjust_brightness("image.png", "black.png", 0)

        with Image.open("black.png") as img:
            assert img.getpixel((0, 0)) == (0, 0, 0)

    def test_one_preserves_brightness(self, tmp_workdir):
        Image.new("RGB", (10, 10), (100, 150, 200)).save("image.png")

        adjust_brightness("image.png", "same.png", 1)

        with Image.open("same.png") as img:
            assert img.getpixel((0, 0)) == (100, 150, 200)

    @pytest.mark.parametrize("value", [-1, float("nan"), float("inf"), -float("inf"), True, "1.5", None])
    def test_invalid_value_raises_value_error(self, tmp_workdir, value):
        Image.new("RGB", (10, 10)).save("image.png")

        with pytest.raises(ValueError):
            adjust_brightness("image.png", "output.png", value)
    def test_palette_image_is_converted_and_brightened(self, tmp_workdir):
        img = Image.new("P", (10, 10), 0)
        img.putpalette([100, 100, 100] + [0] * 765)  # color slot 0 = gray 100
        img.save("palette.png")

        adjust_brightness("palette.png", "bright.png", 1.5)

        with Image.open("bright.png") as img:
            assert img.getpixel((0, 0)) == (150, 150, 150)

    def test_rgba_image_can_be_saved_as_jpeg(self, tmp_workdir):
        Image.new("RGBA", (10, 10), (100, 100, 100, 255)).save("rgba.png")

        adjust_brightness("rgba.png", "bright.jpg", 1.5)

        with Image.open("bright.jpg") as img:
            assert img.mode == "RGB"
            
    def test_public_import(self):
        assert public_adjust_brightness is adjust_brightness


class TestCropImage:
    """Tests for crop_image function."""

    def test_crops_to_given_coordinates(self, sample_png):
        crop_image(sample_png, "cropped.png", 10, 10, 50, 40)
        assert os.path.exists("cropped.png")
        with Image.open("cropped.png") as img:
            assert img.size == (40, 30)

    def test_crops_entire_image(self, sample_png):
        crop_image(sample_png, "full_crop.png", 0, 0, 100, 60)
        with Image.open("full_crop.png") as img:
            assert img.size == (100, 60)

    def test_crop_rgba_image_saved_as_jpeg(self, sample_rgba_png):
        crop_image(sample_rgba_png, "cropped.jpg", 5, 5, 45, 35)
        with Image.open("cropped.jpg") as img:
            assert img.mode == "RGB"
            assert img.size == (40, 30)

    @pytest.mark.parametrize(
        "coords",
        [
            (-1, 0, 50, 50),
            (0, -1, 50, 50),
            (0, 0, -1, 50),
            (0, 0, 50, -1),
            ("0", 0, 50, 50),
            (0, 0, 50.5, 50),
            (True, 0, 50, 50),
            (0, False, 50, 50),
            (None, 0, 50, 50),
        ],
    )
    def test_invalid_coordinate_types_or_values(self, sample_png, coords):
        with pytest.raises(ValueError, match="must be non-negative integers"):
            crop_image(sample_png, "out.png", *coords)

    @pytest.mark.parametrize(
        "left, top, right, bottom",
        [
            (50, 10, 50, 30),  # left == right
            (60, 10, 50, 30),  # left > right
            (10, 30, 50, 30),  # top == bottom
            (10, 40, 50, 30),  # top > bottom
        ],
    )
    def test_inverted_coordinates_raise_value_error(self, sample_png, left, top, right, bottom):
        with pytest.raises(ValueError):
            crop_image(sample_png, "out.png", left, top, right, bottom)

    @pytest.mark.parametrize(
        "left, top, right, bottom",
        [
            (0, 0, 101, 60),   # right exceeds width (100)
            (0, 0, 100, 61),   # bottom exceeds height (60)
            (0, 0, 200, 200),  # both exceed
        ],
    )
    def test_out_of_bounds_coordinates_raise_value_error(self, sample_png, left, top, right, bottom):
        with pytest.raises(ValueError, match="exceed image dimensions"):
            crop_image(sample_png, "out.png", left, top, right, bottom)

    def test_missing_input_file_raises_error(self, tmp_workdir):
        with pytest.raises(ImageProcessingError):
            crop_image("nonexistent.png", "out.png", 0, 0, 10, 10)

    def test_public_import(self):
        assert public_crop_image is crop_image
