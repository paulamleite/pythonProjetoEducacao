from Inputs.constantes import (CSV_MICRODADOS, CSV_AGREGADOS)
from Inputs.ImportarDados import importar_dados_csv
from Calculos.CalcularAlunos import calcular_provas_alunos
from Calculos.CalcularAgregados import calcular_resultado_agregados
from Outputs.GerarMicrodados import gerar_planilha_microdados
from Outputs.GerarAgregados import gerar_planilha_agregado

if __name__ == '__main__':
    importar_dados_csv()
    calcular_provas_alunos()
    calcular_resultado_agregados()
    gerar_planilha_microdados(CSV_MICRODADOS)
    gerar_planilha_agregado(CSV_AGREGADOS)
