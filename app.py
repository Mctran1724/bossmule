import PySimpleGUI as sg
from bossing_mule import Bosser


## TODO: 
## Dynamically updating UI elements for each bosser (https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Layout_Add_and_Delete_Rows.py),
##  and the calculations and functionality to add boss crystals. Each bosser should bring up a window where you can add those.
## https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Layout_Add_and_Delete_Rows.py
#Settings
sg.theme("BluePurple")

# GUI Definition
remaining_crystals = 180
boss_mules = set()


def adding_window():
    print("Adding Window Opening")
    layout = [
        [sg.T("Character Name: "), sg.In(key='add_char_name'), sg.T("Level: "), sg.In(key='add_level'), sg.B("Add")]
    ]

    window = sg.Window("Add Boss Mule", layout, modal=True)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "Add":
            bosser_name = values['add_char_name']
            bosser_class = "Class name implemented later"
            bosser_level = values['add_level']
            add_remove_bosser(bosser_name, bosser_class, bosser_level, add=True)
    
    window.close()

def add_remove_bosser(name: str, job: str, level: int, index: int, add: bool) -> None:
    bosser = Bosser(name, job, level, index)
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


def display_bossers(sortby: str = 'level'):
    boss_mule_list = list(boss_mules)

    #add functionality to the sorting later
    sortkeys = {
        'level': lambda x: x.level,
        'mesos': lambda x: x.total_meso,
        'time': lambda x: x.clear_time
    }

    boss_mule_list.sort(key=sortkeys[sortby])

    rows = []


    for bosser in boss_mule_list:
        #add a row add a row bit by bit for item in the boss mules list
        window[('-BOSSER_ROW-', event[i])].update(visible=False)
    


def bosser_row(bosser, item_index: int):
    #Later add clear time and align the string lengths
    bosser_text = f'{bosser.name}: Level {bosser.level} {bosser.job} | {bosser.total_meso} mesos | {bosser.clear_time} minutes'
    row =  [sg.pin(sg.Col([[sg.B(sg.SYMBOL_X_SMALL, border_width=0, button_color=(sg.theme_text_color(), sg.theme_background_color()), k=('-DEL-', item_index), tooltip='Delete this item'),
                            sg.T(bosser_text),
                            sg.T(f'Key number {item_index}', k=('-STATUS-', item_index))]], k=('-BOSSER_ROW-', item_index)))]

    return row

#main
def main():
    main_layout = [
        [sg.T("Boss Mules Here"), sg.B('+', tooltip='Add a bossing mule to your roster'), sg.B('View', tooltip='View your bossing fleet')]
    ]
    window = sg.Window("Boss Mule Tracker", main_layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        elif event == "+":
            adding_window()

        elif event == 'Update':
            display_bossers()
            
        elif event[0] == '-DEL-':
            window[('-BOSSER_ROW-', event[1])].update(visible=False)

    window.close()

if __name__=="__main__":
    main()