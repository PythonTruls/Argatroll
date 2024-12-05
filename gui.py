import tkinter as tk
import csv
import highscore_counting as highscore
import argatroll
import random
import argatroll_solver

"""This program imports all relevant functions and classes and using them all to build a GUI with Tkinter
to the game 'arga troll'
'highscore_counting' for leader board creation
'argatroll_solver' for algoritm to solve any board
'argatroll' for the main game functions of the game
"""


class Gamewindow(tk.Frame):
    """Class that creates a object that can place widgets that performs the main gameplay
    The tk.frame makes the object inherit the frame class. Thiss allows it to make a frame
    in which it can place all its widgets
    """
    #It contains it's parent which will be a container of frames
    #'controller' is the ruling object which 'controlls' all it's containing frames
    def __init__(self,parent,controller): 
        

        tk.Frame.__init__(self,parent) #this makes it possible to put in the object Gamewindow into a frame

        
        self.font = ("Comic Sans MS", 15, "bold")
        self.controller = controller
        self.buttons = dict() #buttons will be stored in a dictionary
        self.cheat = 0 #this can change to '1' indicating solver algoritm has been used
        self.troll_counter()

        #Creating cooridnate buttons
        for coordinate in controller.game.coordinates:
            #Button function and info
            self.buttons[coordinate] = tk.Button(self,text=" ",width=20,height=10,command=lambda position = coordinate: self.button_clicked(position))
            #Placing buttons using tkinter grid
            self.buttons[coordinate].grid(row=coordinate[0],column=coordinate[1])
        
        algoritm_btn = tk.Button(self,text="solve with algoritm",width=20,height=10,command=lambda: self.algoritm_solver())
        algoritm_btn.grid(row=5,column=self.controller.game.size+10)

    #Coordinate-buttons clicked by user
    def button_clicked(self,position):
        """When button inside the buttons dictionary are clicked
        multiple 'checks' are performed in order to performe relevant action¨
        either place troll, remove troll, notify player of incorrect move
        """

        self.controller.game.reseting_coordinate_values() #resetting all coordinate values to 1

        if self.controller.game.limiting_to_one_row(position): #check if row is usable
            if self.controller.game.angry_troll_check(position): #Checks if the position doesnt 'agrevate trolls'
                self.occupying_button(position=position) #occupies related coordinates
            else:
                if position in self.controller.game.trolls: #if a troll is clicked upon it will instead remove it
                    self.deoccupying_button(position=position)
                else:
                    self.creating_angry_label() #if a occupied coordinate is clicked user will be notified
        else:
            self.creating_non_available_label(positon=position) #if action is performed outside row-range

        self.controller.game.occupying_coordinates() #occuppying coordinates are changed to 1
        self.coloring_occupied()
        self.troll_counter()
    
    def alogritm_btn_click(self,position,move):
        """Method called when the algoritm function clicks a button
        similar to when the player clicks a button
        """
        if move == "occupy":
            self.occupying_button(position=position)
        elif move == "undo":
            self.deoccupying_button(position=position)

        self.controller.game.occupying_coordinates()
        self.coloring_occupied()
        self.troll_counter()
    
    def algoritm_solver(self):
        """Methdo called when the player whants to solve with algoritm
        """
        self.cheat = 1 #Means the player used the algoritm

        for troll in self.controller.game.trolls[::-1]: #Clears the board if trolls are already placed
            self.deoccupying_button(troll)

        #updating board after trolls are removed
        self.controller.game.occupying_coordinates() 
        self.coloring_occupied()

        #creates object of an imported class which can perform solver-algoritm
        solver = argatroll_solver.Algoritm2(self.controller.game,self.alogritm_btn_click)
        solver.solver()

    def occupying_button(self,position):
        """Method that is called when a new troll is placed
        """
        new_coordinates = self.controller.game.changing_coordinates(self.controller.game.adding_troll(position))
        self.controller.game.changing_occupied_list(new_coordinates,"occupy")
        self.buttons[position]["text"] = "X"
    
    def deoccupying_button(self,position):
        """Method called when a troll is removed
        """
        new_coordinates = self.controller.game.changing_coordinates(self.controller.game.removing_troll(position))
        self.controller.game.changing_occupied_list(new_coordinates,"undo")
        self.buttons[position]["text"] = " "

    def creating_angry_label(self):
        """Places a label notifying the player that a troll got angry
        """
        color = ["red","blue","yellow"]
        i = random.randint(0,2) #for randomizing a background color
        self.angrytroll_message = tk.Label(self,text="Trolls got angry!",font=self.font,bg=color[i])
        self.angrytroll_message.grid(row=3,column=self.controller.game.size + 10)

    def creating_non_available_label(self,positon):
        """Places a label notifying the player that a move cant be performed on wanted row
        """
        self.wrongrow_message = tk.Label(self,text="One row at a time!",font=self.font)
        self.wrongrow_message.grid(row = positon[0], column=(self.controller.game.size +1))
    
    def troll_counter(self):
        """Placing label which keeps the count of trolls placed on the board,
        this will also be used to check if all trolls are placed.
        Fucton can be called upon anytime the label need to be updated
        """
        
        counter_font = ("Comic Sans MS", 25, "bold")

        #Troll counter display
        text = f"Trolls placed: {len(self.controller.game.trolls)} / {self.controller.game.size}"
        troll_counter = tk.Label(self, text=text,font=counter_font, padx=25)
        troll_counter.grid(row=0,column=self.controller.game.size +1)
        self.finish_game() #calls the method to check if game is finished

    def finish_game(self):
        """method that keeps track on if the game is finished,
        meaning all possible trolls are placed
        """
        trolls_placed = len(self.controller.game.trolls)
        match trolls_placed:
            case self.controller.game.size:

                if self.cheat: #if cheat (algoritm) was used 
                    #the playingtime is drastically increased, making it ignored to not interfere with the leaderboard
                    self.controller.time.append(highscore.current_time()*2) 
                else:
                    #the main objects time list is appended with the finish time
                    self.controller.time.append(highscore.current_time())

                #total playingtime is calculated
                self.game_time()

                #button to continue to the next frame is created, lambda function sice method is not in class
                next_btn = tk.Button(self,width=20,height=10,text="next",command=lambda:self.controller.creating_postgame(self.controller.game.size))
                next_btn.grid(row=5,column=self.controller.game.size+10)
            case _:
                pass
            
    def game_time(self):
        """method calculates playingtime
        by retreving the difference in computertime when game started and finished
        """
        try:
            play_time = round((self.controller.time[1]-self.controller.time[0]),2)
            time_label = tk.Label(self,width=40,height=5,font=self.font,text=f"Congratulations, game finished in:{play_time}s")
            time_label.grid(row = 4,column=self.controller.game.size+10)
        except IndexError:
            pass

    def coloring_occupied(self):
        """coloring the occupied coordinates on the game board
        purpose is to help player see occupied coordinates
        """
        for coordinate in self.controller.game.coordinates:

            if self.controller.game.board[coordinate]:
                self.buttons[coordinate]["bg"]="white"

            elif not self.controller.game.board[coordinate]:
                self.buttons[coordinate]["bg"]="light goldenrod"

            else:
                print("error")


