import ukr_numbers 
import sys
import time
import turtle
import math
import random
t = None

debug = False  # Увімкнути/вимкнути відладочний режим

# Словник ключових слів

keywords_default = {
    "pet_names": ["петрик", "петя","черепаха"],
    "actions": {
        "create": "зробив",
        "add": "додав",
        "subtract": "відняв",
        "multiply": "помножив",
        "cos": "косинус",
        "sin": "синус",
        "tan": "тангенс",
        


        "divide": "поділив",
        "read": "прочитав",
        "ask": ["спитав", "пита"],
        "say": ["сказав", "каже"],
        "sleep": "заснув",
        "remember": "вспомнив",
        "draw": "малює",
        "down": "опустив",
        "forward": "вперед",
        "backward": "назад",
        "left": "вліво",
        "right": "вправо",
        "end_draw": "закінчив",
        "up": "підняв",
        "assign": "переписав",
        "center": "центр",
        "speed": "швидкість",
        
    },
    "prepositions": {
        "to": ["до", "в"],
        "from": "з",
        "on": "на"
    },
    "condition_start": "якщо",
    "condition_end": "ну і все",
    "chapter_marker": "речення:",
    "repeat": "повторити",
    "condition_words": {
        "not": "не",
        "equals": "дорівнює",
        "greater": "більше",
        "less": "менше"
    },
    "boolean": {
        "yes": "так",
        "no": "ні"
    },
    "time_units": {
        "seconds": ["секунд", "секунди", "секунда", "секунду"],
        "minutes": ["хвилин", "хвилину", "хвилиночок"],
        "hours": ["годин", "години", "годину"]
    }
}
keywords_mcpetya = {
    "pet_names": ["мспетрик", "мспетя", "черепаха","тіп"],
    "actions": {
        "create": "напотужнічав",
        "add": "накидав",
        "subtract": "змінусив",
        "multiply": "захардкорив",
        "cos": "косанув",
        "sin": "сінанув",
        "tan": "танканув",
        "divide": "розшарив",
        "read": "зачитав",
        "ask": ["запитав", "спитав"],
        "say": ["влепив", "відкинув"],
        "sleep": "зашкварився",
        "remember": "згадав",
        "draw": "намалював",
        "down": "опустив",
        "forward": "погнав",
        "backward": "відкотівся",
        "left": "наліво",
        "right": "направо",
        "end_draw": "закінчив",
        "up": "підняв",
        "assign": "записав",
        "center": "вцентрячив",
        "speed": "форсанув"
    },
    "prepositions": {
        "to": ["в", "до"],
        "from": "із",
        "on": "на"
    },
    "condition_start": "базовано",
    "condition_end": "опа чіназес",
    "chapter_marker": "рофл:",
    "repeat": "флексити",
    "condition_words": {
        "not": "нє",
        "equals": "саме",
        "greater": "більше",
        "less": "менше"
    },
    "boolean": {
        "yes": "ага",
        "no": "нєа"
    },
    "time_units": {
        "seconds": ["сек", "сєкунд", "сєкунду"],
        "minutes": ["хв", "хвилинку", "хвильку"],
        "hours": ["год", "годинку", "годин"]
    }
}


keywords = keywords_default

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
        if condition[1] == keywords["condition_words"]["not"]:
            if variables_memory[find_closest_variable(condition[0], variables_memory)] != " ".join(condition[2:]):
                debug_print("умова істина")
                return True
            else:
                debug_print("умова не істина")
                return False
        elif condition[1] == keywords["condition_words"]["equals"]:
            if variables_memory[find_closest_variable(condition[0], variables_memory)] == " ".join(condition[2:]):
                debug_print("умова істина")
                return True
            else:
                debug_print("умова не істина")
                return False
        elif condition[1] == keywords["condition_words"]["greater"]:
            if variables_memory[find_closest_variable(condition[0], variables_memory)] > ukr_numbers.parse_number(" ".join(condition[2:])):
                debug_print("умова істина")
                return True
            else:
                debug_print("умова не істина")
                return False
        elif condition[1] == keywords["condition_words"]["less"]:
            if variables_memory[find_closest_variable(condition[0], variables_memory)] < ukr_numbers.parse_number(" ".join(condition[2:])):
                debug_print("умова істина")
                return True
            else:
                debug_print("умова не істина")
                return False
    else:
        cl_var = find_closest_variable(" ".join(condition).lower(), variables_memory)
        if cl_var is not None:
            if variables_memory[cl_var] == keywords["boolean"]["no"]:
                return False
            if variables_memory[cl_var] == keywords["boolean"]["yes"]:
                return True

