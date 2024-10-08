import configparser
import os
import sys

def read_bytes_from_file(filepath, offset, len_of_bytes=2):
    # open the file
    with open(filepath, 'rb') as f:
        # read the bytes at offset, from beginning of file.
        f.seek(offset)
        file_bytes = f.read(len_of_bytes)

    if file_bytes[-1:].decode() == "<" or file_bytes[-1:].decode() == ".":
        file_bytes = file_bytes[:-1]

    # return the bytes
    return file_bytes

def write_bytes_to_file(filepath, offset, bytes_to_write):
    # open the file
    with open(filepath, 'r+b') as f:
        # write the bytes at the offset, from the beginning of file
        f.seek(offset)
        f.write(bytes(bytes_to_write, 'utf-8'))
    
    return True

def replace_bytes_at_offset(filepath, offset, new_bytes):
    # get rest of file starting from our offset
    with open(filepath, 'rb') as f:
        f.seek(offset)
        content = f.read()

    num_bytes_to_replace = 3
    temp_bytes = content[:num_bytes_to_replace]

    # check that we aren't overwriting any bytes we don't want to
    if temp_bytes[-1:].decode() == "<" or temp_bytes[-1:].decode() == ".":
        num_bytes_to_replace -= 1

    new_content = content[num_bytes_to_replace:]
    new_content = new_bytes.encode() + new_content

    # write changes to file
    with open(filepath, 'r+b') as f:
        f.seek(offset)
        f.write(new_content)
        f.truncate()

    return True

def add_bytes_at_offset(filepath, offset, new_bytes):
    with open(filepath, 'rb') as f:
        f.seek(offset + 1)
        content = f.read()

    new_content = new_bytes + content

    with open(filepath, 'r+b') as f:
        f.seek(offset + 1)
        f.write(new_content)
        f.truncate()

    return True

def remove_number_of_bytes_at_offset(filepath, offset, num_to_remove=1, byte_check=None):
    with open(filepath, 'rb') as f:
        f.seek(offset)
        content = f.read()

    # check the content at the bytes is what we think it is [optional]
    if byte_check != None and content[:1] != byte_check:
        return False

    new_content = content[num_to_remove:]

    with open(filepath, 'r+b') as f:
        f.seek(offset)
        f.write(new_content)
        f.truncate()

    return True

def set_byte_status(filepath, offset, new_bytes):
    old_bytes = read_bytes_from_file(filepath, offset, 3)

    if old_bytes[-1:].decode() == "<":
        old_bytes = old_bytes[:-1]

    old_bytes_len = len(old_bytes)
    new_bytes_len = len(new_bytes)

    if new_bytes_len > old_bytes_len:
        return 1
    elif new_bytes_len < old_bytes_len:
        return 2
    else:
        return 0

def handle_byte_status(filepath, offset, byte_status):
    if byte_status == 1:
        return remove_number_of_bytes_at_offset(filepath, offset - 16, 1, b'\r')
    elif byte_status == 2:
        return add_bytes_at_offset(filepath, offset - 16, b'\r')
    else:
        return True

def calculate_correct_offset(filepath, offset):
    old_bytes = read_bytes_from_file(filepath, offset - 1, 3)

    if old_bytes[:1].decode() == ">":
        return offset
    else:
        return offset - 1

