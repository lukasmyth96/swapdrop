import os
import random
import shutil

import django
django.setup()
from django.contrib.auth.models import User
from products.models import Product
from products.model_enums import ProductStatus


if __name__ == '__main__':
    """
    This script is used to upload fake products using scraped product images stored in a single folder.

    For image file in src dir:
    - copies file into media/product_pics
    - rename file
    - create Product object using that file
    - save Product object
    """

    users = User.objects.all()

    src_dir = '/home/luka/Pictures/Swapdrop'
    dest_dir = '/home/luka/PycharmProjects/SWAPDROP/mysite/media/product_pics'
    media_dir = '/media/product_pics'


    filenames = [file for file in os.listdir(src_dir) if file.endswith('.jpg')]
    for idx, filename in enumerate(filenames):
        src_path = os.path.join(src_dir, filename)
        dest_path = os.path.join(dest_dir, filename)
        shutil.copy(src_path, dest_path)

        renamed_filename = 'product_{}.jpg'.format(idx)
        renamed_path = os.path.join(dest_dir, renamed_filename)
        os.rename(dest_path, renamed_path)

        product = Product(name='test',
                          description='test',
                          image=os.path.join('product_pics', renamed_filename),
                          owner=random.choice(users),
                          status=ProductStatus.LIVE)
        product.save()
