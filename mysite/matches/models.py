from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Like(models.Model):

    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        abbreviated_product_name = self.product.__str__()[:25]
        return f'{self.liked_by}  --> LIKED -->  {abbreviated_product_name}  --> OWNED BY -->  {self.product.owner}'


class Offer(models.Model):

    desired_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers_desired')
    offered_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers_offered')

    def __str__(self):
        abbreviated_desired_product_name = self.desired_product.__str__()[:25] #just truncating.
        abbreviated_offered_product_name = self.offered_product.__str__()[:25]
        return f'{abbreviated_offered_product_name}--> OFFERED FOR --> {abbreviated_desired_product_name}'
