import tkinter as tk
import turtle as tt
import time
import random
import winsound
import os

#=========================================================================================================================================================================================================================#
#MAKE WINDOWS AND CANVASES HERE
#=========================================================================================================================================================================================================================#

#Setting up and configuring our main window
root=tk.Tk()
root.title("TETRIS")
root.geometry("500x800")
root.config(bg="#e75c24")
bg=tk.PhotoImage(file="bg.png")
img=tk.Label(root,image=bg)                                                                             #Setting main window's background
img.place(x=-29,y=0)
winsound.PlaySound("music",winsound.SND_LOOP | winsound.SND_ASYNC | winsound.SND_FILENAME)

#Setting up and configuring our canvases.
game=tk.Canvas(root, width=400, height=700)                                                             #Setting canvas on which the game is played
game.grid(row=0, columnspan=6, padx=45, pady=50)
main_menu=tk.Canvas(root, width=400, height=700)                                                        #Setting main menu canvas which contains buttons, highscores, controls, etc
main_menu.grid(row=0, columnspan=6, padx=45, pady=50)
main_menu.config(bg="black")
main_menu.create_text(200,150,fill="white",text="PRESS SPACE TO START",font="fixedsys 20")
main_menu.create_text(200,200,fill="white",text="HIGHSCORES",font="fixedsys 40")
main_menu.create_text(200,650,fill="white",text="CONTROLS:\n←  or  a  TO GO LEFT\n→  or  d  TO GO RIGHT\n↑   or  w  TO ROTATE"
                                                "\np  TO PAUSE THE GAME\n(Game stays paused for 3 seconds "
                                                "after unpause)",font="fixedsys 8")
#Leaderboard file is opened and data is retrieved in a list. Even indexes represent player names and odd indexes represent player scores
f=open("leaderboard.txt","r")                                                                           
data=f.readlines()
temp=data[0].split(",")                                                                                
for i in range(len(temp)):
    if i%2==0:
        main_menu.create_text(90, 280+(i*30), fill="white", text=(temp[i],":",temp[i+1]), font="fixedsys 30",anchor="w")

#Creates a canvas displaying the credits
def credits():                                                                                         
    temp_canvas = tk.Canvas(root, width=400, height=700)
    temp_canvas.grid(row=0, columnspan=6, padx=45, pady=50)
    temp_canvas.config(bg="black")
    temp_canvas.create_text(40, 320, fill="white", text="MADE BY:\n\nAYESH AHMAD", font="fixedsys 23",anchor="w")
    def destroy():
        temp_canvas.destroy()
    btn3 = tk.Button(temp_canvas, text="\n   DONE   \n", font="fixedsys", command=destroy).place(x=160, y=470)
#Creates a canvas displaying the game details
def details():                                                                                         
    temp_canvas = tk.Canvas(root, width=400, height=700)
    temp_canvas.grid(row=0, columnspan=6, padx=45, pady=50)
    temp_canvas.config(bg="black")
    temp_canvas.create_text(35, 50, fill="white", text="GAME OBJECTIVE", font="fixedsys 30",anchor="w")
    temp_canvas.create_text(27, 160, fill="white", text="In Tetris, your goal is to stack the blocks\ninto multiple rows and destroy them."
                                                    "\n\nA row is destroyed when it is full.\n\n""Collect as many points as you can "
                                                    "before the \ngame is over to secure your position on \nthe leaderboard.\n\n"
                                                    "Destroying each row awardss you 100 points",font="fixedsys 16", anchor="w")
    temp_canvas.create_text(35, 270, fill="white", text="GAME OBSTACLES", font="fixedsys 30", anchor="w")
    temp_canvas.create_text(27, 370, fill="white", text="Throughout the game you will be presented \nwith certain obstacles.\n\nEvery 300 "
                                                    "points, the game will become \nfaster.\n\nEvery 500 points, an indestructible row "
                                                    "\nwill be added to the bottom of the grid, \nthus reducing your space", font="fixedsys 16", anchor="w")
    temp_canvas.create_text(120, 470, fill="white", text="CHEATS", font="fixedsys 30", anchor="w")
    temp_canvas.create_text(25, 570, fill="white", text="Press 'x' to skip the upcoming block.\n\nPress 'z' to slow down the game.\n"
                                                    "(Visible effect at score>300\n\nPress 'c' to destroy the bottom row\n\nPress 'ESC' "
                                                    "to minimize the game and open \na recipe for cooking brownies!", font="fixedsys 16", anchor="w")
    def destroy():
        temp_canvas.destroy()
    btn4 = tk.Button(temp_canvas, text="   DONE   ", font="fixedsys", command=destroy).place(x=160, y=655)
