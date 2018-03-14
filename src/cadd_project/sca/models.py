# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create,
#        modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alocacacaodisciplinasemdepartamento(models.Model):
    """Classe importada da tabela alocacacaodisciplinasemdepartamento do banco de dados SCA"""

    id = models.BigAutoField(primary_key=True)
    departamento = models.ForeignKey('Departamento', models.DO_NOTHING,
                        blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alocacacaodisciplinasemdepartamento'


class Aluno(models.Model):
    """Classe importada da tabela aluno do banco de dados SCA"""
    """TODO: Faltam os campos email, situacao, faixa e formaEvasao não contemplados no esquema"""

    id = models.BigAutoField(primary_key=True)
    matricula = models.CharField(max_length=255, blank=True, null=True)
    cpf = models.CharField(max_length=255, blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    datanascimento = models.DateTimeField(db_column='dataNascimento',
                        blank=True, null=True)
    historico = models.ForeignKey('Historicoescolar', models.DO_NOTHING,
                    blank=True, null=True)
    versaocurso = models.ForeignKey('Versaocurso', models.DO_NOTHING,
                    db_column='versaoCurso_id', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aluno'


class Blocoequivalencia(models.Model):
    """Classe importada da tabela blocoequivalencia do banco de dados SCA"""

    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'blocoequivalencia'


class Curso(models.Model):
    """Classe importada da tabela curso do banco de dados SCA"""

    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    sigla = models.CharField(max_length=255, blank=True, null=True)
    coordenador = models.ForeignKey('Professor', models.DO_NOTHING,
                        blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'curso'


class CursoDisciplina(models.Model):
    """Classe importada da tabela curso_disciplina do banco de dados SCA"""

    curso = models.ForeignKey(Curso, models.DO_NOTHING)
    disciplinas = models.ForeignKey('Disciplina', models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'curso_disciplina'


class Departamento(models.Model):
    """Classe importada da tabela departamento do banco de dados SCA"""

    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    sigla = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'departamento'


class DepartamentoDisciplina(models.Model):
    """Classe importada da tabela departamento_disciplina do banco de dados SCA"""

    departamento = models.ForeignKey(Departamento, models.DO_NOTHING,
                        primary_key=True)
    disciplinas = models.ForeignKey('Disciplina', models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'departamento_disciplina'
        unique_together = (('departamento', 'disciplinas'),)


class DepartamentoProfessor(models.Model):
    """Classe importada da tabela departamento_professor do banco de dados SCA"""

    departamento = models.ForeignKey(Departamento, models.DO_NOTHING,
                        primary_key=True)
    professores = models.ForeignKey('Professor', models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'departamento_professor'
        unique_together = (('departamento', 'professores'),)


class Disciplina(models.Model):
    """Classe importada da tabela disciplina do banco de dados SCA"""
    """Incluído o campo ehoptativa diferentemente do diagrama de classes"""

    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    codigo = models.CharField(max_length=255, blank=True, null=True)
    quantidadecreditos = models.IntegerField(db_column='quantidadeCreditos',
                            blank=True, null=True)
    cargahoraria = models.IntegerField(db_column='cargaHoraria')
    ehoptativa = models.TextField(db_column='ehOptativa', blank=True, null=True)
    versaocurso = models.ForeignKey('Versaocurso', models.DO_NOTHING,
                            db_column='versaoCurso_id', blank=True, null=True)
    alocacao_depto = models.ForeignKey(Departamento, models.DO_NOTHING,
                            blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'disciplina'


#class DisciplinaPrereqs(models.Model):
#    """Classe importada da tabela disciplina_prereqs do banco de dados SCA"""
#    """TODO: Não entendi o porquê de ser relacionado com gradedisponibilidade"""

#    grade = models.ForeignKey('Gradedisponibilidade', models.DO_NOTHING, primary_key=True)
#    disciplina = models.ForeignKey(Disciplina, models.DO_NOTHING)

#    class Meta:
#        managed = False
#        db_table = 'disciplina_prereqs'
#        unique_together = (('grade', 'disciplina'),)


class DisciplinasEquivalentes(models.Model):
    """Classe importada da tabela disciplinas_equivalentes do banco de dados SCA"""

    bloco = models.ForeignKey(Blocoequivalencia, models.DO_NOTHING,
                primary_key=True)
    disciplinasequivalentes = models.ForeignKey(Disciplina, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'disciplinas_equivalentes'
        unique_together = (('bloco', 'disciplinasequivalentes'),)


class DisciplinasOriginais(models.Model):
    """Classe importada da tabela disciplinas_originais do banco de dados SCA"""

    bloco = models.ForeignKey(Blocoequivalencia, models.DO_NOTHING,
                primary_key=True)
    disciplinasoriginais = models.ForeignKey(Disciplina, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'disciplinas_originais'
        unique_together = (('bloco', 'disciplinasoriginais'),)


class Historicoescolar(models.Model):
    """Classe importada da tabela historicoescolar do banco de dados SCA"""

    id = models.BigAutoField(primary_key=True)
    versaocurso = models.ForeignKey('Versaocurso', models.DO_NOTHING,
                        db_column='versaoCurso_id', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historicoescolar'


class Itemhistoricoescolar(models.Model):
    """Classe importada da tabela itemhistoricoescolar do banco de dados SCA"""
    """TODO: Necessita dos campos mediaFinal e faltas não contemplados no esquema"""

    id = models.BigAutoField(primary_key=True)
    ano = models.IntegerField(blank=True, null=True)
    periodo = models.IntegerField(blank=True, null=True)
    situacao = models.IntegerField(blank=True, null=True)
    disciplina = models.ForeignKey(Disciplina, models.DO_NOTHING,
                                blank=True, null=True)
    historico_escolar = models.ForeignKey(Historicoescolar, models.DO_NOTHING,
                                blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'itemhistoricoescolar'


class Professor(models.Model):
    """Classe importada da tabela professor do banco de dados SCA"""
    """Retirados os campos desnecessários"""

    id = models.BigAutoField(primary_key=True)
    matricula = models.CharField(max_length=255, blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'professor'


class ProfessorDisciplina(models.Model):
    """Classe importada da tabela professor_disciplina do banco de dados SCA"""

    professor = models.ForeignKey(Professor, models.DO_NOTHING, primary_key=True)
    disciplina = models.ForeignKey(Disciplina, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'professor_disciplina'
        unique_together = (('professor', 'disciplina'),)


class Tabelaequivalencias(models.Model):
    """Classe importada da tabela tabelaequivalencias do banco de dados SCA"""

    id = models.BigAutoField(primary_key=True)
    versaocursocorrespondente = models.ForeignKey('Versaocurso',
            models.DO_NOTHING, db_column='versaoCursoCorrespondente_id',
            blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tabelaequivalencias'


class TabelaequivalenciasBlocoequivalencia(models.Model):
    """Classe importada da tabela tabelaequivalencias_blocoequivalencia do banco de dados SCA"""

    tabelaequivalencias = models.ForeignKey(Tabelaequivalencias,
                                models.DO_NOTHING, primary_key=True)
    blocosequivalencia = models.ForeignKey(Blocoequivalencia,
                                models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'tabelaequivalencias_blocoequivalencia'
        unique_together = (('tabelaequivalencias', 'blocosequivalencia'),)


class Turma(models.Model):
    """Classe importada da tabela turma do banco de dados SCA"""

    id = models.BigAutoField(primary_key=True)
    codigo = models.CharField(max_length=255, blank=True, null=True)
    ano = models.IntegerField(blank=True, null=True)
    periodo = models.IntegerField(blank=True, null=True)
    disciplina = models.ForeignKey(Disciplina, models.DO_NOTHING, blank=True,
                        null=True)
    professor = models.ForeignKey(Professor, models.DO_NOTHING, blank=True,
                        null=True)

    class Meta:
        managed = False
        db_table = 'turma'


class Versaocurso(models.Model):
    """Classe importada da tabela versaocurso do banco de dados SCA"""

    id = models.BigAutoField(primary_key=True)
    cargahorariaminoptativas = models.TextField(db_column='cargaHorariaMinOptativas',
                                    blank=True, null=True)
    numero = models.CharField(max_length=255, blank=True, null=True)
    qtdperiodominimo = models.IntegerField(db_column='qtdPeriodoMinimo',
                                    blank=True, null=True)
    situacao = models.IntegerField(blank=True, null=True)
    curso = models.ForeignKey(Curso, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'versaocurso'


class VersaocursoTabelaequivalencias(models.Model):
    """Classe importada da tabela versaocurso_tabelaequivalencias do banco de dados SCA"""

    versaocurso = models.ForeignKey(Versaocurso, models.DO_NOTHING,
                            primary_key=True)
    tabelasequivalencias = models.ForeignKey(Tabelaequivalencias,
                            models.DO_NOTHING,
                            db_column='tabelasEquivalencias_id', unique=True)

    class Meta:
        managed = False
        db_table = 'versaocurso_tabelaequivalencias'
        unique_together = (('versaocurso', 'tabelasequivalencias'),)
