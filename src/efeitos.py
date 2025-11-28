#!/usr/bin/env python3
"""
Nesta parte deve desenvolver um programa em Python para exibir o texto
introduzido na linha de comandos de acordo com determinados "efeitos
especiais" (ver à frente). O seu programa deve ser invocado da seguinte
forma (propositadamente, neste e noutros programas deste enunciado 
omitimos o interpretador; ou seja, consonte a sua plataforma poderá ter
que prefxar o script com python ou python3):

    $ efeitos.py [-i INTERVALO] [-d DIM] palavra1 [palavra2] ... [palavraN]

Depois aplica cada um dos efeitos em baixo descritos ao texto que 
resulta da concatenação de palavra1, palavra2, etc. No enunciado
encontra o significado das opções '-i' e '-d'.

Os caracteres do texto (que resultam da concatenação de todas as 
palavras) devem ser exibidos individualmente.

A opção -i permite indicar intervalo de tempo entre exibições, ao passo que 
a opção -d indica a dimensão da linha onde apropriado.

Para já, os efeitos a desenvolver são:

    * Diagonal Esquerda 
    * Diagonal Direita, Texto Invertido
    * Diagonais Cruzadas
    * Em V (traços do V com texto invertido entre si)
    * Em Escada, Palavras por Ordem Inversa
    * Texto Deslizante
    * Destapa Posições Aleatórias
    * Destapa Matriz em Posições Aleatórias

O programa exibe um menu com opções para ver cada um dos efeitos de
forma individual, e todos em conjunto.

--------------------------------------------------------------------------------

(C) João Galamba, 2025
Código sob licença MIT. Consultar: https://mit-license.org/
"""

from console_utils import clear_screen, pause


def main():
    clear_screen()
    print("Hello, World!")
    pause()
#:

if __name__ == '__main__':
    main()
