# Import af de nødvendige biblioteker
import csv
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
import numpy as np
from calendar import monthrange

import os
os.system("clear")

print("Velkommen")

# PROGRAMMET SKAL KUNNE PARSE CSV-FILEN (IMPORTÈR OG INDLÆS CSV-FILEN).
# PRINT HVOR MANGE DATAINDTASTNINGER DER ER FOR HVER KOMMUNE.

# Vi laver en funktion, vi kan kalde på i MENU'en.
def Observationer():
    with open('/Users/Emil/Desktop/data.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))

        # Finder antallet af observationer for hver kommune. Vi har kaldt kommune for city.
        kommune_antal = {}

        for row in data[1:]:  # Dette får programmet til at skippe den først række, da det er overskrifter.
            kommune = row[2] # Kommuner er række 3, hvilket vi kalder row[2], da rækkerne starter fra 0.
            if kommune not in kommune_antal: # Deler kommunerne op, så observationer i samme kommune tælles sammen.
                kommune_antal[kommune] = 0
            kommune_antal[kommune] += 1

        # Vi printer hvor mange observationer der er ved hver enkelt kommune.
        for kommune, count in kommune_antal.items():
            print(f"{kommune}: {count}")



# LAV ET "BAR PLOT", DER VISER DEN GENNEMSNITLIGE MÅNEDLIGE LATENCY FOR FREDERIKSBERG OG HERNING I ÈN GRAF.

# Vi laver en funktion, vi kan kalde på i MENU'en.
def Gml(): #Gennemsnitlige månedlige latency
    with open('/Users/Emil/Desktop/data.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))

    frederiksberg_data = {}
    herning_data = {}

    for row in data[1:]:  # Overskriften skippes igen ved brug af [1:].
        city = row[2]
        date = datetime.strptime(row[0], '%Y-%m-%d')  # Bruger "strptime" for at fortælle programmet rækken er dato.
        month = date.strftime('%B')  # Bruger "strftime" for at navnet på måneden.
        speed = float(row[5].split()[0])  # Fjerner ms fra dataen, for at splitte tal og tekst.

        # Vi laver en dictonary, så dataen passer til de rigtige kommuner.
        if city == "Frederiksberg":
            if month in frederiksberg_data:
                # Hvis måneden i dataen er Frederiksberg, så tilføjer vi dataen til Frederiksbergs dataliste.
                frederiksberg_data[month].append(speed)
            else:
                # Hvis måneden ikke er Frederiksberg, tilføjer vi dataen til en ny liste.
                frederiksberg_data[month] = [speed]
        elif city == "Herning":
            if month in herning_data: # Hvis måneden i dataen er Herning, så tilføjer vi dataen til Hernings dataliste.
                herning_data[month].append(speed)
            else:
                herning_data[month] = [speed] # Hvis måneden ikke er Herning, tilføjer vi dataen til en ny liste.

    # Vi beregner den gennemsnitlige hastighed for henholdsvis Frederiksberg og Herning.
    frederiksberg_averages = {month: sum(speeds) / len(speeds) for month, speeds in frederiksberg_data.items()}
    herning_averages = {month: sum(speeds) / len(speeds) for month, speeds in herning_data.items()}

    # Positioner for søjlerne i plottet.
    bar_positions = np.arange(len(frederiksberg_averages))

    # Printer et Bar plot
    plt.bar(bar_positions - 0.15, frederiksberg_averages.values(), width=0.3, label="Frederiksberg")
    plt.bar(bar_positions + 0.15, herning_averages.values(), width=0.3, label="Herning")
    plt.xticks(bar_positions, frederiksberg_averages.keys())
    plt.legend()
    plt.show()


# LAV ET SCATTER PLOT AF DE HØJESTE DOWNLOADHASTIGHEDER FOR HVER KOMMUNE.

# Vi laver en funktion, vi kan kalde på i MENU'en.
def Scatterplot():
    with open('/Users/Emil/Desktop/data.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))

    # Vi laver en liste af den højest download hastighed for hver kommune.
    highest_speed = {}

    for row in data[1:]: # Vi skipper første række, da det er en overskift i datasættet.
        city = row[2] # Kommune er række 3, men vi kalder den row[2] da første række starter fra 0.
        speed = float(row[3]) # Speed er række 2, og vi konvertere den til en float.

    # Vi opdatere listen for højeste hastigheder for hver kommune.
        if city not in highest_speed or speed > highest_speed[city]:
            highest_speed[city] = speed

    # Get the list of city names and download speeds. Liste over kommune navne og download hastigheder.
    x = list(highest_speed.keys())
    y = list(highest_speed.values())

    # Vi kan nu begynde at lave et scatterplot.
    for i, city in enumerate(x):
        plt.scatter(city, y[i])

    # Vi sætter x-aksen til at være kommuner, samt definerer x-aksen til at være den vertical for et bedre layout.
    plt.xticks(x, rotation='vertical')

    # Vi navngiver akserne og en titel.
    plt.xlabel('City')
    plt.ylabel('Highest Download Speed')
    plt.title('Highest Download Speed per City')

    # Fremkalder et scatterplot.
    plt.show()


# Vi bruger et While loop til at fremkalde funktioner. Samt give forbrugeren muligheder.
while True:
    prompt = "> " # For bedre layout for forbrugeren.
    user_input = input("""
Enter 1: Observations.
Enter 2: Bar plot.
Enter 3: Scatterplot.
Enter Q: Exit:
""" + prompt)
    if user_input == "1":
        Observationer() # Hvis forbrugeren skriver 1 i inputtet, vil det fremkalde funktionen Observationer.
    elif user_input == "2":
        Gml() # Hvis forbrugeren skriver 2 i inputtet, vil det fremkalde funktionen Gml.
    elif user_input == "3":
        Scatterplot() # Hvis forbrugeren skriver 3 i inputtet, vil det fremkalde funktionen Scatterplot.
    elif user_input == "Q":
        exit() # Hvis forbrugeren skriver Q i inputtet, vil det afslutte programmet.
    else:
        print("Invalid input. Please try again.") # Hvis forbrugeren skriver andre variable, vil programmet spørger efter input igen.