def set_command_handler(filepath, options, commands_help, choice):
    choice_args = choice.split(" ")

    # not enough / too many args.
    if len(choice_args) < 3:
        print("Not enough args.", commands_help['set']['usage'])
        return False
    elif len(choice_args) > 3:
        print("Too many args.", commands_help['set']['usage'])
        return False

    # empty values error handling
    if choice_args[1] == "":
        print("Category number is empty.", commands_help['set']['usage'])
        return False
    elif choice_args[2] == "":
        print("New FOV Value is empty.", commands_help['set']['usage'])
        return False

    # check both values are int
    try:
        int(choice_args[1])
        int(choice_args[2])
    except ValueError as e:
        non_int_value = str(e).replace('invalid literal for int() with base 10: ', '')
        print("Expected a whole number, got", non_int_value)
        return False

    # check if the category number, is valid.
    if int(choice_args[1]) > len(options.keys()) - 1:
        print("The category number", choice_args[1], "is out of range.")
        print("Value should be", len(options.keys()) - 1, "or less")
        return False
    
    # force the new fov value to be within the range, if needed.
    if int(choice_args[2]) > 999:
        choice_args[2] = "180"
        print("Warning: The value", choice_args[2], "is greater than 999! Setting it to 180...")
    elif int(choice_args[2]) < 1:
        choice_args[2] = "01"
        print("Warning: The value", choice_args[2], "is less than 1 Setting it to 1...")
    elif int(choice_args[2]) > 180:
        print("Warning: The value", choice_args[2], "is greater than 180\nGoing above 180 causes the FOV to flip or freak out, which can cause some people to feel motion sick, please do this at your own risk.")

    if int(choice_args[2]) < 10 and int(choice_args) != 1:
        choice_args[2] = f"0{choice_args[2]}"
    
    if choice_args[2].isnumeric():
        choice_args[2] = str(choice_args[2])

    key = list(options.keys())[int(choice_args[1])]

    # handle byte addition/removal
    offset = calculate_correct_offset(filepath, options[key]['offset'])
    byte_status = set_byte_status(filepath, offset, choice_args[2])
    
    # write new value to file
    replace_bytes_at_offset(filepath, offset, choice_args[2])

    handle_byte_status(filepath, offset, byte_status)

    print("Sucessfully set", key, "to", choice_args[2])
    return True
    
def get_command_handler(filepath, options, commands_help, choice):
    choice_args = choice.split(" ")

    # not enough / too many args.
    if len(choice_args) < 2:
        print("Not enough args.", commands_help['get']['usage'])
        return False
    elif len(choice_args) > 2:
        print("Too many args.", commands_help['get']['usage'])
        return False
    
    # check if the value is an int
    try:
        int(choice_args[1])
    except ValueError as e:
        non_int_value = str(e).replace('invalid literal for int() with base 10: ', '')
        print("Expected a whole number, got", non_int_value)
        return False

    # check if the category number, is valid.
    if int(choice_args[1]) > len(options.keys()) - 1:
        print("The category number", choice_args[1], "is out of range.")
        print("Value should be", len(options.keys()) - 1, "or less")
        return False

    # empty values error handling
    if choice_args[1] == "":
        print("Category number is empty.", commands_help['set']['usage'])
        return False
    
    key = list(options.keys())[int(choice_args[1])]
    offset = calculate_correct_offset(filepath, options[key]['offset'])
    our_bytes = read_bytes_from_file(filepath, offset, 3)
    print(key, "value is", our_bytes.decode('utf-8'))
    return True

def info_command_handler(filepath, options, commands_help, choice):
    choice_args = choice.split(" ")

    # not enough / too many args.
    if len(choice_args) < 2:
        print("Not enough args.", commands_help['info']['usage'])
        return False
    elif len(choice_args) > 2:
        print("Too many args.", commands_help['info']['usage'])
        return False
    
    # check if the value is an int
    try:
        int(choice_args[1])
    except ValueError as e:
        non_int_value = str(e).replace('invalid literal for int() with base 10: ', '')
        print("Expected a whole number, got", non_int_value)
        return False

    # check if the category number, is valid.
    if int(choice_args[1]) > len(options.keys()) - 1:
        print("The category number", choice_args[1], "is out of range.")
        print("Value should be", len(options.keys()) - 1, "or less")
        return False

    # empty values error handling
    if choice_args[1] == "":
        print("Category number is empty.", commands_help['set']['usage'])
        return False
    
    key = list(options.keys())[int(choice_args[1])]
    print(key, options[key]['description'], sep=" --> ")
    return True

def reset_command_handler(filepath, options, commands_help):
    for i, key in enumerate(options.keys()):
        set_command_handler(filepath, options, commands_help, f"set {i} {options[key]['default_value']}")

    print("Successfully reset all FOV values to their default!")
    return True

