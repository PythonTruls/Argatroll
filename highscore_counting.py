import time
import csv

"""this prgram takes care of the csv writing and the highscore appending and time returning
"""

def stop_watch_1():
    """wont be used in the project"""
    #Timer starts
    starttime = time.time()
    value = ""


    while value != "q":
        value = input(":")
        
        totaltime = round((time.time() - starttime), 4)
        
    return totaltime

def current_time():
    """return the coputer-time in seconds"""
    return time.time()


def stop_watch_2():
    """wont be used in the project"""
    start = 0
    sleep = 0.1

    while start < 5:
        time.sleep(sleep)
        start += sleep
        print(round(start),2)

    return start

def highscore_appending(score,player_name,size):
    """takes player name, the time to finish game and the size of the game
    and writes it over to a csv file using a dict writer"""

    playetime = round((score[1]-score[0]),2)
    if playetime > 10000:
        return

    highscore_dictionary = []
    dictkeys = ['highscore', 'playername','gamesize']


    highscore_dictionary.append({'highscore':playetime,'playername':player_name,'gamesize':size})


    with open('highscore.csv', mode="r", newline="") as file:

        reader = csv.DictReader(file,fieldnames=dictkeys,delimiter=",")

        empty = not any(row for row in reader) #true if there is nothing inside the csv file

        match empty:
            case False: #if there is something inside
                for row in reader: #writes over everything to the list in order to later sort it
                    highscore_dictionary.append(row)
    
    with open('highscore.csv',mode="w") as file:

        writer = csv.DictWriter(file, fieldnames=dictkeys,delimiter=",")
        writer.writeheader()

        for player in sorted(highscore_dictionary, key=lambda player: float(player['highscore'])): #sorts according to the time
            writer.writerow(player) #writes over to csv file in a sorted manner

