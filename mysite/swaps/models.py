import datetime
import math

from django.db import models
from django.utils import timezone
from django_enumfield import enum
from django.contrib.auth.models import User

from mysite.settings import CHECKOUT_TIMEOUT_HOURS
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

    def timeout_reached(self):
        self.status = SwapStatus.TIMED_OUT
        self.save(update_fields=['status'])
        self.offered_product.status = ProductStatus.LIVE
        self.offered_product.save(update_fields=['status'])
        self.desired_product.status = ProductStatus.LIVE
        self.desired_product.save(update_fields=['status'])

    @property
    def hours_left_to_checkout(self):
        hours_left_to_checkout = None
        if self.status == SwapStatus.PENDING_CHECKOUT:
            timeout_time = self.date_accepted + datetime.timedelta(hours=CHECKOUT_TIMEOUT_HOURS)
            time_left_to_checkout = timeout_time - timezone.now()
            hours_left_to_checkout = max(0, math.floor(time_left_to_checkout.total_seconds() / 3600))

        return hours_left_to_checkout