def gset_command_handler(filepath, options, commands_help, choice):
    choice_args = choice.split(" ")

    # not enough / too many args.
    if len(choice_args) < 2:
        print("Not enough args.", commands_help['info']['usage'])
        return False
    elif len(choice_args) > 2:
        print("Too many args.", commands_help['info']['usage'])
        return False
    
    # check if the value is an int
    try:
        float(choice_args[1])
    except ValueError as e:
        non_int_value = str(e).replace('invalid literal for int() with base 10: ', '')
        print("Expected a floating point number, got", non_int_value)
        return False

    # empty values error handling
    if choice_args[1] == "":
        print("Category number is empty.", commands_help['set']['usage'])
        return False

    # calculate and set fov multiplier
    for i, key in enumerate(options.keys()):
        default_value = int(options[key]['default_value'])
        fov_value_int = round(default_value * float(choice_args[1]))
        
        set_command_handler(filepath, options, commands_help, f"set {i} {fov_value_int}")
        
    print("Sucessfully modified all values!")
    return True

def load_command_handler(filepath, options, commands_help):
    '''Load FOV values from a SR2Fov.ini file'''
    config = configparser.ConfigParser()

    # check file exsists
    read_value = config.read('SR2Fov.ini')

    if len(read_value) == 0:
        print("'SR2Fov.ini' file not found!")
        return False

    # handle error if 'FOV' section doesn't exsist.
    try:
        fov = config['FOV']
    except KeyError as e:
        print("'SR2Fov.ini' does not have the section", str(e))
        return False

    # fill key list
    keys = []
    for key in options.keys():
        keys.append(key.replace(' ', '').lower())

    # set all the values
    for key in fov:
        if not key in keys:
            continue

        category_number = keys.index(key)
        set_command_handler(filepath, options, commands_help, f"set {category_number} {fov[key]}")

    print("Loaded all values from 'SR2Fov.ini'")

def get_file_path():
    '''Try to load the filepath from config file, if that fails ask the user'''
    folder_path_seperator = "/"

    if sys.platform == "windows":
        folder_path_seperator = "\\"

    config = configparser.ConfigParser()

    # check file exsists
    read_value = config.read('SR2Fov.ini')

    if len(read_value) > 0:
        filepath = config['PATH']['gamedirectory'].replace('"', '')

        if filepath [-1:] == folder_path_seperator:
            filepath = filepath[:-1]

        if os.path.exists(f"{filepath}{folder_path_seperator}common.vpp_pc"):
            return f"{filepath}{folder_path_seperator}common.vpp_pc"
        else:
            print(f"'{filepath}{folder_path_seperator}common.vpp_pc' is invalid")

    print("Couldn't get filepath from 'SR2Fov.ini' file")

    should_exit = False

    while not should_exit:
        choice = input("Please enter the full path to your Saints Row 2 game folder: ")

        if choice[-1:] == folder_path_seperator:
            choice = choice[:-1]


        if not os.path.exists(f"{choice}{folder_path_seperator}common.vpp_pc"):
            print("The path is invalid, please try again.")
        else:
            should_exit = True

    return f"{choice}{folder_path_seperator}common.vpp_pc"

