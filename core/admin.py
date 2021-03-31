from django.contrib import admin

# Register your models here.
from core.models import Category, \
    Expense, User, Month, Entry, \
    Post, Comment, Currency, CompanyStock, UserCompany

admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(User)
admin.site.register(Month)
admin.site.register(Entry)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Currency)
admin.site.register(CompanyStock)
admin.site.register(UserCompany)

