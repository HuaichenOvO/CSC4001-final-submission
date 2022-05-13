from django.contrib import admin
from .models import *

# Register your models here.
# controls the presence of tables in the database

admin.site.register(Token)
admin.site.register(Client)
admin.site.register(Task)
admin.site.register(Order)
admin.site.register(Address)
# admin.site.register(Message)
# admin.site.register(Foo)