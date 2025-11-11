import re
import copy
import pandas as pd


def is_symbol(symbol: str) -> tuple[bool, str] | tuple[bool, None]:
    symbols = '+-|^<-=><:[]'
    if symbol.strip() in symbols:
        return True, f'<op,{symbol[:-1]}>'
    return False, None


def is_string(lexim: str) -> tuple[bool, str] | tuple[bool, None]:
    if lexim.strip()[-1] == '"' and lexim.strip()[0] == '"':
        return True, f'<str,{lexim[:-1]}>'
    return False, None


def is_number(number: str) -> tuple[bool, None] | tuple[bool, str]:
    numbers = '0123456789/'
    for i in number.strip():
        if i in numbers:
            continue
        else:
            return False, None
    return True, f'<number,{lexim[:-1]}>'


def is_Id(id: str) -> tuple[bool, str] | tuple[bool, None]:
    global num_id
    global id_dict
    j = 0
    state = 0
    str_av = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#'
    while True:
        ch = id[j]
        match state:
            case 0:
                if ch == '&':
                    state = 1
                    j += 1
                else:
                    state = 4
            case 1:
                if ch in str_av:
                    state = 2
                    j += 1
                else:
                    state = 4
            case 2:
                if ch in str_av:
                    state = 2
                    j += 1
                elif ch == '&':
                    state = 3
                    j += 1
                else:
                    state = 4
            case 3:
                if ch == '\n':
                    test = id_dict.get(id.strip(), 'no')
                    if test == 'no':
                        num_id += 1
                        id_dict[id.strip()] = f'<id,{num_id}>'
                        return True, f'<id,{num_id}>'
                    else:
                        return True, id_dict[id.strip()]
                else:
                    state = 4
            case 4:
                return False, None


def repeat(lexim):
    j = 0
    state = 0
    while True:
        ch = lexim[j]
        match state:
            case 0:
                if ch == 'r':
                    state = 1
                    j += 1
                else:
                    state = 7
            case 1:
                if ch == 'e':
                    state = 2
                    j += 1
                else:
                    state = 7
            case 2:
                if ch == 'p':
                    state = 3
                    j += 1
                else:
                    state = 7
            case 3:
                if ch == 'e':
                    state = 4
                    j += 1
                else:
                    state = 7
            case 4:
                if ch == 'a':
                    state = 5
                    j += 1
                else:
                    state = 7
            case 5:
                if ch == 't':
                    state = 6
                    j += 1
                else:
                    state = 7
            case 6:
                if ch == '\n':
                    return True, '<forwhile>'
                else:
                    state = 7
            case 7:
                return False, None


def func(lexim):
    j = 0
    state = 0
    while True:
        ch = lexim[j]
        match state:
            case 0:
                if ch == 'f':
                    state = 1
                    j += 1
                else:
                    state = 5
            case 1:
                if ch == 'u':
                    state = 2
                    j += 1
                else:
                    state = 5
            case 2:
                if ch == 'n':
                    state = 3
                    j += 1
                else:
                    state = 5
            case 3:
                if ch == 'c':
                    state = 4
                    j += 1
                else:
                    state = 5
            case 4:
                if ch == '\n':
                    return True, '<def>'
                else:
                    state = 5
            case 5:
                return False, None


def verd(lexim):
    j = 0
    state = 0
    while True:
        ch = lexim[j]
        match state:
            case 0:
                if ch == 'v':
                    state = 1
                    j += 1
                else:
                    state = 5
            case 1:
                if ch == 'e':
                    state = 2
                    j += 1
                else:
                    state = 5
            case 2:
                if ch == 'r':
                    state = 3
                    j += 1
                else:
                    state = 5
            case 3:
                if ch == 'd':
                    state = 4
                    j += 1
                else:
                    state = 5
            case 4:
                if ch == '\n':
                    return True, '<mkboolian>'
                else:
                    state = 5
            case 5:
                return False, None


def se(lexim):
    j = 0
    state = 0
    while True:
        ch = lexim[j]
        match state:
            case 0:
                if ch == 's':
                    state = 1
                    j += 1
                else:
                    state = 3
            case 1:
                if ch == 'e':
                    state = 2
                    j += 1
                else:
                    state = 3
            case 2:
                if ch == '\n':
                    return True, '<if>'
                else:
                    state = 3
            case 3:
                return False, None


def alse(lexim):
    j = 0
    state = 0
    while True:
        ch = lexim[j]
        match state:
            case 0:
                if ch == 'a':
                    state = 1
                    j += 1
                else:
                    state = 5
            case 1:
                if ch == 'l':
                    state = 2
                    j += 1
                else:
                    state = 5
            case 2:
                if ch == 's':
                    state = 3
                    j += 1
                else:
                    state = 5
            case 3:
                if ch == 'e':
                    state = 4
                    j += 1
                else:
                    state = 5
            case 4:
                if ch == '\n':
                    return True, '<elif>'
                else:
                    state = 5
            case 5:
                return False, None


