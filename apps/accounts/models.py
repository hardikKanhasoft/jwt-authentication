from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, name, is_tc, phone_no, password=None):
        """
        Creates and saves a User with the given email, name, tc and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            is_tc=is_tc,
            phone_no=phone_no,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, is_tc, phone_no, password=None):
        """
        Creates and saves a superuser with the ggiven email, name, tc and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            is_tc=is_tc,
            phone_no=phone_no,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=10)
    is_tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(
        Group,
        blank=True,
        verbose_name="groups",
        help_text="The groups this user belongs to.",
        related_name="accounts_user_groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        verbose_name="user permissions",
        help_text="Specific permissions for this user.",
        related_name="accounts_user_permissions" 
)
    objects = UserManager()
    USERNAME_FIELD = "email"