class Welcomemenu(tk.Frame):
    """This is a class that inherits the Frame class from tkinter,
    this will be the first page shown to the player
    here game information is shown and player info and preferences are retrieved
    """

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)#parent will be the frame container inside the object referenced by the name controller
        

        font=('Helvetica',15,'bold')

        game_info = tk.Text(self, width=60,height=15,font = font) #Places a widget that can show contents of a text document
        game_info.pack() #tkinter pack is used on this frame

        with open("game_text.txt",mode="r") as file:
            welcome = file.read()
            game_info.insert(tk.END,welcome)#inserts the contents of a text file into the 'text' widget
            file.close()
    
        question = tk.Label(self,text="What is your name?",font=font,fg="brown")
        name_entry = tk.Entry(self,width=50,font=font) #entry widget to retrive name
        
        
        #all buttons of different sizes that can be choosen to play the game on
        #labmda since method is not in the class, '.get()' retrives the variabel string inside entry widget
        size_entry_4 = tk.Button(self,text="4",bg="lime",font=font,command=lambda: controller.creating_game_board(4,name_entry.get()))
        size_entry_5 = tk.Button(self,text="5",bg="green",font=font,command=lambda: controller.creating_game_board(5,name_entry.get()))
        size_entry_6 = tk.Button(self,text="6",bg="yellow",font=font,command=lambda: controller.creating_game_board(6,name_entry.get()))
        size_entry_7 = tk.Button(self,text="7",bg="red",font=font,command=lambda: controller.creating_game_board(7,name_entry.get()))

        #pack all widgets on board
        question.pack(pady = 20)
        name_entry.pack(pady= 20) 
        size_entry_4.pack(padx=5,ipadx=20,ipady=20,side="top")
        size_entry_5.pack(padx=5,ipadx=20,ipady=20,side="top")
        size_entry_6.pack(padx=5,ipadx=20,ipady=20,side="top")
        size_entry_7.pack(padx=5,ipadx=20,ipady=20,side="top")

