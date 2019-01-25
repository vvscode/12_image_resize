import argparse
import sys
import os
from PIL import Image
import re


def pil_image_input(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError("File not exists")

    try:
        return path, Image.open(path)
    except OSError:
        raise argparse.ArgumentTypeError("File is not an image")


def resize_image(path_to_original, path_to_result):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="devman image resizer script"
    )
    parser.add_argument("input_file", help="Path to image for resizing", type=pil_image_input)
    parser.add_argument('--output', help='Path for output file', type=argparse.FileType('r'))
    parser.add_argument('--scale', metavar='scale', type=float,
                        help='How many times to enlarge the image (maybe less than 1)')
    parser.add_argument('--width', type=int, help='Output width')
    parser.add_argument('--height', type=int, help='Output height')
    args = parser.parse_args()

    if not (args.scale or args.width or args.height):
        sys.exit("At least one transformation param width/height/scale should be passed")
    if args.scale and (args.width or args.height):
        sys.exit("You can't use `scale` param and `width`/`height` together")

    input_image_path, input_image = args.input_file
    scale = args.scale
    width = args.width
    height = args.height
    output_path = args.output

    current_width = input_image.width
    current_height = input_image.height
    current_proportion = current_height / current_width

    if scale:
        target_width = int(current_width * scale)
        target_height = int(current_height * scale)
    elif width and height:
        target_height = height
        target_width = width
        if target_height / target_width != current_proportion:
            print("The proportions do not match")
    elif width:
        target_width = width
        target_height = int(current_proportion * target_width)
    else:
        target_height = height
        target_width = int(target_height / current_proportion)

    target_output_path = output_path or re.sub(r'(\.\w+?)?$', r'__{}x{}\1'.format(target_width, target_height),
                                        input_image_path, count=1)

    data = {
        "input_image_path": input_image_path,
        "scale": scale,
        "width": width,
        "height": height,
        "output_path": output_path,

        "current_width": current_width,
        "current_height": current_height,
        "current_proportion": current_proportion,

        "target_width": target_width,
        "target_height": target_height,
        "target_output_path":target_output_path
    }
    for key in data:
        print(key, data[key])