def handle_sleep(words):
    time_unit = words[-1].lower()
    time_value = ukr_numbers.parse_number(" ".join(words[3:-1]))
    
    if time_unit in keywords["time_units"]["seconds"]:
        time.sleep(time_value)
    elif time_unit in keywords["time_units"]["minutes"]:
        time.sleep(time_value * 60)
    elif time_unit in keywords["time_units"]["hours"]:
        time.sleep(time_value * 3600)
def check_turtle_exists():
    global t
    if t is None:
        t = turtle.Turtle()
        print('нова черепашка')
    else: print('черепашка вже існує')
    
def parse_number(words):
    result = ukr_numbers.parse_number(" ".join(words))

    if result is None:
        result = variables_memory[find_closest_variable(" ".join(words), variables_memory)]
    return result


def handle_draw(words):
    global t
    words = words[2:]
    print('хтось малює: ', words[0].lower())
    if words[0].lower() == keywords["actions"]["down"]:
        check_turtle_exists()
        t.pendown()
    elif words[0].lower() == keywords["actions"]["up"]:
        check_turtle_exists()
        t.penup()
    elif words[0].lower() == keywords["actions"]["forward"]:
        check_turtle_exists()
        distance = parse_number(words[2:-1])
        t.forward(distance)
        
        # Приклад виклику функції
        # Петрик малює вперед сто
    elif words[0].lower() == keywords["actions"]["backward"]:
        check_turtle_exists()
        distance = parse_number(words[2:-1])
        t.backward(distance)
    elif words[0].lower() == keywords["actions"]["left"]:
        check_turtle_exists()
        angle = parse_number(words[2:-1])
        t.left(angle)
    elif words[0].lower() == keywords["actions"]["right"]:
        check_turtle_exists()
        angle = parse_number(words[2:-1])
        t.right(angle)
    elif words[0].lower() == keywords["actions"]["end_draw"]:
        if t is not None:
            t.screen.mainloop()
    elif words[0].lower() == keywords["prepositions"]["to"][0]:
        print("додому!?")
        if words[1].lower() == keywords["actions"]["center"]:
            check_turtle_exists()
            print("додому!")
            t.home()
    elif words[0].lower() == keywords["actions"]["speed"]:
        check_turtle_exists()
        speed = parse_number(words[2:])
        t.speed(speed)
def handle_assign(words, variables_memory):
    #variables_memory[words[2].lower()] = variables_memory[find_closest_variable(" ".join(words[3:]), variables_memory)]
    pass
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

    if line.startswith(keywords["condition_start"]):
        if not check_condition(words[1:-1]):
            debug_print("додаєм шар")
            layer += 1
    elif line.startswith(keywords["condition_end"]):
        if layer != 0:
            layer -= 1

    if layer != 0:
        return last_variable

    if words[0].lower() in keywords["pet_names"]:
        action = words[1].lower()

        action_map = {
            keywords["actions"]["create"]: lambda: handle_create_variable(words, variables_memory),
            keywords["actions"]["add"]: lambda: handle_addition(words, variables_memory, last_variable),
            keywords["actions"]["subtract"]: lambda: handle_subtraction(words, variables_memory, last_variable),
            keywords["actions"]["multiply"]: lambda: handle_mult(words, variables_memory, last_variable),
            keywords["actions"]["divide"]: lambda: handle_div(words, variables_memory, last_variable),
            keywords["actions"]["read"]: lambda: handle_read_variable(variables_memory, last_variable),
            keywords["actions"]["ask"][0]: lambda: handle_input_variable(words, variables_memory),
            keywords["actions"]["ask"][1]: lambda: handle_input_variable(words, variables_memory),
            keywords["actions"]["say"][0]: lambda: print(" ".join(words[2:])),
            keywords["actions"]["sleep"]: lambda: handle_sleep(words),
            keywords["actions"]["draw"]: lambda: handle_draw(words),
            keywords["actions"]["say"][1]: lambda: print(" ".join(words[2:])),
            keywords["actions"]["remember"]: lambda: find_closest_variable(" ".join(words[2:]), variables_memory),
            keywords["actions"]["assign"]: lambda: handle_assign(words, variables_memory),
            keywords["actions"]["cos"]: lambda: handle_cosine(words, variables_memory, last_variable),
            keywords["actions"]["sin"]: lambda: handle_sine(words, variables_memory, last_variable),
            keywords["actions"]["tan"]: lambda: handle_tangent(words, variables_memory, last_variable),
        }

        if action in action_map:
            result = action_map[action]()
            if action == keywords["actions"]["create"]:
                last_variable = result
            elif action == keywords["actions"]["remember"]:
                last_variable = result

    elif words[0].lower() == keywords["chapter_marker"]:
        chapter_name = " ".join(words[1:]).lower()
        if chapter_name not in chapters:
            chapters[chapter_name] = line_index
    elif words[0].lower() == keywords["repeat"]:
        debug_print(chapters)
        line_index = chapters[" ".join(words[1:]).lower()]

    return last_variable

def handle_mult(words, variables_memory, last_variable):
    if words[-2].lower() in keywords["prepositions"]["on"]:
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
    if words[-2].lower() in keywords["prepositions"]["on"]:
        var_name = last_variable
        resolved_var = find_closest_variable(var_name, variables_memory)
        if resolved_var is None:
            raise ValueError("Змінна не знайдена для ділення.")
        num = ukr_numbers.parse_integer(words[3:])
        
        if num is None:
            var_name_to_div = " ".join(words[3:])
            num = variables_memory[find_closest_variable(var_name_to_div, variables_memory)]
        variables_memory[resolved_var] /= num

def handle_create_variable(words, variables_memory):
    var_name = clean_variable_name(words[2])
    variables_memory[var_name] = 0
    return var_name

def handle_addition(words, variables_memory, last_variable):
    if words[-2].lower() in keywords["prepositions"]["to"]:
        var_name = last_variable
        resolved_var = find_closest_variable(var_name, variables_memory)
        if resolved_var is None:
            raise ValueError("Змінна не знайдена для додавання.")
        num = ukr_numbers.parse_integer(words[2:-2])
        if num is None:
            var_name_to_add = " ".join(words[2:-2])
            num = variables_memory[find_closest_variable(var_name_to_add, variables_memory)]
        variables_memory[resolved_var] += num

def handle_cosine(words, variables_memory, last_variable):
    if words[-2].lower() in keywords["prepositions"]["on"]:
        var_name = last_variable
        resolved_var = find_closest_variable(var_name, variables_memory)
        if resolved_var is None:
            raise ValueError("Змінна не знайдена для косинуса.")
        angle = ukr_numbers.parse_integer(words[2:-2])
        if angle is None:
            var_name_to_cos = " ".join(words[2:-2])
            angle = variables_memory[find_closest_variable(var_name_to_cos, variables_memory)]
        variables_memory[resolved_var] = math.cos(math.radians(angle))
def handle_sine(words, variables_memory, last_variable):
    if words[-2].lower() in keywords["prepositions"]["on"]:
        var_name = last_variable
        resolved_var = find_closest_variable(var_name, variables_memory)
        if resolved_var is None:
            raise ValueError("Змінна не знайдена для синуса.")
        angle = ukr_numbers.parse_integer(words[2:-2])
        if angle is None:
            var_name_to_sin = " ".join(words[2:-2])
            angle = variables_memory[find_closest_variable(var_name_to_sin, variables_memory)]
        variables_memory[resolved_var] = math.sin(math.radians(angle))
def handle_tangent(words, variables_memory, last_variable):
    if words[-2].lower() in keywords["prepositions"]["on"]:
        var_name = last_variable
        resolved_var = find_closest_variable(var_name, variables_memory)
        if resolved_var is None:
            raise ValueError("Змінна не знайдена для тангенса.")
        angle = ukr_numbers.parse_integer(words[2:-2])
        if angle is None:
            var_name_to_tan = " ".join(words[2:-2])
            angle = variables_memory[find_closest_variable(var_name_to_tan, variables_memory)]
        variables_memory[resolved_var] = math.tan(math.radians(angle))
    # Приклад використання:
    # handle_tangent(["петя", "тангенс", "на", "45"], variables_memory, last_variable)
    


def handle_subtraction(words, variables_memory, last_variable):
    if words[-2].lower() in keywords["prepositions"]["from"]:
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
        if filepath.endswith('.мспетрик'):
            keywords = keywords_mcpetya
        result = interpret_code(code)
    except FileNotFoundError:
        print(f"- Файл '{filepath}' не знайдено.")
