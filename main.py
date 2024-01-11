def is_well_formed(proposition):
    bracket_level = 0
    for char in proposition:
        bracket_level += 1 if char == "(" else -1 if char == ")" and bracket_level > 0 else 0
        if bracket_level < 0:
            return False
    return bracket_level == 0

def parse_proposition(p, truth_values):
    p = p.replace(" ", "")

    if not is_well_formed(p):
        return "Error"

    while p[0] == "(" and p[-1] == ")" and is_well_formed(p[1:len(p) - 1]):
        p = p[1:len(p) - 1]

    if len(p) == 1:
        return truth_values[p]

    operators = {"→": lambda x, y: (not x) or y,
                 "↔": lambda x, y: x == y,
                 "∨": lambda x, y: x or y,
                 "∧": lambda x, y: x and y,
                 "¬": lambda x: not x}

    for operator in operators.keys():
        bracket_level = 0
        for i in reversed(range(len(p))):
            if p[i] == "(":
                bracket_level += 1
            elif p[i] == ")":
                bracket_level -= 1
            if p[i] == operator and bracket_level == 0:
                if operator == "¬":
                    return operators[operator](parse_proposition(p[i + 1:], truth_values))
                else:
                    return operators[operator](parse_proposition(p[0:i], truth_values),
                                               parse_proposition(p[i + 1:], truth_values))

def write_truth_table(proposition):
    truth_values = {char: False for char in proposition if char.isalpha()}

    for statement in truth_values.keys():
        print(statement, end="  |  ")
    print(proposition)

    for _ in range(2**len(truth_values)):
        for truth_value in truth_values.values():
            print("T" if truth_value else "F", end="  |  ")
        print("T" if parse_proposition(proposition, truth_values) else "F")

        for variable in reversed(list(truth_values.keys())):
            truth_values[variable] = not truth_values[variable]
            if truth_values[variable]:
                break

def main():
    proposition1 = "¬(P∨(¬P∧Q))"
    proposition2 = "¬P∧¬Q"
    print()
    print(f'Truth table for proposition 1: {proposition1}\n')
    write_truth_table(proposition1)
    print()
    print(f'Truth table for proposition 2: {proposition2}\n')
    write_truth_table(proposition2)

    if are_truth_tables_equivalent(proposition1, proposition2):
        print("\nThe propositions are equivalent.")
    else:
        print("\nThe propositions are not equivalent.")

def are_truth_tables_equivalent(proposition1, proposition2):
    variables1 = set(char for char in proposition1 if char.isalpha())
    variables2 = set(char for char in proposition2 if char.isalpha())

    if variables1 != variables2:
        return False

    truth_values = {char: False for char in variables1}

    first_iteration = True
    for _ in range(2**len(truth_values)):
        if not first_iteration:
            value1 = parse_proposition(proposition1, truth_values)
            value2 = parse_proposition(proposition2, truth_values)

            if bool(value1) != bool(value2):
                return False

        first_iteration = False

        for variable in reversed(list(truth_values.keys())):
            truth_values[variable] = not truth_values[variable]
            if truth_values[variable]:
                break

    return True


if __name__ == "__main__":
    main()
