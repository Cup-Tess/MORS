# Generated by Django 4.0.2 on 2022-02-10 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(blank=True, max_length=200, null=True)),
                ('summa', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('selector', models.CharField(blank=True, choices=[('П', 'Продукты'), ('Т', 'Транспорт'), ('О', 'Одежда'), ('С', 'Коммунальные услуги'), ('А', 'Аптеки'), ('Ж', 'Дом'), ('Д', 'Доход')], max_length=50, verbose_name='selector')),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
