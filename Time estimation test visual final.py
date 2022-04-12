#import required libraries
import os
import random
import numpy
import tkinter as tk
from tkinter import filedialog
from tkinter.constants import BOTTOM, TOP
from tkinter.filedialog import asksaveasfile
import pandas as pd
from psychopy import visual
from psychopy import event
from psychopy import core
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB']
from psychopy.sound.backend_ptb import SoundPTB
#################################################################
#################################################################


times_between_first_last_rectangles=[0.800,1.000,1.200] 
number_shapes_between_first_last_rectangles=[0,1,2]
colors_between_first_last_rectangles=[0,1] #0 means all colors are similar, 1 means between_shapes have different colors
shapes_between_first_last=[2,3] #2 means all shapes are similar, 3 means between_shapes are different
all_together=[[0.800,1.000,1.200],[0,1,2],[0,1],[2,3]] 

# define insert box
fields = 'Last Name', 'First Name', 'Age', 'Gender', 'Education'
information=[]
def fetch(entries):
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        information.append(text)
        print('%s: %s' % (field, text)) 

def makeform(root, fields):
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries

if __name__ == '__main__':
    root = tk.Tk()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
    b1 = tk.Button(root, text='Save',
                  command=(lambda e=ents: fetch(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text='Start', command=root.destroy)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()

    
#################################################################


#define a white screen
win = visual.Window(size=[1200, 800],units="pix",fullscr=True,color=[1, 1, 1])

#define a beep using psychtoolbox sound motor withfrequency=1000 and duration=0.05 sec
mainSound = SoundPTB(value=1000, secs=0.05)

#made mouse invisible 
event. Mouse(visible=False)


#difine a function to show a message with a specific position and size
def myText(message,position,size):
    text=visual.TextStim(win, text=message, 
        color=(-1, -1, -1),pos=position, units="pix", height=size, wrapWidth=1000)
    text.draw()

#define a shape with a specific color and vertices
# the shape type depends on the vertices
def myShape(fill_color, shape_vertices):
    shape=visual.shape.ShapeStim(win, units='pix', colorSpace='rgb', 
        fillColor=fill_color, lineColor='white', lineWidth=2.5,
        vertices=(shape_vertices),closeShape=True, pos=(0,0), size=350, ori=0.0, opacity=0.6)
    shape.draw()

#define a global function=exit program for 'Escape'
key='escape'
def sysExit():
    os._exit(1)
event.globalKeys.add(key=key, func=sysExit)

#show a text
myText('Test 1',(0,0),100)
win.flip()
core.wait(4)

data_interval=[]

myText('At each trial, a number of shapes appear consecutively on the screen. Please note the time interval between the first and last red rectangle.',(0,20),50)
myText('Press Enter to continue!',(0,-200),30)

win.flip()
#wait until the enter key is pressed
event.waitKeys(keyList='return')
core.wait(2)

for h in range (0,3):  #3 repeats
    
    #define all possible combinations of elements in the all_together list. It is 3*3*2*2=36 possible combinations.    
    myList_interval=[list(x) for x in numpy.array(numpy.meshgrid(*all_together)).T.reshape(-1,len(all_together))]
    
    #36 cycles
    for i in range (0,36):  

        #randomly select an element from 36 elements
        mySelectedElement_interval=random.choice(myList_interval)
                
        #each selected element has 4 sub-elements with indecses from 0 to 3        
        miliSecond_interval=mySelectedElement_interval[0]
        trial_interval=int(mySelectedElement_interval[1])
        complexity_interval=mySelectedElement_interval[2]
        shape_interval=mySelectedElement_interval[3]
        
        #calculate the time interval between two consecutive shapes
        interval_interval=((miliSecond_interval-0.1)-(trial_interval*0.1))/(trial_interval+1) 
        
        #a white screen for 2 sec
        win.flip()
        core.wait(2)
        
        #show the first red rectangle for 0.1 sec
        myShape('red',((-0.5,0.5), (-0.5,-0.5), (0.5,-0.5), (0.5,0.5))) #red rect
        win.flip()
        core.wait(0.1)
        
        #a white screen
        win.flip()
        core.wait(interval_interval)
        
        
        if trial_interval==0 and complexity_interval==0 and shape_interval==2:  #just two red rectangles
            win.flip()
            core.wait(interval_interval)
        elif trial_interval>0 and complexity_interval==0 and shape_interval==2:  #two red rectangles with one or two red rectangles between them
            for j in range (0,trial_interval):
                myShape('red',((-0.5,0.5), (-0.5,-0.5), (0.5,-0.5), (0.5,0.5))) #red rect
                win.flip()
                core.wait(0.1)
                win.flip()
                core.wait(interval_interval)
        elif trial_interval>0 and complexity_interval==1 and shape_interval==2: #two red rectangles with one or two rectangles with black or green colors between them
            possible_interval_color=['black','green']
            for j in range (0,trial_interval):
                interval_color=random.choice(possible_interval_color)
                myShape(interval_color,((-0.5,0.5), (-0.5,-0.5), (0.5,-0.5), (0.5,0.5)))
                win.flip()
                core.wait(0.1)
                win.flip()
                core.wait(interval_interval)
                possible_interval_color.remove(interval_color)
        elif trial_interval>0 and complexity_interval==0 and shape_interval==3: #two red rectangles with one or two red shapes between them
            possible_interval_shape=[((0,0.5), (-0.5,-0.5), (0.5,-0.5)),
                                        ((0,0.5), (-0.5,0), (0,-0.5),(0.5,0))] #triangle, diamond
            for j in range (0,trial_interval):
                interval_shape=random.choice(possible_interval_shape)
                myShape('red',interval_shape)
                win.flip()
                core.wait(0.1)
                win.flip()
                core.wait(interval_interval)
                possible_interval_shape.remove(interval_shape)
        elif trial_interval>0 and complexity_interval==1 and shape_interval==3: #two red rectangles with one or two rectangles with black or green color between them
            possible_interval_color=['black','green']
            possible_interval_shape=[((0,0.5), (-0.5,-0.5), (0.5,-0.5)),
                                        ((0,0.5), (-0.5,0), (0,-0.5),(0.5,0))] #triangle, diamond
            for j in range (0,trial_interval):
                interval_color=random.choice(possible_interval_color)
                interval_shape=random.choice(possible_interval_shape)
                myShape(interval_color,interval_shape)
                win.flip()
                core.wait(0.1)
                win.flip()
                core.wait(interval_interval)
                possible_interval_color.remove(interval_color) #remove the randomly selected color from the list to prevent replacement
                possible_interval_shape.remove(interval_shape) #remove the randomly selected shape from the list to prevent replacement
        
        #show the last red rectangle for 0.1 sec
        myShape('red',((-0.5,0.5), (-0.5,-0.5), (0.5,-0.5), (0.5,0.5))) #red rect
        win.flip()
        core.wait(0.1)
        win.flip()
        core.wait(2)
        
        myText('Now press the space bar two times at the interval equal to the time interval between the first and last red rectangle.',(0,40),50)
        win.flip()

        response_interval=[] # difine an empty list 
        response_interval.append(trial_interval) # append trial to the list
        
        event.clearEvents() # clear all previus key presses

        spacePressed=0 
        while spacePressed<2:
            for click in range (len([0,1,2])):
                if event.getKeys(keyList='space'): #if space was pressed
                    mainSound.play() #play the sound 
                    response_interval.append(core.getTime()) #register the time of key press
                    spacePressed=spacePressed+1
                    core.wait(0.2) #wait fo 0.2 second
                    break

        #register time interval between two space presses
        diff_list_interval = [] 
        diff_list_interval.append(trial_interval)
        diff_list_interval.append(miliSecond_interval)
        for x, y in zip(response_interval[1::], response_interval[2::]):
            diff_list_interval.append(y-x)
            diff_list_interval.append(complexity_interval)
            diff_list_interval.append(shape_interval)
        data_interval.append(diff_list_interval)
        
        core.wait(2)
        #remove the randomly selected pair from the list to prevent replacement  
        myList_interval.remove(mySelectedElement_interval) 

df_interval=pd.DataFrame(data_interval)
df_interval[5] = df_interval[2]-df_interval[1] #define a new column which is the subtraction of two other columns
df_interval[6]=pd.Series(information) #append information as a new column with different number of rows

#################################################################
#################################################################
#################################################################

myText('Test 2',(0,0),100)
win.flip()
core.wait(4)

data_number_interval=[]

myText('In this test, please note both the number of shapes that appear on the screen at each trial and the time interval between each two consecutive shapes.',(0,20),50)
myText('Press Enter to continue!',(0,-200),30)

win.flip()
event.waitKeys(keyList='return')
core.wait(2)

for h in range (0,3):  #3 repeats

    myList_number_interval=[list(x) for x in numpy.array(numpy.meshgrid(*all_together)).T.reshape(-1,len(all_together))]
        
    #36 cycles
    for i in range (0,36): 
        
        mySelectedElement_number_interval=random.choice(myList_number_interval)
        
        miliSecond_number_interval=mySelectedElement_number_interval[0]
        trial_number_interval=int(mySelectedElement_number_interval[1]) 
        complexity_number_interval=mySelectedElement_number_interval[2]
        shape_number_interval=mySelectedElement_number_interval[3]

        #calculate the time interval between two consecutive rects
        interval_number_interval=((miliSecond_number_interval-0.1)-(trial_number_interval*0.1))/(trial_number_interval+1) 
        Expected_tapping_interval=(miliSecond_number_interval-0.1)/(trial_number_interval+1) 
        
        win.flip()
        core.wait(2)
        
        myShape('red',((-0.5,0.5), (-0.5,-0.5), (0.5,-0.5), (0.5,0.5))) #red rect
        win.flip()
        core.wait(0.1)
        win.flip()
        core.wait(interval_number_interval)

        
        if trial_number_interval==0 and complexity_number_interval==0 and shape_number_interval==2:
            win.flip()
            core.wait(interval_number_interval)
        elif trial_number_interval>0 and complexity_number_interval==0 and shape_number_interval==2:
            for j in range (0,trial_number_interval):
                myShape('red',((-0.5,0.5), (-0.5,-0.5), (0.5,-0.5), (0.5,0.5))) #red rect
                win.flip()
                core.wait(0.1)
                win.flip()
                core.wait(interval_number_interval)
        elif trial_number_interval>0 and complexity_number_interval==1 and shape_number_interval==2:
            possible_number_interval_color=['black','green']
            for j in range (0,trial_number_interval):
                interval_color=random.choice(possible_number_interval_color)
                myShape(interval_color,((-0.5,0.5), (-0.5,-0.5), (0.5,-0.5), (0.5,0.5)))
                win.flip()
                core.wait(0.1)
                win.flip()
                core.wait(interval_number_interval)
                possible_number_interval_color.remove(interval_color)
        elif trial_number_interval>0 and complexity_number_interval==0 and shape_number_interval==3:
            possible_number_interval_shape=[((0,0.5), (-0.5,-0.5), (0.5,-0.5)),
                                        ((0,0.5), (-0.5,0), (0,-0.5),(0.5,0))] #triangle, diamond
            for j in range (0,trial_number_interval):
                interval_shape=random.choice(possible_number_interval_shape)
                myShape('red',interval_shape)
                win.flip()
                core.wait(0.1)
                win.flip()
                core.wait(interval_number_interval)
                possible_number_interval_shape.remove(interval_shape)
        elif trial_number_interval>0 and complexity_number_interval==1 and shape_number_interval==3:
            possible_number_interval_color=['black','green']
            possible_number_interval_shape=[((0,0.5), (-0.5,-0.5), (0.5,-0.5)),
                                        ((0,0.5), (-0.5,0), (0,-0.5),(0.5,0))] #triangle, diamond
            for j in range (0,trial_number_interval):
                interval_color=random.choice(possible_number_interval_color)
                interval_shape=random.choice(possible_number_interval_shape)
                myShape(interval_color,interval_shape)
                win.flip()
                core.wait(0.1)
                win.flip()
                core.wait(interval_number_interval)
                possible_number_interval_color.remove(interval_color)
                possible_number_interval_shape.remove(interval_shape)
                
        #draw the second red rect
        myShape('red',((-0.5,0.5), (-0.5,-0.5), (0.5,-0.5), (0.5,0.5))) #red rect
        win.flip()
        core.wait(0.1)
        win.flip()
        core.wait(2)

        #show text 3
        myText('Now press the space bar as many times as you saw the shapes and at intervals equal to the time interval between the consecutive shapes.',(0,40),50)
        myText('When you are done, press Enter to continue!',(0,-200),30)
        win.flip()

        #the main difference between test 1 and test 2 is in this section. In test 1, just 2 presses are registered.
        #But in test 2, all key presses are registered and difference between each two presses are registered. 
        response_number_interval=[] # difine an empty list 
        response_number_interval.append(trial_number_interval) # append trial to the list
        event.clearEvents() # clear all previus key presses
        while not event.getKeys(keyList='return'):
            for o in range (len([trial_number_interval+2])):
                if event.getKeys(keyList='space'): #if space was pressed
                    response_number_interval.append(core.getTime()) #register the time of key press
                    mainSound.play() #play the sound
                    core.wait(0.2)
                    break

        #register time interval between two space presses
        diff_list_number_interval = [] 
        diff_list_number_interval.append(complexity_number_interval)
        diff_list_number_interval.append(trial_number_interval)
        diff_list_number_interval.append(miliSecond_number_interval)
        diff_list_number_interval.append(shape_number_interval)
        diff_list_number_interval.append(interval_number_interval)
        diff_list_number_interval.append(Expected_tapping_interval)
        
        for z, w in zip(response_number_interval[1::], response_number_interval[2::]):
            diff_list_number_interval.append(w-z)
            
        data_number_interval.append(diff_list_number_interval)
        core.wait(2)
        #remove the randomly selected pair from the list to prevent replacement  
        myList_number_interval.remove(mySelectedElement_number_interval)

df_number_interval=pd.DataFrame(data_number_interval)

myText('Thanks for your participation!',(0,0),50)
win.flip()
core.wait(4)
win.close() # close the psychopy window
                            
#################################################################
#################################################################

#combine the results of test 1 and test 2 
results=pd.concat([df_interval, df_number_interval], ignore_index=True, axis=1)
results.index +=1 # start the index in the dataframe from 1 instead of 0
pd.set_option('display.max_columns', None) # show all columns in the dataframe
pd.set_option('display.max_rows', None)  # show all rows in the dataframe

results=str(results)  #convert the dataframe to string 


#define save box
my_w = tk.Tk()
my_w.geometry("400x300")  # Size of the window 
my_w.title('Time test Number and Interval')
my_font1=('times', 18, 'bold')
l1 = tk.Label(my_w,text='Save File',width=30,font=my_font1)
l1.grid(row=1,column=1)
b1 = tk.Button(my_w, text='Save', 
width=20,command = lambda:save_file())
b1.grid(row=2,column=1) 
def save_file():
    file = filedialog.asksaveasfilename(
        filetypes=[("txt file", ".txt")],
    defaultextension=".txt")
    fob=open(file,'w')
    fob.write(results)
    fob.close()
my_w.mainloop() 




