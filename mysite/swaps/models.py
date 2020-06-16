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
    date_accepted = models.DateTimeField(null=True, blank=True)
    status = enum.EnumField(SwapStatus, default=SwapStatus.PENDING_REVIEW)

    def __str__(self):
        return f'product: {self.offered_product.id} offered for product: {self.desired_product.id} - status: {self.status.label}'

    def refresh_status(self):
        """
        Updates swap status based on the status's of two two products involved.
        """
        if (self.offered_product.status == ProductStatus.CHECKOUT_COMPLETE) and (self.desired_product.status == ProductStatus.CHECKOUT_COMPLETE):
            self.status = SwapStatus.CHECKOUT_COMPLETE
            self.save(update_fields=['status'])

        if (self.offered_product.status == ProductStatus.DELIVERED) and (self.desired_product.status == ProductStatus.DELIVERED):
            self.status = SwapStatus.SWAP_COMPLETE
            self.save(update_fields=['status'])
