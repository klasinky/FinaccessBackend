from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from mptt.models import MPTTModel, TreeForeignKey


class ModelBase(models.Model):
    """Model base"""
    created_at = models.DateTimeField(auto_created=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def soft_delete(self):
        self.delete_at = timezone.now()
        self.is_active = False

    class Meta:
        abstract = True


class Currency(ModelBase):
    name = models.CharField('Name', max_length=255, unique=True)
    symbol = models.CharField('Symbol', max_length=255)

    # @classmethod
    # def get_default_pk(self):
    #     currency = self.objects.get_or_create(
    #         name='Euro', symbol='€')
    #     return currency.pk

    class Meta:
        ordering = ('name',)


class UserManager(BaseUserManager):

    def create_user(self, username, email, name, password=None):
        if not username:
            raise ValueError('User must have an username')
        if not email:
            raise ValueError('User must have an email')
        if not name:
            raise ValueError('User must have a name')
        if not password:
            raise ValueError('User must have a password')

        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            username=username
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self,username, email, name, password=None):

        if not username:
            raise ValueError('User must have an username')
        if not email:
            raise ValueError('User must have an email')
        if not name:
            raise ValueError('User must have a name')
        if not password:
            raise ValueError('User must have a password')

        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            username=username
        )
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self.db)
        return user


class User(AbstractBaseUser):
    username = models.CharField('Username', max_length=255, unique=True)
    email = models.EmailField('Email', max_length=255, unique=True)
    name = models.CharField('Name', max_length=255)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']


class Category(models.Model):
    name = models.CharField('Name', max_length=255)


class Month(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)


class AmountBase(ModelBase):
    name = models.CharField('Name', max_length=255)
    description = models.TextField('Entry')
    amount = models.FloatField('Amount')
    month = models.ForeignKey(Month, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class Entry(AmountBase):

    def __str__(self):
        return self.name


class Expense(AmountBase):

    def __str__(self):
        return self.name


class Post(ModelBase):
    title = models.CharField('Title', max_length=255)
    description = models.TextField()
    finished = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_like' )

    def total_likes(self):
        return self.likes.count()


class Comment(MPTTModel, ModelBase):
    description = models.TextField(null=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', related_name='children', null=True, db_index=True, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='comment_like')

    def total_likes(self):
        return self.likes.count()


class CompanyStock(ModelBase):
    name = models.CharField('Name', max_length=255)
    url = models.URLField(max_length=255)


class UserCompany(ModelBase):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    companystock = models.ForeignKey(CompanyStock, on_delete=models.CASCADE)