def al(lexim):
    j = 0
    state = 0
    while True:
        ch = lexim[j]
        match state:
            case 0:
                if ch == 'a':
                    state = 1
                    j += 1
                else:
                    state = 3
            case 1:
                if ch == 'l':
                    state = 2
                    j += 1
                else:
                    state = 3
            case 2:
                if ch == '\n':
                    return True, '<else>'
                else:
                    state = 3
            case 3:
                return False, None


def en(lexim):
    j = 0
    state = 0
    while True:
        ch = lexim[j]
        match state:
            case 0:
                if ch == 'e':
                    state = 1
                    j += 1
                else:
                    state = 3
            case 1:
                if ch == 'n':
                    state = 2
                    j += 1
                else:
                    state = 3
            case 2:
                if ch == '\n':
                    return True, '<in>'
                else:
                    state = 3
            case 3:
                return False, None


def bro(lexim):
    j = 0
    state = 0
    while True:
        ch = lexim[j]
        match state:
            case 0:
                if ch == 'b':
                    state = 1
                    j += 1
                else:
                    state = 4
            case 1:
                if ch == 'r':
                    state = 2
                    j += 1
                else:
                    state = 4
            case 2:
                if ch == 'o':
                    state = 3
                    j += 1
                else:
                    state = 4
            case 3:
                if ch == '\n':
                    return True, '<defcall>'
                else:
                    state = 4
            case 4:
                return False, None


def ritorno(lexim):
    j = 0
    state = 0
    while True:
        ch = lexim[j]
        match state:
            case 0:
                if ch == 'r':
                    state = 1
                    j += 1
                else:
                    state = 8
            case 1:
                if ch == 'i':
                    state = 2
                    j += 1
                else:
                    state = 8
            case 2:
                if ch == 't':
                    state = 3
                    j += 1
                else:
                    state = 8
            case 3:
                if ch == 'o':
                    state = 4
                    j += 1
                else:
                    state = 8
            case 4:
                if ch == 'r':
                    state = 5
                    j += 1
                else:
                    state = 8
            case 5:
                if ch == 'n':
                    state = 6
                    j += 1
                else:
                    state = 8
            case 6:
                if ch == 'o':
                    state = 7
                    j += 1
                else:
                    state = 8
            case 7:
                if ch == '\n':
                    return True, '<return>'
                else:
                    state = 8
            case 8:
                return False, None


def ilg(lexim):
    j = 0
    state = 0
    while True:
        ch = lexim[j]
        match state:
            case 0:
                if ch == 'i':
                    state = 1
                    j += 1
                else:
                    state = 4
            case 1:
                if ch == 'l':
                    state = 2
                    j += 1
                else:
                    state = 4
            case 2:
                if ch == 'g':
                    state = 3
                    j += 1
                else:
                    state = 4
            case 3:
                if ch == '\n':
                    return True, '<mknumber>'
                else:
                    state = 4
            case 4:
                return False, None


def rango(lexim):
    j = 0
    state = 0
    while True:
        ch = lexim[j]
        match state:
            case 0:
                if ch == 'r':
                    state = 1
                    j += 1
                else:
                    state = 6
            case 1:
                if ch == 'a':
                    state = 2
                    j += 1
                else:
                    state = 6
            case 2:
                if ch == 'n':
                    state = 3
                    j += 1
                else:
                    state = 6
            case 3:
                if ch == 'g':
                    state = 4
                    j += 1
                else:
                    state = 6
            case 4:
                if ch == 'o':
                    state = 5
                    j += 1
                else:
                    state = 6
            case 5:
                if ch == '\n':
                    return True, '<range_num>'
                else:
                    state = 6
            case 6:
                return False, None


def caden(lexim):
    j = 0
    state = 0
    while True:
        ch = lexim[j]
        match state:
            case 0:
                if ch == 'c':
                    state = 1
                    j += 1
                else:
                    state = 6
            case 1:
                if ch == 'a':
                    state = 2
                    j += 1
                else:
                    state = 6
            case 2:
                if ch == 'd':
                    state = 3
                    j += 1
                else:
                    state = 6
            case 3:
                if ch == 'e':
                    state = 4
                    j += 1
                else:
                    state = 6
            case 4:
                if ch == 'n':
                    state = 5
                    j += 1
                else:
                    state = 6
            case 5:
                if ch == '\n':
                    return True, '<mkstr>'
                else:
                    state = 6
            case 6:
                return False, None


