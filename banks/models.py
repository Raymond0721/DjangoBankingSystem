from django.db import models
from django.conf import settings
from django.utils import timezone


class Bank(models.Model):
    bank_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    inst_num = models.CharField(max_length=20)
    swift_code = models.CharField(max_length=11)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='banks')

    def __str__(self):
        return self.name


class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=200)
    transit_num = models.CharField(max_length=20)
    address = models.TextField()
    email = models.EmailField()
    capacity = models.PositiveIntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} Branch of {self.bank.name}"
