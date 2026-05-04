import random
import pandas as pd
from itertools import combinations
import json

file_nome = r'C:\Users\Henrique\Desktop\labprogramacao tarefa 2\nome_utentes.txt'
file_apelido = r'C:\Users\Henrique\Desktop\labprogramacao tarefa 2\apelido_utentes.txt'
file_medicamentos = r'C:\Users\Henrique\Desktop\labprogramacao tarefa 2\medicamentos.txt'
file_excel_medicamentos = r'C:\Users\Henrique\Desktop\labprogramacao tarefa 2\matriz_medicamentos.xlsx'


NIVEIS_INTERACAO = {
    0: "Sem interação",
    1: "Interação mínima",
    2: "Interação moderada",
    3: "Interação significativa",
    4: "Interação grave",
    5: "Interação muito grave"
}

def read_file(filepath: str) -> list:
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

def read_excel(filepath: str) -> pd.DataFrame:
    df = pd.read_excel(filepath, index_col=0)
    return df

def criar_json(file_nome: str, file_apelido: str, file_medicamentos: str, file_excel_medicamentos: str) -> None:
    resultados = calcular_interacao_medicamentos(file_nome, file_apelido, file_medicamentos, file_excel_medicamentos)
    resultados_serializaveis = []
    for r in resultados:
        interacoes_formatadas = [
            {
                'par': f"{i['par'][0]} + {i['par'][1]}",
                'valor': i['valor'],
                'descricao': i['descricao']
            }
            for i in r['interacoes']
        ]
        resultados_serializaveis.append({
            'utente': r['utente'],
            'medicamentos': r['medicamentos'],
            'interacoes': interacoes_formatadas
        })

    with open('data.json', 'w', encoding='utf-8') as outfile:
        json.dump(resultados_serializaveis, outfile, ensure_ascii=False, indent=4)

    return None


def criar_utente(numero_utente: int, file_nome: str, file_apelido: str) -> str:
    nome = random.choice(read_file(file_nome))
    apelido = random.choice(read_file(file_apelido))
    return f'{numero_utente} - {nome} {apelido}'

def criar_utentes(file_nome: str, file_apelido: str) -> list:
    utentes = []
    numero_utente_lista = []
    for i in range(random.randint(5, 30)):
        numero_utente = random.randint(1000, 10000)
        if numero_utente in numero_utente_lista:
            numero_utente += 1
        else:
            numero_utente_lista.append(numero_utente)
        utente = criar_utente(numero_utente, file_nome, file_apelido)
        utentes.append(utente)
    return utentes

def criar_receita_medica(file_nome: str, file_apelido: str, file_medicamentos: str) -> list:
    utentes = criar_utentes(file_nome, file_apelido)
    medicamentos = read_file(file_medicamentos)
    receitas = []
    for utente in utentes:
        medicamento = [random.choice(medicamentos) for i in range(random.randint(2, 4))]
        receita = {'utente': utente, 'medicamentos': medicamento}
        receitas.append(receita)
    return receitas

def verificar_interacao(med1: str, med2: str, tabela: pd.DataFrame) -> dict:
    """Check interaction between two medications in the matrix."""
    try:
        valor = tabela.loc[med1, med2]
        if pd.isna(valor):
            valor = tabela.loc[med2, med1]
        if pd.isna(valor):
            return {'par': (med1, med2), 'valor': None, 'descricao': 'Sem dados'}

        try:
            valor = int(float(valor))
        except (ValueError, TypeError):
            return {'par': (med1, med2), 'valor': None, 'descricao': 'Valor inválido na tabela'}

        return {
            'par': (med1, med2),
            'valor': valor,
            'descricao': NIVEIS_INTERACAO.get(valor, 'Desconhecido')  
        }
    except KeyError:
        return {'par': (med1, med2), 'valor': None, 'descricao': 'Medicamento não encontrado na tabela'}

def calcular_interacao_medicamentos(file_nome: str, file_apelido: str, file_medicamentos: str, file_excel_medicamentos: str) -> list:
    receitas = criar_receita_medica(file_nome, file_apelido, file_medicamentos)
    tabela_medicamentos = read_excel(file_excel_medicamentos)

    resultados = []

    for receita in receitas:
        utente = receita['utente']
        medicamentos = receita['medicamentos']
        lista_interacoes = []  
        for med1, med2 in combinations(medicamentos, 2):
            interacao = verificar_interacao(med1, med2, tabela_medicamentos)
            lista_interacoes.append(interacao)

        resultado = {
            'utente': utente,
            'medicamentos': medicamentos,
            'interacoes': lista_interacoes,
        }
        resultados.append(resultado)

    return resultados

def imprimir_resultados(resultados: list):
    for r in resultados:
        print(f"\n")
        print(f"Utente: {r['utente']}")
        print(f"Medicamentos: {', '.join(r['medicamentos'])}")
        print(f"Interações encontradas:")
        for interacao in r['interacoes']:
            med1, med2 = interacao['par']
            valor = interacao['valor'] if interacao['valor'] is not None else '?'
            print(f"  {med1} + {med2}: [{valor}] {interacao['descricao']}")


criar_json(file_nome, file_apelido, file_medicamentos, file_excel_medicamentos)