class Postgame(tk.Frame):
    """This is a class that inherits the Frame class from tkinter,
    this will be the last page shown to the player
    here leaderboard can be shown to the player
    and the choice to either quit or return to the main window again
    """

    #controller will be the rulign class choosing which frame to show, this is root
    def __init__(self,parent,controller,player_name,time,game_size):
        tk.Frame.__init__(self,parent)#parent will be the frame container in which this frame is placed

        self.font=('Helvetica',15,'bold')
        self.size = game_size
        self.controller = controller #making the controller calss-global
        self.player_labels = dict() 

        highscore.highscore_appending(player_name=player_name,score=time,size=game_size)#writes the finished game to the highscore csv

        leaderboard_size = tk.StringVar() #used since the optionsmenu widget is used
        leaderboard_size.set(value=game_size)
        
        leaderboard_dopdown = tk.OptionMenu(self,leaderboard_size,"4","5","6","7") #choose which leaderboard to show
        leaderboard_dopdown.pack(side="top",ipadx=20,ipady=20)

        show_leaderboard = tk.Button(self,text="Show leaderboard",font=self.font,command=lambda: self.packing_leaderboard(leaderboard_size.get()))
        show_leaderboard.pack(side="top",ipadx=10,ipady=10)

        quit_btn = tk.Button(self,text="Quit",bg="red",font=self.font,command=quit)
        quit_btn.pack(side="top",ipadx=20,ipady=15)

        back_to_menu_btn = tk.Button(self,text="Menu",bg="green",font=self.font,command = lambda: controller.switch_screen(Welcomemenu))
        back_to_menu_btn.pack(side="top",ipadx=20,ipady=15)

         

    def packing_leaderboard(self,leaderboard_size):

        dictkeys = ['highscore', 'playername','gamesize'] #keys to sort csv file
        
        self.destroying_player_labels() #destroys current leaderboard labels

        with open("highscore.csv",mode="r") as file:
            
            reader = csv.DictReader(file,fieldnames=dictkeys) #creates csv reader
            next(reader)
            i = 1
            for row in reader:
                player = row["playername"]
                time = row["highscore"]
                gamesize = row["gamesize"]

                if gamesize != leaderboard_size: #if the row does not show a score from asked game size it is ignored
                    continue
                    
                elif i <= 15: #only the top 15 are shown
                    self.player_labels[i] = tk.Label(self,text=f"{i}. '{player}' with time {time}s, with gameboard {gamesize}x{gamesize}",font=self.font)
                    self.player_labels[i].pack(side = "top")
                    i += 1

    def destroying_player_labels(self):
        """Method which destroys th currently shown leaderboard
        """
        try:
            for i in range(1,16):
                self.player_labels[i].destroy()
        except KeyError:
            pass

        

        

class Argatroll(tk.Tk):
    """this is class creates a the object referred to as 'controller throughout the program
    Object created whith this class creates a root that can controll frames created,
    in this case the created frames are Welcomemenu, Gamewindow and Postgame.
    The class inherits from the tkinter class Tk.
    """

    def __init__(self):

        #creates the root window, that will be interacted with in order to create the game 'arga troll'
        tk.Tk.__init__(self)

        self.time = []

        self.container = tk.Frame(self) #creates a frame, root is itself since it has inherited from Tk
        self.container.pack(side="top",fill="both",expand=True) #this places frame on the top, fills both ways and expands if root is resized

        self.container.grid_rowconfigure(0, weight = 1)#this configures how the rows will look, starting at 0
        self.container.grid_columnconfigure(0, weight = 1)#configures the columns in the same manner, and how they will be interacted with

        self.frame_container = {} #dictionary using class name as key and object as value
        frame1 = Welcomemenu(self.container,self) #first frame is the welcome menu

        self.frame_container[Welcomemenu] = frame1 #welcome menu frame is added to the dictionary
        frame1.grid(row = 0, column = 0, sticky ="nsew") #frame is place inside the container in top left then sticks to north,south,east,west (all sides)
        
        self.switch_screen(Welcomemenu) #calls method, changing container contents to frame1

    def creating_game_board(self,size,player_name):
        """method creates the second frame, of class Gameboard
        it uses the player info and preferences and creates firstly a gambeboard form 'argatroll.py'"""

        self.player_name = player_name
        self.time.append(highscore.current_time()) #start time is recorded

        coordinates = argatroll.coordinate_system(size) #creates a coordinate system using the game size
        array = argatroll.coordinate_values(coordinates) #connects coordinates with values of 1
        self.game = argatroll.Gameboard(size,coordinates=coordinates,array=array) #creates the object Gameboard

        frame2 = Gamewindow(self.container,self) #frame2 is created to summon object Gamewindow
        self.frame_container[Gamewindow] = frame2
        frame2.grid(row=0,column=0, sticky="nsew") #placed inside container

    def creating_postgame(self,game_size):
        """method creates the last frame
        Same proceedure as Gamewindow
        """
        frame3 = Postgame(self.container,self,self.player_name,self.time,game_size)
        self.frame_container[Postgame] = frame3
        frame3.grid(row = 0, column= 0 , sticky= "nsew")
    
    def switch_screen(self,cont):
        """method to call when wanting to swhich frame that is placed inside the container
        this is used by referencing correct key in dictionary
        """
        self.time=[]
        frame = self.frame_container[cont]
        frame.tkraise()

def main():
    """main function starts the loop to showcase the root
    """
    app_argatroll = Argatroll()
    app_argatroll.title("Arga troll")
    app_argatroll.geometry("2500x1500")
    app_argatroll.mainloop()

main()