import time
import csv


def stop_watch_1():
    #Timer starts
    starttime = time.time()
    value = ""


    while value != "q":
        value = input(":")
        
        totaltime = round((time.time() - starttime), 4)
        
    return totaltime

def current_time():
    return time.time()


def stop_watch_2():
    start = 0
    sleep = 0.1

    while start < 5:
        time.sleep(sleep)
        start += sleep
        print(round(start),2)

    return start

def highscore_appending(score,player_name,size):

    playetime = round((score[1]-score[0]),2)
    if playetime > 10000:
        return

    highscore_dictionary = []
    dictkeys = ['highscore', 'playername','gamesize']


    highscore_dictionary.append({'highscore':playetime,'playername':player_name,'gamesize':size})


    with open('highscore.csv', mode="r", newline="") as file:

        reader = csv.DictReader(file,fieldnames=dictkeys,delimiter=",")

        empty = not any(row for row in reader)

        match empty:
            case False:
                for row in reader:
                    highscore_dictionary.append(row)
    
    with open('highscore.csv',mode="w") as file:

        writer = csv.DictWriter(file, fieldnames=dictkeys,delimiter=",")
        writer.writeheader()

        for player in sorted(highscore_dictionary, key=lambda player: float(player['highscore'])):
            writer.writerow(player)

