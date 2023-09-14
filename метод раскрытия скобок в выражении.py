import re


def simplify(expr):
    """
    Применяет правила раскрытия скобок к выражению expr, пока возможно.
    """
    while "(" in expr:
        # Находим самую внутреннюю скобку
        start = expr.rindex("(")
        end = start + expr[start:].index(")") + 1

        # Вычисляем выражение внутри скобок
        subexpr = expr[start+1:end-1]
        value = evaluate(subexpr)

        # Заменяем скобки на значение
        expr = expr[:start] + str(value) + expr[end:]

    return expr

def evaluate(expr):
    """
    Вычисляет значение выражения expr, которое не содержит скобок.
    """
    # Сначала обрабатываем все умножения и деления
    while "*" in expr or "/" in expr:
        tokens = re.findall(r"\d+|\S", expr)
        for i in range(len(tokens)):
            if tokens[i] == "*":
                a = int(tokens[i-1])
                b = int(tokens[i+1])
                tokens[i-1:i+2] = [str(a * b)]
                break
            elif tokens[i] == "/":
                a = int(tokens[i-1])
                b = int(tokens[i+1])
                tokens[i-1:i+2] = [str(a / b)]
                break
        expr = "".join(tokens)

    # Затем обрабатываем все сложения и вычитания
    while "+" in expr or "-" in expr:
        tokens = re.findall(r"\d+|\S", expr)
        for i in range(len(tokens)):
            if tokens[i] == "+":
                a = int(tokens[i-1])
                b = int(tokens[i+1])
                tokens[i-1:i+2] = [str(a + b)]
                break
            elif tokens[i] == "-":
                a = int(tokens[i-1])
                b = int(tokens[i+1])
                tokens[i-1:i+2] = [str(a - b)]
                break
        expr = "".join(tokens)

    return int(expr)



print(simplify("((7 - 4) * (5 + 6)) / (2 + 3)"))
print(simplify("(2 + 3)"))