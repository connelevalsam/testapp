from django.contrib import admin
from .models import Message, Transaction


class ManageAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'description', 'address', 'email')

class Trans(admin.ModelAdmin):
    list_display = ('uid', 'message', 'cost', 'money_paid', 'money_made', 'shipping_cost')


admin.site.register(Message, ManageAdmin)

admin.site.register(Transaction, Trans)
