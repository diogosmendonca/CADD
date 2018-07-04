# Generated by Django 2.0.4 on 2018-06-17 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alocacacaodisciplinasemdepartamento',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'managed': False,
                'db_table': 'alocacacaodisciplinasemdepartamento',
            },
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('matricula', models.CharField(blank=True, max_length=255, null=True)),
                ('cpf', models.CharField(blank=True, max_length=255, null=True)),
                ('nome', models.CharField(blank=True, max_length=255, null=True)),
                ('endereco', models.CharField(blank=True, max_length=255, null=True)),
                ('datanascimento', models.DateTimeField(blank=True, db_column='dataNascimento', null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'aluno',
            },
        ),
        migrations.CreateModel(
            name='Atividadecomplementar',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cargahorariamax', models.TextField(blank=True, db_column='cargaHorariaMax', null=True)),
                ('cargahorariamin', models.TextField(blank=True, db_column='cargaHorariaMin', null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'atividadecomplementar',
            },
        ),
        migrations.CreateModel(
            name='Blocoequivalencia',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'managed': False,
                'db_table': 'blocoequivalencia',
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(blank=True, max_length=255, null=True)),
                ('sigla', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'curso',
            },
        ),
        migrations.CreateModel(
            name='Cursodisciplina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
                'db_table': 'curso_disciplina',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(blank=True, max_length=255, null=True)),
                ('sigla', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'departamento',
            },
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(blank=True, max_length=255, null=True)),
                ('codigo', models.CharField(blank=True, max_length=255, null=True)),
                ('quantidadecreditos', models.IntegerField(blank=True, db_column='quantidadeCreditos', null=True)),
                ('cargahoraria', models.IntegerField(db_column='cargaHoraria')),
                ('ehoptativa', models.NullBooleanField(db_column='ehOptativa', verbose_name='Optativa')),
            ],
            options={
                'managed': False,
                'db_table': 'disciplina',
            },
        ),
        migrations.CreateModel(
            name='Historicoescolar',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'managed': False,
                'db_table': 'historicoescolar',
            },
        ),
        migrations.CreateModel(
            name='Inscricao',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'managed': False,
                'db_table': 'inscricao',
            },
        ),
        migrations.CreateModel(
            name='Itemhistoricoescolar',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ano', models.IntegerField(blank=True, null=True)),
                ('periodo', models.IntegerField(blank=True, null=True)),
                ('situacao', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'itemhistoricoescolar',
            },
        ),
        migrations.CreateModel(
            name='Notafinal',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('frequencia', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('notap1', models.DecimalField(blank=True, db_column='notaP1', decimal_places=2, max_digits=19, null=True)),
                ('notap2', models.DecimalField(blank=True, db_column='notaP2', decimal_places=2, max_digits=19, null=True)),
                ('notap3', models.DecimalField(blank=True, db_column='notaP3', decimal_places=2, max_digits=19, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'notafinal',
            },
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('matricula', models.CharField(blank=True, max_length=255, null=True)),
                ('cpf', models.CharField(blank=True, max_length=255, null=True)),
                ('datanascimento', models.DateTimeField(blank=True, db_column='dataNascimento', null=True)),
                ('endereco', models.CharField(blank=True, max_length=255, null=True)),
                ('nome', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'professor',
            },
        ),
        migrations.CreateModel(
            name='Registroatividadecomplementar',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cargahoraria', models.TextField(blank=True, db_column='cargaHoraria', null=True)),
                ('dataanalise', models.DateTimeField(blank=True, db_column='dataAnalise', null=True)),
                ('descricao', models.CharField(blank=True, max_length=255, null=True)),
                ('estado', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'registroatividadecomplementar',
            },
        ),
        migrations.CreateModel(
            name='Tabelaatividadescomplementares',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'managed': False,
                'db_table': 'tabelaatividadescomplementares',
            },
        ),
        migrations.CreateModel(
            name='TabelaatividadescomplementaresAtividadecomplementar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
                'db_table': 'tabelaatividadescomplementares_atividadecomplementar',
            },
        ),
        migrations.CreateModel(
            name='Tabelaequivalencias',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'managed': False,
                'db_table': 'tabelaequivalencias',
            },
        ),
        migrations.CreateModel(
            name='Tipoatividadecomplementar',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('categoria', models.IntegerField(blank=True, null=True)),
                ('descricao', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'tipoatividadecomplementar',
            },
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(blank=True, max_length=255, null=True)),
                ('ano', models.IntegerField(blank=True, null=True)),
                ('periodo', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'turma',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(db_column='TYPE', max_length=30, unique=True)),
            ],
            options={
                'managed': False,
                'db_table': 'user_profile',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateTimeField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('login', models.CharField(max_length=255, unique=True)),
                ('matricula', models.CharField(blank=True, max_length=255, null=True)),
                ('nome', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Versaocurso',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('numero', models.CharField(blank=True, max_length=255, null=True)),
                ('qtdperiodominimo', models.IntegerField(blank=True, db_column='qtdPeriodoMinimo', null=True)),
                ('situacao', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'versaocurso',
            },
        ),
        migrations.CreateModel(
            name='Departamentodisciplina',
            fields=[
                ('departamento', models.OneToOneField(db_column='Departamento_id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='sca.Departamento')),
            ],
            options={
                'managed': False,
                'db_table': 'departamento_disciplina',
            },
        ),
        migrations.CreateModel(
            name='Departamentoprofessor',
            fields=[
                ('departamento', models.OneToOneField(db_column='Departamento_id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='sca.Departamento')),
            ],
            options={
                'managed': False,
                'db_table': 'departamento_professor',
            },
        ),
        migrations.CreateModel(
            name='DisciplinaPrereqs',
            fields=[
                ('grade', models.OneToOneField(db_column='GRADE_ID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='grade', serialize=False, to='sca.Disciplina')),
            ],
            options={
                'managed': False,
                'db_table': 'disciplina_prereqs',
            },
        ),
        migrations.CreateModel(
            name='Disciplinasequivalentes',
            fields=[
                ('bloco', models.OneToOneField(db_column='BLOCO_ID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='sca.Blocoequivalencia')),
            ],
            options={
                'managed': False,
                'db_table': 'disciplinas_equivalentes',
            },
        ),
        migrations.CreateModel(
            name='Disciplinasoriginais',
            fields=[
                ('bloco', models.OneToOneField(db_column='BLOCO_ID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='sca.Blocoequivalencia')),
            ],
            options={
                'managed': False,
                'db_table': 'disciplinas_originais',
            },
        ),
        migrations.CreateModel(
            name='Professordisciplina',
            fields=[
                ('professor', models.OneToOneField(db_column='PROFESSOR_ID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='sca.Professor')),
            ],
            options={
                'managed': False,
                'db_table': 'professor_disciplina',
            },
        ),
        migrations.CreateModel(
            name='TabelaequivalenciasBlocoequivalencia',
            fields=[
                ('tabelaequivalencias', models.OneToOneField(db_column='TabelaEquivalencias_id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='sca.Tabelaequivalencias')),
            ],
            options={
                'managed': False,
                'db_table': 'tabelaequivalencias_blocoequivalencia',
            },
        ),
        migrations.CreateModel(
            name='Useruserprofile',
            fields=[
                ('user', models.OneToOneField(db_column='USER_ID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='sca.Users')),
            ],
            options={
                'managed': False,
                'db_table': 'user_user_profile',
            },
        ),
        migrations.CreateModel(
            name='VersaocursoTabelaequivalencias',
            fields=[
                ('versaocurso', models.OneToOneField(db_column='VersaoCurso_id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='sca.Versaocurso')),
            ],
            options={
                'managed': False,
                'db_table': 'versaocurso_tabelaequivalencias',
            },
        ),
    ]