btn2=tk.Button(main_menu,text="\n  CREDITS  \n",font="fixedsys",command=credits).place(x=20,y=468)      #Button to display credits
btn3=tk.Button(main_menu,text="\n  DETAILS  \n",font="fixedsys",command=details).place(x=280,y=468)     #Button to display game details

#Setting our canvas which takes an input from the user for their name
user_input=tk.Canvas(root, width=200, height=300)                                                       
user_input.place(x=175,y=500)
user_input.config(bg="black")
e=tk.Entry(user_input)
e.pack()
name=''
has_run=False                                                                                           #Used to keep track of whether or not the user has entered their username

#Retrieves the text entered by the user in the Entry box and stores it into a variable called name
def store():                                                                                            
    global name,e, has_run
    if len(e.get())==3:
        name=e.get()
        user_input.destroy()
        screen.listen()
        screen.onkeypress(lambda: start_game(), "space")
        has_run=True
        return
btn=tk.Button(user_input,text="ENTER YOUR NAME\n(3 LETTERS ONLY)\n(CLICK IF DONE)",font="fixedsys",command=store).pack()

#Creating a Turtle Screen on our mainwhich the turtle will draw
screen=tt.TurtleScreen(game)
screen.setworldcoordinates(-195,-335,195,335)
screen.bgcolor("black")
screen.tracer(0)
#Creating our pen which generates blocks
pen=tt.RawTurtle(screen, visible=False)
pen.penup()
pen.speed(0)
pen.shape("square")
pen.setundobuffer(None)

#=========================================================================================================================================================================================================================#
#SHAPE CLASS
#=========================================================================================================================================================================================================================#

class Shape():
    def __init__(self):
        global shapes
        self.x=6
        self.y=0
        self.color=random.randint(1,7)                                                                  #Picks a color for the block from the color list afterwards. 0 represents a blank canvas.
        self.counter=0                                                                                  #Counter meant to keep track of the number of time rotate command was called for the shape. This counter
                                                                                                        #Used for our wiggle easter egg
        self.shape=random.choice(shapes)                                                                #Chooses a random shape each time a shape is made
        self.height=len(self.shape)                                                                     #The height of the shape is stored for later calculations
        self.width = len(self.shape[0])                                                                 #The width of the shape is stored for later calculations

    #Moves the shape left on button click
    def move_left(self,grid):                                                               
        if self.x>0 and self.can_move(grid):
            if grid[self.y+self.height][self.x-1]==0:                                                   #Only allow the movement of the block if it can move, doesn't go out of list index, and the space to its left is empty
                self.erase_shape(grid)
                self.x-=1                                                                               #x-coordinate of the shape is decremented by 1 before it is drawn again
    #Moves the shape right on button click
    def move_right(self,grid):                                                                         
        if self.x<13-self.width and self.can_move(grid):
            if grid[self.y+self.height][self.x+self.width]==0:                                          #Only allow the movement of the block if it can move, doesn't go out of list index, and the space to its right is empty
                self.erase_shape(grid)
                self.x+=1                                                                               #x-coordinate of the shape is incremented by 1 before it is drawn again
    #Draw the shape again with its updated values
    def draw_shape(self,grid):                                                                          
        for y in range(self.height):
            for x in range(self.width):
                if self.shape[y][x]==1:
                    grid[self.y+y][self.x+x]=self.color                                                 #The colors of the current position of the shape are updated to match those assigned to it
    #Erases the shape before its updated position is drawn again
    def erase_shape(self,grid):                                                                         
        for y in range(self.height):
            for x in range(self.width):
                if self.shape[y][x]==1:
                    grid[self.y+y][self.x+x]=0                                                          #The colors of the current position of the shape are updated to 0
    #Checks if the shape can move
    def can_move(self,grid):                                                                            
        hollow=False                                                                                    #Hollow is a special condition reserved for blocks whose entire bottom row is not an on bit (all 1s)
        move=True                                                                                       #The shape can move by default
        y=self.height
        x=0
        temp=0
        temp2=0
        #As long as the entire bottom row has not been checked for an off bit (0), this block of code runs
        while x!=self.width:           
            #If an off bit is found, then check for an on bit in the same x-coordinate at the above row                                                                 
            if self.shape[y-1][x]==0:         
                #If the same x-coordinate at the above row contains an on bit, hollow is made True                                                          
                if self.shape[y-2][x]==1:                                                               
                    temp=x
                    temp2=y
                    hollow=True
                    break
                y-=1                                                                                                                                         
                continue
            x+=1                                                                         
            continue
        #Uses the same logic for a normal fall but it is modified to take the hollow blocks into account.
        if hollow:                                                
            if grid[self.y+temp2-1][self.x+temp]!=0:                                                                                                                      
                    move=False
        for x in range(self.width):                                                             
            if self.shape[self.height-1][x]==1:                                                     
                if grid[self.y+self.height][self.x+x]!=0:                                             
                    move=False
        #If the next position of the block is empty, then it can move
        return move                                               
    #Rotates the shape on button click
    def rotate(self,grid):                                                                           
        global wiggle
        shape.counter+=1      
        #Fun bug made into an easter egg                                                                          
        if shape.counter>10:                                                                           
            wiggle=True
        rotated_shape=[]
        #Logic for rotating the shape (rows are turned into columns and vice versa)
        for x in range(len(self.shape[0])):                                                             
            new_row=[]
            for y in range(len(self.shape)-1,-1,-1):
                new_row.append(self.shape[y][x])
            rotated_shape.append(new_row)                                                             
        right_side=self.x+len(rotated_shape[0])
        #If the rotated shape does not go off the grid, only then erase the shape and overwrite it to match the rotated one
        if right_side<len(grid[0]):                                                                     
            self.erase_shape(grid)
            self.shape=rotated_shape
            self.height=len(self.shape)                                                               
            self.width=len(self.shape[0])
            winsound.Beep(2000, 23)

