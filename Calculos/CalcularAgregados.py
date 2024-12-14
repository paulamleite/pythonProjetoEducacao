from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import sessionmaker

from Calculos.CalcularAlunos import get_classificacao
from Entidades.CriarEntidades import (Base, Municipio, Escola, Turma, Prova, CalculoAgregado)
from Inputs.constantes import DB_PATH

engine = create_engine(DB_PATH, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def calcular_turma() -> None:
    """
    Agregado corresponde a turma, escola e município.
    O cálculo dos agregados é feito com base na rede, etapa e disciplina.
    A rede é um atributo da escola, a etapa é um atributo da turma e as disciplinas planejadas para cada etapa
    estão definidas no gabarito.
    Como a turma terá apenas uma rede e etapa, é preciso fazer loop apenas para disciplina.
    O cálculo da turma é o somatório dos alunos daquela turma em cada disciplina.
    """
    session = Session()
    lista_turmas = session.execute(select(Turma)
                                   .execution_options(stream_results=True)
                                   ).scalars().all()
    lista_provas = session.execute(select(Prova)
                                   .execution_options(stream_results=True)
                                   ).scalars().all()
    for turma in lista_turmas:
        qt_alunos_previstos = len(turma.lista_alunos_turma)
        for dc_disciplina in {prova_planejada.dc_disciplina
                              for prova_planejada in lista_provas
                              if prova_planejada.cd_aluno_inep in ((aluno.cd_aluno_inep
                                                                    for aluno in  turma.lista_alunos_turma))
                              }:
            qt_alunos_avaliados = 0
            qt_itens_apresentados = 0
            qt_itens_respondidos = None
            qt_acertos = None
            qt_media_itens_respondidos = None
            qt_media_acertos = None
            tx_media_acertos = None
            dc_classificacao = None
            for prova in (prova_planejada
                          for prova_planejada in lista_provas
                          if prova_planejada.dc_disciplina == dc_disciplina
                             and prova_planejada.cd_aluno_inep in ((aluno.cd_aluno_inep
                                                                    for aluno in turma.lista_alunos_turma))
                          ):
                qt_itens_apresentados += prova.qt_itens_apresentados
                if prova.qt_itens_respondidos:
                    qt_itens_respondidos = (int(0 if qt_itens_respondidos is None else qt_itens_respondidos)
                                            + prova.qt_itens_respondidos)
                    qt_acertos = int(0 if qt_acertos is None else qt_acertos) + prova.qt_acertos
                    qt_alunos_avaliados += 1
            tx_participacao = round(qt_alunos_avaliados / qt_alunos_previstos * 100, 2)
            qt_media_itens_apresentados = round(qt_itens_apresentados / qt_alunos_previstos, 0)
            if qt_alunos_avaliados:
                qt_media_itens_respondidos = round(qt_itens_respondidos / qt_alunos_avaliados, 0)
                qt_media_acertos = round(qt_acertos / qt_alunos_avaliados, 0)
                tx_media_acertos = round(qt_media_acertos / qt_media_itens_respondidos * 100, 2)
                dc_classificacao = get_classificacao(tx_media_acertos)
            calculo = CalculoAgregado(id_entidade_agregado=turma.id_turma
                                      , dc_tipo_entidade='Turma'
                                      , dc_rede_escola=turma.escola_turma.dc_rede_escola
                                      , dc_etapa_turma=turma.dc_etapa_turma
                                      , dc_disciplina=dc_disciplina
                                      , qt_alunos_previstos=qt_alunos_previstos
                                      , qt_alunos_avaliados=qt_alunos_avaliados
                                      , tx_participacao=tx_participacao
                                      , qt_itens_apresentados=qt_itens_apresentados
                                      , qt_itens_respondidos=qt_itens_respondidos
                                      , qt_acertos=qt_acertos
                                      , qt_media_itens_apresentados=qt_media_itens_apresentados
                                      , qt_media_itens_respondidos=qt_media_itens_respondidos
                                      , qt_media_acertos=qt_media_acertos
                                      , tx_media_acertos=tx_media_acertos
                                      , dc_classificacao=dc_classificacao
                                      )
            session.add(calculo)
    session.commit()
    session.close()

def calcular_escola() -> None:
    """
    O cálculo da escola é o somatório das turmas daquela escola em cada etapa e disciplina.
    """
    session = Session()
    lista_escolas = session.execute(select(Escola)
                                   .execution_options(stream_results=True)
                                   ).scalars().all()
    lista_calculo_turmas = session.execute(select(CalculoAgregado)
                                           .where(CalculoAgregado.dc_tipo_entidade=='Turma')
                                           .execution_options(stream_results=True)
                                           ).scalars().all()

    for escola in lista_escolas:
        for dc_etapa_turma, dc_disciplina in {(calculo.dc_etapa_turma, calculo.dc_disciplina)
                                              for calculo in lista_calculo_turmas
                                              if calculo.id_entidade_agregado in ((turma.id_turma
                                                                            for turma in escola.lista_turmas_escola))
                                              }:
            qt_alunos_previstos = 0
            qt_alunos_avaliados = 0
            qt_itens_apresentados = 0
            qt_itens_respondidos = None
            qt_acertos = None
            qt_media_itens_respondidos = None
            qt_media_acertos = None
            tx_media_acertos = None
            dc_classificacao = None
            for calculo_turma in (calculo
                                 for calculo in lista_calculo_turmas
                                 if calculo.dc_etapa_turma == dc_etapa_turma
                                    and calculo.dc_disciplina == dc_disciplina
                                    and calculo.id_entidade_agregado in ((turma.id_turma
                                                                          for turma in escola.lista_turmas_escola
                                                                          if turma.dc_etapa_turma == dc_etapa_turma))
                                 ):
                qt_alunos_previstos += calculo_turma.qt_alunos_previstos
                qt_alunos_avaliados += calculo_turma.qt_alunos_avaliados
                qt_itens_apresentados += calculo_turma.qt_itens_apresentados
                if calculo_turma.qt_itens_respondidos:
                    qt_itens_respondidos = (int(0 if qt_itens_respondidos is None else qt_itens_respondidos)
                                            + calculo_turma.qt_itens_respondidos)
                    qt_acertos = int(0 if qt_acertos is None else qt_acertos) + calculo_turma.qt_acertos
            tx_participacao = round(qt_alunos_avaliados / qt_alunos_previstos * 100, 2)
            qt_media_itens_apresentados = round(qt_itens_apresentados / qt_alunos_previstos, 0)
            if qt_alunos_avaliados:
                qt_media_itens_respondidos = round(qt_itens_respondidos / qt_alunos_avaliados, 0)
                qt_media_acertos = round(qt_acertos / qt_alunos_avaliados, 0)
                tx_media_acertos = round(qt_media_acertos / qt_media_itens_respondidos * 100, 2)
                dc_classificacao = get_classificacao(tx_media_acertos)
            calculo = CalculoAgregado(id_entidade_agregado=escola.cd_escola_inep
                                        , dc_tipo_entidade='Escola'
                                        , dc_rede_escola=escola.dc_rede_escola
                                        , dc_etapa_turma=dc_etapa_turma
                                        , dc_disciplina=dc_disciplina
                                        , qt_alunos_previstos=qt_alunos_previstos
                                        , qt_alunos_avaliados=qt_alunos_avaliados
                                        , tx_participacao=tx_participacao
                                        , qt_itens_apresentados=qt_itens_apresentados
                                        , qt_itens_respondidos=qt_itens_respondidos
                                        , qt_acertos=qt_acertos
                                        , qt_media_itens_apresentados=qt_media_itens_apresentados
                                        , qt_media_itens_respondidos=qt_media_itens_respondidos
                                        , qt_media_acertos=qt_media_acertos
                                        , tx_media_acertos=tx_media_acertos
                                        , dc_classificacao=dc_classificacao
                                        )
            session.add(calculo)
    session.commit()
    session.close()

def calcular_municipio() -> None:
    """
    O cálculo do município é o somatório das escolas daquele municipio em cada rede, etapa e disciplina.
    """
    session = Session()
    lista_municipios = session.execute(select(Municipio)
                                   .execution_options(stream_results=True)
                                   ).scalars().all()
    lista_calculo_escolas = session.execute(select(CalculoAgregado)
                                           .where(CalculoAgregado.dc_tipo_entidade=='Escola')
                                           .execution_options(stream_results=True)
                                           ).scalars().all()
    for municipio in lista_municipios:
        for dc_rede_escola, dc_etapa_turma, dc_disciplina in {(calculo.dc_rede_escola
                                                               , calculo.dc_etapa_turma
                                                               , calculo.dc_disciplina)
                                                              for calculo in lista_calculo_escolas
                                                              if calculo.id_entidade_agregado in ((escola.cd_escola_inep
                                                                    for escola in municipio.lista_escolas_municipio))
                                                              }:
            qt_alunos_previstos = 0
            qt_alunos_avaliados = 0
            tx_participacao = 0.0
            qt_itens_apresentados = 0
            qt_itens_respondidos = None
            qt_acertos = None
            qt_media_itens_apresentados = 0
            qt_media_itens_respondidos = None
            qt_media_acertos = None
            tx_media_acertos = None
            dc_classificacao = None
            for calculo_escola in (calculo
                                   for calculo in lista_calculo_escolas
                                   if calculo.dc_rede_escola == dc_rede_escola
                                      and calculo.dc_etapa_turma == dc_etapa_turma
                                      and calculo.dc_disciplina == dc_disciplina
                                      and calculo.id_entidade_agregado in ((escola.cd_escola_inep
                                                                        for escola in municipio.lista_escolas_municipio
                                                                            if escola.dc_rede_escola == dc_rede_escola))
                                   ):
                qt_alunos_previstos += calculo_escola.qt_alunos_previstos
                qt_alunos_avaliados += calculo_escola.qt_alunos_avaliados
                qt_itens_apresentados += calculo_escola.qt_itens_apresentados
                if calculo_escola.qt_itens_respondidos:
                    qt_itens_respondidos = (
                                int(0 if qt_itens_respondidos is None else qt_itens_respondidos)
                                + calculo_escola.qt_itens_respondidos)
                    qt_acertos = int(0 if qt_acertos is None else qt_acertos) + calculo_escola.qt_acertos
            tx_participacao = round(qt_alunos_avaliados / qt_alunos_previstos * 100, 2)
            qt_media_itens_apresentados = round(qt_itens_apresentados / qt_alunos_previstos, 0)
            if qt_alunos_avaliados:
                qt_media_itens_respondidos = round(qt_itens_respondidos / qt_alunos_avaliados, 0)
                qt_media_acertos = round(qt_acertos / qt_alunos_avaliados, 0)
                tx_media_acertos = round(qt_media_acertos / qt_media_itens_respondidos * 100, 2)
                dc_classificacao = get_classificacao(tx_media_acertos)
            calculo = CalculoAgregado(id_entidade_agregado=municipio.cd_municipio_ibge
                                      , dc_tipo_entidade='Municipio'
                                      , dc_rede_escola=dc_rede_escola
                                      , dc_etapa_turma=dc_etapa_turma
                                      , dc_disciplina=dc_disciplina
                                      , qt_alunos_previstos=qt_alunos_previstos
                                      , qt_alunos_avaliados=qt_alunos_avaliados
                                      , tx_participacao=tx_participacao
                                      , qt_itens_apresentados=qt_itens_apresentados
                                      , qt_itens_respondidos=qt_itens_respondidos
                                      , qt_acertos=qt_acertos
                                      , qt_media_itens_apresentados=qt_media_itens_apresentados
                                      , qt_media_itens_respondidos=qt_media_itens_respondidos
                                      , qt_media_acertos=qt_media_acertos
                                      , tx_media_acertos=tx_media_acertos
                                      , dc_classificacao=dc_classificacao
                                      )
            session.add(calculo)
    session.commit()
    session.close()

def excluir_calculo_agregados() -> None:
    session = Session()
    session.execute(delete(CalculoAgregado))
    session.commit()
    session.close()

def calcular_resultado_agregados() -> None:
    excluir_calculo_agregados()
    calcular_turma()
    print("Agregado TURMA calculado com sucesso!")
    calcular_escola()
    print("Agregado ESCOLA calculado com sucesso!")
    calcular_municipio()
    print("Agregado MUNICÍPIO calculado com sucesso!")

#Apenas para teste local porque deverá ser usado p main.py
if __name__ == '__main__':
    calcular_resultado_agregados()