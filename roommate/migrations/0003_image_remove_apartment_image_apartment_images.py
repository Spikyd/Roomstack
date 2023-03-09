# Generated by Django 4.1.7 on 2023-03-07 11:33

from django.db import migrations, models
import roommate.models


class Migration(migrations.Migration):

    dependencies = [
        ('roommate', '0002_rename_room_favorite_apartment_alter_apartment_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=roommate.models.get_upload_path)),
            ],
        ),
        migrations.RemoveField(
            model_name='apartment',
            name='image',
        ),
        migrations.AddField(
            model_name='apartment',
            name='images',
            field=models.ManyToManyField(blank=True, to='roommate.image'),
        ),
    ]
