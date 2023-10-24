import PySimpleGUI as sg
from bossing_mule import Bosser
from boss_crystal import boss_list, modes

## TODO: 
## Include a way to save and withdraw bossing mule data from a file upon running
## Dynamically updating UI elements for each bosser (https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Layout_Add_and_Delete_Rows.py),
##  and the calculations and functionality to add boss crystals. Each bosser should bring up a window where you can add those.
## https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Layout_Add_and_Delete_Rows.py
#Settings
sg.theme("SandyBeach")

# GUI Definition
remaining_crystals = 180
boss_mules = dict() #maps name to bosser object


#Add a new bossing mule
def add_mule():
    all_classes = ['Hero', 'Paladin', 'Dark Knight']

    layout = [
                [sg.Text('Add bossing mule')],
                [sg.T('Name: '), sg.Input(key='-NAME-', enable_events=True)],
                [sg.T('Class: '), sg.Combo(all_classes, key='-CLASS-')],
                [sg.T('Level: '), sg.Input(key='-LEVEL-', enable_events=True)],
                [sg.Text(size=(25,1), k='-OUTPUT-')],
                [sg.Button('Add'), sg.Button('Exit')]
            ]
    

    window = sg.Window('Add Bossing Mule', layout, finalize=True, modal=True)

    while True:
        event, values = window.read()
        
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "Add":
            #read in the data and add it to the mules set
            new_bosser = Bosser(*values.values(), bosser_index=0)
            boss_mules[values['-NAME-']] = new_bosser
            #automatically bring up the bosses that this character does
            edit_mule(values['-NAME-'])
    window.close()


#Edit an existing bossing mule
def edit_mule(character_name): 
    bosser = boss_mules[character_name]
    
    name = bosser.name
    job = bosser.job
    level = bosser.level    

    layout = [
        [sg.Text(f'Level {level} {job} {name}', auto_size_text=True)]
    ]

    #add all the boss crystals that are currently done
    for crystal in bosser.boss_crystals:
        crystal_line = [sg.Text(crystal)]
        layout.append(crystal_line)

    add_crystal_line = [sg.T('Enter boss crystal information below: Name, Difficulty, Party Size, Clear Time')]
    input_line = [sg.Combo(boss_list, key='-BOSSNAME-'), sg.Combo(modes, key='-DIFFICULTY-'), sg.Combo([x for x in range(1,7)], key='-PTSIZE-'), sg.Input(key='-CLEARTIME-'), sg.B('Add', tooltip=f'Add boss crystal to bossing mule {name}'), sg.B('Remove', tooltip=f'Remove crystal from {name}')]

    layout.append(add_crystal_line)
    layout.append(input_line)

    print(layout)

    window = sg.Window('Edit Bossing Mule', layout, finalize=True, modal=True)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == 'Add':
            print(values.values())
            bosser.add_crystal(*values.values())
        elif event == 'Remove':
            try:
                print(values.values())
                bosser.remove_crystal(*values.values())
            except Exception as e:
                print(e)
    window.close()


#View bossing mules
##TODO
## Working on this xD
def view_bossers(): 
    layout = [[sg.T(f"{x.level} {x.job} {x.name}: {x.total_mesos()} in {x.total_time()} minutes."), sg.Button("Edit", key=f'{x.name}-EDIT-'), sg.Button(f"X", key=f'{x.name}-REMOVE-')] for x in boss_mules.values()]
    window = sg.Window("Boss Mule Roster", layout, finalize=True, modal=True)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif "-EDIT-" in event:
            char_name = event[:-6]
            print(f"Editing {char_name}")
        
    window.close()


#main
def main():
    main_layout = [
        [sg.T("Boss Mules Here"), sg.B('+', tooltip='Add a bossing mule to your roster'), sg.B('View', tooltip='View your weekly bossers')]
    ]
    window = sg.Window("Boss Mule Tracker", main_layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        elif event[0] == '+':
            add_mule()

        elif event[0] == 'View':
            view_bossers()


    window.close()

if __name__=="__main__":
    main()
    print(boss_mules)