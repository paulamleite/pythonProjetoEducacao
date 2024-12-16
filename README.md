# pythonProjetoEducacao

Objetivo: Calcular as notas dos alunos da rede municipal e classificá-los em desempenho muito baixo, baixo, médio e alto. A partir dos microdados (cálculo dos alunos), fazer o cálculo dos agregados de turma, escola e município.

Descrição: Haverá arquivos csv na pasta inputs para carga das entidades (alunos, turmas, escolas e município), das provas feitas e dos gabaritos de cada etapa e disicplina. Será feito o cálculo a nível do aluno e de cada agregado e serão gerados arquivos csv na pasta outputs com o resultado dos cálculos de microdados e de agregados.

Ferramentas: Foi utilizada a linguagem Python com banco de dados relacional SQLite3 e SQLAlchemy para a camada ORM.

Execução do programa: É necessário instalar o SQLAlchemy (pip install sqlalchemy) e executar o main.py da pasta raiz.