# Generated by Django 2.1.5 on 2019-09-09 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0015_auto_20190909_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='user_img',
            field=models.ImageField(unique=True, upload_to='user_images/'),
        ),
    ]
