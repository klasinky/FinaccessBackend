from django.contrib import admin

# Register your models here.
from core.models import Category, Expense, User, Month

admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(User)
admin.site.register(Month)
