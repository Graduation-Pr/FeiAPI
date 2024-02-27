# Generated by Django 5.0.2 on 2024-02-27 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctorprofile",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="doctorprofile",
            name="full_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="doctorprofile",
            name="username",
            field=models.CharField(default="", max_length=150, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="patientprofile",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="patientprofile",
            name="full_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="patientprofile",
            name="username",
            field=models.CharField(default="", max_length=150, unique=True),
            preserve_default=False,
        ),
    ]
