import os
import random
import shutil
from datetime import datetime
import time

from tqdm import tqdm
from PIL import Image

import django
django.setup()
from django.contrib.auth.models import User
from products.models import Product
from products.model_enums import ProductStatus, ClothingType
from sizes.models import Size, GenderOptions


if __name__ == '__main__':
    """
    This script is used to upload fake products using scraped product images stored in a single folder.

    NOTE - you must populate the DB with size objects before running this script
    NOTE - you must set DJANGO_DEVELOPMENT=true in the environment variables for this script

    For image file in src dir:
    - copies file into media/product_pics
    - rename file
    - create Product object using that file
    - save Product object
    """
    # Config
    src_dir = '/home/luka/Pictures/Swapdrop'
    dest_dir = '/home/luka/PycharmProjects/SWAPDROP/mysite/media/product_pics'
    media_dir = '/media/product_pics'
    max_to_upload = 100

    filenames = [file for file in os.listdir(src_dir) if file.endswith('.jpg')]
    for idx, filename in tqdm(enumerate(filenames)):
        src_path = os.path.join(src_dir, filename)
        dest_path = os.path.join(dest_dir, filename)
        shutil.copy(src_path, dest_path)

        _, file_extension = os.path.splitext(filename)
        new_filename = datetime.now().strftime(f'%d_%m_%Y_%H_%M_%S{file_extension}')
        renamed_path = os.path.join(dest_dir, new_filename)
        os.rename(dest_path, renamed_path)

        product = Product(name='test',
                          description='test',
                          gender=random.choice([g for g in GenderOptions]),
                          clothing_type=random.choice([ct for ct in ClothingType]),
                          size=random.choice(Size.objects.all()),
                          image=os.path.join('product_pics', new_filename),
                          owner=random.choice(User.objects.all()),
                          status=ProductStatus.LIVE)

        img = Image.open(renamed_path)
        product.cropped_dimensions = (0, 0, img.width, img.height)

        product.save()

        if idx >= max_to_upload:
            break

        time.sleep(2)  # just to make sure that no images get same filename
