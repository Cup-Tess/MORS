from django.conf import settings
from django.db import models
from django.utils import timezone



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
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.notes