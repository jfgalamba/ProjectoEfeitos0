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

import sys
import time
import random
from typing import Callable, Iterable

from console_utils import clear_screen, pause, show_msg, show_msgs, ask
from utils import renumerate


DEFAULT_LINE_LEN = 40     # em caracteres
DEFAULT_DELAY = 0.1       # em segundos (neste caso temos 0.1s)


def main():
    txt = 'FRASCO AZUL'
    while True:
        clear_screen()
        show_menu_options()
        try:
            opcao = ask("  OPÇÃO> ")
        except KeyboardInterrupt:
            break
        print()

        clear_screen()
        match opcao.upper():
            case '1':
                show_left_to_right_diagonal_effect(txt)
            case '2':
                show_right_to_left_diagonal_effect(txt)
            case '3':
                show_x_effect(txt)
            case '4':
                show_v_effect(txt)
            case '5':
                show_stair_effect(txt)
            case '6':
                show_slidding_effect(txt)
            case '7':
                show_uncover_line_effect(txt, speedup = 0.5)
            case '8':
                show_uncover_matrix_effect(txt, speedup = 2.0)
            case 'T' | 'TODOS':
                all_effects(
                    txt,
                    (
                        show_left_to_right_diagonal_effect,
                        show_right_to_left_diagonal_effect,
                        show_x_effect,
                        show_v_effect,
                        show_stair_effect,
                        show_slidding_effect,
                        lambda txt: show_uncover_line_effect(txt, speedup = 0.5),
                        lambda txt: show_uncover_matrix_effect(txt, speedup = 2.0)
                    ),
                )
                continue
            case 'E' | 'ENCERRAR':
                break
            case _:
                print(f"Opção <{opcao}> inválida")

        pause()
    #: while => main loop: the program should terminate when this loop ends
    show_msg("  O programa vai encerrar!\n")
#:

def show_menu_options():
    menu = """
****************************************************
*                                                  *
*  EFEITO                                          *
*                                                  *
*    1 - Diagonal Esquerda                         *
*    2 - Diagonal Direita, Texto Invertido         *
*    3 - Diagonais Cruzadas                        *
*    4 - Em V                                      *
*    5 - Escada, Palavras Ordem Inversa            *
*    6 - Deslizante                                *
*    7 - Destapa Posições Aleatórias               *
*    8 - Destapa Matriz                            *
*    T - Todos                                     *
*    E - Encerrar                                  *
*                                                  *
****************************************************
"""
    show_msgs(menu.split('\n'))
    print()
#:

def show_left_to_right_diagonal_effect(txt: str):
    for i, ch in enumerate(txt):
        show_msg(f"{' ' * i}{ch}")
#:

def show_right_to_left_diagonal_effect(txt: str):
    for i, ch in renumerate(txt):
        show_msg(f"{' ' * i}{ch}")
#:

def show_x_effect(txt: str):
    for l, ch in enumerate(txt):
        show_msg(end='')   # indent the line like in all other show_msgs
        for c in range(len(txt)):
            if l == c or l + c == len(txt) - 1:
                show_msg(ch, indent = 0, end = '')
            else:
                show_msg(' ', indent = 0, end = '')
        print()
#:

def show_v_effect(txt: str):
    isc = len(txt) * 2 - 2      # inside_spaces_count
    osc = 0                     # outside_spaces_count
    for ch1, ch2 in zip(txt, reversed(txt)):
        show_msg(f"{' ' * osc}{ch1}{' ' * isc}{ch2}{' ' * osc}")
        isc -= 2
        osc += 1
#:

def show_stair_effect(txt: str):
    words = reversed(txt.split())
    for i, word in enumerate(words):
        show_msg(f"{' ' * i}{word}")
#:

def show_slidding_effect(txt: str, line_len = DEFAULT_LINE_LEN, delay = DEFAULT_DELAY):
    try:
        i = 0
        while True:
            line = ['.'] * line_len
            for j, ch in enumerate(txt):
                line[(i + j) % line_len] = ch
            show_msg(f"{''.join(line)}", end = '\r')
            i += 1
            time.sleep(delay)
    except KeyboardInterrupt:
        show_msg(f"{''.join(line)}")  # type: ignore
#:

def show_uncover_line_effect(txt: str, delay = DEFAULT_DELAY, speedup = 1.0):
    delay /= speedup
    random_positions = list(range(len(txt)))
    random.shuffle(random_positions)
    line = ['.'] * len(txt)
    for pos in random_positions:
        line[pos] = txt[pos]
        show_msg(''.join(line), end = '\r')
        time.sleep(delay)
    print()
#:

def show_uncover_matrix_effect(txt: str, delay = DEFAULT_DELAY, speedup = 1.0):
    delay /= speedup
    random_positions = list(range(len(txt) ** 2))
    random.shuffle(random_positions)
    matrix = [['.' for _ in range(len(txt))] for _ in range(len(txt))]

    for pos in random_positions:
        clear_screen()
        l = pos // len(txt)
        c = pos % len(txt)
        matrix[l][c] = txt[c]
        # print('\n'.join(''.join(line) for line in matrix))
        show_msgs(''.join(line) for line in matrix)
        time.sleep(delay)
#:

def all_effects(
        txt: str, 
        effects: Iterable[Callable],
        clear_screen_ = True,
        pause_ = True,
):
    clear_screen_fn = (lambda: None, clear_screen)[clear_screen_]
    pause_fn        = (lambda: None, pause)[pause_]
    for effect in effects:
        clear_screen_fn()
        effect(txt)
        pause_fn()
#:

if __name__ == '__main__':
    main()
