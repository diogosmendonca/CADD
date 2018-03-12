from django.db import models

# Create your models here.

class Comissao(models.Model):
    descricao = models.CharField(u'Descrição', max_length=50, blank=False, null=False)

    class Meta:
        managed = True


class Membro(models.Model):
    ativo = models.IntegerField(u'Ativo')
    presidente = models.IntegerField(u'Presidente')
    portaria = models.CharField(u'Portaria', max_length=50, blank=False, null=True)
    comissao = models.ForeignKey('Comissao', models.DO_NOTHING, blank=False, null=True)
    professor = models.ForeignKey('Professor', models.DO_NOTHING, blank=False, null=True)

    class Meta:
        managed = True


class Reuniao(models.Model):
    SITUACAO_CHOICES = (
        ('A', 'Agendada'),
        ('C', 'Cancelada'),
        ('E', 'Encerrada'),
    )
    TIPO_CHOICES = (
        ('I', 'Informação'),
        ('C', 'Convocação'),
    )

    data = models.DateField(u'Data', blank=False, null=False)
    inicio = models.DateTimeField(u'Início', blank=False, null=False)
    local = models.CharField(u'Local', max_length=50, blank=False, null=False)
    situacao = models.CharField(u'Situação', max_length=1, choices=SITUACAO_CHOICES, blank=False, default='A')
    tipo = models.CharField(u'Tipo', max_length=1, choices=TIPO_CHOICES, blank=False, default='I')
    anotacao = models.TextField(u'Anotação', blank=True)
    comissao = models.ForeignKey('Comissao', models.DO_NOTHING, blank=False, null=True)

    class Meta:
        managed = True


class Convocacao(models.Model):
    envioemail = models.IntegerField(u'Email')
    presente = models.IntegerField(u'Presente')
    anotacao = models.TextField(u'Anotação', blank=True)
    reuniao = models.ForeignKey('Reuniao', models.DO_NOTHING, blank=False, null=False)
    aluno = models.ForeignKey('Aluno', models.DO_NOTHING, blank=False, null=False)

    class Meta:
        managed = True


class Documento(models.Model):
    ano = models.IntegerField(u'Ano')
    semestre = models.IntegerField(u'Semestre')
    descricao = models.CharField(u'Descrição', max_length=50, blank=False, null=False)
    indice = models.CharField(u'Índice', max_length=50, blank=False, null=False)
    aluno = models.ForeignKey('Aluno', models.DO_NOTHING, blank=False, null=False)

    class Meta:
        managed = True


class Horario(models.Model):
    ano = models.IntegerField(u'Ano')
    semestre = models.IntegerField(u'Semestre')
    curso = models.ForeignKey('Curso', models.DO_NOTHING, blank=False, null=True)

    class Meta:
        managed = True


class ItemHorario(models.Model):
    periodo = models.IntegerField(u'Período')
    diasemana = models.IntegerField()
    inicio = models.DateTimeField(u'Início', blank=False, null=False)
    fim = models.DateTimeField(u'Início', blank=False, null=False)
    horario = models.ForeignKey('Horario', models.DO_NOTHING, blank=False, null=False)
    professor = models.ForeignKey('Professor', models.DO_NOTHING, blank=False, null=False)
    departamento = models.ForeignKey('Departamento', models.DO_NOTHING, blank=False, null=False)
    disciplina = models.ForeignKey('Disciplina', models.DO_NOTHING, blank=False, null=False)
    turma = models.ForeignKey('Turma', models.DO_NOTHING, blank=False, null=False)

    class Meta:
        managed = True


class Plano(models.Model):
    SITUACAO_CHOICES = (
        ('M', 'Montado'),
        ('A', 'Avaliado'),
        ('E', 'Encerrado'),
    )
    ano = models.IntegerField(u'Ano')
    semestre = models.IntegerField(u'Semestre')
    situacao = models.CharField(u'Situação', max_length=1, choices=SITUACAO_CHOICES, blank=False, default='M')
    avaliacao = models.TextField(u'Anotação', blank=True)
    aluno = models.ForeignKey('Aluno', models.DO_NOTHING, blank=False, null=False)

    class Meta:
        managed = True


class ItemPlanoAtual(models.Model):
    plano = models.ForeignKey('Plano', models.DO_NOTHING, blank=False, null=False)
    itemhorario = models.ForeignKey('ItemHorario', models.DO_NOTHING, blank=False, null=False)

    class Meta:
        managed = True


class PlanoFuturo(models.Model):
    ano = models.IntegerField(u'Ano')
    periodo = models.IntegerField(u'Período')
    plano = models.ForeignKey('Plano', models.DO_NOTHING, blank=False, null=False)

    class Meta:
        managed = True


class ItemPlanoFuturo(models.Model):
    planofuturo = models.ForeignKey('PlanoFuturo', models.DO_NOTHING, blank=False, null=False)
    disciplina = models.ForeignKey('Disciplina', models.DO_NOTHING, blank=False, null=False)

    class Meta:
        managed = True
