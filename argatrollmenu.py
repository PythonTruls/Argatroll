"""This will be all the player messages
"""

def welcoming_the_player():
    message = {}
    i = 0
    with open('game_text.txt',mode="r") as file:
        for line in file:
            message[i] = line
            i += 1
    return message
            

def main():
    welcoming_the_player()

if __name__ == "__main__":
    main() 