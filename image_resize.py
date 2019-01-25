import argparse
import sys
import os
from PIL import Image
import re


def pil_image_input_type(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError("File not exists")

    try:
        return path, Image.open(path)
    except OSError:
        raise argparse.ArgumentTypeError("File is not an image")

def get_image_size(pil_image):
    return pil_image.width, pil_image.height

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="devman image resizer script"
    )
    parser.add_argument("input_file", help="Path to image for resizing", type=pil_image_input_type)
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
    input_scale = args.scale
    input_width = args.width
    input_height = args.height
    input_result_path = args.output

    current_width = input_image.width
    current_height = input_image.height
    current_proportion = current_height / current_width

    if input_scale:
        target_width = int(current_width * input_scale)
        target_height = int(current_height * input_scale)
    elif input_width and input_height:
        target_height = input_height
        target_width = input_width
        if target_height / target_width != current_proportion:
            print("The proportions do not match")
    elif input_width:
        target_width = input_width
        target_height = int(current_proportion * target_width)
    else:
        target_height = input_height
        target_width = int(target_height / current_proportion)

    target_result_path = input_result_path or re.sub(r'(\.\w+?)?$', r'__{}x{}\1'.format(target_width, target_height),
                                                     input_image_path, count=1)

    output_image = input_image.resize((target_width, target_height))
    output_image.save(target_result_path)

    print("File was saved to `{}`".format(target_result_path))
