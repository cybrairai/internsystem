from django.db import models, transaction
from django.db.models import Sum
from core.models import User, Card, Semester
from django.utils import timezone
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class VoucherWallet(models.Model):
    user = models.ForeignKey(User)
    semester = models.ForeignKey(Semester)
    cached_balance = models.DecimalField(default=0, max_digits=8, decimal_places=2, editable=False)

    class Meta:
        unique_together = ("user", "semester")

    def calculate_balance(self):
        vouchers_earned = WorkLog.objects.filter(wallet=self).aggregate(sum=Sum('vouchers'))['sum'] or Decimal(0)
        vouchers_used = VoucherUseLog.objects.filter(wallet=self).aggregate(sum=Sum('vouchers'))['sum'] or Decimal(0)
        self.cached_balance = vouchers_earned - vouchers_used
        self.save()
        return self.cached_balance

    def __str__(self):
        return str(self.user)+" ("+str(self.semester)+")"

class WorkLog(models.Model):
    wallet = models.ForeignKey(VoucherWallet)
    date_issued = models.DateTimeField(auto_now_add=True)
    date_worked = models.DateField()
    work_group = models.CharField(max_length=20)
    hours = models.DecimalField(max_digits=8, decimal_places=1)
    vouchers = models.DecimalField(max_digits=8, decimal_places=2)
    issuing_user = models.ForeignKey(User)
    comment = models.CharField(max_length=100)

    def __str__(self):
        return str(self.wallet)+" "+str(self.date_worked)+" "+str(self.hours)+" hours"

    def clean(self):
        if self.hours <= 0:
            raise ValidationError({'hours': _("Hours must be positive")})

        if self.vouchers <= 0:
            raise ValidationError({'vouchers': _("Vouchers must be positive")})

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super(WorkLog, self).save(*args, **kwargs)
            self.wallet.calculate_balance()

class VoucherUseLog(models.Model):
    wallet = models.ForeignKey(VoucherWallet)
    date_spent = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100)
    vouchers = models.IntegerField()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.wallet.calculate_balance()

    def clean(self):
        if self.vouchers is None or self.vouchers <= 0 or (self.vouchers % 1) != 0:
            raise ValidationError({'vouchers': _('Vouchers must be a positive whole number')})

    def __str__(self):
        return "%s - %s at %s (%s)" % (self.wallet, self.vouchers, self.date_spent, self.comment)

