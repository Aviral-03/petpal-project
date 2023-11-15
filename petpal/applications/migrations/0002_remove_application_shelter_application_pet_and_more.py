# Generated by Django 4.2.6 on 2023-11-15 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pet_listings', '0002_pets_image'),
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='shelter',
        ),
        migrations.AddField(
            model_name='application',
            name='pet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pet_listings.pets'),
        ),
        migrations.AlterField(
            model_name='application',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]