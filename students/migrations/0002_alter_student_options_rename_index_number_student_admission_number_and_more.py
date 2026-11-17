import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={
                'ordering': ['class_name', 'last_name', 'first_name'],
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students'
            },
        ),
        migrations.RenameField(
            model_name='student',
            old_name='index_number',
            new_name='admission_number',
        ),
        migrations.AlterField(
            model_name='student',
            name='admission_number',
            field=models.CharField(max_length=20, unique=True, verbose_name='Admission Number'),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='class_name',
            field=models.CharField(max_length=20, verbose_name='Class'),
        ),
        migrations.AddField(
            model_name='student',
            name='date_registered',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date Registered'),
            preserve_default=False,
        ),
    ]
