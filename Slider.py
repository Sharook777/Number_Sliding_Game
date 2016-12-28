
# Slider.py
# A number sliding puzzle (version v.2.1)
# used a more modern python GUI module tkinter
# tested with python 34 03sept2016
'''
    Game window is divided into 16 tiles. Objective of the game is arrange these
    tiles in an order from 1 to 15 and last one is empty. You can move tiles to
    empty space using up, down, left and right keys in the keyboard

'''
################################################################################
#########################                          #############################
#########################      AUTHOR SHAROOK      #############################
#########################      SLIDING PUZZLE      #############################
#########################          GAME            #############################
#########################                          #############################
################################################################################




from tkinter import *
import threading
import random
import winsound


root=Tk()
root.geometry('250x275')
root.resizable(0,0)
root.title('SLIDER')


frame=Frame(root)

canvas=Canvas(frame,background='grey',width=250,height=250)
canvas.focus_set()
canvas.pack()

frame.pack()


Gameover=False
time=0
starter=False


frame2=Frame(root)

timer=Label(frame2,text='Time: 00   ',bg="black",fg="white")
timer.pack(side='right')

frame2.pack(fill=X)





def start():
   
    x,y=2,2
    global dot,dottext,com
    n=1
    com={}
    
    num=random.sample(range(0,16),16)
    
          
    for i in range(16):
       
        r=num.pop()
        
        if(r==0):
            dot=canvas.create_rectangle(x,y,x+60,y+60,outline='black',fill='black',tag='dot')
            dottext=canvas.create_text(x+29,y+29,fill='black',font=50,tag='dottext',text=r)
            
            i=i-1
            
            #print('dot and dottext',dot,dottext)
            
        else:
            tags='rect'+str(n)
            rect=canvas.create_rectangle(x,y,x+60,y+60,outline='#dbf',fill='white',tag=tags)
            
            texttag='text'+str(n)
            
            te=canvas.create_text(x+29,y+29,fill='black',font=50,tag=texttag,text=r)
            n=n+1
            #com[r]=tags

            #print('rectangle tags',rect,tags)
            #print('text tags',r,texttag,te)
            

        
            temp={r:tags}
            com.update(temp)
        
        #print(temp)

       
        x=x+62
        
        if(x==250):
            y=y+62
            x=2

    #print(com)       

    #checker=com.values()
    
    #print(com.keys())

def movethread():       
    
    threading.Thread(target=clock).start()


def motion():
    global starter
    starter=True
    #lock=threading.Lock()
    #lock.acquire()
    w=62
    coord=canvas.coords(dot)
    #print(coord)

    x1,y1,x2,y2=int(coord[0]),int(coord[1]),int(coord[2]),int(coord[3])
    #print(x1,y1,x2,y2)

    global u,v
    
    if(direction=='left'):
        if(x2==248):
            #print('no move')
            return
        else:
            canvas.move('dot',w,0)
            canvas.move('dottext',w,0)
            u,v=-w,0

            overlap()
            check()

    elif(direction=='down'):
        if(y1==2):
            #print('no move')
            return
        else:
            canvas.move('dot',0,-w)
            canvas.move('dottext',0,-w)
            u,v=0,w

            overlap()
            check()

    elif(direction=='right'):
        if(x1==2):
            #print('no move')
            return
        else:
            canvas.move('dot',-w,0)
            canvas.move('dottext',-w,0)
            u,v=w,0

            overlap()
            check()  
   

    elif(direction=='up'):
        if(y2==248):
            #print('no move')
            return
        else:
            canvas.move('dot',0,w)
            canvas.move('dottext',0,w)
            u,v=0,-w
        
            overlap()
            check()
        

        
    
    
    #lock.release()


def overlap():
    coord=canvas.coords(dot)
    #print(coord)
    
    overlap=canvas.find_overlapping(coord[0]+30,coord[1]+30,coord[2]-30,coord[3]-30)
    #print(overlap)
    #print(canvas.gettags(overlap[0]))
    
    if(overlap[0]==dot and overlap[1]==dottext):
       canvas.move(canvas.gettags(overlap[2]),u,v)
       canvas.move(canvas.gettags(overlap[3]),u,v)
       
    else:
       canvas.move(canvas.gettags(overlap[0]),u,v)
       canvas.move(canvas.gettags(overlap[1]),u,v)
    



def check():
    global Gameover
    #print('call arrived')
    x,y=2,2
    
    for ij in range(1,16):
        #print(ij)
        gap=com[ij]
        
        #print(gap)
        done=canvas.coords(gap)
        
        #print(done)
        
        x1,y1,x2,y2=int(done[0]),int(done[1]),int(done[2]),int(done[3])
        #print(x1,y1,x2,y2)
        
        if(x1==x and y1==y and x2==x+60 and y2==int(y+60)):
            #print('attained position',ij)
            x=x+62
            if(x==250):
                y=y+62
                x=2
            if(ij==15):
                canvas.create_text(125,125,fill='red',font=80,tag='finish',
                                   text='Good Job\n You Finished')
                Gameover=True
                #start()
                #canvas.unbind('<key>',press)
            continue
        else:
            break
        
        
    



def press(event):
    
    global direction
    direction=None

    
    if(starter==False):
        movethread()
    
    if(Gameover==False):
        if(event.keycode==37):
            direction='left'
        elif(event.keycode==38):
            direction='up'
        elif(event.keycode==39):
            direction='right'
        elif(event.keycode==40):
            direction='down'
    
    
        if direction:
            #print(direction)
            motion()

def clock():
    global time
    if(Gameover==True):
        return
    
    time=time+1
    winsound.Beep(100,100)
    timer['text']='Time: '+str(time)
    canvas.after(1000,clock)
    


start()


canvas.bind('<Key>',press)


root.mainloop()
