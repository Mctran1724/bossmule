import PySimpleGUI as sg
from bossing_mule import Bosser

# GUI Definition
remaining_crystals = 180
boss_mules = set()


def add_remove_bosser(name: str, job: str, level: int, add: bool) -> None:
    bosser = Bosser(name, job, level)
    if add:
        try:
            boss_mules.add(bosser)
            sg.popup_no_titlebar(f"Added {name}")
        except Exception as e:
            print(e)
            sg.popup_no_titlebar(f'Level {level} {job} {name} already exists.')
    else:
        try:
            boss_mules.remove(bosser)
            sg.popup_no_titlebar(f"Removed {name}")
        except Exception as e:
            print(e)
            sg.popup_no_titlebar(f"Level {level} {job} {name} does not already exist.")


def display_bossers(sortby = 'level'):
    boss_mule_list = list(boss_mules)
    #add functionality to the sorting later
    sortkeys = {
        'level': lambda x: x.level,
        'mesos': lambda x: x.total_meso,
        'time': lambda x: x.clear_time
    }

    boss_mule_list.sort(key=sortkeys[sortby])

    #make this a dataframe or table after
    text = ""
    for bosser in boss_mule_list:
        s = f"Level {bosser.level} {bosser.job} {bosser.name} | {bosser.total_meso} | {bosser.clear_time} \n"
        text += s 

    sg.popup_scrolled(text)

layout = [
    [sg.Text("Boss Mules Here")],
    [sg.Text("Character Name: "), sg.Input(key='add_char_name'), sg.Text("Level: "), sg.Input(key='add_level'), sg.Button("Add")],
    [sg.Text("Character Name: "), sg.Input(key='remove_char_name'), sg.Text("Level: "), sg.Input(key='remove_level'), sg.Button("Remove")],
    [sg.Button("Calculate"), sg.Button("Display Bossers")]
]

window = sg.Window("Boss Mule Tracker", layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    elif event == "Add":
        bosser_name = values['add_char_name']
        bosser_class = "Class name implemented later"
        bosser_level = values['add_level']
        add_remove_bosser(bosser_name, bosser_class, bosser_level, add=True)
        
    elif event == "Remove":
        bosser_name = values['remove_char_name']
        bosser_class = "Class name implemented later"
        bosser_level = values['remove_level']
        add_remove_bosser(bosser_name, bosser_class, bosser_level, add=False)

    elif event == 'Display Bossers':
        display_bossers()

window.close()

print(boss_mules)