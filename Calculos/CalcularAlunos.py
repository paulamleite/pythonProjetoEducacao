from sqlalchemy import create_engine, select, func, delete
from sqlalchemy.orm import sessionmaker

from Entidades.CriarEntidades import (Base, Aluno, ProvaFeita, Gabarito, Prova)
from Inputs.constantes import DB_PATH

engine = create_engine(DB_PATH, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def excluir_Prova() -> None:
    session = Session()
    session.execute(delete(Prova))
    session.commit()
    session.close()

def criar_provas() -> None:
    """
    Cria as provas planejadas para o aluno.
    O programa recebe a lista de provas feitas pelo aluno e salva no objeto da classe ProvaFeita.
    Mas o aluno pode não ter feito todas as provas planejadas para ele.
    Então, teremos o objeto da classe ProvaFeita e o objeto da classe Prova que corresponde a todas as provas planejadas.
    A definição de quais provas são planejadas depende da etapa e da disciplina.
    A classe Gabarito tem a informação de etapa e disciplina.
    Então, é preciso ver a turma do aluno para saber a etapa.
    Depois, é preciso ver no Gabarito quais são as disciplinas para aquela etapa.
    """
    excluir_Prova()
    session = Session()
    lista_etapa_disciplina_qtItens = session.execute(select(Gabarito.dc_etapa_turma
                                                            , Gabarito.dc_disciplina
                                                            , func.max(Gabarito.cd_posicao_item).label("qt_itens"))
                                                     .group_by(Gabarito.dc_etapa_turma, Gabarito.dc_disciplina)
                                                     ).all()
    lista_alunos = session.execute(select(Aluno)
                                   .execution_options(stream_results=True)
                                   ).scalars().all()
    for aluno in lista_alunos:
        for cd_disciplina, qt_itens in ((etapa_disciplina_qtItens[1], etapa_disciplina_qtItens[2])
                                        for etapa_disciplina_qtItens in lista_etapa_disciplina_qtItens
                                        if etapa_disciplina_qtItens[0] == aluno.turma_aluno.dc_etapa_turma):
            prova = Prova(cd_aluno_inep=aluno.cd_aluno_inep
                          , dc_disciplina=cd_disciplina
                          , qt_itens_apresentados=qt_itens)
            aluno.lista_provas_aluno.append(prova)
    session.commit()
    session.close()

def get_classificacao(tx_acertos: float) -> str:
    dc_classificacao = "Muito baixo"
    if tx_acertos >= 25 and tx_acertos < 50:
        dc_classificacao = "Baixo"
    elif tx_acertos >= 50 and tx_acertos < 75:
        dc_classificacao = "Médio"
    elif tx_acertos >= 75:
        dc_classificacao = "Alto"
    return dc_classificacao

def corrigir_provas() -> None:
    """
    Será feita a correção para todas as provas planejadas para o aluno.
    Caso não exista ProvaFeita para um aluno em determinada disciplina, ainda assim teremos a prova planejada,
    mas sem valores para nota e classificação do desempenho.
    """
    session = Session()
    lista_provas_feitas = session.execute(select(ProvaFeita)
                                          .execution_options(stream_results=True)
                                          ).scalars().all()
    lista_gabarito_itens = session.execute(select(Gabarito)
                                           .execution_options(stream_results=True)
                                           ).scalars().all()
    for prova_feita in lista_provas_feitas:
        #Usei filter e pop para pegar o objeto prova em vez de pegar uma lista [] ou iterator ()
        prova_planejada = list(filter(lambda prova: prova.dc_disciplina==prova_feita.dc_disciplina
                                      , prova_feita.prova_feita_aluno.lista_provas_aluno)).pop()
        qt_itens_respondidos = None
        qt_acertos = None
        tx_acertos = None
        dc_classificacao = None
        # Vou transformar o objeto prova_feita em um tipo dicionário para que eu possa manipular mais facilmente
        # os campos vl_campo_001, vl_campo_002, ...
        prova_feita_dict = dict(prova_feita.__dict__.items())
        for indice in range(1, prova_planejada.qt_itens_apresentados + 1):
            # vou montas os campos vl_campo_001, vl_campo_002, ... e quantos forem precisos de acordo com a etapa e disciplina
            variavel = "vl_campo_" + str(indice).rjust(3, '0')
            if prova_feita_dict[variavel]:
                qt_itens_respondidos = int(0 if qt_itens_respondidos is None else qt_itens_respondidos)+1
                gabarito_item = list(filter(lambda gabarito:
                                    gabarito.dc_etapa_turma==prova_feita.prova_feita_aluno.turma_aluno.dc_etapa_turma
                                    and gabarito.dc_disciplina==prova_feita.dc_disciplina
                                    and gabarito.cd_posicao_item==indice
                                            , lista_gabarito_itens)
                                     ).pop()
                if prova_feita_dict[variavel] == gabarito_item.vl_gabarito:
                    qt_acertos = int(0 if qt_acertos is None else qt_acertos)+1
        if qt_itens_respondidos:
            tx_acertos = round(qt_acertos / qt_itens_respondidos * 100, 2)
            dc_classificacao = get_classificacao(tx_acertos)
        prova_planejada.qt_itens_respondidos = qt_itens_respondidos
        prova_planejada.qt_acertos = qt_acertos
        prova_planejada.tx_acertos = tx_acertos
        prova_planejada.dc_classificacao = dc_classificacao
        session.commit()
    session.close()

def calcular_provas_alunos() -> None:
    criar_provas()
    print("Provas planejadas criadas com sucesso!")
    corrigir_provas()
    print("Provas corrigidas com sucesso!")

#Apenas para teste local porque deverá ser usado p main.py
if __name__ == '__main__':
    calcular_provas_alunos()
