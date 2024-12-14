from csv import DictReader

from sqlalchemy import create_engine, select, and_, delete
from sqlalchemy.orm import sessionmaker

from Inputs.constantes import (DB_PATH, CSV_ENTIDADE, CSV_PROVA_FEITA, CSV_GABARITO)
from Entidades.CriarEntidades import (Base, Municipio, Escola, Turma, Aluno, ProvaFeita, Gabarito)

engine = create_engine(DB_PATH, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def importar_entidades_csv(csv_nome: str) -> None:
    session = Session()
    with open(csv_nome, mode="r", newline='', encoding="UTF-8") as arq:
        csv = DictReader(arq, delimiter=";")
        for linha in csv:
            municipio = session.execute(select(Municipio)
                                        .where(Municipio.cd_municipio_ibge == linha["cd_municipio_ibge"])
                                        .execution_options(stream_results=True)
                                        ).scalars().first()
            if not municipio:
                municipio = Municipio(cd_municipio_ibge=linha["cd_municipio_ibge"]
                                      , nm_municipio=linha["nm_municipio"])
            escola = session.execute(select(Escola)
                                     .where(Escola.cd_escola_inep == linha["cd_escola_inep"])
                                     .execution_options(stream_results=True)
                                     ).scalars().first()
            if not escola:
                escola = Escola(cd_escola_inep=linha["cd_escola_inep"]
                                , nm_escola=linha["nm_escola"]
                                , dc_rede_escola=linha["dc_rede_escola"]
                                , municipio_escola=municipio)
            turma = session.execute(select(Turma)
                                    .where(and_(Turma.nm_turma == linha["nm_turma"]
                                                , Turma.dc_etapa_turma == linha["dc_etapa_turma"]
                                                , Turma.cd_escola_inep == linha["cd_escola_inep"]))
                                    .execution_options(stream_results=True)
                                    ).scalars().first()
            if not turma:
                turma = Turma(nm_turma=linha["nm_turma"]
                              , dc_etapa_turma=linha["dc_etapa_turma"]
                              , escola_turma=escola)
            aluno = session.execute(select(Aluno)
                                    .where(Aluno.cd_aluno_inep == linha["cd_aluno_inep"])
                                    .execution_options(stream_results=True)
                                    ).scalars().first()
            if not aluno:
                aluno = Aluno(cd_aluno_inep=linha["cd_aluno_inep"]
                              , nm_aluno=linha["nm_aluno"]
                              , turma_aluno=turma)
            session.add(aluno)
            session.commit()
    session.close()

def excluir_provas_feitas() -> None:
    session = Session()
    session.execute(delete(ProvaFeita))
    session.commit()
    session.close()

def importar_provas_feitas_csv(csv_nome: str) -> None:
    excluir_provas_feitas()
    session = Session()
    with open(csv_nome, mode="r", newline='', encoding="UTF-8") as arq:
        csv = DictReader(arq, delimiter=";")
        provas_feitas = [
            ProvaFeita(cd_aluno_inep=linha["cd_aluno_inep"]
                     , dc_disciplina=linha["dc_disciplina"]
                     , vl_campo_001=linha["vl_campo_001"]
                     , vl_campo_002=linha["vl_campo_002"]
                     , vl_campo_003=linha["vl_campo_003"]
                     , vl_campo_004=linha["vl_campo_004"]
                     , vl_campo_005=linha["vl_campo_005"]
                     , vl_campo_006=linha["vl_campo_006"]
                     , vl_campo_007=linha["vl_campo_007"]
                     , vl_campo_008=linha["vl_campo_008"]
                     , vl_campo_009=linha["vl_campo_009"]
                     , vl_campo_010=linha["vl_campo_010"]
                     , vl_campo_011=linha["vl_campo_011"]
                     , vl_campo_012=linha["vl_campo_012"]
                     , vl_campo_013=linha["vl_campo_013"]
                     , vl_campo_014=linha["vl_campo_014"]
                     , vl_campo_015=linha["vl_campo_015"]
                     , vl_campo_016=linha["vl_campo_016"]
                     , vl_campo_017=linha["vl_campo_017"]
                     , vl_campo_018=linha["vl_campo_018"]
                     , vl_campo_019=linha["vl_campo_019"]
                     , vl_campo_020=linha["vl_campo_020"]
                     )
            for linha in csv
        ]
    session.bulk_save_objects(provas_feitas)
    session.commit()
    session.close()

def excluir_gabaritos() -> None:
    session = Session()
    session.execute(delete(Gabarito))
    session.commit()
    session.close()

def importar_gabarito_csv(csv_nome: str) -> None:
    excluir_gabaritos()
    session = Session()
    with open(csv_nome, mode="r", newline='', encoding="UTF-8") as arq:
        csv = DictReader(arq, delimiter=";")
        gabaritos = [
            Gabarito(dc_etapa_turma=linha["dc_etapa_turma"]
                     , dc_disciplina=linha["dc_disciplina"]
                     , cd_posicao_item=linha["cd_posicao_item"]
                     , vl_gabarito=linha["vl_gabarito"]
                     )
            for linha in csv
        ]
    session.bulk_save_objects(gabaritos)
    session.commit()
    session.close()

def importar_dados_csv() -> None:
    importar_entidades_csv(CSV_ENTIDADE)
    print("Entidades importadas com sucesso!")
    importar_provas_feitas_csv(CSV_PROVA_FEITA)
    print("Provas feitas importadas com sucesso!")
    importar_gabarito_csv(CSV_GABARITO)
    print("Gabarito importado com sucesso!")

#Apenas para teste local porque deverá ser usado p main.py
if __name__ == '__main__':
    importar_dados_csv()
