# Generated by Django 3.2.16 on 2022-11-23 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='coaches', to='users.Student'),
        ),
    ]
