import sys


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    char_map = {
        '(': 'LEFT_PAREN',
        ')': 'RIGHT_PAREN',
        '{': 'LEFT_BRACE',
        '}': 'RIGHT_BRACE',
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'STAR',
        '/': 'SLASH',
        '.': 'DOT',
        ';': 'SEMICOLON',
        ',': 'COMMA',
        '=': 'EQUAL',
        '!': 'BANG',
        '>': 'GREATER',
        '<': 'LESS'
    }

    reserved = {
        'and': 'AND',
        'class': 'CLASS',
        'else': 'ELSE',
        'false': 'FALSE',
        'for': 'FOR',
        'fun': 'FUN',
        'if': 'IF',
        'nil': "NIL",
        'or':'OR',
        'print': 'PRINT',
        'return': 'RETURN',
        'super': 'SUPER',
        'this': 'THIS',
        'true': 'TRUE',
        'var': 'VAR',
        'while': 'WHILE'
    }

    def isnumber(c):
        return c >= '0' and c <= '9'
    
    def isalpha(c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c == '_')

    def isalphanum(c):
        return isalpha(c) or isnumber(c)
    
    err = False
    for idx, line in enumerate(file_contents.split('\n')):
        c = 0
        while c < len(line):
            if line[c] in char_map:
                if line[c] in ['=', '!', '<', '>'] and c + 1 < len(line) and line[c + 1] == '=':
                    print(f'{char_map[line[c]]}_{char_map[line[c + 1]]} {line[c]}{line[c + 1]} null')
                    c += 1

                elif line[c] == '/' and c + 1 < len(line) and line[c + 1] == '/':
                    break

                else:
                    print(f'{char_map[line[c]]} {line[c]} null')
            
            elif line[c] in [' ', '\t']:
                ...
            
            elif line[c] == "\"":
                    c += 1
                    s = ""
                    while c < len(line):
                        if line[c] == '\"':
                            break
                        s += line[c]
                        c += 1
                    if c < len(line):
                        print(f"STRING \"{s}\" {s}")
                    else:
                        err = True
                        print(f"[line {idx + 1}] Error: Unterminated string.", file=sys.stderr)
                    
            elif isnumber(line[c]):
                s = ""
                dot = False
                while c < len(line) and isnumber(line[c]):
                    s += line[c]
                    c += 1

                if c < len(line) and line[c] == '.' and c + 1 < len(line) and isnumber(line[c + 1]):
                    s += '.'
                    c += 1
                    dot = True

                while c < len(line) and isnumber(line[c]):
                    s += line[c]
                    c += 1
                
                fl = s
                if not dot:
                    fl += '.0'
                while fl[-1] == '0' and fl[-2] == '0':
                    fl = fl[:-1]
                
                print(f"NUMBER {s} {fl}")
                    
                continue

            elif isalpha(line[c]):
                s = ""
                while c < len(line) and isalphanum(line[c]):
                    s += line[c]
                    c += 1
                
                if s in reserved:
                    print(f'{reserved[s]} {s} null')
                else:
                    print(f"IDENTIFIER {s} null")

                continue
            
            else:
                err = True
                print(f"[line {idx + 1}] Error: Unexpected character: {line[c]}", file=sys.stderr)
            
            c += 1
                
    print("EOF  null")
    
    if err:
        exit(65)


if __name__ == "__main__":
    main()
