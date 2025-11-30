"""
Utilitários (essencialmente funções) para usar na em programas que
correm no terminal.

--------------------------------------------------------------------------------

(C) João Galamba, 2025
Código sob licença MIT. Consultar: https://mit-license.org/
"""

import sys
import os
import subprocess as subproc
from collections.abc import Mapping
from typing import Iterable, Any
from contextlib import contextmanager


__all__ = (
    'accept',
    'show_msg',
    'show_msgs',
    'confirm',
    'ask',
    'show_msg',
    'show_msgs',
    'show_table',
    'pause',
    'clear_screen',
    'supports_ansi_terminal',
    'set_global_indentation',
    'temp_indentation',
)


_indentation = 3
_language = 'en'


def accept(
        msg: str, 
        error_msg: str, 
        check_fn = lambda _: True,
        convert_fn = lambda x: x, 
        indent = _indentation
) -> Any:
    """
    Accepts a value read from the standard input, optionally 
    validating it with `check_fn` and converting it to another type
    with `convert_fn`. Note that the value will only be accepted 
    if `check_fn` returns `True` and `convert_fn` successfully 
    completes. Thus, `check_fn` should be a boolean function, while 
    `convert_fn` should signal a failed conversion by raising an 
    exception. `check_fn` is called before `convert_fn` and is applied
    directly to the string value read from stdin. Of course, you can
    implement all the validation logic in `convert_fn`, without ever 
    needing to use `check_fn`.

    Examples:
    1. Accept an integer:
        accept(
            msg = "Enter an integer: ",
            error_msg = "Invalid integer {}",
            convert_fn = int,
        )

    2. Accept a positive integer:
        accept(
            msg = "Enter a positive integer: ",
            error_msg = "Invalid value {}",
            check_fn = str.isdigit,
            convert_fn = int,
        )

    3. Accept a positive integer, 2nd version:
        def to_positive_int(val: str) -> int:
            int_val = int(val)
            if int_val <= 0:
                raise ValueError(f'{val} is not a positive integer')
            return int_val

        accept(
            msg = "Enter a positive integer: ",
            error_msg = "Invalid value {}",
            convert_fn = to_positive_int,
        )

    4. Accept a positive integer with exactly five digits:
        accept(
            msg = "Enter a valid ID: ",
            error_msg = "Invalid text {}",
            check_fn = lambda id_: id_.isdigit() and len(id_) == 5 and id_[0] != 0,
            convert_fn = int,
        )

    5. Accept a non-emtpy string with at least two characters:
        accept(
            msg = "Enter valid text: ",
            error_msg = "Invalid ID {}",
            check_fn = lambda txt: len(txt.strip()) >= 2,
        )
    """
    while True:
        value_str = ask(msg, indent = indent)
        if check_fn(value_str):
            try:
                return convert_fn(value_str)
            except Exception:
                pass
        # we reached this point iif the check failed or an
        # exception was raised
        show_msg(error_msg.format(value_str))
        pause('')
        clear_screen()
#:

