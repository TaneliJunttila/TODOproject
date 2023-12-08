#loads content from file
import colorama, json
import pandas as pd
from datetime import datetime
import os
while True:
    colorama.init(autoreset=True)
    today = datetime.today()
    file_handle = open("todo_laskuri_tietolista2.0.json", "r", encoding="utf-8")
    content = file_handle.read()
    data = json.loads(content)
    file_handle.close()

    #read files
    #prints content in mostly readable form, calculates difference and sorts list
    todo_lists = []
    for entry in data:
        temp_list = []
        time = entry["time"].replace(" ", "_")
        time = datetime.strptime(time, "%Y-%m-%d_%H:%M:%S")
        difference = time - today
        time = time.strftime("%d.%m.%Y %H:%M:%S")
        temp_list.append(time)
        temp_list.append(entry["todo"])
        temp_list.append(entry["note"])
        temp_list.append(difference)
        todo_lists.append(temp_list)
    todo_lists = sorted(todo_lists, key=lambda x:x[3])

    #readable for humans:
    print("Todo list:")
    if len(todo_lists) == 0:
        print("Empty!")
    else:
        print()
        for entry2 in todo_lists:
            readable_difference = pd.Timedelta(entry2[3]).round(freq='S')
            print(colorama.Fore.YELLOW + f"{entry2[1]}")
            print("Muistiinpanot: " + "\n" + colorama.Fore.LIGHTRED_EX + str(entry2[2]))
            print("Aikaa jäljellä: " + colorama.Fore.LIGHTRED_EX + str(readable_difference))
            print("Valmis mennessä: " + colorama.Fore.LIGHTRED_EX + str(entry2[0]))
            print()
    print("Valitse toiminto: lisää merkintä (l), poista merkintä (p), muokkaa merkintää (m), exit (e):")
    choice = input()
    if choice.lower() == "l":
        todo = input("Anna tehtävän otsikko: \n")
        print()
        while True:
            try:
                time = input("Anna tehtävälle aikaraja muodossa (30.11.2022 13:45:00): \n").replace(" ", "_")
                time = datetime.strptime(time, "%d.%m.%Y_%H:%M:%S")
                time = time.strftime("%Y-%m-%d %H:%M:%S")
                print()
                break
            except Exception:
                print("Lue Päivämäärä tarkasti")
                print()
        note = input("Anna muistiinpanot: \n")
        entry = {"time": time, "todo": todo, "note": note}
        data.append(entry)
        data = json.dumps(data)
        file_handle = open("todo_laskuri_tietolista2.0.json", "w")
        file_handle.write(data)
        file_handle.close()
        print("Added!")
    elif choice.lower() == "p":
        x=0
        for entry3 in data:
            print(f"{x} {entry3['todo']}")
            x += 1
        
        if len(data) == 0:
            print("Lista on tyhjä.")
        else:
            to_be_deleted = int(input("Minkä numeron merkinnän haluat poistaa?: \n"))
            del data[to_be_deleted]
            data = json.dumps(data)
            file_handle = open("todo_laskuri_tietolista2.0.json", "w")
            file_handle.write(data)
            file_handle.close()
            print("Poistettu!")
            print()
    elif choice.lower() == "m":
        x = 0
        for entry3 in data:
            print(f"{x} {entry3['todo']}")
            x += 1
        if len(data) == 0:
            print("Lista on tyhjä.")
        else:
            to_be_edited_index = int(input("Minkä numeron merkintää haluat muokata?: \n"))
            to_be_edited = data[to_be_edited_index]
            del data[to_be_edited_index]
            print(f"Vanha otsikko: {to_be_edited['todo']}")
            todo = input("Anna uusi otsikko: \n")
            print(f"Vanha aikaraja: {to_be_edited['time']}")
            while True:
                try:
                    time = input("Anna tehtävälle uusi aikaraja muodossa (30.11.2022 13:45:00): \n").replace(" ", "_")
                    time = datetime.strptime(time, "%d.%m.%Y_%H:%M:%S")
                    time = time.strftime("%Y-%m-%d %H:%M:%S")
                    break
                except Exception:
                    print("Lue Päivämäärä tarkasti")
            print(f"Vanha muistiinpano: {to_be_edited['note']}")
            note = input("Anna uusi muistiinpano: \n")
            entry = {"time": time, "todo": todo, "note": note}
            data.append(entry)
            data = json.dumps(data)
            file_handle = open("todo_laskuri_tietolista2.0.json", "w")
            file_handle.write(data)
            file_handle.close()
            print("Muokattu!")
    else:
        break