#=========================================================================================================================================================================================================================#
#GENERAL FUNCTIONS
#=========================================================================================================================================================================================================================#

#Draws our upcoming shape
def draw_upcoming(pen):                                                                                     
    pen.clear()
    top=270
    right=105
    for y in range(nshape.height):
        for x in range(nshape.width):
            if wiggle:
                pen.right(10)
            screen_x = right + (x * 20)
            screen_y = top - (y * 20)
            pen.color("white")
            if nshape.shape==horizontal:
                pen.goto(screen_x-10, screen_y-10)
            elif nshape.shape==vertical:
                pen.goto(130, screen_y+20)
            elif nshape.shape==square:
                pen.goto(screen_x+10, screen_y)
            else:
                pen.goto(screen_x, screen_y)
            if nshape.shape[y][x] == 1:
                pen.stamp()

#Draws our updated grid
def draw_grid(pen, grid):                                                                               
    pen.clear()
    draw_upcoming(pen)                                                                                 
    pen.shape("square")
    top=200
    right=-125
    colors=['black','DeepSkyBlue3','DodgerBlue4','orange','gold','green4','MediumPurple2','firebrick3',"#e75c24","snow2"]   #Colors are represented by the number of their index position
    #The grid simply consists of 12x24 20 pixel blocks which have been assigned a number and this function plots them one by one
    for y in range(len(grid)):
        for x in range(len(grid[0])):  
            #The number stored in the current index on the grid is retrieved, our color variable stores the color refered to by the number, the pen is given that color                                                                                                                          
            screen_x=right+(x*20)
            screen_y=top-(y*20)
            color_num=grid[y][x]                                                                        
            color=colors[color_num]                                                                     
            pen.color(color)                                                                            
            pen.goto(screen_x,screen_y)
            pen.stamp()

