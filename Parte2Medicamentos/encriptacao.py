from constantes import lista_numeros, lista_alfabeto

def encriptar(texto: str) -> str:
    """
    Encripta uma string utilizando uma cifra de substituição posicional.

    Cada caractere é deslocado para a frente no alfabeto/números com uma chave 
    determinada pela sua posição na lista original: posições pares usam chave 3, 
    posições ímpares usam chave 5.
    
    Argumentos:
        texto (str): A string em texto simples a encriptar (nomes ou IDs).

    Retorna:
        str: A string encriptada.
    """
    palavra_encriptada = ""
    for letra in texto.lower():
        if letra == " ":
            palavra_encriptada += " "
        elif letra in lista_numeros:
            posicao = lista_numeros.index(letra)
            if posicao % 2 == 0:
                chave = 3
            else:                
                chave = 5
            nova_posicao = (posicao + chave) % 10
            palavra_encriptada += lista_numeros[nova_posicao]
        elif letra in lista_alfabeto:
            posicao = lista_alfabeto.index(letra)
            if posicao % 2 == 0:
                chave = 3
            else:
                chave = 5
            nova_posicao = (posicao + chave) % 26
            palavra_encriptada += lista_alfabeto[nova_posicao]
    return palavra_encriptada