given_code = input('Enter the file name.txt-> ')
key_list = [repeat, func, verd, se, alse, al, en, bro, ritorno, ilg, rango, caden]
num_id = 0
token_dict = {'key_word': [], 'Id': [], 'symbol': [], 'numbers and string': []}
id_dict = dict()
with open(given_code, 'r') as fh_code:
    with open('Tokens.txt', 'w') as fh_token:
        code_lines = fh_code.readlines()
        ch_line = copy.deepcopy(code_lines)
        code_line = []
        for i in code_lines:
            code_line.append(i.strip().split())
        code_lines = []
        for i in code_line:
            temp = []
            for j in i:
                temp.append(j + '\n')
            code_lines.append(temp)
        for num_line, line in enumerate(code_lines):
            for end, lexim in enumerate(line):
                for key in key_list:
                    key_word = key(lexim)
                    if key_word[0]:
                        break
                Id = is_Id(lexim)
                num = is_number(lexim)
                symbol_ = is_symbol(lexim)
                str_ = is_string(lexim)
                if key_word[0]:
                    fh_token.write(key_word[1] + ' ')
                    token_dict['key_word'].append(key_word[1])
                    if end == len(line)-1:
                        fh_token.write('\n')
                elif Id[0]:
                    fh_token.write(Id[1] + ' ')
                    token_dict['Id'].append(Id[1])
                    if end == len(line) - 1:
                        fh_token.write('\n')
                elif symbol_[0]:
                    fh_token.write(symbol_[1] + ' ')
                    token_dict['symbol'].append(symbol_[1])
                    if end == len(line) - 1:
                        fh_token.write('\n')
                elif num[0]:
                    fh_token.write(num[1] + ' ')
                    token_dict['numbers and string'].append(num[1])
                    if end == len(line) - 1:
                        fh_token.write('\n')
                elif str_[0]:
                    fh_token.write(str_[1] + ' ')
                    token_dict['numbers and string'].append(str_[1])
                    if end == len(line) - 1:
                        fh_token.write('\n')
                else:
                    match_ = "\nrepeat\nfunc\nverd\nse\nalse\nal\nen\nbro\nritorno\nilg\nrango\n+\n-\n|\n^\n<-\n=\n>\n<\n:\n[\n]"
                    list_s = []
                    flag_id = True
                    make_wh = 1
                    if lexim[0].startswith('&') or lexim[:-1].endswith('&'):
                        make_change = input(f'error in line {num_line + 1} and lexim {lexim} your variable is not complete\n'
                                            f'do you want me to complete it for you :) y/n')
                        flag_id = False
                    elif len(lexim.strip()) >= 3:
                        list_s = re.findall('\n(' + lexim.strip()[:2] + '.+)\n', match_)
                        list_s = list_s + re.findall('\n(.+' + lexim.strip()[-2:] + ')\n', match_)
                    else:
                        list_s = re.findall("(" + lexim.strip()[:1] + '..)\n', match_)
                        list_s = list_s + re.findall('\n(.' + lexim.strip()[1:] + ')\n', match_)
                    if len(list_s) < 1 and flag_id:
                        print(
                            f"error in line {num_line + 1} and lexim {lexim} did you mean number or string or i don't know :( ")
                        make_change = 'n'
                    elif flag_id:
                        make_change = input(f"error in line {num_line + 1} and lexim {lexim} did you mean -> {list_s}\n"
                                            f"do you want to change it y/n")
                        if len(list_s) >= 2 and make_change.lower() == 'y':
                            make_wh = input('which one do you want to change to it 1 or 2 or.....')
                    if make_change.lower() == 'n':
                        exit()
                    elif flag_id:
                        # make the change for the key word in the line that we have
                        ch_line[num_line] = ch_line[num_line].replace(lexim.strip(), list_s[int(make_wh) - 1])
                        for key in key_list:
                            key_word = key(list_s[int(make_wh) -1] + '\n')
                            if key_word[0]:
                                break
                        if key_word[0]:
                            fh_token.write(key_word[1] + ' ')
                            token_dict['key_word'].append(key_word[1])
                        with open(given_code, 'w') as fh1:
                            for i in ch_line:
                                fh1.write(i)
                    elif lexim[0].startswith('&'):
                        # make change the lexim and the line that we want
                        ch_line[num_line] = ch_line[num_line].replace(lexim.strip(), lexim.strip() + '&')
                        lexim = lexim.strip() + '&\n'
                        Id = is_Id(lexim)
                        if Id[0]:
                            fh_token.write(Id[1] + ' ')
                            token_dict['Id'].append(Id[1])
                            if end == len(line) - 1:
                                fh_token.write('\n')
                        with open(given_code, 'w') as fh1:
                            for i in ch_line:
                                fh1.write(i)
                    elif lexim[:-1].endswith('&'):
                        ch_line[num_line] = ch_line[num_line].replace(lexim.strip(), '&' + lexim.strip())
                        lexim = '&' + lexim
                        Id = is_Id(lexim)
                        if Id[0]:
                            fh_token.write(Id[1] + ' ')
                            token_dict['Id'].append(Id[1])
                            if end == len(line) - 1:
                                fh_token.write('\n')
                        with open(given_code, 'w') as fh1:
                            for i in ch_line:
                                fh1.write(i)
df_tokens = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in token_dict.items()]))
with open('Tokens_table.txt', 'w') as fh_table:
    dfAsString = df_tokens.to_string(header=True, index=True)
    fh_table.write(dfAsString)
df_id = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in id_dict.items()]))
with open('id_table.txt', 'w') as fh_table:
    dfAsString = df_id.to_string(header=True, index=True)
    fh_table.write(dfAsString)
