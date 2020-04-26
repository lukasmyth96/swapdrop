from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Like(models.Model):

    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        abbreviated_product_name = self.product.__str__()[:25]
        return f'{self.liked_by}  --> LIKED -->  {abbreviated_product_name}  --> OWNED BY -->  {self.product.owner}'
