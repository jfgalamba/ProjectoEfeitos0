#!/usr/env python
"""
Nesta parte deve desenvolver um programa em Python para exibir o texto
introduzido na linha de comandos de acordo com determinados "efeitos
especiais" (ver à frente). O seu programa deve ser invocado da seguinte
forma (propositadamente, neste e noutros programas deste enunciado 
omitimos o interpretador; ou seja, consonte a sua plataforma poderá ter
que prefxar o script com python ou python3):

    $ efeitos.py [-i INTERVALO] [-d DIM] palavra1 [palavra2] ... [palavraN]

Depois aplica cada um dos efeitos em baixo descritos ao texto que 
resulta da concatenação de palavra1, palavra2, etc. Consoante a sua
plataforma, poderá ter que invocar directamente o interpretador Os
caracteres do texto (que resultam da concatenação de todas as palavras)
devem ser exibidos individualmente.

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

O programa exibe um menu com opções indivuais cada um dos efeitos, e uma
opção para vê-los todos em sucessão.

--------------------------------------------------------------------------------

(C) João Galamba, 2025
Código sob licença MIT - https://mit-license.org/
"""

import sys
import time
import random

from console_utils import clear_screen, pause


DEFAULT_LINE_LEN = 20
DEFAULT_DELAY = 0.2


def main():
    if len(sys.argv) < 2:
        print("Utilização: [python] efeitos.py PALAVRA1...")
        sys.exit(2)
    
    txt = ' '.join(sys.argv[1:])

    slidding_effect(txt)
    pause()
    clear_screen()

    uncover_line_effect(txt, speedup = 0.5)
    pause()
    clear_screen()

    uncover_matrix_effect(txt, speedup = 2.0)
    pause()
    clear_screen()
#:

def slidding_effect(txt: str, line_len = DEFAULT_LINE_LEN, delay = DEFAULT_DELAY):
    try:
        i = 0
        while True:
            line = ['.'] * line_len
            for j, ch in enumerate(txt):
                line[(i + j) % line_len] = ch
            print(f"{''.join(line)}", end = '\r')
            i += 1
            time.sleep(delay)
    except KeyboardInterrupt:
        print(f"{''.join(line)}")  # type: ignore
#:

def uncover_line_effect(txt: str, delay = DEFAULT_DELAY, speedup = 1.0):
    delay /= speedup
    random_positions = list(range(len(txt)))
    random.shuffle(random_positions)
    line = ['.'] * len(txt)
    for pos in random_positions:
        line[pos] = txt[pos]
        print(''.join(line), end = '\r')
        time.sleep(delay)
    print()
#:

def uncover_matrix_effect(txt: str, delay = DEFAULT_DELAY, speedup = 1.0):
    delay /= speedup
    random_positions = list(range(len(txt) ** 2))
    random.shuffle(random_positions)
    matrix = [['.' for _ in range(len(txt))] for _ in range(len(txt))]

    for pos in random_positions:
        clear_screen()
        l = pos // len(txt)
        c = pos % len(txt)
        matrix[l][c] = txt[c]
        print('\n'.join(''.join(line) for line in matrix))
        time.sleep(delay)
#:

if __name__ == '__main__':
    main()

"""
EFEITO DESLIZANTE => ANÁLISE DA VERSÃO SIMLES
line_len = 10
txt = 'JOSE'
i = 0:
    line = '..........' (em lista)
    j = 0..3, ch = 'J'..'E':
        line[(0 + 0) % 10=0] = 'J'
        line[(0 + 1) % 10=1] = 'O'
        line[(0 + 2) % 10=2] = 'S'
        line[(0 + 3) % 10=2] = 'E'
    line = 'JOSE......'
i = 1:
    line = '..........' (em lista)
    j = 0..3, ch = 'J'..'E':
        line[(1 + 0) % 10=1] = 'J'
        line[(1 + 1) % 10=2] = 'O'
        line[(1 + 2) % 10=3] = 'S'
        line[(1 + 3) % 10=4] = 'E'
    line = '.JOSE.....'
i = 7:
    line = '..........' (em lista)
    j = 0..3, ch = 'J'..'E':
        line[(7 + 0) % 10=7] = 'J'
        line[(7 + 1) % 10=8] = 'O'
        line[(7 + 2) % 10=9] = 'S'
        line[(7 + 3) % 10=0] = 'E'   # 10 % 10 == 0, ou seja, fica line[0] = 'E'
    line = 'E......JOS'
i = 17:
    line = '..........' (em lista)
    j = 0..3, ch = 'J'..'E':
        line[(17 + 0) % 10=7] = 'J'
        line[(17 + 1) % 10=8] = 'O'
        line[(17 + 2) % 10=9] = 'S'
        line[(17 + 3) % 10=0] = 'E'  # 20 % 10 == 0, ou seja, fica line[0] = 'E'
    line = 'E......JOS'
"""

"""
EFEITO DESLIZANTE => VERSÃO COMPLICADA...

def efeito_deslizante(txt: str, line_len = DEFAULT_LINE_LEN, delay=DEFAULT_DELAY):
    try:
        i = 0
        while True:
            line = ['.'] * line_len
            line[i:i + len(txt)] = txt[:line_len - i] 
            if line_len - i < len(txt):
                line[:len(txt) + i - line_len] = txt[line_len-i:]

            print(f"{''.join(line)}", end='\r')

            i = (i + 1) % line_len
            time.sleep(delay)
    except KeyboardInterrupt:
        pass
#:

line_len = 10
txt = 'JOSE'
line[i:i+len(txt)] = txt[:line_len-i]
    i == 0 => line[0:4] = txt[:10-0=10] == 'JOSE'
    i == 1 => line[1:5] = txt[:10-1=9]  == 'JOSE'
    i == 8 => line[8:12] = txt[:10-8=2]  == 'JO'
    i == 9 => line[9:13] = txt[:10-9=1]  == 'J'

line_len-i < txt_len ? line[:txt_len+i-line_len] = txt[line_len-i:]
    i = 0 => 10-0=10 < 4? False => 
    i = 1 => 10-1=9 < 4? False  =>
    i = 6 => 10-6=4 < 4? False  => 
    i = 7 => 10-7=3 < 4? True   => line[:4+7-10=1] = txt[10-7=3:] == 'E'
    i = 8 => 10-8=2 < 4? True   => line[:4+8-10=2] = txt[10-8=2:] == 'SE'
    i = 9 => txt[10-9=1:]  == 'OSE'

0123456789
SE......JO
OSE......J
JOSE......
"""


"""
EFEITO MATRIZ => ANÁLISE

txt = 'ABCD'  # ou qq string de 4 caracteres

 |  0  1  2  3
-+-------------
0|  0  1  2  3
1|  4  5  6  7
2|  8  9 10 11
3| 12 13 14 15
-+--------------

pos |  line
----+----------
  1 |  1 // 4 = 0
  2 |  2 // 4 = 0
  9 |  9 // 4 = 2
 15 | 15 // 4 = 3

pos |  column
----+----------
  1 | 1 % 4 = 1
  2 | 2 % 4 = 2
  9 | 9 % 4 = 1
 15 | 15 % 4 = 3
"""
