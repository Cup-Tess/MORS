from django.conf import settings
from django.db import models


class Post(models.Model):
    SELECTOR_TRAT = (
        ('П', 'Продукты'),
        ('Т', 'Транспорт'),
        ('О', 'Одежда'),
        ('С', 'Коммунальные услуги'),
        ('А', 'Аптеки'),
        ('Ж', 'Дом'),
        ('Д', 'Доход'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notes = models.CharField(blank=True, null=True, max_length=200)
    summa = models.DecimalField(default=0, max_digits=10, decimal_places=1)
    selector = models.CharField(max_length=50, choices=SELECTOR_TRAT, verbose_name="selector", blank=True)
    published_date = models.CharField(max_length=100, blank=True, null=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.selector


class Datas(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    edin = models.IntegerField(default=1)
    SI = models.CharField(max_length=100, default='рубль')
    data1 = models.CharField(max_length=100, blank=True, null=True)
    data2 = models.CharField(max_length=100, blank=True, null=True)
    ost = models.DecimalField(default=0, max_digits=10, decimal_places=1)

    def publish(self):
        self.save()

    def __str__(self):
        return self.SI