def confirm(
        msg: str, 
        default = '',
        indent = _indentation, 
        language = _language,
) -> bool:
    """
    >>> confirm("Do you like peanuts? ")
    Do you like peanuts? [yn] maybe
    Please answer Y or N.
    Do you like peanuts? [yn]
    An explicit answer is required. Please answer Y or N.
    Do you like peanuts? [yn] n
    False
    >>> confirm("Will it rain tomorrow? ", default = 'Y')
    Will it rain tomorrow? [Yn] ja
    Please answer Y or N.
    Will it rain tomorrow? [Yn]
    True
    >>> confirm("Tomorrow is the day after yesterday? ", default = 'N')
    Tomorrow is the day after yesterday? [yN] nein
    Please answer Y or N.
    Tomorrow is the day after yesterday? [yN]
    False
    >>> confirm("Tomorrow is the day after yesterday? ", default = 'BATATAS')
    Traceback (most recent call last):
    ...
    ValueError: Invalid default value: BATATAS
    """

    localized_text = {
        'en': {
            'default_text_dict': {
                'Y': '[Yn]',
                'N': '[yN]',
                '': '[yn]',
            },
            'acceptable_answers': {
                'yes': ('YES', 'Y'),
                'no': ('NO', 'N'),
            },
            'explicit_answer_required': 
                "An explicit answer is required. Please answer Y or N.",
            'invalid_answer': "Please answer Y or N.",
        },
        'pt': {
            'default_text_dict' : {
                'Y': '[Sn]',
                'N': '[sN]',
                '': '[sn]',
            },
            'acceptable_answers': {
                'yes': ('SIM', 'S'),
                'no': ('NÃO', 'NAO', 'N'),
            },
            'explicit_answer_required': 
                "É necessária uma resposta explícita. Por favor indique S ou N.",
            'invalid_answer': "Por favor, responda apenas S ou N.",
        },
    }

    local_text = localized_text[language]
    default_text_dict = local_text['default_text_dict']
    default_text = default_text_dict.get(default)
    if default_text is None:
        raise ValueError(f'Invalid default value: {default}.')
    yes_answers = local_text['acceptable_answers']['yes']
    no_answers = local_text['acceptable_answers']['no']

    msg += f'{default_text} '

    while True:
        ans = ask(msg, indent = indent).strip()
        ans_upper = ans.upper()

        if ans_upper in yes_answers:
            return True
        elif ans_upper in no_answers:
            return False
        elif ans_upper == '':
            if default:
                return default == 'Y'
            show_msg(local_text['explicit_answer_required'], indent = indent)
        else:
            show_msg(local_text['invalid_answer'], indent=indent)
#:

def ask(msg: str, indent = _indentation) -> str:
    return input(f"{indent * ' '}{msg}")
#:

def show_msg(*args, indent = _indentation, **kargs):
    print_args = [' ' * (indent - 1), *args] if indent > 0 else [*args]
    print(*print_args, **kargs)
#:

def show_msgs(msgs: Iterable[str], *args, indent = _indentation, **kargs):
    for msg in msgs:
        show_msg(msg, *args, indent = indent, **kargs)
#:

def show_table(
        elements: Iterable, 
        col_defs: dict[str, dict], 
        *show_args, 
        **show_kargs
):
    """
    EXAMPLE:
        def show_table_with_prods(prods: ProductCollection):
            show_table(
                prods,
                col_defs = {
                    'id': {'name': 'ID', 'align': '^', 'width': 8},
                    'name': {'name': 'Nome', 'align': '<', 'width': 26},
                    'prod_type': {'name': 'Tipo', 'align': '<', 'width': 8},
                    'quantity': {'name': 'Quantidade', 'align': '>', 'width': 16},
                    'price' : {'name': 'Preço', 'align': '>', 'width': 14,
                            'decimal_places': 2, 'unit': '€'},
                }
            )
        #:
    """

    # Generate HEADER
    header_fmt = ' | '.join(f"{{:^{col['width']}}}" for col in col_defs.values())
    header = header_fmt.format(*(col['name'] for col in col_defs.values()))

    # Generate SEPARATOR between HEADER and DATA
    # Generate `width + 2` dashes for all columns except for the first
    # and last columns; for these, generate `width + 1` dashes.
    sep_fmt = '+'.join('{}' for _ in col_defs)
    col_defs_values = list(col_defs.values())
    sep = sep_fmt.format(
        *[
            f"{'-' * (col_defs_values[0]['width'] + 1)}",
            *(f"{'-' * (col_def['width'] + 2)}" for col_def in col_defs_values[1:-1]),
            f"{'-' * (col_defs_values[-1]['width'] + 1)}",
        ]
    )

    # Generate DATA LINES
    def data_field_fmt_spec(col_def: dict) -> str:
        align = f"{col_def['align']}"
        width = f"{col_def['width']}"
        return f"{{:{align}{width}}}"
    #:
    data_line_fmt = ' | '.join(
        data_field_fmt_spec(col_def) for col_def in col_defs_values
    )

    data_lines = []
    for elem in elements:
        args = []
        for attr, col_def in col_defs.items():
            # Either val is Mapping (like a dictionary) or an object
            val = (
                elem[attr] if isinstance(elem, Mapping) else getattr(elem, attr)
            )
            convert_fn = col_def.get('convert_fn', lambda x: x)
            val = convert_fn(val)
            if 'decimal_places' in col_def:
                decimal_places_fmt = f'{{:.{col_def['decimal_places']}f}}' 
                val = decimal_places_fmt.format(val)
            unit = col_def.get('unit', '')
            args.append(f'{val}{unit}')
        data_lines.append(data_line_fmt.format(*args))

    if not data_lines:
        raise ValueError('Asked to generate table for empty collection/iterable.')

    # Now show everything
    for table_section in (header, sep, *data_lines):
        show_msg(table_section, *show_args, **show_kargs)
