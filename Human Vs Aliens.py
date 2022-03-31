from sre_parse import State
import tkinter as tk
import string #for a string to store alphabet
import os, sys #help with importing images
from PIL import Image, ImageTk #help with implementing images into GUI
from PIL.ImageTk import PhotoImage
import random
from tkinter import messagebox

# from numpy import piecewise

class Board(tk.Frame):

    def __init__(self, parent, length, width): #self=Frame, parent=root        
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.length = length    
        self.width = width
        self.config(height=100*self.length, width=100*self.width)
        self.pack()
        self.points=0
        self.protected=0
        self.deadpcs=[]
        self.label = tk.Label(self,text="",font=("Helvetica",100))
        self.label.grid(rowspan=8,column=0,padx=5)
        self.humanpoint=0
        self.alienpoint=0
        self.square_color = None
        self.squares = {} #stores squares with pos as key and button as value
        self.ranks = string.ascii_lowercase
        self.white_images = {} #stores images of pieces
        self.black_images = {}
        self.white_pieces = ["pyimage1"] #for convenience when calling all white pieces
        self.black_pieces = ["pyimage3"]
        self.dice_pieces = ["\u2680","\u2681","\u2682","\u2683","\u2684","\u2685"]
        self.locked_pieces={} 
        self.buttons_pressed = 0
        self.turns = 0
        self.cp=1
        self.sq1 = None #first square clicked
        self.sq2 = None 
        self.sq1_button = None #button associated with the square clicked
        self.sq2_button = None
        self.piece_color = None
        self.dice=0
        
        self.set_squares()
        self.info = tk.Label(self,text=f"Turn: {self.getplayer()}",font=("Helvetica",10))
        self.info.grid(row=6,column=0,padx=1)
        self.win = tk.Label(self,text="",font=("Arial Bold",10))
        self.win.grid(row=1,rowspan=2,column=0)
        self.score = tk.Label(self,text="REMEMBER: Human do not listen the first time. So you have to click twice to make/select them listen to you.\nThis sucks but thats how stubborn humans are...\n\nDeveoped by Prabhjee Singh")
        self.score.grid(row=20, column=2,columnspan=10)
        self.status = tk.Label(self,text=f"",font=("Arial Bold",10))
        self.status.grid(row=10,rowspan=5,column=1,columnspan = 10)


    def roll_dice(self):
        if (self.checkwin()==False):
            d1=random.choice(self.dice_pieces)
            self.dice=d1       
            self.label.config(text=d1)
            self.stop=False
            self.square_color=None
            self.info.config(text=f"Turn: {self.getplayer()}")
            self.buttons_pressed=0
            self.win.config(text=f"ScoreBoard:\nPlayer 1 (Aliens) : {self.alienpoint}\n    Player 2 (Humans) : {self.humanpoint} ")
            board.gameplay()
            # print("w",self.alienpoint,"h",self.humanpoint)
            # print("dead: ", self.deadpcs)

#   print(self.locked_pieces)
    def checkwin(self):
        if(self.alienpoint>=4):
            self.win.config(text="Team Aliens Wins")
            tk.messagebox.showinfo("YaY!","Team Aliens Wins! Forget the Earth (or save environment)")
            return True
        elif(self.humanpoint>=4):
            self.win.config(text="Team Humans Wins")
            tk.messagebox.showinfo("YaY!","Team Humans Wins! You have Successfully defended yourself \n (in game not in reality so better start replenishing the environment)")
            return True
        else:
            return False


    def select_piece(self, button): #called when a square button is pressed, consists of majority of the movement code
        print(f"select piece {self.buttons_pressed} button {button['image']}")
        if button["image"] == "pyimage1" and self.buttons_pressed == 0: #checks color of first piece
            self.piece_color = "white"
        elif button["image"] == "pyimage2" and self.buttons_pressed == 0:
            self.piece_color = "black"      
        player =  self.getplayer()
        print(f"player = {player} , color = {self.piece_color},stop = {self.stop}")

