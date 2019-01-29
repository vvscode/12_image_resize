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
        sys.exit("At least one transformation param width/height/scale should be passed")

    if scale and (width or height):
        sys.exit("You can't use `scale` param and `width`/`height` together")

    if scale < 0 or height < 0 or width < 0:
        sys.exit("You can't pass negative values of params")

    if not os.path.isfile(args.input_file):
        sys.exit("File not exists")


if __name__ == "__main__":
    args = parse_options()
    validate_params(args)

    try:
        with Image.open(args.input_file) as image:
            target_size = get_target_size(
                current_size=image.size,
                input_scale=args.scale,
                input_width=args.width,
                input_height=args.height
            )
            target_width, target_height = target_size

            # I know about comparation with some precision
            # But here I what to compare certain ratio (7999x8000 != 8000x8000)
            if target_height / target_width != image.height / image.width:
                print("The proportions do not match")

            target_result_path = get_output_path(
                input_result_path=args.output,
                input_image_path=args.input_file,
                target_size=target_size
            )

            output_image = image.resize((target_width, target_height))

    except OSError:
        raise sys.exit("File is not an image")

    if os.path.isfile(target_result_path) and input(
            'File already exists. Do you want to replace it? (y/n) ').lower() != 'y':
        sys.exit()

    output_image.save(target_result_path)
    print("File was saved to `{}`".format(target_result_path))
