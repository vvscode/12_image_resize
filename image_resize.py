import argparse
import sys
import os
from PIL import Image
import re


def parse_options():
    parser = argparse.ArgumentParser(
        description="devman image resizer script"
    )
    parser.add_argument("input_file", help="Path to image for resizing")
    parser.add_argument("--output", help="Path for output file")
    parser.add_argument("--scale", metavar="scale", type=float,
                        help="How many times to enlarge the image (maybe less than 1)")
    parser.add_argument("--width", type=int, help="Output width")
    parser.add_argument("--height", type=int, help="Output height")
    return parser.parse_args()


def get_target_size(current_size, input_scale, input_width, input_height):
    current_width, current_height = current_size
    current_proportion = current_height / current_width

    if input_scale:
        target_width = int(current_width * input_scale)
        target_height = int(current_height * input_scale)
    elif input_width and input_height:
        target_height = input_height
        target_width = input_width
    elif input_width:
        target_width = input_width
        target_height = int(current_proportion * target_width)
    else:
        target_height = input_height
        target_width = int(target_height / current_proportion)

    return target_width, target_height


def get_output_path(input_result_path, input_image_path, target_size):
    return input_result_path or re.sub(
        r"(\.\w+?)?$", r"__{}x{}\1".format(*target_size),
        input_image_path,
        count=1
    )


def validate_params(args):
    scale = args.scale or 0
    width = args.width or 0
    height = args.height or 0

    if not (scale or width or height):
        return "At least one transformation param width/height/scale should be passed"

    if scale and (width or height):
        return "You can't use `scale` param and `width`/`height` together"

    if scale < 0 or height < 0 or width < 0:
        return "You can't pass negative values of params"

    if not os.path.isfile(args.input_file):
        return "File not exists"


def get_image_size(path):
    try:
        with Image.open(path) as image:
            return image.size
    except OSError:
        return None


def resize_image(path, target_result_path, target_size):
    try:
        with Image.open(path) as image:
            output_image = image.resize(target_size)
            output_image.save(target_result_path)
            return True
    except OSError:
        return None


def is_ratio_diff(current_size, new_size):
    target_width, target_height = new_size
    current_width, current_height = current_size
    # I know about comparation with some precision
    # But here I what to compare certain ratio (7999x8000 != 8000x8000)
    return target_height / target_width != current_height / current_width

def notify_if_ratio_changed(current_size, new_size):
    if is_ratio_diff(image_size, target_size):
        print("Warning: The proportions do not match")

def request_yes_no(text):
    response = input(text + ' (y/n)').lower()
    return response.startswith('y')


if __name__ == "__main__":
    args = parse_options()
    validation_error = validate_params(args)
    if validation_error:
        sys.exit(validation_error)

    image_size = get_image_size(args.input_file)

    if not image_size:
        sys.exit("Can't process this file")

    target_size = get_target_size(
        current_size=image_size,
        input_scale=args.scale,
        input_width=args.width,
        input_height=args.height
    )

    notify_if_ratio_changed(image_size, target_size)

    target_result_path = get_output_path(
        input_result_path=args.output,
        input_image_path=args.input_file,
        target_size=target_size
    )

    if os.path.isfile(target_result_path) \
            and not request_yes_no('File already exists. Do you want to replace it?'):
        sys.exit()

    if not resize_image(args.input_file, target_result_path, target_size):
        sys.exit("Can't process file")

    print("File was saved to `{}`".format(target_result_path))