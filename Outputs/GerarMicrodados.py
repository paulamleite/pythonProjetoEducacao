from _csv import writer

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from Entidades.CriarEntidades import (Base, Prova)
from Inputs.constantes import (DB_PATH, CSV_MICRODADOS)

engine = create_engine(DB_PATH, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def gerar_planilha_microdados(csv_nome: str) -> None:
    session = Session()
    lista_provas = session.execute(select(Prova)
                                   .execution_options(stream_results=True)
                                   ).scalars().all()
    with open(csv_nome, mode='a', newline='', encoding='UTF-8') as arq:
        csv = writer(arq, delimiter=';')
        csv.writerow(['cd_municipio_ibge'
                         ,'nm_municipio'
                         ,'dc_rede_escola'
                         ,'cd_escola_inep'
                         ,'nm_escola'
                         ,'dc_etapa_turma'
                         , 'nm_turma'
                         , 'cd_aluno_inep'
                         , 'nm_aluno'
                         , 'dc_disciplina'
                         , 'qt_itens_apresentados'
                         , 'qt_itens_respondidos'
                         , 'qt_acertos'
                         , 'tx_acertos'
                         , 'dc_classificacao'])
        [csv.writerow([
            prova.prova_aluno.turma_aluno.escola_turma.municipio_escola.cd_municipio_ibge
                , prova.prova_aluno.turma_aluno.escola_turma.municipio_escola.nm_municipio
                , prova.prova_aluno.turma_aluno.escola_turma.dc_rede_escola
                , prova.prova_aluno.turma_aluno.escola_turma.cd_escola_inep
                , prova.prova_aluno.turma_aluno.escola_turma.nm_escola
                , prova.prova_aluno.turma_aluno.dc_etapa_turma
                , prova.prova_aluno.turma_aluno.nm_turma
                , prova.prova_aluno.cd_aluno_inep
                , prova.prova_aluno.nm_aluno
                , prova.dc_disciplina
                , prova.qt_itens_apresentados
                , prova.qt_itens_respondidos
                , prova.qt_acertos
                , prova.tx_acertos
                , prova.dc_classificacao
                ])
            for prova in lista_provas
         ]
    print("Planilha de microdados gerada com sucesso!")
    session.close()

#Apenas para teste local porque deverá ser usado p main.py
if __name__ == '__main__':
    gerar_planilha_microdados(CSV_MICRODADOS)