#:

def pause(msg: str="Pressione ENTER para continuar...", indent = _indentation):
    if msg:
        show_msg(msg, indent = indent)
    match os.name:
        case 'nt':      # Windows (excepto Win9X)
            os.system("pause>nul|set/p=")
        case 'posix':   # Unixes e compatíveis
            if os.path.exists('/bin/bash'):
                os.system('/bin/bash -c "read -s -n 1"')
            else:
                input()
        case _:
            input()
#:

def clear_screen():
    """
    Clear the console/terminal screen without flickering.

    * On most modern terminals (Linux, macOS, Windows Terminal, VS Code, etc.)
      it uses the ANSI escape sequence → instant, no flash.
    * If the terminal does not understand ANSI (rare on Windows cmd.exe when
      COLOR is disabled) it falls back to `cls`/`clear` **once** and then
      enables ANSI support for the rest of the session.
    """
    # 1. Try the fast ANSI way first
    if supports_ansi_terminal():
        sys.stdout.write("\x1b[2J\x1b[H")   # clear + move cursor home
        sys.stdout.flush()
        return

    # 2. Fallback: native command (may flash once)
    command = "cls" if os.name == "nt" else "clear"
    subproc.call(command, shell=True, stdout=subproc.DEVNULL, stderr=subproc.DEVNULL)

    # 3. On Windows cmd.exe enable ANSI for the *next* calls
    if os.name == "nt":
        # Enable virtual terminal processing (Windows 10+)
        try:
            import ctypes
            from ctypes import wintypes

            kernel32 = ctypes.windll.kernel32
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            mode = wintypes.DWORD()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
        except Exception:
            pass  # stay with the one-time flash
#:

def supports_ansi_terminal() -> bool:
    """
    Return True if the current stdout seems to understand ANSI codes
    (cached for speed).
    """
    # Cache the result on the function object
    if hasattr(supports_ansi_terminal, "cached"):
        return supports_ansi_terminal.cached  # type: ignore

    # Windows 10+ with enabled VT processing, most *nix terminals, etc.
    supported = bool(
        hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
        and (os.name != "nt" or os.getenv("WT_SESSION")  # Windows Terminal
             or os.getenv("ANSICON") or "NO_COLOR" not in os.environ)
    )

    # Extra check for Windows cmd.exe
    if os.name == "nt" and not supported:
        # Try to query the console mode
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_uint()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                supported = bool(mode.value & 0x0004)  # VT processing flag
        except Exception:
            pass

    supports_ansi_terminal.cached = supported   # type: ignore
    return supported
#:

#
# def clear_screen():
#     if os.name == 'posix':
#         subprocess.run(['clear'])
#     elif os.name == 'nt':
#         subprocess.run(['cls'], shell = True)
# #:


def set_global_indentation(new_identation: int):
    global _indentation
    if new_identation < 0:
        raise ValueError(f'Negative indentation: {new_identation}')
    _indentation = new_identation
#:

@contextmanager
def temp_indentation(new_identation: int):
    old_indentation = _indentation
    try:
        set_global_indentation(new_identation)
        yield
    finally:
        set_global_indentation(old_indentation)
#:
