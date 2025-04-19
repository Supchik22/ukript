import ukr_numbers  # Поки не використовується
import sys

debug = False  # Увімкнути/вимкнути відладочний режим

chapters = {}
variables_memory = {}
last_variable = None
chapter_name = None
layer = 0

def debug_print(*args, **kwargs):
    if debug:
        print(*args, **kwargs)

def find_closest_variable(name, variables_memory):
    name = name.lower()
    if name in variables_memory:
        return name
    for key in variables_memory:
        if name in key.lower() or key.lower() in name:
            return key
    return None

def clean_variable_name(name):
    return name.lower().strip('",.')

def check_condition(condition):
    if len(condition) != 1:
        if condition[1] == "дорівнює":
            if variables_memory[find_closest_variable(condition[0], variables_memory)] == " ".join(condition[2:]):
                debug_print("умова істина")
                return True
            else:
                debug_print("умова не істина")
                return False
    else:
        cl_var = find_closest_variable(" ".join(condition).lower(), variables_memory)
        if cl_var is not None:
            if variables_memory[cl_var] == "ні":
                return False
            if variables_memory[cl_var] == "так":
                return True

def process_line(line, variables_memory, last_variable):
    line = line.strip()
    if not line:
        return last_variable

    if line.endswith("."):
        line = line[:-1]

    words = line.split()
    if len(words) == 0:
        return last_variable
    global layer
    global line_index

    if line.startswith("якщо"):
        if not check_condition(words[1:-1]):
            debug_print("додаєм шар")
            layer += 1
    elif line.startswith("ну і все"):
        if layer != 0:
            layer -= 1

    if layer != 0:
        return last_variable

    if words[0].lower() in ["петрик", "петя"]:
        action = words[1].lower()
        if action == "зробив":
            last_variable = handle_create_variable(words, variables_memory)
        elif action == "додав":
            handle_addition(words, variables_memory, last_variable)
        elif action == "відняв":
            handle_subtraction(words, variables_memory, last_variable)
        elif action == "помножив":
            handle_mult(words, variables_memory, last_variable)
        elif action == "поділив":
            handle_div(words, variables_memory, last_variable)
        elif action == "прочитав":
            handle_read_variable(variables_memory, last_variable)
        elif action in ["спитав", "пита"]:
            handle_input_variable(words, variables_memory)
        elif action in ["сказав", "каже"]:
            print(" ".join(words[2:]))
        elif action == "вспомнив":
            var_name = " ".join(words[2:])
            last_variable = find_closest_variable(var_name, variables_memory)

    elif words[0].lower() == "речення:":
        chapter_name = " ".join(words[1:]).lower()
        if chapter_name not in chapters:
            chapters[chapter_name] = line_index
    elif words[0].lower() == "повторити":
        debug_print(chapters)
        line_index = chapters[" ".join(words[1:]).lower()]

    return last_variable

def handle_mult(words, variables_memory, last_variable):
    if words[-2].lower().startswith("на"):
        var_name = last_variable
        resolved_var = find_closest_variable(var_name, variables_memory)
        if resolved_var is None:
            raise ValueError("Змінна не знайдена для множення.")
        num = ukr_numbers.parse_integer(words[2:-2])
        if num is None:
            var_name_to_mult = " ".join(words[2:-2])
            num = variables_memory[find_closest_variable(var_name_to_mult, variables_memory)]
        variables_memory[resolved_var] *= num
def handle_div(words, variables_memory, last_variable):
    if words[-2].lower().startswith("на"):
        var_name = last_variable
        resolved_var = find_closest_variable(var_name, variables_memory)
        if resolved_var is None:
            raise ValueError("Змінна не знайдена для ділення.")
        num = ukr_numbers.parse_integer(words[3:])
        
        if num is None:
            var_name_to_div = " ".join(words[3:])
            num = variables_memory[find_closest_variable(var_name_to_div, variables_memory)]
        variables_memory[resolved_var] /= num
    # приклад "петя поділив на два"

def handle_create_variable(words, variables_memory):
    var_name = clean_variable_name(words[2])
    variables_memory[var_name] = 0
    return var_name

def handle_addition(words, variables_memory, last_variable):
    if words[-2].lower().startswith("до"):
        var_name = last_variable
        resolved_var = find_closest_variable(var_name, variables_memory)
        if resolved_var is None:
            raise ValueError("Змінна не знайдена для додавання.")
        num = ukr_numbers.parse_integer(words[2:-2])
        if num is None:
            var_name_to_add = " ".join(words[2:-2])
            num = variables_memory[find_closest_variable(var_name_to_add, variables_memory)]
        variables_memory[resolved_var] += num

def handle_subtraction(words, variables_memory, last_variable):
    if words[-2].lower().startswith("з"):
        var_name = last_variable
        resolved_var = find_closest_variable(var_name, variables_memory)
        if resolved_var is None:
            raise ValueError("Змінна не знайдена для віднімання.")
        variables_memory[resolved_var] -= ukr_numbers.parse_integer(words[2:-2])

def handle_read_variable(variables_memory, last_variable):
    var_name = last_variable
    resolved_var = find_closest_variable(var_name, variables_memory)
    if resolved_var is None:
        raise ValueError("Змінна не знайдена для читання.")
    print(f"{resolved_var} це є {ukr_numbers.i_to_words(variables_memory[resolved_var])} ({variables_memory[resolved_var]})")

def handle_input_variable(words, variables_memory):
    result = input("Ваша відповідь: ")
    var_name = words[2:]
    var_name = " ".join(var_name).lower()
    var_name = clean_variable_name(var_name)
    variables_memory[var_name] = ukr_numbers.parse_integer(result.split())
    if variables_memory[var_name] is None:
        variables_memory[var_name] = result

line_index = 0

def interpret_code(code):
    global chapter_name
    global last_variable
    lines = code.splitlines()
    global line_index

    while line_index < len(lines):
        line = lines[line_index]
        last_variable = process_line(line, variables_memory, last_variable)
        line_index += 1

    return variables_memory

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("- Вкажи шлях до файлу як аргумент.")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        result = interpret_code(code)
    except FileNotFoundError:
        print(f"- Файл '{filepath}' не знайдено.")