def main_menu(filepath):
    options = {'General FOV':{'description':"This is your FOV while moving normally on foot.", 'offset':10313098, 'default_value':"58"},
               'Sprinting FOV':{'description':"This is your FOV while spriting.", 'offset':10313559, 'default_value':"56"},
               'Interior FOV':{'description':"This is your FOV while inside a room or building.", 'offset':10314055, 'default_value':"50"},
               'Interior Sprint FOV':{'description':"This is your FOV when sprinting while inside a room or building.", 'offset':10314055, 'default_value':"48"},
               'Fine Aim FOV':{'description':"This is your FOV while fine aiming.", 'offset':10314967, 'default_value':"40"},
               'Human Shield FOV':{'description':"This is your FOV while holding a human shield.", 'offset':10317342, 'default_value':"50"},
               'Vehicle Passenger FOV':{'description':"This is your FOV as a while in a vehicle as a passenger.", 'offset':10319224, 'offset2':10319736, 'default_value':"50"},
               'Land Vehicle FOV':{'description':"This is your FOV while driving a land-based vehicle.", 'offset':10318272, 'offset2':10318780, 'default_value':"50"},
               'Boat Vehicle FOV':{'description':"This is your FOV while driving a water-based vehicle.", 'offset':10320183, 'default_value':"60"},
               'Helicopter FOV':{'description':"This is your FOV while driving a helicopter.", 'offset':10320658, 'default_value':"60"},
               'Airplane FOV':{'description':"This is your FOV while driving an airplane.", 'offset':10321129, 'default_value':"60"},
               'Swimming FOV':{'description':"This is your FOV while swimming.", 'offset':10323000, 'default_value':"50"},
               'Climbing FOV':{'description':"This is your FOV while climbing over an object, like a fence.", 'offset':10323925, 'default_value':"50"},
               'Ragdoll FOV':{'description':"This is your FOV while in ragdoll form.", 'offset':10324387, 'default_value':"50"},
               'Falling FOV':{'description':"This is your FOV while falling, without a parachute", 'offset':10324847, 'default_value':"65"},
               'Freefall FOV':{'description':"This is your FOV while falling when wearing a parachute", 'offset':10325308, 'default_value':"75"},
               'Parachute FOV':{'description':"This is your FOV while gliding with a parachute", 'offset':10325770, 'default_value':"90"},
               'Fireworks Truck FOV':{'description':"This is your FOV while in the back of the fireworks truck in the mission \"Thank You and Goodnight!\", it is not used for anything else.", 'offset':10330527, 'default_value':"40"}}

    commands_help = {'help':{'description':"Show this message", 'usage':"help"},
                     'info':{'description':"Show a brief message about a category", 'usage':"info [category_number]"},
                     'get':{'description':"Get the FOV value for a category", 'usage':"get [category_number]"},
                     'set':{'description':"Set the FOV for a category", 'usage':"set [category_number] [new_fov_value]"},
                     'gset':{'description':"Globally set all FOV values based on a multiplier.", 'usage':"gset [float_multiplier]"},
                     'reset':{'description':"Set all FOV categories back to their default values.", 'usage':"reset"},
                     'load':{'description':"Load FOV values from the 'SR2Fov.ini' file\nNote: The SR2Fov.ini file must be in the same directory as the script.", 'usage':"load"}}

    should_exit = False
    should_refresh = True
    
    # main menu loop
    while not should_exit:
        
        if should_refresh:
            for i, option in enumerate(options.keys()):
                print(str(i) + ".", option)
            should_refresh = False

        choice = input("\nPlease type a command or 'help' if you need a list of commands: ")


        # handle commands
        if choice.lower().startswith("set"):
            set_command_handler(filepath, options, commands_help, choice)
        elif choice.lower().startswith("get"):
            get_command_handler(filepath, options, commands_help, choice) 
        elif choice.lower().startswith("gset"):
            gset_command_handler(filepath, options, commands_help, choice)
        elif choice.lower().startswith("load"):
            load_command_handler(filepath, options, commands_help)
        elif choice.lower().startswith("info"):
            info_command_handler(filepath, options, commands_help, choice)
        elif choice.lower() == "reset":
            reset_command_handler(filepath, options, commands_help)
        elif choice.lower() == "help":
            for command in commands_help.keys():
                print(command)
                print("     description:", commands_help[command]['description'])
                print("     usage:", commands_help[command]['usage'], "\n")
            continue
        elif choice.lower() == "quit" or choice.lower() == "exit":
            quit()
        else:
            print("Invalid command", f"'{choice.split(" ")[0]}'", ". try 'help' if you're stuck.")

if __name__ == "__main__":
    filepath = get_file_path()
    main_menu(filepath) 
