# Generated by Django 4.1.2 on 2022-10-24 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_image_featured'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-id']},
        ),
    ]
