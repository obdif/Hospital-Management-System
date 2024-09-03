from django.contrib import admin
from . import models


class  PaymentAdmin(admin.ModelAdmin):
    list_display  = ["id", "ref", 'amount', "verified", "date_created"]

admin.site.register(models.Payment, PaymentAdmin)
admin.site.register(models.UserWallet)