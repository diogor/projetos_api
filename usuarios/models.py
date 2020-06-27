import hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser


def upload_directory_path(instance, filename):
    return 'users/{}/{}.{}'.format(
        instance.username, hashlib.sha224(filename.encode()).hexdigest(),
        filename.split(".")[-1:]
    )


class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to=upload_directory_path)
    apresentacao = models.CharField(max_length=120, blank=True, null=True)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}' or self.username
