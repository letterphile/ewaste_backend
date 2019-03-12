# Generated by Django 2.1.7 on 2019-03-03 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_remove_file_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='file',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.File'),
            preserve_default=False,
        ),
    ]