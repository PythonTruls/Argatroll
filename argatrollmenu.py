"""This will be all the player messages
"""

def welcoming_the_player():
    with open('game_text.txt',mode="r") as file:
        for line in file:
            print(line)

    player_name = input("Your name: ")
    return player_name

def rules_of_the_game(player_name):
    print(f"Alright {player_name}!")
    


def main():
    rules_of_the_game(welcoming_the_player())

if __name__ == "__main__":
    main() 