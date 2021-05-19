from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from mptt.models import MPTTModel, TreeForeignKey


class ModelBase(models.Model):
    """ModelBase"""
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def soft_delete(self):
        self.delete_at = timezone.now()
        self.is_active = False

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class Currency(ModelBase):
    """Currency, modelo para divisas"""
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
    """User Manager, crea usuario y superusuario"""
    def create_user(self, username, email, name, password=None):
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        if not name:
            raise ValueError('El usuario debe tener un nombre')
        if not password:
            raise ValueError('El usuario debe tener una contraseña')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            username=username,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, name, password=None):

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
        user.is_staff = True

        user.set_password(password)
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User, modelo para usuario"""
    username = models.CharField('Username', max_length=255, unique=True)
    email = models.EmailField('Email', max_length=255, unique=True)
    name = models.CharField('Name', max_length=255)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=1)
    date_joined = models.DateTimeField(
        verbose_name='date joined',
        auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='profiles')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']


class UserFollowing(ModelBase):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'], name='unique_followers')
        ]


class Category(ModelBase):
    """Category, modelo para categorias de ingresos y gastos"""
    name = models.CharField('Name', max_length=255)


class Month(ModelBase):
    """Month, modelo para llevar el control del mes"""
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class AmountBase(ModelBase):
    """AmountBase, Base para los ingresos y gastos"""
    name = models.CharField('Name', max_length=255)
    description = models.TextField('Entry')
    amount = models.FloatField('Amount')
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class Entry(AmountBase):
    """Entry, modelo para los ingresos"""
    def __str__(self):
        return self.name


class Expense(AmountBase):
    """Expense, modelo para los gastos"""
    def __str__(self):
        return self.name


class Tag(ModelBase):
    """Tags para los post"""
    name = models.CharField('Tag', max_length=255)
    color = models.CharField('Color', max_length=255)


class Post(ModelBase):
    """Post, modelo para el post"""
    title = models.CharField('Title', max_length=255)
    description = models.TextField()
    finished = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    likes = models.ManyToManyField(User, through='PostLike',)
    tags = models.ManyToManyField(Tag, related_name='tags')

    def total_likes(self):
        return self.likes.count()


class PostLike(ModelBase):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(MPTTModel, ModelBase):
    """Comment, modelo para los comentarios del post"""
    description = models.TextField(null=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', related_name='children', null=True,
                            db_index=True, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='comment_like')

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ('-created_at',)


class CompanyStock(ModelBase):
    """CompanyStock, modelo para api de acciones de la bolsa"""
    name = models.CharField('Name', max_length=255)
    symbol = models.CharField('Symbol', max_length=255)


class UserCompany(ModelBase):
    """UserCompany, modelo para vincular un usuario con una accion de bolsa"""
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    companystock = models.ForeignKey(CompanyStock, on_delete=models.CASCADE)
