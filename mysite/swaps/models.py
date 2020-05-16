from django.db import models
from django.utils import timezone
from django_enumfield import enum
from django.contrib.auth.models import User

from products.models import Product
from products.model_enums import ProductStatus
from .model_enums import SwapStatus



class Swap(models.Model):

    desired_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='swaps_desired')
    offered_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='swaps_offered')
    date_offered = models.DateTimeField(default=timezone.now)
    status = enum.EnumField(SwapStatus, default=SwapStatus.PENDING_REVIEW)

    def __str__(self):
        abbreviated_desired_product_name = self.desired_product.__str__()[:20]  # just truncating.
        abbreviated_offered_product_name = self.offered_product.__str__()[:20]
        return f'{self.offered_product.owner.username} *OFFERED* {abbreviated_offered_product_name} ' \
               f' *FOR* {abbreviated_desired_product_name}  *OWNED BY* {self.desired_product.owner.username}  *STATUS: {self.status.name}*'

    def refresh_status(self):
        """
        Updates swap status based on the status's of two two products involved.
        """
        if (self.offered_product.status == ProductStatus.CHECKOUT_COMPLETE) and (self.desired_product.status == ProductStatus.CHECKOUT_COMPLETE):
            self.status = SwapStatus.CHECKOUT_COMPLETE

        if (self.offered_product.status == ProductStatus.DELIVERED) and (self.desired_product.status == ProductStatus.DELIVERED):
            self.status = SwapStatus.SWAP_COMPLETE
