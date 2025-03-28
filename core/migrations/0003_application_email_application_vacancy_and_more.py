# Generated by Django 4.2.20 on 2025-03-29 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_application_alter_vacancy_was_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='email',
            field=models.EmailField(default='rukhadze.liza@gtu.ge', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application',
            name='vacancy',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='core.vacancy'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vacancy',
            name='company_email',
            field=models.EmailField(default='lizirukh@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='application',
            table='applications',
        ),
    ]
