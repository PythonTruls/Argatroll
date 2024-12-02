import tkinter as tk
import csv
import highscore_counting as highscore
import argatroll
import random
import tries
import time


class Gamewindow(tk.Frame):

    def __init__(self,parent,controller):

        tk.Frame.__init__(self,parent)

        
        self.font = ("Comic Sans MS", 20, "bold")
        self.controller = controller
        self.buttons = dict()

        self.troll_counter()

        #Creating buttons
        for coordinate in controller.game.coordinates:
            #Button function and info
            self.buttons[coordinate] = tk.Button(self,text=" ",width=20,height=10,command=lambda position = coordinate: self.button_clicked(position))
            #Button grid
            self.buttons[coordinate].grid(row=coordinate[0],column=coordinate[1])
        
        algoritm_btn = tk.Button(self,text="solve with algoritm",width=20,height=10,command=lambda: self.algoritm_solver())
        algoritm_btn.grid(row=5,column=self.controller.game.size+10)

    #Button click
    def button_clicked(self,position):

        self.controller.game.reseting_coordinate_values()

        if self.controller.game.limiting_to_one_row(position):
            if self.controller.game.angry_troll_check(position):
                self.occupying_button(position=position)
            else:
                if position in self.controller.game.trolls:
                    self.deoccupying_button(position=position)
                else:
                    self.creating_angry_label()
        else:
            self.creating_non_available_label(positon=position)

        self.controller.game.occupying_coordinates()
        self.coloring_occupied()
        self.troll_counter()
    
    def alogritm_btn_click(self,position,move):

        if move == "occupy":
            self.occupying_button(position=position)
        elif move == "undo":
            self.deoccupying_button(position=position)

        self.controller.game.occupying_coordinates()
        self.coloring_occupied()
        self.troll_counter()
    
    def algoritm_solver(self):
        for troll in self.controller.game.trolls:
            self.deoccupying_button(troll)
        solver = tries.Algoritm2(self.controller.game,self.alogritm_btn_click)
        solver.solver()

    def occupying_button(self,position):
        new_coordinates = self.controller.game.changing_coordinates(self.controller.game.adding_troll(position))
        self.controller.game.changing_occupied_list(new_coordinates,"occupy")
        self.buttons[position]["text"] = "X"
    
    def deoccupying_button(self,position):
        new_coordinates = self.controller.game.changing_coordinates(self.controller.game.removing_troll(position))
        self.controller.game.changing_occupied_list(new_coordinates,"undo")
        self.buttons[position]["text"] = " "

    def creating_angry_label(self):
        color = ["red","blue","yellow"]
        i = random.randint(0,2)
        self.angrytroll_message = tk.Label(self,text="Trolls got angry!",font=self.font,bg=color[i])
        self.angrytroll_message.grid(row=self.controller.game.size + 6,column=self.controller.game.size //2)

    def creating_non_available_label(self,positon):
        self.wrongrow_message = tk.Label(self,text="One row at a time!",font=self.font)
        self.wrongrow_message.grid(row = positon[0], column=(self.controller.game.size +1))
    
    def troll_counter(self):
        #Troll counter display
        text = f"Trolls placed: {len(self.controller.game.trolls)} / {self.controller.game.size}"
        troll_counter = tk.Label(self, text=text,font=self.font, padx=25)
        troll_counter.grid(row=0,column=self.controller.game.size +1)
        self.finish_game()

    def finish_game(self):
        trolls_placed = len(self.controller.game.trolls)
        match trolls_placed:
            case self.controller.game.size:
                next_btn = tk.Button(self,width=20,height=10,text="next",command=lambda:self.controller.creating_postgame(self.controller.game.size))
                next_btn.grid(row=5,column=self.controller.game.size+10)
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
        game_info.pack()

        with open("game_text.txt",mode="r") as file:
            welcome = file.read()
            game_info.insert(tk.END,welcome)
            file.close()
    
        question = tk.Label(self,text="What is your name?",font=font,fg="brown")
        name_entry = tk.Entry(self,width=50,font=font)
        
        

        size_entry_4 = tk.Button(self,text="4",bg="lime",font=font,command=lambda: controller.creating_game_board(4,name_entry.get()))
        size_entry_5 = tk.Button(self,text="5",bg="green",font=font,command=lambda: controller.creating_game_board(5,name_entry.get()))
        size_entry_6 = tk.Button(self,text="6",bg="yellow",font=font,command=lambda: controller.creating_game_board(6,name_entry.get()))
        size_entry_7 = tk.Button(self,text="7",bg="red",font=font,command=lambda: controller.creating_game_board(7,name_entry.get()))

        question.pack(pady = 20)
        name_entry.pack(pady= 20)
        size_entry_4.pack(padx=5,ipadx=20,ipady=20,side="top")
        size_entry_5.pack(padx=5,ipadx=20,ipady=20,side="top")
        size_entry_6.pack(padx=5,ipadx=20,ipady=20,side="top")
        size_entry_7.pack(padx=5,ipadx=20,ipady=20,side="top")

class Postgame(tk.Frame):
    def __init__(self,parent,controller,player_name,time,game_size):
        tk.Frame.__init__(self,parent)

        font=('Helvetica',15,'bold')
        self.size = game_size

        dictkeys = ['highscore', 'playername','gamesize']
        lables = dict()

        highscore.highscore_appending(player_name=player_name,score=time,size=game_size)

        with open("highscore.csv",mode="r") as file:
            
            reader = csv.DictReader(file,fieldnames=dictkeys)
            next(reader)

            i = 1
            for row in reader:
                if i <= 15:
                    player = row["playername"]
                    time = row["highscore"]
                    gamesize = row["gamesize"]
                    lables[i] = tk.Label(self,text=f"{i}. '{player}' with time {time}s, with gameboard {gamesize}x{gamesize}",font=font)
                    lables[i].pack(side = "top")
                    i += 1

        quit_btn = tk.Button(self,text="Quit",bg="red",font=font,command=quit)
        quit_btn.pack(side="bottom",ipadx=10,ipady=15)

        

class Argatroll(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)

        self.time = []

        self.container = tk.Frame(self)
        self.container.pack(side="top",fill="both",expand=True)

        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.frame_container = {}
        frame1 = Welcomemenu(self.container,self)

        self.frame_container[Welcomemenu] = frame1
        frame1.grid(row = 0, column = 0, sticky ="nsew")
        
        self.switch_screen(Welcomemenu)

    def creating_game_board(self,size,player_name):
        self.player_name = player_name
        self.time.append(highscore.current_time())

        coordinates = argatroll.coordinate_system(size)
        array = argatroll.coordinate_values(coordinates)
        self.game = argatroll.Gameboard(size,coordinates=coordinates,array=array)

        frame2 = Gamewindow(self.container,self)
        self.frame_container[Gamewindow] = frame2
        frame2.grid(row=0,column=0, sticky="nsew")

    def creating_postgame(self,game_size):
        self.time.append(highscore.current_time())
        frame3 = Postgame(self.container,self,self.player_name,self.time,game_size)
        self.frame_container[Postgame] = frame3
        frame3.grid(row = 0, column= 0 , sticky= "nsew")
    
    def switch_screen(self,cont):
        frame = self.frame_container[cont]
        frame.tkraise()

def main():
    app = Argatroll()
    app.title("Arga troll")
    app.geometry("2000x1200")
    app.mainloop()

main()