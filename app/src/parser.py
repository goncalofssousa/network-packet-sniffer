_ops = ["!=", "==", ">=", "<=", ">", "<"]


# ----------------------------
# Utils
# ----------------------------


def get_nested_value(obj, path):
    parts = path.split(".")
    for p in parts:
        if not isinstance(obj, dict) or p not in obj:
            return None
        obj = obj[p]
    return obj


def cast(value, ref):
    if ref is None:
        return value

    if isinstance(ref, bool):
        return str(value).lower() == "true"

    try:
        return type(ref)(value)
    except Exception:
        return value


def compare(a, op, b):
    if op == "==":
        return a == b
    if op == "!=":
        return a != b
    if a is None:
        return False
    try:
        if op == ">":
            return a > b
        if op == "<":
            return a < b
        if op == ">=":
            return a >= b
        if op == "<=":
            return a <= b
    except TypeError:
        return False
    return False


# ----------------------------
# Tokenizer
# ----------------------------


def tokenize(s):
    tokens = []
    i = 0

    while i < len(s):
        if s[i].isspace():
            i += 1
            continue

        if s[i] in "()":
            tokens.append(s[i])
            i += 1
            continue

        matched = False
        for op in sorted(_ops, key=len, reverse=True):
            if s.startswith(op, i):
                tokens.append(op)
                i += len(op)
                matched = True
                break
        if matched:
            continue

        # and/or
        if s.startswith("and", i):
            tokens.append("and")
            i += 3
            continue
        if s.startswith("or", i):
            tokens.append("or")
            i += 2
            continue

        j = i
        while i < len(s) and s[i] not in " ()":
            # parar se encontrar operador
            if any(s.startswith(op, i) for op in _ops):
                break
            if s.startswith("and", i) or s.startswith("or", i):
                break
            i += 1

        tokens.append(s[j:i])

    return tokens


precedence = {"or": 1, "and": 2, "==": 3, "!=": 3, ">": 3, "<": 3, ">=": 3, "<=": 3}


def to_rpn(tokens):
    output = []
    stack = []

    for t in tokens:
        if t == "(":
            stack.append(t)

        elif t == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())

            if not stack:
                raise ValueError("Parênteses mal fechados")

            stack.pop()

        elif t in precedence:
            while (
                stack
                and stack[-1] in precedence
                and precedence[stack[-1]] >= precedence[t]
            ):
                output.append(stack.pop())

            stack.append(t)

        else:
            output.append(t)

    while stack:
        if stack[-1] == "(":
            raise ValueError("Parênteses mal fechados")

        output.append(stack.pop())

    return output


def rpn_to_ast(rpn):
    stack = []

    for t in rpn:
        if t in precedence:
            if len(stack) < 2:
                raise ValueError("Operador sem operandos suficientes")

            right = stack.pop()
            left = stack.pop()
            stack.append((t, left, right))
        else:
            if t == "":
                raise ValueError("Token vazio no filtro")

            stack.append(t)

    if len(stack) != 1:
        raise ValueError("Expressão de filtro inválida")

    return stack[0]

# ----------------------------
# Evaluator
# ----------------------------


def eval_ast(ast, data):

    if isinstance(ast, tuple) and ast[0] in ("and", "or"):
        op, left, right = ast

        left_res = eval_ast(left, data)
        right_res = eval_ast(right, data)

        if op == "and":
            return [e for e in left_res if e in right_res]

        if op == "or":
            return list({id(e): e for e in left_res + right_res}.values())

    if isinstance(ast, tuple):
        op, field, value = ast
        result = []

        for e in data:
            data_value = get_nested_value(e, field)
            if data_value is None:
                continue
            comp_value = cast(value, data_value)

            if compare(data_value, op, comp_value):
                result.append(e)

        return result

    return []


def parse_filter(filter_str, data):
    if filter_str is None or filter_str.strip() == "":
        return sorted(data, key=lambda p: p.get("packet_id", 0))


    try:
        tokens = tokenize(filter_str)
        rpn = to_rpn(tokens)
        ast = rpn_to_ast(rpn)

        result = eval_ast(ast, data)
        return sorted(result, key=lambda p: p.get("packet_id", 0))

    except Exception as e:
        print("Filtro inválido:", e)
        return sorted(data, key=lambda p: p.get("packet_id", 0))
