from django.db import models
from django.utils import timezone
from django_enumfield import enum
from django.contrib.auth.models import User

from products.models import Product
from .model_enums import OfferStatus



class Offer(models.Model):

    desired_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers_desired')
    offered_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers_offered')
    date_offered = models.DateTimeField(default=timezone.now)
    status = enum.EnumField(OfferStatus, default=OfferStatus.PENDING)

    def __str__(self):
        abbreviated_desired_product_name = self.desired_product.__str__()[:20]  # just truncating.
        abbreviated_offered_product_name = self.offered_product.__str__()[:20]
        return f'{self.offered_product.owner.username} *OFFERED* {abbreviated_offered_product_name} ' \
               f' *FOR* {abbreviated_desired_product_name}  *OWNED BY* {self.desired_product.owner.username}  *STATUS: {self.status.name}*'
