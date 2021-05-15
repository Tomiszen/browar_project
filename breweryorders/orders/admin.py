from django.contrib import admin
from .models import Beer, Distribution, Stock, Lot, Order, OrderItem

@admin.register(Beer)
class BeerAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    search_fields = ('name', 'type')

@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ('beer', 'package', 'capacity', 'boxquantity', 'price')
    search_fields = ('beer', )
    list_filter = ('package', 'capacity')

admin.site.register(Stock)
admin.site.register(Lot)
admin.site.register(Order)
admin.site.register(OrderItem)

# Register your models here.
