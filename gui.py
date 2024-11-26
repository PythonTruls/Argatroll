import tkinter as tk
from tkinter import messagebox
from tkinter import Grid
import argatroll
import argatrollmenu as menu


class Gamewindow(tk.Frame):

    def __init__(self,parent,controller):

        tk.Frame.__init__(self,parent)

        
        font = ("Comic Sans MS", 20, "bold")
        self.controller = controller
        self.buttons = dict()


        #Troll counter display
        text = f"Trolls placed: {len(controller.game.trolls)} / {controller.game.size}"
        troll_counter = tk.Label(self, text=text,font=font, padx=25)
        troll_counter.grid(row=1,column=controller.game.size +1)

        #Creating buttons
        for coordinate in controller.game.coordinates:
            #Button function and info
            self.buttons[coordinate] = tk.Button(self,text=" ",width=20,height=10,command=lambda position = coordinate: self.button_clicked(position))
            #Button grid
            self.buttons[coordinate].grid(row=coordinate[0],column=coordinate[1])

    #Button click
    def button_clicked(self,position):

        self.controller.game.reseting_coordinate_values()

        if self.controller.game.angry_troll_check(position):
            new_coordinates = self.controller.game.changing_coordinates(self.controller.game.adding_troll(position))
            self.controller.game.changing_occupied_list(new_coordinates,"occupy")
            self.buttons[position]["text"] = "X"

        else:
            if position in self.controller.game.trolls:
                new_coordinates = self.controller.game.changing_coordinates(self.controller.game.removing_troll(position))
                self.controller.game.changing_occupied_list(new_coordinates,"undo")
                self.buttons[position]["text"] = " "
            else:
                print("trolls got angry!")

        self.controller.game.occupying_coordinates()
        self.coloring_occupied()
        self.troll_counter()
    
    def troll_counter(self):
        self.finish_game()

    def finish_game(self):
        trolls_placed = len(self.controller.game.trolls)
        match trolls_placed:
            case self.controller.game.size:
                quit()
            case _:
                pass
            

    def coloring_occupied(self):
        for coordinate in self.controller.game.coordinates:

            if self.controller.game.board[coordinate]:
                self.buttons[coordinate]["bg"]="white"

            elif not self.controller.game.board[coordinate]:
                self.buttons[coordinate]["bg"]="light goldenrod"

            else:
                print("error")


class Welcomemenu(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        font=('Helvetica',15,'bold')

        game_info = tk.Text(self, width=60,height=15,font = font)
        game_info.pack(pady=20,padx =20)

        with open("game_text.txt",mode="r") as file:
            welcome = file.read()
            game_info.insert(tk.END,welcome)
            file.close()
    
        name_entry = tk.Entry(self,textvariable=controller.player_name,font=font)

        size_entry_4 = tk.Button(self,text="4",command=lambda: controller.creating_game_board(4))
        size_entry_5 = tk.Button(self,text="5",command=lambda: controller.creating_game_board(5))
        size_entry_6 = tk.Button(self,text="6",command=lambda: controller.creating_game_board(6))
        size_entry_7 = tk.Button(self,text="7",command=lambda: controller.creating_game_board(7))
        
        name_entry.pack(pady=20)
        size_entry_4.pack(padx= 10)
        size_entry_5.pack(padx=15)
        size_entry_6.pack(padx=20)
        size_entry_7.pack(padx=25)

        
        

class Argatroll(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)

        self.player_name = tk.StringVar

        self.container = tk.Frame(self)
        self.container.pack(side="top",fill="both",expand=True)

        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.frame_container = {}
        frame1 = Welcomemenu(self.container,self)

        self.frame_container[Welcomemenu] = frame1
        frame1.grid(row = 0, column = 0, sticky ="nsew")
        
        

        self.switch_screen(Welcomemenu)

    def creating_game_board(self,size):
        coordinates = argatroll.coordinate_system(size)
        array = argatroll.coordinate_values(coordinates)
        self.game = argatroll.Gameboard(size,coordinates=coordinates,array=array)

        frame2 = Gamewindow(self.container,self)
        self.frame_container[Gamewindow] = frame2
        frame2.grid(row=0,column=0, sticky="nsew")
    
    def switch_screen(self,cont):
        frame = self.frame_container[cont]
        frame.tkraise()

def main():
    app = Argatroll()
    app.title("Arga troll")
    app.geometry("1500x900")
    app.mainloop()

main()