#Deletes a row and moves everything down when it is called
def del_row(grid):                                                                                      
    global delay, score, event
    y=23
    #If our clear cheat is activated then a row is deleted regardless when a shape lands on another. #It also bypasses all score conditions such as speeding up the game every 300 points and inserting an indestructible row every 500 points
    if event:                                                                                
        winsound.Beep(5000, 23)
        score += 100
        #Starting from the bottom row up, everything is copied to the next row
        for y_copy in range(23 - 1, -1,-1):                                                             
            for x_copy in range(1, 13):
                grid[y_copy + 1][x_copy] = grid[y_copy][x_copy]
        event=False                                                                                     
    while y>-1:                                                                                        
        full_row=True                                                                                   
        for x in range(0,12):
            #A row is not considered full if either a single black block is found or the row is made of indestructible blocks
            if grid[y][x]==0 or grid[y][x]==9:                                                         
                full_row=False
                y-=1
                break
        #Each time a row is cleared, add 100 points to the score
        if full_row:                                                                                   
            winsound.Beep(5000, 23)
            score+=100                            
            #Increase game speed                                                      
            if score%300==0 and delay>0.01:                                                            
                delay-=0.01
            #Starting from the bottom row up, everything is copied to the next row
            for y_copy in range(y-1,-1,-1):                                                             
                for x_copy in range(1,12):
                    grid[y_copy+1][x_copy]=grid[y_copy][x_copy]
            #If the score is divisible by 500, add an indestructible row of blocks
            if score % 500 == 0 and score != 0:                                                         
                winsound.Beep(1000, 23)
                #Starting from the top down, everything is copied to the previous row and an indestructible row is added to the very bottom
                for y_copy in range(1, 24,1):                                                           
                    for x_copy in range(1, 13):
                        grid[y_copy - 1][x_copy] = grid[y_copy][x_copy]
                        grid[y_copy][x_copy] = 9
#Displays score
def scoreboard(pen,score):                                                                              
    pen.goto(-55,235)
    pen.color("white")
    pen.write("Score:{}".format(score),move=False,align="center",font=("fixedsys",30,"normal"))
#Starts our game by destroying the main menu canvas, thus revealing the game's canvas underneath it
def start_game():                                                                                      
    global pause, p, main_menu
    #Game only starts if the game is in a pasued state and the user has enterd their name
    if p==0 and has_run==True:                                                                          
        main_menu.destroy()
        pause=False
        p=1
        return
#Pauses the game
def stop():
    global pause, p,x
    pause_menu = tk.Canvas(root, width=190, height=110)           
    #Create a canvas for our pause menu                                      
    def create():                                                                                      
        global x
        if p==1:
            pause_menu.place(x=155, y=500)
            pause_menu.config(bg="black")
            pause_menu.create_text(100, 25, fill="white", text="PAUSED", font="fixedsys 30")
            pause_menu.create_text(100, 75, fill="white", text="PRESS 'p' TO RESUME.\n YOU WILL BE GIVEN\nTHREE SECONDS UPON\n     RESUMING.", font="fixedsys 10")
            x=pause_menu                                                                              
        if p==0:                                                                                      
            x.destroy()
            pause_menu.destroy()
    if p==1:
        create()
        pause=True
        p=0
        return
    if p==0:
        create()
        time.sleep(3)                                                                     
        pause=False
        p=1
        return
#Skips the upcoming shape
def skip():                                                                                             
    global nshape
    nshape=Shape()
#Resets our delay to 0.07 (slows down game)
def slow():                                                                                             
    global delay
    delay=0.07
#Makes event=True, which determines whether or not the bypass conditions/del row cheat is activated
def clear():                                                                                            
    global event
    event=True
#Minimizes our game and displays a recipe for cooking brownies upon pressing escape
def bosskey(event):                                                                                     
    global first_run
    if first_run:
        stop()
        root.iconify()
        tt.bgpic("brownies.png")
        first_run=False
        return
    if first_run==False and pause==False:
        stop()
        first_run=True
        return
root.bind('<Escape>',lambda event: bosskey(event))
#Restarts our game
def restart_program():                                                                                  
    global root
    root.destroy()
    os.startfile("Tetris.py")

#=========================================================================================================================================================================================================================#
#UNIVERSAL VARIABLES
#=========================================================================================================================================================================================================================#

delay=0.06                                                                                              
grid=[                                                                                                  #Tetris Grid
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,8,8,8,8,8,8,8,8,8,8,8,8,8],
]       
#Starting co-ord is (0,0) and last co-ord is (13,24) written into seperate lines for ease in understanding                                                                                                
square=[[1,1],                                                                                       
        [1,1]]
horizontal=[[1,1,1,1]]
vertical=[[1],
          [1],
          [1],
          [1]]
Lleft=[[1,0,0],
       [1,1,1]]
Lright=[[0,0,1],
        [1,1,1]]
Zright=[[0,1,1],
        [1,1,0]]
Zleft=[[1,1,0],
       [0,1,1]]
t=[[0,1,0],
   [1,1,1]]
