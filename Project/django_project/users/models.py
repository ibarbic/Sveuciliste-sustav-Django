from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.deletion import CASCADE
from .managers import UserManager


from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


class Uloge(models.Model):
    naziv = models.CharField(max_length=50)

    class Meta:
        db_table = 'uloge'


class CustomUser(AbstractBaseUser):
    email = models.CharField(verbose_name="email", max_length=55, unique=True)
    password = models.CharField(max_length=128, unique=True)
    role = models.ForeignKey(Uloge, on_delete=models.CASCADE, default=3)
    status = models.CharField(max_length=10, default="none")
    username = models.CharField(max_length=30)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_staff = models.IntegerField(default=False)
    is_active = models.IntegerField(default=True)
    is_superuser = models.IntegerField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.email  # kad zelimo isprintat ime usera dobijemo ovo

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = 'korisnici'


class Predmeti(models.Model):
    ime = models.CharField(max_length=255)
    kod = models.CharField(unique=True, max_length=16)
    program = models.TextField(default="None")
    bodovi = models.IntegerField(null=True, blank=True)
    sem_redovni = models.IntegerField(null=True, blank=True)
    sem_izvanredni = models.IntegerField(null=True, blank=True)
    izborni = models.CharField(max_length=2)
    nositelj = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'predmeti'


class Upisi(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    status = models.CharField(max_length=64, default="nepolozen")

    class Meta:
        db_table = 'upisi'
