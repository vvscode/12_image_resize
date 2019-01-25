# Image Resizer

Script allow you resize images.

It uses external packages which you can install with `pip3 install -r requirements.txt`

You can get help for script usage with `-h` flag, like 

```bash
$ python3 image_resize.py -h
usage: image_resize.py [-h] [--output OUTPUT] [--scale scale] [--width WIDTH]
                       [--height HEIGHT]
                       input_file

devman image resizer script

positional arguments:
  input_file       Path to image for resizing

optional arguments:
  -h, --help       show this help message and exit
  --output OUTPUT  Path for output file
  --scale scale    How many times to enlarge the image (maybe less than 1)
  --width WIDTH    Output width
  --height HEIGHT  Output height
```

Example of script usage:

```bash
$ python3 image_resize.py ~/Desktop/1.png --scale 10
File was saved to `/Users/vvscode/Desktop/1__740x840.png`
```


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
