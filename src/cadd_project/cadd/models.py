from django.db import models
from django.utils import timezone

# Create your models here.

PERIODO_CHOICES = (
    (1, '1º semestre'),
    (2, '2º semestre'),
)


class Comissao(models.Model):
    """Classe de uso do sistema para o cadastro das comissões"""

    descricao = models.CharField(u'Descrição', max_length=50, blank=False,
                    null=False)
    curso = models.ForeignKey('sca.Curso', models.DO_NOTHING, blank=False,
                    null=False)

    def __str__(self):
        return self.descricao

    class Meta:
        managed = True
        db_table = 'comissao'
        app_label = 'cadd'


class Membro(models.Model):
    """Classe de uso do sistema para o cadastro dos membros das CADDs"""

    ativo = models.BooleanField(u'Ativo')
    presidente = models.BooleanField(u'Presidente')
    portaria = models.CharField(u'Portaria', max_length=50, blank=False,
                        null=False)
    comissao = models.ForeignKey('Comissao', models.DO_NOTHING, blank=False,
                        null=False)
    professor = models.ForeignKey('sca.Professor', models.DO_NOTHING,
                        blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'membro'
        app_label = 'cadd'


class Reuniao(models.Model):
    """Classe de uso do sistema para o agendamento das reuniões"""

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
    inicio = models.TimeField(u'Início', blank=False, null=False)
    local = models.CharField(u'Local', max_length=50, blank=False, null=False)
    situacao = models.CharField(u'Situação', max_length=1,
                    choices=SITUACAO_CHOICES, blank=False, default='A')
    tipo = models.CharField(u'Tipo', max_length=1, choices=TIPO_CHOICES,
                    blank=False, default='I')
    anotacao = models.TextField(u'Anotação', blank=True, null=True)
    comissao = models.ForeignKey('Comissao', models.DO_NOTHING, blank=False,
                    null=False)

    class Meta:
        managed = True
        db_table = 'reuniao'
        app_label = 'cadd'


class Convocacao(models.Model):
    """Classe de uso do sistema para a guarda dos alunos convocados às reuniões"""

    envioemail = models.BooleanField(u'Email')
    presente = models.BooleanField(u'Presente')
    anotacao = models.TextField(u'Anotação', blank=True, null=True)
    reuniao = models.ForeignKey('Reuniao', models.DO_NOTHING, blank=False,
                    null=False)
    aluno = models.ForeignKey('sca.Aluno', models.DO_NOTHING, blank=False,
                    null=False)

    class Meta:
        managed = True
        db_table = 'convocacao'
        app_label = 'cadd'


class Documento(models.Model):
    """Classe de uso do sistema para a guarda dos documentos escaneados dos alunos"""

    ano = models.PositiveSmallIntegerField(u'Ano', blank=False, null=False)
    periodo = models.PositiveSmallIntegerField(u'Período', choices=PERIODO_CHOICES,
                    blank=False, default=1, null=False)
    descricao = models.CharField(u'Descrição', max_length=50, blank=False,
                    null=False)
    indice = models.FileField(u'Índice', max_length=50, blank=False, null=False)
    aluno = models.ForeignKey('sca.Aluno', models.DO_NOTHING, blank=False,
                    null=False)

    class Meta:
        managed = True
        db_table = 'documento'
        app_label = 'cadd'


class Horario(models.Model):
    """Classe de uso do sistema para a guarda da prévia do horário do semestre subsequente"""

    ano = models.PositiveSmallIntegerField(u'Ano', blank=False, null=False)
    periodo = models.PositiveSmallIntegerField(u'Período', choices=PERIODO_CHOICES,
                    blank=False, default=1, null=False)
    curso = models.ForeignKey('sca.Curso', models.DO_NOTHING, blank=False,
                null=False)

    def __str__(self):
        return str(self.ano) + '.' + str(self.periodo) + '-' + self.curso.sigla

    class Meta:
        managed = True
        db_table = 'horario'
        app_label = 'cadd'


class ItemHorario(models.Model):
    """Classe de uso do sistema para a guarda dos itens da prévia do horário"""

    DIASEMANA_CHOICES = (
        (0, 'Domingo'),
        (1, 'Segunda-feira'),
        (2, 'Terça-feira'),
        (3, 'Quarta-feira'),
        (4, 'Quinta-feira'),
        (5, 'Sexta-feira'),
        (6, 'Sábado'),
    )

    periodo = models.CharField(u'Período', max_length=3, blank=False,
                        null=False)
    diasemana = models.PositiveSmallIntegerField(u'Dia da semana', blank=False,
                        null=False, choices=DIASEMANA_CHOICES)
    inicio = models.TimeField(u'Início', blank=False, null=False)
    fim = models.TimeField(u'Início', blank=False, null=False)
    horario = models.ForeignKey('Horario', models.DO_NOTHING, blank=False,
                        null=False)
    professor = models.ForeignKey('sca.Professor', models.DO_NOTHING,
                        blank=False, null=False)
    departamento = models.ForeignKey('sca.Departamento', models.DO_NOTHING,
                        blank=False, null=False)
    disciplina = models.ForeignKey('sca.Disciplina', models.DO_NOTHING,
                        blank=False, null=False)
    turma = models.ForeignKey('sca.Turma', models.DO_NOTHING, blank=False,
                        null=False)

    class Meta:
        managed = True
        db_table = 'item_horario'
        app_label = 'cadd'


class Plano(models.Model):
    """Classe de uso do sistema para a guarda dos planos de estudo dos alunos"""

    SITUACAO_CHOICES = (
        ('M', 'Montado'),
        ('A', 'Avaliado'),
        ('E', 'Encerrado'),
    )
    ano = models.PositiveSmallIntegerField(u'Ano', blank=False, null=False)
    periodo = models.PositiveSmallIntegerField(u'Período', choices=PERIODO_CHOICES,
                    blank=False, default=1, null=False)
    situacao = models.CharField(u'Situação', max_length=1,
                    choices=SITUACAO_CHOICES, blank=False, default='M')
    avaliacao = models.TextField(u'Anotação', blank=True, null=True)
    aluno = models.ForeignKey('sca.Aluno', models.DO_NOTHING, blank=False,
                    null=False)

    class Meta:
        managed = True
        db_table = 'plano'
        app_label = 'cadd'


class ItemPlanoAtual(models.Model):
    """Classe de uso do sistema para a guarda dos itens atuais do plano de estudo dos alunos"""

    plano = models.ForeignKey('Plano', models.DO_NOTHING, blank=False,
                    null=False)
    itemhorario = models.ForeignKey('ItemHorario', models.DO_NOTHING,
                    blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'item_plano_atual'
        app_label = 'cadd'


class PlanoFuturo(models.Model):
    """Classe de uso do sistema para a guarda do plano de estudo futuro dos alunos"""

    ano = models.PositiveSmallIntegerField(u'Ano', blank=False, null=False)
    periodo = models.PositiveSmallIntegerField(u'Período', choices=PERIODO_CHOICES,
                    blank=False, default=1, null=False)
    plano = models.ForeignKey('Plano', models.DO_NOTHING, blank=False,
                    null=False)

    class Meta:
        managed = True
        db_table = 'plano_futuro'
        app_label = 'cadd'


class ItemPlanoFuturo(models.Model):
    """Classe de uso do sistema para a guarda dos itens do futuro do plano de estudo dos alunos"""

    planofuturo = models.ForeignKey('PlanoFuturo', models.DO_NOTHING,
                        blank=False, null=False)
    disciplina = models.ForeignKey('sca.Disciplina', models.DO_NOTHING,
                        blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'item_plano_futuro'
        app_label = 'cadd'
