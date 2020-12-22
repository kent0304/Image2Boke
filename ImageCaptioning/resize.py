import argparse
import os
import requests
import io
from PIL import Image
from build_vocab import unpickle


def resize_image(image, size):
    """Resize an image to the given size."""
    return image.resize(size, Image.ANTIALIAS)

def resize_images(image_paths, output_dir, size):
    """Resize the images in 'image_dir' and save into 'output_dir'."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    images = unpickle(image_paths)
    num_images = len(images)
    for i, image in enumerate(images):
        with Image.open(io.BytesIO(requests.get(image).content)) as img:
            img = resize_image(img, size)
            img.save(output_dir + str(i) + '.jpg')
        if (i+1) % 100 == 0:
            print ("[{}/{}] Resized the images and saved into '{}'."
                   .format(i+1, num_images, output_dir))

def main(args):
    image_paths = args.image_paths
    output_dir = args.output_dir
    image_size = [args.image_size, args.image_size]
    resize_images(image_paths, output_dir, image_size)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_paths', type=str, default='./data/imagepath_list.pkl',
                        help='directory for train images')
    parser.add_argument('--output_dir', type=str, default='./data/resized_bokete_images/',
                        help='directory for saving resized images')
    parser.add_argument('--image_size', type=int, default=256,
                        help='size for image after processing')
    args = parser.parse_args()
    main(args)

