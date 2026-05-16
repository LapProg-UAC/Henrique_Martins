import random
import pandas as pd
from itertools import combinations
import json
from constantes import FILES, NIVEIS_INTERACAO
from encriptacao import encriptar

def read_text_file(filepath: str) -> list:
    """
    Lê o conteúdo de um ficheiro de texto

    Args:
        filepath (str): O caminho para o ficheiro de texto

    Returns:
        list: Uma lista de strings com as linhas do ficheiro. Devolve uma lista vazia se o ficheiro não existir.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print("Arquivo não encontrado")
        return []

def carregar_dados() -> tuple:
    """
    Carrega todos os ficheiros de suporte necessários

    Returns:
        tuple: Um tuplo contendo três listas e um DataFrame .
    """
    nomes = read_text_file(FILES['nomes'])
    apelidos = read_text_file(FILES['apelidos'])
    medicamentos = read_text_file(FILES['medicamentos'])
    tabela = pd.read_excel(FILES['matriz'], index_col=0)
    return nomes, apelidos, medicamentos, tabela

def criar_utentes(nomes: list, apelidos: list) -> list:
    """
    Gera uma lista aleatória de utentes com IDs únicos e encriptados.

    Args:
        nomes (list): Lista de nomes próprios
        apelidos (list): Lista de apelidos 
    Returns:
        list: Uma lista de strings, cada uma representando um utente 
    """
    qtd_utentes = random.randint(5, 30)
    ids_unicos = random.sample(range(1000, 10000), qtd_utentes)
    utentes = []
    for num in ids_unicos:
        nome = random.choice(nomes)
        apelido = random.choice(apelidos)
        id_encriptado = encriptar(str(num))
        utentes.append(f"{id_encriptado} - {nome} {apelido}")
    return utentes

def criar_receitas_medicas(utentes: list, medicamentos: list) -> list:
    """
    Atribui prescrições aleatórias de medicamentos a cada utente.

    Args:
        utentes (list): Lista de utentes 
        medicamentos (list): Lista de medicamentos 

    Returns:
        list: Lista de dicionários, associando cada utente à sua lista de medicamentos
    """
    receitas = []
    for utente in utentes:
        qtd_medicamentos = random.randint(2, 4)
        meds_prescritos = random.sample(medicamentos, qtd_medicamentos)
        receitas.append({'utente': utente, 'medicamentos': meds_prescritos})
    return receitas

def verificar_interacao(med1: str, med2: str, tabela: pd.DataFrame) -> dict:
    """
    Consulta da matriz para determinar o nível de interação entre dois medicamentos

    Args:
        med1 (str): O nome do primeiro medicamento
        med2 (str): O nome do segundo medicamento
        tabela (pd.DataFrame): A matriz do Excel 

    Returns:
        dict: Dados da interação contendo o par de medicamentos, o valor numérico e a descrição 
    """
    try:
        valor = tabela.loc[med1, med2]
        if pd.isna(valor):
            valor = tabela.loc[med2, med1]
        if pd.isna(valor):
            return {'par': (med1, med2), 'valor': None, 'descricao': 'Sem dados'}
        else:
            return {
                'par': (med1, med2),
                'valor': valor,
                'descricao': NIVEIS_INTERACAO.get(valor, 'Desconhecido')
            }
    except KeyError:
        return {'par': (med1, med2), 'valor': None, 'descricao': 'Medicamento não encontrado na tabela'}
    
def calcular_todas_interacoes(receitas: list, tabela: pd.DataFrame) -> list:
    """
    Calcula as interações de todos os pares possíveis de medicamentos em cada receita

    Args:
        receitas (list): Lista das receitas agrupadas por utente.
        tabela (pd.DataFrame): A matriz de interações.

    Returns:
        list: Lista final de resultados contendo o utente, medicamentos e todas as suas interações 
    """
    resultados = []
    for receita in receitas:
        lista_interacoes = []
        for med1, med2 in combinations(receita['medicamentos'], 2):
            interacao = verificar_interacao(med1, med2, tabela)
            lista_interacoes.append(interacao)
        resultados.append({
            'utente': receita['utente'],
            'medicamentos': receita['medicamentos'],
            'interacoes': lista_interacoes,
        })
    return resultados

def exportar_para_json(resultados: list, output_filename: str = 'data.json') -> None:
    """

    Args:
        resultados (list): Os resultados processados a exportar
        output_filename (str): O nome do ficheiro onde os dados serão guardados

    Returns:
        None
    """
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
    escrever_json(resultados_serializaveis, output_filename)
    return None

def escrever_json(resultados_serializaveis: list, output_filename: str) -> None:
    """
    Executa a operação de escrita da lista formatada num ficheiro json

    Args:
        resultados_serializaveis (list): A lista formatada 
        output_filename (str): O caminho do ficheiro de destino

    Returns:
        None
    """
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        json.dump(resultados_serializaveis, outfile, ensure_ascii=False, indent=4)
    return None

def main():
    nomes, apelidos, medicamentos, tabela_medicamentos = carregar_dados()
    utentes = criar_utentes(nomes, apelidos)
    receitas = criar_receitas_medicas(utentes, medicamentos)
    resultados = calcular_todas_interacoes(receitas, tabela_medicamentos)
    exportar_para_json(resultados)

if __name__ == '__main__':
    main()