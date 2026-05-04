import openpyxl
import random
import sys

def read_file(filepath:str)->list:
    with open(filepath, 'r' , encoding='utf-8') as file:
        return file.read().splitlines()
    


def criar_matriz(filepath: str) -> list:
    header = read_file(filepath)
    matriz = [[''] + header]  

    for i in range(len(header)):
        linhas = [header[i]]  
        for j in range(len(header)):
            if header[i] == header[j]:
                linhas.append('')
            else:
                linhas.append(str(random.randint(0, 5)))
        matriz.append(linhas)  
    return matriz


def exportar_excel( filepath:str , output_filepath:str):
    matriz = criar_matriz(filepath)
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            sheet.cell(row=i+1, column=j+1, value=matriz[i][j])

    workbook.save(output_filepath)

if __name__ == "__main__":
    filepath = sys.argv[1]
    output_filepath = sys.argv[2]
    exportar_excel(filepath, output_filepath)