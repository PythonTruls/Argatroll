import tkinter as tk
from tkinter import Grid
import argatroll
import argatrollmenu as menu

#Colout change

class Gui:

    def __init__(self,game,root):
        self.game = game
        self.root = root
        self.buttons = dict()
        self.troll = tk.PhotoImage(file= 'gnome.png')

    #Button click
    def button_clicked(self,position):

        self.game.reseting_coordinate_values()

        if self.game.angry_troll_check(position):
            new_coordinates = self.game.changing_coordinates(self.game.adding_troll(position))
            self.game.changing_occupied_list(new_coordinates,"occupy")
            self.buttons[position]["text"] = "X"

        else:
            if position in self.game.trolls:
                new_coordinates = self.game.changing_coordinates(self.game.removing_troll(position))
                self.game.changing_occupied_list(new_coordinates,"undo")
                self.buttons[position]["text"] = " "
            else:
                print("trolls got angry!")

        self.game.occupying_coordinates()

        for coordinate in self.game.coordinates:
            if self.game.board[coordinate]:
                self.buttons[coordinate]["bg"]="white"
            elif not self.game.board[coordinate]:
                self.buttons[coordinate]["bg"]="light goldenrod"
            else:
                print("error")

    #Build our buttons
    def building_buttons(self):
        

        #Creating buttons
        for coordinate in self.game.coordinates:
            #Button function and info
            self.buttons[coordinate] = tk.Button(self.root,text=" ",width=20,height=10,command=lambda position = coordinate: self.button_clicked(position))
            #Button grid
            self.buttons[coordinate].grid(row=coordinate[0],column=coordinate[1],)

    def colouring(self,occupied_list):
        for coordinate in occupied_list:
            self.buttons[coordinate]["bg"]="red"

    def playing(self):
        self.building_buttons()
        self.root.mainloop()


def main():

    root = tk.Tk()
    root.geometry("1500x900")
    root.title("Arga troll")

    size = 5
    array = {}
    coordinates = argatroll.coordinate_system(size)

    game1 = argatroll.Gameboard(size,coordinates,array)
    
    game = Gui(game1,root)
    
    game.playing()

main()