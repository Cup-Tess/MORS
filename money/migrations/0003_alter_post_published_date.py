# Generated by Django 4.0.2 on 2022-02-19 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0002_alter_post_published_date_alter_post_summa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
