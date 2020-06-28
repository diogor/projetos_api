import hashlib
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


def upload_directory_path(instance, filename):
    return 'users/{}/{}.{}'.format(
        instance.username, hashlib.sha224(filename.encode()).hexdigest(),
        filename.split(".")[-1:]
    )


class MyUserManager(BaseUserManager):
    def create_user(self, telefone, nome, password=None):
        if not telefone:
            raise ValueError('Users must have a phone #')

        user = self.model(
            telefone=telefone,
            nome=nome
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nome, telefone, password):
        user = self.create_user(
            telefone,
            password=password,
            nome=nome
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    telefone = PhoneNumberField(unique=True)
    nome = models.CharField(max_length=300)
    avatar = models.ImageField(null=True, upload_to=upload_directory_path)
    apresentacao = models.CharField(max_length=120, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'telefone'
    REQUIRED_FIELDS = ['nome']

    class Meta:
        ordering = ['nome']

    def get_full_name(self):
        return self.nome or self.telefone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return f'{self.nome} - {self.telefone}'
