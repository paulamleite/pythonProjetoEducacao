from _csv import writer

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from Entidades.CriarEntidades import (Base, Municipio, Escola, Turma, CalculoAgregado)
from Inputs.constantes import (DB_PATH, CSV_AGREGADOS)

engine = create_engine(DB_PATH, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def gerar_planilha_agregado(csv_nome: str) -> None:
    session = Session()
    lista_calculo_agregados = session.execute(select(CalculoAgregado)
                                              .execution_options(stream_results=True)
                                              ).scalars().all()
    lista_turmas = session.execute(select(Turma)
                                   .execution_options(stream_results=True)
                                   ).scalars().all()
    lista_escolas = session.execute(select(Escola)
                                    .execution_options(stream_results=True)
                                    ).scalars().all()
    lista_municipios = session.execute(select(Municipio)
                                       .execution_options(stream_results=True)
                                       ).scalars().all()
    with open(csv_nome, mode='a', newline='', encoding='UTF-8') as arq:
        csv = writer(arq, delimiter=';')
        csv.writerow(['dc_tipo'
                         ,'cd_municipio_ibge'
                         ,'nm_municipio'
                         ,'dc_rede_escola'
                         ,'cd_escola_inep'
                         ,'nm_escola'
                         ,'dc_etapa_turma'
                         ,'nm_turma'
                         ,'dc_disciplina'
                         ,'qt_alunos_previstos'
                         ,'qt_alunos_avaliados'
                         ,'tx_participacao'
                         ,'qt_media_itens_apresentados'
                         ,'qt_media_itens_respondidos'
                         ,'qt_media_acertos'
                         ,'tx_media_acertos'
                         ,'dc_classificacao']
        )
        for agregado in lista_calculo_agregados:
            nm_turma = None
            cd_escola_inep = None
            nm_escola = None
            if agregado.dc_tipo_entidade == 'Turma':
                turma = list(filter(lambda turma: turma.id_turma == agregado.id_entidade_agregado, lista_turmas)
                             ).pop()
                nm_turma = turma.nm_turma
                cd_escola_inep = turma.cd_escola_inep
            if agregado.dc_tipo_entidade == 'Escola' or cd_escola_inep:
                escola = list(filter(lambda escola: escola.cd_escola_inep == int(agregado.id_entidade_agregado
                                                                                 if cd_escola_inep is None
                                                                                 else cd_escola_inep)
                                     , lista_escolas)
                              ).pop()
                cd_escola_inep = escola.cd_escola_inep
                nm_escola = escola.nm_escola
                cd_municipio_ibge = escola.cd_municipio_ibge
            municipio = list(filter(lambda municipio: municipio.cd_municipio_ibge == cd_municipio_ibge
                                    , lista_municipios)
                             ).pop()
            cd_municipio_ibge = municipio.cd_municipio_ibge
            nm_municipio = municipio.nm_municipio
            csv.writerow([agregado.dc_tipo_entidade
                                 , cd_municipio_ibge
                                 , nm_municipio
                                 , agregado.dc_rede_escola
                                 , cd_escola_inep
                                 , nm_escola
                                 , agregado.dc_etapa_turma
                                 , nm_turma
                                 , agregado.dc_disciplina
                                 , agregado.qt_alunos_previstos
                                 , agregado.qt_alunos_avaliados
                                 , agregado.tx_participacao
                                 , agregado.qt_media_itens_apresentados
                                 , agregado.qt_media_itens_respondidos
                                 , agregado.qt_media_acertos
                                 , agregado.tx_media_acertos
                                 , agregado.dc_classificacao]
            )
    print("Planilha de resultados agregados gerada com sucesso!")
    session.close()

#Apenas para teste local porque deverá ser usado p main.py
if __name__ == '__main__':
    gerar_planilha_agregado(CSV_AGREGADOS)