from datetime import datetime
from pathlib import Path

current_path = Path(__file__).resolve()
project_root = current_path.parent.parent
inputs_path = current_path.parent
ouputs_path = f"{project_root}\\Outputs"

DB_PATH = f"sqlite:///{project_root}\\BD\\bd_Hogwarts.db"

CSV_ENTIDADE = f"{inputs_path}\\lista_alunos.csv"
CSV_PROVA_FEITA = f"{inputs_path}\\lista_provas_feitas.csv"
CSV_GABARITO = f"{inputs_path}\\lista_gabaritos.csv"
CSV_MICRODADOS = f"{ouputs_path}\\microdados.csv"
nome_arquivo_microdados = "microdados_"+datetime.now().strftime('%y%m%d%H%M')+".csv"
CSV_MICRODADOS = f"{ouputs_path}\\{nome_arquivo_microdados}"
nome_arquivo_agregados = "agregados_"+datetime.now().strftime('%y%m%d%H%M')+".csv"
CSV_AGREGADOS = f"{ouputs_path}\\{nome_arquivo_agregados}"