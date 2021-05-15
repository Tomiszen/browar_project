from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Stock, Lot, Order, OrderItem, Distribution

@receiver(post_save, sender=Lot)
def add_lot(sender, instance=None, created=False, **kwargs):
    if created:
        stock, is_created = Stock.objects.get_or_create(distribution=instance.distribution)
        stock.quantity += instance.quantity
        stock.save()

@receiver(post_save, sender=OrderItem)
def sub_order(sender, instance=None, created=False, **kwargs):
    if created:
        stock = Stock.objects.get(distribution=instance.distribution)
        stock.quantity -= instance.quantity
        stock.save()
        order = Order.objects.get(id=instance.order.id)
        order.totalamount += instance.amount
        order.save()

@receiver(pre_save, sender=OrderItem)
def calc_amount(sender, instance=None, created=False, **kwargs):
    distribution = Distribution.objects.get(id=instance.distribution.id)
    instance.amount = instance.quantity * distribution.price


