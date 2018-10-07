from __future__ import unicode_literals

from django.db import migrations, models
import judge.models
import judge.utils.problem_data


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0069_judge_blocking'),
    ]

    operations = [
        migrations.AddField(
            model_name='problemdata',
            name='custom_judge',
            field=models.FileField(blank=True, null=True, storage=judge.utils.problem_data.ProblemDataStorage(), upload_to=judge.models.problem_directory_file, verbose_name='custom judge file'),
        )
    ]
