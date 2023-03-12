# Generated by Django 4.1.7 on 2023-03-03 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('SA', 'Super Admin'), ('A', 'Admin'), ('U', 'User')], max_length=2)),
            ],
        ),
    ]
