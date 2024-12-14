from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()

class Municipio(Base):
    __tablename__ = "tb_municipios"

    cd_municipio_ibge: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    nm_municipio: Mapped[str] = mapped_column(String(100), nullable=False)
    lista_escolas_municipio: Mapped[List["Escola"]] = relationship(back_populates="municipio_escola")

    def __repr__(self):
        return (f'cd_municipio_ibge={self.cd_municipio_ibge}'
                f', nm_municipio={self.nm_municipio}')


class Escola(Base):
    __tablename__ = "tb_escolas"

    cd_escola_inep: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    nm_escola: Mapped[str] = mapped_column(String(100), nullable=False)
    dc_rede_escola: Mapped[str] = mapped_column(String(9), nullable=False)
    cd_municipio_ibge = mapped_column(ForeignKey("tb_municipios.cd_municipio_ibge"))
    municipio_escola: Mapped[Municipio] = relationship(back_populates="lista_escolas_municipio")
    lista_turmas_escola: Mapped[List["Turma"]] = relationship(back_populates="escola_turma")

    def __repr__(self):
        return (f'cd_escola_inep={self.cd_escola_inep}'
                f', nm_escola={self.nm_escola}'
                f', dc_rede_escola={self.dc_rede_escola}'
                f', cd_municipio_ibge={self.cd_municipio_ibge}'
                )


class Turma(Base):
    __tablename__ = "tb_turmas"

    id_turma: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nm_turma: Mapped[str] = mapped_column(String(50), nullable=False)
    dc_etapa_turma: Mapped[str] = mapped_column(String(3), nullable=False)
    cd_escola_inep = mapped_column(ForeignKey("tb_escolas.cd_escola_inep"))
    escola_turma: Mapped[Escola] = relationship(back_populates="lista_turmas_escola")
    lista_alunos_turma: Mapped[List["Aluno"]] = relationship(back_populates="turma_aluno")

    def __repr__(self):
        return (f'id_turma={self.id_turma}'
                f', nm_turma={self.nm_turma}'
                f', dc_etapa_turma={self.dc_etapa_turma}'
                f', cd_escola_inep={self.cd_escola_inep}'
                )


class Aluno(Base):
    __tablename__ = "tb_alunos"

    cd_aluno_inep: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    nm_aluno: Mapped[str] = mapped_column(String(100), nullable=False)
    id_turma = mapped_column(ForeignKey("tb_turmas.id_turma"))
    turma_aluno: Mapped[Turma] = relationship(back_populates="lista_alunos_turma")
    lista_provas_feitas_aluno: Mapped[List["ProvaFeita"]] = relationship(back_populates="prova_feita_aluno")
    lista_provas_aluno: Mapped[List["Prova"]] = relationship(back_populates="prova_aluno")

    def __repr__(self):
        return (f'cd_aluno_inep={self.cd_aluno_inep}'
                f', nm_aluno={self.nm_aluno}'
                f', dc_etapa_turma={self.turma_aluno.dc_etapa_turma}'
                f', id_turma={self.turma_aluno.id_turma}'
                )


class ProvaFeita(Base):
    __tablename__ = "tb_provas_feitas"

    id_prova_feita: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cd_aluno_inep = mapped_column(ForeignKey("tb_alunos.cd_aluno_inep"))
    dc_disciplina: Mapped[str] = mapped_column(String(2), nullable=False)
    vl_campo_001: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_002: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_003: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_004: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_005: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_006: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_007: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_008: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_009: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_010: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_011: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_012: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_013: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_014: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_015: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_016: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_017: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_018: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_019: Mapped[str] = mapped_column(String(1), nullable=True)
    vl_campo_020: Mapped[str] = mapped_column(String(1), nullable=True)
    prova_feita_aluno: Mapped[Aluno] = relationship(back_populates="lista_provas_feitas_aluno")

    def __repr__(self):
        return (f'id_prova_feita={self.id_prova_feita}'
                f', cd_aluno_inep={self.cd_aluno_inep}'
                f', dc_disciplina={self.dc_disciplina}')


class Gabarito(Base):
    __tablename__ = "tb_gabaritos"

    dc_etapa_turma: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    dc_disciplina: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    cd_posicao_item: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    vl_gabarito: Mapped[str] = mapped_column(String(1), nullable=False)

    def __repr__(self):
        return (f'{self.dc_etapa_turma}'
                f', {self.dc_disciplina}'
                f', {self.cd_posicao_item}'
                f', {self.vl_gabarito}')


class Prova(Base):
    __tablename__ = "tb_provas"

    id_prova: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cd_aluno_inep = mapped_column(ForeignKey("tb_alunos.cd_aluno_inep"))
    dc_disciplina: Mapped[str] = mapped_column(String(2), nullable=False)
    qt_itens_apresentados: Mapped[int] = mapped_column(nullable=False)
    qt_itens_respondidos: Mapped[int] = mapped_column(nullable=True)
    qt_acertos: Mapped[int] = mapped_column(nullable=True)
    tx_acertos: Mapped[float] = mapped_column(nullable=True)
    dc_classificacao: Mapped[str] = mapped_column(String(11), nullable=True)
    prova_aluno: Mapped[Aluno] = relationship(back_populates="lista_provas_aluno")

    def __repr__(self):
        return (f'id_prova={self.id_prova}'
                f', cd_aluno_inep={self.cd_aluno_inep}'
                f', dc_disciplina={self.dc_disciplina}'
                f', qt_itens_apresentados={self.qt_itens_apresentados}'
                f', qt_itens_respondidos={self.qt_itens_respondidos}'
                f', qt_acertos={self.qt_acertos}'
                f', tx_acertos={self.tx_acertos}'
                f', dc_classificacao={self.dc_classificacao}')


class CalculoAgregado(Base):
    __tablename__ = "tb_calculo_agregados"

    id_entidade_agregado: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    dc_tipo_entidade: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    dc_rede_escola: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    dc_etapa_turma: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    dc_disciplina: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    qt_alunos_previstos: Mapped[int] = mapped_column(nullable=False)
    qt_alunos_avaliados: Mapped[int] = mapped_column(nullable=True)
    tx_participacao: Mapped[float] = mapped_column(nullable=True)
    qt_itens_apresentados: Mapped[int] = mapped_column(nullable=False)
    qt_itens_respondidos: Mapped[int] = mapped_column(nullable=True)
    qt_acertos: Mapped[int] = mapped_column(nullable=True)
    qt_media_itens_apresentados: Mapped[int] = mapped_column(nullable=False)
    qt_media_itens_respondidos: Mapped[int] = mapped_column(nullable=True)
    qt_media_acertos: Mapped[int] = mapped_column(nullable=True)
    tx_media_acertos: Mapped[float] = mapped_column(nullable=True)
    dc_classificacao: Mapped[str] = mapped_column(String(11), nullable=True)

    def __repr__(self):
        return (f'id_entidade_agregado={self.id_entidade_agregado}'
                f', dc_tipo_entidade={self.dc_tipo_entidade}'
                f', dc_rede_escola={self.dc_rede_escola}'
                f', dc_etapa_turma={self.dc_etapa_turma}'
                f', dc_disciplina={self.dc_disciplina}'
                f', qt_media_itens_apresentados={self.qt_media_itens_apresentados}'
                f', qt_media_itens_respondidos={self.qt_media_itens_respondidos}'
                f', qt_media_acertos={self.qt_media_acertos}'
                f', tx_media_acertos={self.tx_media_acertos}'
                f', dc_classificacao={self.dc_classificacao}')
