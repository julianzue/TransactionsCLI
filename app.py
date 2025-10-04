from colorama import Fore, Style, init
import csv
import json
import os
import pyfiglet


init()

c = Fore.LIGHTCYAN_EX
y = Fore.LIGHTYELLOW_EX
r = Fore.LIGHTRED_EX
g = Fore.LIGHTGREEN_EX
b = Fore.LIGHTBLUE_EX
re = Fore.RESET

dim = Style.DIM
res = Style.RESET_ALL


if not os.path.exists("data.json"):
    with open("data.json", "w", encoding="utf-8") as json_file:
        json.dump([], json_file, indent=4)


def first_start():
    text = pyfiglet.figlet_format("transactions".upper())

    print(text)

    show_help()
    start()


def show_help():
    print(f"{c}[*]{re} import      {dim}Import a new csv file{res}") # Sparkasse
    print(f"{c}[*]{re} list        {dim}List all data{res}")
    print(f"{c}[*]{re} list in     {dim}List only incoming transactions{res}")
    print(f"{c}[*]{re} list out    {dim}List only outgoing transactions{res}")
    print(f"{c}[*]{re} delete      {dim}Remove all data{res}")
    print(f"{c}[*]{re} search      {dim}Search in list{res}")
    print(f"{c}[*]{re} search line {dim}Search in list{res}")
    print(f"{c}[*]{re} sort        {dim}Sort by price (large -> low){res}")
    print(f"{c}[*]{re} statistic   {dim}Shows the statistic{res}")
    print(f"{c}[*]{re} help        {dim}Shows this help{res}")
    print(f"{c}[*]{re} clear       {dim}Clear the screen{res}")
    print(f"{c}[*]{re} exit        {dim}Close this program{res}")

    print("")

    start()


def start():
    choice = input(f"{y}[+] {re}")

    print("")

    if choice == "import":
        import_csv()
    
    elif choice == "list":
        show_list()

    elif choice == "list in":
        show_list_in()

    elif choice == "list out":
        show_list_out()

    elif choice == "delete":
        delete_list()

    elif choice == "search":
        search()

    elif choice == "search line":
        search_line()

    elif choice == "sort":
        sort_by_price()

    elif choice == "statistic":
        statistic()

    elif choice == "help":
        show_help()        
        
    elif choice == "clear":
        clear()

    elif choice == "exit":
        close()
    
    else:
        print(f"{r}[!]{re} Command {r}{choice}{re} not found! Try again.")
        print("")
        start()


def import_csv():
    # Only works with Sparkasse export (csv)

    filename = input(f"{y}[+] Enter Filename: {re}")
    #filename = "/home/julian/Documents/20251003-1021727712-umsatz.CSV"

    # Open the CSV file
    with open(filename, 'r', encoding='latin-1') as file:
        skip = input(f"{y}[+] Skip? {dim}[Y|n]:{res} ")

        if skip == "" or skip == "Y" or skip == "y":
            print(f"{r}[!]{re} Import skipped.")

        else:
            print(f"{c}[*]{re} File successfully imported!")

            # Create a CSV reader object
            reader = csv.reader(file, delimiter=';')

            columns_max_width = []

            count = 0

            # Iterate over each row in the CSV file
            # get max column width
            for row in reader:
                if count == 0:
                    count += 1
                    pass

                else:

                    columns_list = []

                    for column in row:
                        words = column.split()

                        columns_list.append(" ".join(words))

                    with open("data.json", "r", encoding="utf-8") as json_file:
                        data = json.load(json_file)

                    data.append(
                        {
                            "Auftragskonto": columns_list[0],
                            "Buchungstag": columns_list[1],
                            "Valutadatum": columns_list[2],
                            "Buchungstext": columns_list[3],
                            "Verwendungszweck": columns_list[4],
                            "Glaeubiger ID": columns_list[5],
                            "Mandatsreferenz": columns_list[6],
                            "Kundenreferenz (End-to-End)": columns_list[7],
                            "Sammlerreferenz": columns_list[8],
                            "Lastschrift Ursprungsbetrag": columns_list[9],
                            "Auslagenersatz Ruecklastschrift": columns_list[10],
                            "Beguenstigter/Zahlungspflichtiger": columns_list[11],
                            "Kontonummer/IBAN": columns_list[12],
                            "BIC (SWIFT-Code)": columns_list[13],
                            "Betrag": columns_list[14],
                            "Waehrung": columns_list[15],
                            "Info": columns_list[16]
                        }
                    )

                    with open("data.json", "w", encoding="utf-8") as json_file:
                        json.dump(data, json_file, indent=4)

    print("")
    start()