shapes=[square,horizontal,vertical,Lleft,Lright,Zright,Zleft,t]
shape=Shape()                                                                                           #Creates our current shape
nshape=Shape()                                                                                          #Creates our next shape
score=0                                                                                                 #Initializing the score
run=True                                                                                                #Allows our game to run in a while loop
p=0                                                                                                     #Determines the current pause state of the game
pause=True                                                                                              #Determines whether or not the game should be paused
wiggle=False                                                                                            #Determines whether or not the blocks will wiggle (easter-egg)
counter=0                                                                                               #Keeps track of the number of times the rotate function was called, used for wiggle
event=False                                                                                             #Keeps track of whether or not the clear cheat key has been activated
x=None                                                                                                  #Used to temporarily hold the canvas created when the game is paused.
first_run=True                                                                                          #Used in bosskey

#=========================================================================================================================================================================================================================#
#CONTROLS
#=========================================================================================================================================================================================================================#

screen.listen()
screen.onkeypress(lambda: shape.move_left(grid),"a")                                                    #Move shape left
screen.onkeypress(lambda: shape.move_left(grid),"Left")
screen.onkeypress(lambda: shape.move_right(grid),"d")                                                   #Move shape right
screen.onkeypress(lambda: shape.move_right(grid),"Right")
screen.onkeypress(lambda: shape.rotate(grid),"w")                                                       #Rotate shape
screen.onkeypress(lambda: shape.rotate(grid),"Up")
screen.onkeypress(lambda: start_game(),"space")                                                         #Start game
screen.onkeypress(lambda: stop(),"p")                                                                   #Pause game
screen.onkeypress(lambda: skip(),"x")                                                                   #Skip upcoming block                                                                            (CHEAT)
screen.onkeypress(lambda: slow(),"z")                                                                   #Slow down the game                                                                             (CHEAT)
screen.onkeypress(lambda: clear(),"c")                                                                  #Clear bottom row upon a block landing and prevent score%300 and score%500 events from occuring (CHEAT)

#=========================================================================================================================================================================================================================#
#MAIN GAME LOOP
#=========================================================================================================================================================================================================================#

while run:
    screen.update()                                                                                     #Updates the turtle screen
    if pause==False:                                                                                    #Game will run if and only if it is not paused
        if shape.y==23-shape.height+1:                                                                  #If the shape is in the last row (can't fall further) then run this
            shape=nshape                                                                                #Our current shape is made into our previous upcoming shape
            nshape=Shape()                                                                              #Our upcoming shape is updated into another one
            del_row(grid)                                                                               #Checks if a row can be deleted or if the clear cheat has been triggered
        if shape.can_move(grid):                                                                        #If the shape can move, then run this
            shape.erase_shape(grid)
            shape.y+=1                                                                                  #The shape's y-coordinate is moved down one block on the grid
            shape.draw_shape(grid)
        else:                                                                                           #If it is neither the last row nor is there space after the current position, the run this
            if shape.y==0:                                                                              #If the block's y-coordinate is 0 (top of the grid), then it has overflown and the game is over
                f=open("leaderboard.txt","r")                                                           #Leaderboard file is opened (contains old highscores and player names)
                data=f.readlines()
                temp=data[0].split(",")                                                                 #File data is retrieved in a list
                for i in range(1,len(temp),2):                                                          #Scores are reviewed in descending order and replaced where needed.
                    if score>=int((temp[i])):
                        if i==5:
                            temp[i] = str(score)
                            temp[i-1]=name
                            break
                        if i==3:
                            temp[i + 2] = temp[i]
                            temp[i+1]=temp[i-1]
                            temp[i] = str(score)
                            temp[i - 1] = name
                            break
                        if i==1:
                            temp[i+4]=temp[i+2]
                            temp[i+3]=temp[i+1]
                            temp[i+2]=temp[i]
                            temp[i + 1] = temp[i - 1]
                            temp[i]=str(score)
                            temp[i - 1] = name
                            break
                f=open("leaderboard.txt","w")
                f.writelines(",".join(temp))                                                            #File is re-written with updated scores
                f.close()
                tk.messagebox.showwarning(title="Game Over!",message="You were not able to destroy the rows in time :(")        #Tells the user that the game is over and then the game is restarted
                restart_program()
            shape=nshape                                                                                #If the block can neither move nor is its y-coorindate 0, then make out current shape into the upcoming one
            nshape=Shape()                                                                              #Make our upcoming shape into a new one
            del_row(grid)                                                                               #Checks if there is a row that can be deleted at the end of each loop

        #Final display based on all previous events in the loop
        draw_grid(pen, grid)
        scoreboard(pen, score)
        time.sleep(delay)

#mainloop
root.mainloop()
