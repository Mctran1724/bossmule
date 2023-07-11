import PySimpleGUI as sg
from bossing_mule import Bosser


## TODO: 
## Dynamically updating UI elements for each bosser (https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Layout_Add_and_Delete_Rows.py),
##  and the calculations and functionality to add boss crystals. Each bosser should bring up a window where you can add those.


# GUI Definition
remaining_crystals = 180
boss_mules = set()


def adding_window():
    print("Adding Window Opening")
    layout = [
        [sg.Text("Character Name: "), sg.Input(key='add_char_name'), sg.Text("Level: "), sg.Input(key='add_level'), sg.Button("Add")]
    ]

    window = sg.Window("add_window", layout, modal=True)
    
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

    rows = []

    #make this a dataframe or table after
    for bosser in boss_mule_list:
        s = f"Level {bosser.level} {bosser.job} {bosser.name} | {bosser.total_meso} | {bosser.clear_time} \n"
        rows.append([s, sg.Button("Remove"), sg.Button("Edit")])

    return rows


#main
def main():
    main_layout = [
        [sg.Text("Boss Mules Here")],
        [sg.Button("Add Bosser"), sg.Button("Update")]
    ]

    window = sg.Window("Boss Mule Tracker", main_layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        elif event == "Add Bosser":
            adding_window()

        elif event == 'Update':
            new_rows = display_bossers()
            #removing previous rows
            main_layout = [
                [sg.Text("Boss Mules Here")],
                [sg.Button("Add Bosser"), sg.Button("Update")]
            ]
            #Now add the new rows back on
            main_layout += new_rows

            #Now update the display
            
    window.close()

if __name__=="__main__":
    main()