def get_sum():
    with open("data.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    total = 0.0

    for line in data:
        price = line["Betrag"]

        dot = price.replace(",", ".")

        total += float(dot)

    print("")
    print(f"{c}[*]{re} Total: {c}{'{:.2f}'.format(total)}{re} {line["Waehrung"]}")

    print("")
    start()


def show_list():
    with open("data.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    for index, line in enumerate(data, 1):

        if float(line["Betrag"].replace(",", ".")) < 0.0:
            color = r
        else:
            color = c

        print(f"{c}{'{:03d}'.format(index)}{re} {line["Buchungstag"]} {color}{'{:8.2f}'.format(float(line["Betrag"].replace(",", ".")))}{re} {line["Waehrung"]} {dim}{g}{"{:<22}".format(line["Kontonummer/IBAN"])}{re} {line["Verwendungszweck"]}{res} {b}{dim}({line["Beguenstigter/Zahlungspflichtiger"]}){res}")

    get_sum()


def show_list_in():
    with open("data.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    counter = 0
    total = 0.0

    for index, line in enumerate(data, 1):

        if float(line["Betrag"].replace(",", ".")) >= 0:

            counter += 1

            total += float(line["Betrag"].replace(",", "."))

            if float(line["Betrag"].replace(",", ".")) < 0.0:
                color = r
            else:
                color = c

            print(f"{c}{'{:03d}'.format(counter)} {dim}{'{:03d}'.format(index)}{res} {line["Buchungstag"]} {color}{'{:8.2f}'.format(float(line["Betrag"].replace(",", ".")))}{re} {line["Waehrung"]} {dim}{g}{"{:<22}".format(line["Kontonummer/IBAN"])}{re} {line["Verwendungszweck"]}{res} {b}{dim}({line["Beguenstigter/Zahlungspflichtiger"]}){res}")

    if total < 0.0:
        color_total = r
    else:
        color_total = c

    print("")
    print(f"{c}[*]{re} Total: {color_total}{'{:.2f}'.format(total)}{re} {line["Waehrung"]}")

    print("")

    start()


def show_list_out():
    with open("data.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    counter = 0
    total = 0.0

    for index, line in enumerate(data, 1):

        if float(line["Betrag"].replace(",", ".")) < 0:

            counter += 1

            total += float(line["Betrag"].replace(",", "."))

            if float(line["Betrag"].replace(",", ".")) < 0.0:
                color = r
            else:
                color = c

            print(f"{c}{'{:03d}'.format(counter)} {dim}{'{:03d}'.format(index)}{res} {line["Buchungstag"]} {color}{'{:8.2f}'.format(float(line["Betrag"].replace(",", ".")))}{re} {line["Waehrung"]} {dim}{g}{"{:<22}".format(line["Kontonummer/IBAN"])}{re} {line["Verwendungszweck"]}{res} {b}{dim}({line["Beguenstigter/Zahlungspflichtiger"]}){res}")

    if total < 0.0:
        color_total = r
    else:
        color_total = c

    print("")
    print(f"{c}[*]{re} Total: {color_total}{'{:.2f}'.format(total)}{re} {line["Waehrung"]}")

    print("")

    start()


def sort_by_price():
    with open("data.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    sorted_data = sorted(data, key=lambda x: float(x['Betrag'].replace(",",".")), reverse=True)

    for index, line in enumerate(sorted_data, 1):

        if float(line["Betrag"].replace(",", ".")) < 0.0:
            color = r
        else:
            color = c

        print(f"{c}{'{:03d}'.format(index)}{re} {line["Buchungstag"]} {color}{'{:8.2f}'.format(float(line["Betrag"].replace(",", ".")))}{re} {line["Waehrung"]} {dim}{g}{"{:<22}".format(line["Kontonummer/IBAN"])}{re} {line["Verwendungszweck"]}{res} {dim}{b}({line["Beguenstigter/Zahlungspflichtiger"]}){res}")

    get_sum()


def search():
    query = input(f"{y}[+] Enter query: {re}")
    query_lower = query.lower()

    print("")

    with open("data.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    counter = 0
    total = 0.0

    for index, line in enumerate(data, 1):

        if query_lower in line["Buchungstag"] or query_lower in line["Betrag"] or query_lower in str(line["Verwendungszweck"]).lower() or query_lower in str(line["Beguenstigter/Zahlungspflichtiger"]).lower() or query in line["Kontonummer/IBAN"]:

            counter += 1

            if float(line["Betrag"].replace(",", ".")) < 0.0:
                color = r
            else:
                color = c

            total += float(line["Betrag"].replace(",", "."))

            print(f"{c}{'{:03d}'.format(counter)} {dim}{'{:03d}'.format(index)}{res} {line["Buchungstag"]} {color}{'{:8.2f}'.format(float(line["Betrag"].replace(",", ".")))}{re} {line["Waehrung"]} {dim}{g}{"{:<22}".format(line["Kontonummer/IBAN"])}{re} {line["Verwendungszweck"]}{res} {b}{dim}({line["Beguenstigter/Zahlungspflichtiger"]}){res}")


    if total < 0.0:
        color_total = r
    else:
        color_total = c

    print("")
    print(f"{c}[*]{re} Total: {color_total}{'{:.2f}'.format(total)}{re} {line["Waehrung"]}")

    print("")
    start()


def search_line():
    line_number = int(input(f"{y}[+] Enter line number: {re}"))

    print("")

    with open("data.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    counter = 0
    total = 0.0

    for index, line in enumerate(data, 1):

        if line_number == index:

            counter += 1

            if float(line["Betrag"].replace(",", ".")) < 0.0:
                color = r
            else:
                color = c

            total += float(line["Betrag"].replace(",", "."))

            print(f"{c}{'{:03d}'.format(counter)} {dim}{'{:03d}'.format(index)}{res} {line["Buchungstag"]} {color}{'{:8.2f}'.format(float(line["Betrag"].replace(",", ".")))}{re} {line["Waehrung"]} {dim}{g}{"{:<22}".format(line["Kontonummer/IBAN"])}{re} {line["Verwendungszweck"]}{res} {b}{dim}({line["Beguenstigter/Zahlungspflichtiger"]}){res}")


    if total < 0.0:
        color_total = r
    else:
        color_total = c

    print("")
    print(f"{c}[*]{re} Total: {color_total}{'{:.2f}'.format(total)}{re} {line["Waehrung"]}")

    print("")
    start()


def delete_list():
    sure = input(f"{y}[+] Are you sure to delete the list? {dim}[Y|n]: {res}")

    if sure == "" or sure == "Y" or sure == "y":
        with open("data.json", "w", encoding="utf-8") as json_file:
            json.dump([], json_file, indent=4)

        print(f"{c}[*]{re} List successfully deleted!")

        import_data = input(f"{y}[+] Import data? {dim}[Y|n]: {res}")

        if import_data == "" or import_data == "Y" or import_data == "y":
            import_csv()
        else:
            start()

    else:
        print(f"{r}[!]{re} Canceled!")
        start()


def statistic():
    with open("data.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    # minimum and maximum price
    # average price

    max_price = 0.0
    min_price = 0.0

    max_price_line = 0
    min_price_line = 0

    sum_price = 0.0
    average = 0.0

    for index, line in enumerate(data, 1):
        betrag = float(str(line["Betrag"]).replace(",","."))

        if betrag >= max_price:
            max_price = betrag
            max_price_line = index

        if betrag <= min_price:
            min_price = betrag
            min_price_line = index

        sum_price += betrag

    # line count

    lines = len(data)

    average = sum_price / lines

    # print values

    if max_price > 0:
        color = c
    else:
        color = r

    print(f"{c}[*]{re} Max price:     {color}{'{:8.2f}'.format(max_price)}{res} {data[0]["Waehrung"]} {dim}(Line: {c}{max_price_line}{re}){res}")

    if min_price > 0:
        color = c
    else:
        color = r

    print(f"{c}[*]{re} Min price:     {color}{'{:8.2f}'.format(min_price)}{res} {data[0]["Waehrung"]} {dim}(Line: {c}{min_price_line}{re}){res}")

    if sum_price > 0:
        color = c
    else:
        color = r

    print(f"{c}[*]{re} Sum price:     {color}{'{:8.2f}'.format(sum_price)}{res} {data[0]["Waehrung"]}")

    if average > 0:
        color = c
    else:
        color = r

    print(f"{c}[*]{re} Average price: {color}{'{:8.2f}'.format(average)}{res} {data[0]["Waehrung"]}")
    print(f"{c}[*]{re} Lines count:   {c}{'{:>8}'.format(lines)}{re}")

    print("")

    start()
        



def clear():
    os.system("clear")
    start()


def close():
    print(f"{r}[!]{re} Programm closed. Bye.")
    quit()


first_start()