#   preventing people from moving their pieces when it's not their turn     
        if(self.stop==False):
            if(self.piece_color=="white"and player=='p2' ) or (self.piece_color=="black"and player=='p1'):
                if self.buttons_pressed == 0: #stores square and button of first square selected
                    self.sq1 = list(self.squares.keys())[list(self.squares.values()).index(button)] #retrieves pos of piece
                    self.sq1_button = button
                    self.buttons_pressed += 1
                    print("button pressed =",self.buttons_pressed)
                    
                elif self.buttons_pressed==1: #stores square and button of second square selected
                    self.sq2 = list(self.squares.keys())[list(self.squares.values()).index(button)]
                    self.sq2_button = button
                    print("2nd button pressed",self.buttons_pressed)
                    if self.sq2 == self.sq1: #prevents self-destruction and allows the user to choose a new piece
                        self.buttons_pressed = 0
                        return 
                    wk="pyimage1"
                    bk="pyimage3"
                    # print(self.friendly_fire(),self.checklocked(self.sq1))
                    
                    if(self.checklocked(self.sq1)==0 and self.friendly_fire()==False):
                        print("entered")
                        if(self.dice=='\u2680'): #1
                            if self.sq1_button["image"] ==  wk or self.sq1_button["image"] == bk: #king movement
                                if (abs(int(self.sq1[1]) - int(self.sq2[1])) < 2) and (abs(self.ranks.find(self.sq1[0]) - self.ranks.find(self.sq2[0]))) < 2: #allows 1 square moves
                                    self.collectPoints()
                                    self.squares[self.sq2].config(image=self.sq1_button["image"]) #moves pice in sq1 to sq2                    self.squares[self.sq2].image = self.sq1_button["image"]
                                    self.squares[self.sq1].config(image=self.white_images["blank.png"]) #clears sq1
                                    self.squares[self.sq1].image = self.white_images["blank.png"]
                                    self.status.config(text="Status: Character successfully moved")
                                    
                                    self.stop=True
                                    self.buttons_pressed=0
                                    # self.turns+=1
                                    return 1
                        
                        elif(self.dice=='\u2681'): #2
                            if self.sq1_button["image"] ==  "pyimage1" or self.sq1_button["image"] == "pyimage3": #king movement
                                if (abs(int(self.sq1[1]) - int(self.sq2[1])) == 2) and (abs(self.ranks.find(self.sq1[0]) - self.ranks.find(self.sq2[0]))) ==2: #allows 1 square moves
                                    self.collectPoints()
                                    self.squares[self.sq2].config(image=self.sq1_button["image"]) #moves pice in sq1 to sq2                    self.squares[self.sq2].image = self.sq1_button["image"]
                                    self.squares[self.sq1].config(image=self.white_images["blank.png"]) #clears sq1
                                    self.squares[self.sq1].image = self.white_images["blank.png"]
                                    self.stop=True
                                    self.status.config(text="Status: Character Successfully moved")
                                    self.buttons_pressed=0
                                    # self.turns+=1
                                    return 1
                
                        elif self.dice=='\u2683':#4
                            if self.sq1_button["image"] ==  wk or self.sq1_button["image"] == bk: #king movement
                                if (abs(int(self.sq1[1]) - int(self.sq2[1])) < 2) and (abs(self.ranks.find(self.sq1[0]) - self.ranks.find(self.sq2[0]))) < 2: #allows 1 square moves
                                    self.collectPoints()
                                    self.squares[self.sq2].config(image=self.sq1_button["image"]) #moves pice in sq1 to sq2                    self.squares[self.sq2].image = self.sq1_button["image"]
                                    self.squares[self.sq1].config(image=self.white_images["blank.png"]) #clears sq1
                                    self.squares[self.sq1].image = self.white_images["blank.png"]
                                    
                                    self.status.config(text="Status: Character successfully moved")
                                    self.stop=True
                                    self.buttons_pressed=0
                                    # self.turns+=1
                            return 1
                
                        # elif self.dice=='\u2684':#5
                        #     # self.turns += 1
                            
                            
                        #     return 1 
                    

                    elif(self.checklocked(self.sq1)==1):
                        # self.turns += 1
                        self.status.config(text="Status: Character is locked")
                        if(self.dice=='\u2685'):#6
                            # print("6",self.getplayer(),self.sq1_button["image"])
                            if (self.getplayer()=='p2'and self.sq1_button["image"]=="pyimage1") or ( self.sq1_button["image"]=="pyimage3" and self.getplayer()=='p1'):
                                print("Hello")
                                if (abs(int(self.sq1[1]) - int(self.sq2[1])) < 2) and (abs(self.ranks.find(self.sq1[0]) - self.ranks.find(self.sq2[0]))) < 2: #allows 1 square moves
                                    self.locked_pieces.pop(self.sq1)
                                    self.status.config(text="Status: Character Unlocked")
                                    self.collectPoints()
                                    self.squares[self.sq2].config(image=self.sq1_button["image"]) #moves pice in sq1 to sq2                    self.squares[self.sq2].image = self.sq1_button["image"]
                                    self.squares[self.sq1].config(image=self.white_images["blank.png"]) #clears sq1
                                    self.squares[self.sq1].image = self.white_images["blank.png"]
                                    self.stop=True
                                    self.buttons_pressed=0
                                    return 1
                        
                        elif self.dice=='\u2683':#4
                            # print(self.sq1,self.locked_pieces)
                            if(self.sq1 in self.locked_pieces):
                                self.locked_pieces.pop(self.sq1)
                                self.stop=True
                                self.status.config(text="Status: Character Unlocked")
                            self.buttons_pressed=0
                            
                    else:print("nono")
                    
                    self.buttons_pressed=0
                    return 1
                        # if self.allowed_piece_move(self.dice) and self.friendly_fire() == False: #makes sure the move is legal
                        # prev_sq1 = self.sq1
                        # prev_sq1_button_piece = self.sq1_button["image"]
                        # prev_sq2 = self.sq2
                        # prev_sq2_button_piece = self.sq2_button["image"]
                        # self.squares[self.sq2].config(image=self.sq1_button["image"]) #moves pice in sq1 to sq2                    self.squares[self.sq2].image = self.sq1_button["image"]
                        # self.squares[self.sq1].config(image=self.white_images["blank.png"]) #clears sq1
                        # self.squares[self.sq1].image = self.white_images["blank.png"]
                        # print("last")
        else:
            self.buttons_pressed = 0
            return

    def collectPoints(self):
        if (self.sq1_button["image"]=="pyimage1" and self.sq2_button["image"]=="pyimage3"):
            self.deadpcs.append("pyimage3")
            self.alienpoint+=1
        elif(self.sq1_button["image"]=="pyimage3" and self.sq2_button["image"]=="pyimage1"):
            self.deadpcs.append("pyimage1")
            self.humanpoint+=1    

    def friendly_fire(self): #prevents capturing your own pieces
        piece_2_color = self.sq2_button["image"]
        if self.piece_color == "white" and piece_2_color in self.white_pieces:
            return True
        if self.piece_color == "black" and piece_2_color in self.black_pieces:
            return True
        else:
            return False
        
  
    
    

    def checklocked(self,sq):
        # print("sq=",sq,"lock up =",self.locked_pieces)
        if sq in self.locked_pieces:
            return 1
        else:
            return 0

    def enableButtons(self):
        print("enable")
        for keys,value in self.squares.items():
            self.squares[keys].config(state = tk.NORMAL,command = lambda key = self.squares[keys]:self.select_piece(key))
            
    def disableButtons(self):
        for keys,value in self.squares.items():
            self.squares[keys].config(state = tk.DISABLED) 

    def set_squares(self): #fills frame with buttons representing squares
        self.Dice_B = tk.Button(self, text="Roll Dice",state=tk.DISABLED,command=self.roll_dice)
        self.Dice_B.grid(row=8,column=0)
        for x in range(8):
            for y in range(8):
                if x%2==0 and y%2==0: #alternates between dark/light tiles
                    self.square_color="tan2"
                    if (x==0 and y==6) or (x==6 and y==0):
                        self.square_color="tan4"
                        
                elif x%2==1 and y%2==1:    
                    self.square_color="tan2"
                    if (x==7 and y==1) or (x==1 and y==7):
                        self.square_color="tan4" 
                
                else:
                    self.square_color="burlywood1"
                    if (x==0 and y==7) or (x==1 and y==6):
                        self.square_color="tan4"
                    elif(x==6 and y==1) or (x==7 and y==0):
                        self.square_color="tan4"
                    
                B = tk.Button(self, bg=self.square_color, activebackground="lawn green")
                B.grid(row=8-x, column=y+2)
                # print(8-x,y)
                pos = self.ranks[y]+str(x+1)
                if(self.square_color=="tan4"):
                    self.locked_pieces[pos]=B
                self.squares.setdefault(pos, B) #creates list of square positions
                
                self.squares[pos].config(state=tk.DISABLED) 
        # print(self.squares)    

    def getplayer(self):
        if(self.turns==-1):
            return "None"
        elif(self.turns%2==0):
            return "p1"
        else:
            return "p2"
    
    #Defines the gameplay of the game
    def gameplay(self):  
        # while(self.points<6):
        
        print("turns = ",self.turns)
        if(self.turns == 0):
            self.status.config(text="Status: Game Started")
        if(self.turns %2 == 0):
            print("Player 1's Turn Aliens")
            point = self.startround(1)
            
        elif(self.turns%2!=0):
            print("Player 2's turn humans")
            point =self.startround(2)
            

    def startround(self,p):
        self.Dice_B.config(state=tk.NORMAL)
        # print("nothing"+ self.dice)
        # print( self.dice )
        d1= self.dice
        # print(d1)
        print(self.turns)
        if(d1=='\u2680'): #For die 1 
            self.status.config(text="Status: Select the character and the location to move ")
            self.turns += 1 
            self.enableButtons()
            
            return 1 

        elif d1=='\u2681':
            self.status.config(text="Status: Select the character and the location to move (Diagonal and 2 move)")
            self.enableButtons()
            self.turns += 1
            return 1

        elif d1=='\u2682':
            self.status.config(text="Status: Your characters got stunned by \"Stupefy\" Enchantment lol")
            self.disableButtons()
            self.turns += 1 
            return 1

        elif d1=='\u2683':
            self.status.config(text="Status: Select the character and another square to unlock or move your character by 1 sq")
            self.enableButtons()
            self.turns += 1 
            return 

        elif d1=='\u2684':
            self.status.config(text="Status: Wait! Stopped time,Strange huh Dr.,... Reading Enchantment! Mobilicorpus!!!")
            self.disableButtons()
            # if(self.getplayer()=='p2'):
            pos=random.choice(list(self.squares.keys()))
            B= self.squares.get(pos)["image"]
            print(pos,B)
            if(self.getplayer()=='p1'):
                if("pyimage1" in self.deadpcs):
                    if(B=='pyimage2'):
                        self.squares[pos].config(image="pyimage1")
                        self.deadpcs.remove("pyimage1")
                        self.status.config(text="Status: It worked, Believe it, Check {pos}")
                    else:
                        self.status.config(text="Status: That's unlucky Better Luck Next Time")
            elif(self.getplayer()=='p2'):
                if("pyimage3" in self.deadpcs):
                    if(B=='pyimage2'):
                        self.squares[pos].config(image="pyimage3")
                        self.deadpcs.remove("pyimage3")
                        self.status.config(text="Status: It worked, Believe it, Check {pos}")
                    else:
                        self.status.config(text="Status: That's unlucky Better Luck Next Time")
            self.turns += 1
            return 1 

        elif d1=='\u2685':
            self.status.config(text="Status: U may now unlock Ur character")
            self.sixdie()
            self.turns += 1 
            return 1
        else:
            return 0
                             
    def sixdie(self): 
        self.enableButtons()
        # print("oops")
        return self.enableButtons()
        




    def import_pieces(self): #opens and stores images of pieces and prepares the pieces for the game for both sides
        path = os.path.join(os.path.dirname(__file__), "Alien") #stores white pieces images into dicts
        w_dirs = os.listdir(path)
        for file in w_dirs:
            img = Image.open(path+"\\"+file)
            img = img.resize((80,80), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(image=img)
            self.white_images.setdefault(file, img)

        path = os.path.join(os.path.dirname(__file__), "Human") #stores black pieces images into dicts
        b_dirs = os.listdir(path)
        for file in b_dirs:
            img = Image.open(path+"\\"+file)
            img = img.resize((80,80), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(image=img)
            self.black_images.setdefault(file, img)

    def set_pieces(self): #places pieces in starting positions
        
        #assigning positions with their default pieces
        self.dict_rank2_pieces = {"a7":"b.png", "a8":"b.png", "b7":"b.png", "b8":"b.png"} 
        self.dict_rank1_pieces = {"g1":"alien.png", "g2":"alien.png","a1":"blank.png", "h1":"alien.png", "h2":"alien.png"}     
        self.dict_rank7_pieces = { "a1":"blank.png","a2":"blank.png","b1":"blank.png","b2":"blank.png","c1":"blank.png","c2":"blank.png"
        ,"c2":"blank.png","c7":"blank.png","c8":"blank.png","d1":"blank.png","d2":"blank.png","d7":"blank.png"
        ,"d8":"blank.png","g7":"blank.png","g8":"blank.png","e1":"blank.png","e2":"blank.png","e7":"blank.png"
        ,"e8":"blank.png","f7":"blank.png","f8":"blank.png","f1":"blank.png","f2":"blank.png","h7":"blank.png","h8":"blank.png"}     

   
   
        for key in self.dict_rank1_pieces: #inserts images into buttons
            starting_piece = self.dict_rank1_pieces[key]
            self.squares[key].config(image=self.white_images[starting_piece])
            self.squares[key].image = self.white_images[starting_piece]
            
        for key in self.dict_rank2_pieces:
            starting_piece = self.dict_rank2_pieces[key]
            self.squares[key].config(image=self.black_images[starting_piece])
            self.squares[key].image = self.black_images[starting_piece]
            
        for key in self.dict_rank7_pieces:
            starting_piece = self.dict_rank7_pieces[key]
            self.squares[key].config(image=self.white_images[starting_piece])
            self.squares[key].image = self.white_images[starting_piece]
            
  
        for rank in range(3,7): #fill rest with blank pieces
            for file in range(8):
                starting_piece = "blank.png"
                pos = self.ranks[file]+str(rank)
                # print(pos)
                self.squares[pos].config(image=self.white_images[starting_piece])
                self.squares[pos].image = self.white_images[starting_piece]

root = tk.Tk() #creates main window with the board and creates board object
root.geometry("900x900")
board = Board(root, 8, 8)
root.title("Human vs. Aliens")
board.import_pieces()

board.set_pieces()  
board.roll_dice()
tk.messagebox.showinfo("If U Don't Know, Now You Know","Aliens came to Earth to replenish the Earth,\n\nNow they are taking the matter to next level by making Homo-Sapiens(Humans) their Slaves \n\n\nIf you are human & want to Make Aliens Slaves,\nThen select human & win this CIVIL WAR \n\n( PS: There is Nothing CIVIL about it :X)")
tk.messagebox.showinfo("Did You Just pressed OK? :0 Press Again :D","Moral is Earth will be saved either way \nIts you who would decide who will be slave of who. \n\nPlayer 1: Aliens       Player2: Humans\n\nThis game is developed by Prabhjee Singh")

# board.gameplay()        
board.mainloop()
