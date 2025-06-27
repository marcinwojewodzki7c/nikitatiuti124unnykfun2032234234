#Interpreter języka programowania Gusew++
#nikitatiutiunnyk.fun

import sys

variables = {}

def cast_value(type_prefix, val):
    if type_prefix == "l_var":
        return int(val)
    elif type_prefix == "TF_var":
        return val.lower() == "true"
    elif type_prefix == "a_var":
        return str(val)
    return val

def eval_expr(expr):
    tokens = expr.split()
    resolved = []
    for tok in tokens:
        if tok in variables:
            typ, val = variables[tok]
            if typ != "l_var":
                raise Exception(f"Zmienna '{tok}' nie jest liczbą")
            resolved.append(str(val))
        else:
            resolved.append(tok)
    return int(eval(" ".join(resolved)))

def run(code):
    lines = code.strip().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("//"):
            i += 1
            continue

        if line.startswith(("l_var", "a_var", "TF_var")):
            type_prefix, rest = line.split(" ", 1)
            name_part, value_part = rest.split("->")
            var_name = name_part.strip().strip('"')
            raw_value = value_part.strip().strip('"')
            variables[var_name] = (type_prefix, cast_value(type_prefix, raw_value))

        elif line.startswith("say "):
            var_name = line[4:].strip().strip('"')
            if var_name in variables:
                print(variables[var_name][1])
            else:
                print(f"[nieznana zmienna: {var_name}]")

        elif line.startswith("ask "):
            var_name = line[4:].strip().strip('"')
            if var_name not in variables:
                print(f"[Błąd: zmienna '{var_name}' nie istnieje]")
                i += 1
                continue
            type_prefix, _ = variables[var_name]
            val = input(f"Podaj wartość dla '{var_name}': ")
            variables[var_name] = (type_prefix, cast_value(type_prefix, val))

        elif line.startswith("math {"):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("}"):
                subline = lines[i].strip()
                if subline.startswith("l_var"):
                    type_prefix, rest = subline.split(" ", 1)
                    name_part, value_part = rest.split("->")
                    var_name = name_part.strip().strip('"')
                    expr = value_part.strip().strip('"')
                    try:
                        result = eval_expr(expr)
                        variables[var_name] = ("l_var", result)
                    except Exception as e:
                        print(f"[Błąd w math: {e}]")
                i += 1

        elif line.startswith("if "):
            var_name = line[4:].strip().strip('"')
            condition = variables.get(var_name, (None, False))[1]
            i += 1
            if_true = []
            if_false = []
            current = if_true
            while i < len(lines):
                l = lines[i].strip()
                if l == "}":
                    break
                if l == "else {":
                    current = if_false
                else:
                    current.append(l)
                i += 1
            block = if_true if condition else if_false
            run("\n".join(block))

        i += 1

if len(sys.argv) == 3 and sys.argv[1] == "-krix":
    filename = sys.argv[2]
    with open(filename, "r", encoding="utf-8") as f:
        run(f.read())
else:
    print("Użycie: gusew -krix plik.gusew")
