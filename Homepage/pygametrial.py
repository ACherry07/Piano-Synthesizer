import pygame
import numpy as np
from numpy import sin, pi as π
from soundmodules import piano_keys as pk, note_freqs as nf
import time
from threading import *
import sys
import os
import tkinter as tk
from tkinter import Tk
from tkinter.messagebox import askyesno,showinfo
from tkinter.simpledialog import askstring
from Constants import *
#https://www.projectrhea.org/rhea/index.php/Fourier_analysis_in_Music
#https://data-flair.training/blogs/deep-surveillance-with-deep-learning-intelligent-video-surveillance-project/

#initialising pygame
pygame.init()

#Variables
D = pygame.display
S = D.set_mode((800,600), pygame.RESIZABLE)
E = pygame.event
Dr = pygame.draw
def avg(l): return sum(l)/len(l)
record = {1:{"E4":0.5},2:{"E4":0.5},3:{"F4":0.5}}
time_record = {}
timestamps = {}
dead = False

#Format
color_active = (255,255,255)
color_passive = (100,100,100)
color_current = color_active
d = {color_active:color_passive, color_passive: color_active}

def hex_to_RGB(hex):
  ''' "#FFFFFF" -> [255,255,255] '''
  # Pass 16 to the integer function for change of base
  return [int(hex[i:i+2], 16) for i in range(1,6,2)]


def RGB_to_hex(RGB):
  ''' [255,255,255] -> "#FFFFFF" '''
  # Components need to be integers for hex to make sense
  RGB = [int(x) for x in RGB]
  return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])  

def color_dict(gradient):
  ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
  return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
      "r":[RGB[0] for RGB in gradient],
      "g":[RGB[1] for RGB in gradient],
      "b":[RGB[2] for RGB in gradient]}

def linear_gradient(start_hex="#c31432", finish_hex="#240b36", n=255):
  ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
  # Starting and ending colors in RGB form
  s = hex_to_RGB(start_hex)
  f = hex_to_RGB(finish_hex)
  # Initilize a list of the output colors with the starting color
  RGB_list = [s]
  # Calcuate a color at each evenly spaced value of t from 1 to n
  for t in range(1, n):
    # Interpolate RGB vector for color at the current value of t
    curr_vector = [
      int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
      for j in range(3)
    ]
    # Add it to our list of output colors
    RGB_list.append(curr_vector)

  return color_dict(RGB_list)

#colors = linear_gradient("#ad5389","#3c1053",n = 30)['hex']
colors = linear_gradient("#000000","#FFFFFF",n = 30)['hex']
#print(colors)
def color_switch(color):
    global color_current
    #print(color_current)
    color_current = d[color]
'''    box = pygame.Rect(10,10,50,50)
    Dr.rect(S,color_current,[10,10,50,50])'''
def button():
    Dr.rect(S,color_current,[10,10,50,50])


def txt(t,font="Corbel",size = 20,color = "#ff0000", italic = False, u = False):
        # defining a font
    try:
        smallfont = pygame.font.Font(font, size)
    except:
        smallfont = pygame.font.SysFont(font, size)
    
    # rendering a text written in
    # this font
    smallfont.italic = italic
    smallfont.underline = u
    text = smallfont.render( t, True , color)
    return text

note_status = dict.fromkeys(nf,False)
nf_white = {i:nf[i]  for i in nf if i.isupper()}
#print(nf_white)
nf_black = {i:nf[i]  for i in nf if i.islower()}
#print(nf_black)
#print(note_status)



c_list = [i for i in range(len(nf_white)) if list(nf_white)[i][0] == "C"]

def keys():
    global white_keys, black_keys, width
    h = S.get_height()
    w = S.get_width()
    x = np.linspace(2*w/10,8*w/10,10)
    width = avg([x[i]-x[i-1] for i in range(1,len(x))]) 
    start = 2
    if defoctave != 0:
        start = max([i for i in c_list if i<defoctave*7])
    white_keys = {list(nf_white.keys())[start+i]:pygame.Rect(x[i]-width/2,round(h/2),width,round(h/2)) for i in range(10) if start+i in range (0,len(nf_white))}
    black_keys = {i.lower():pygame.Rect(white_keys[i].left +3*width/4,round(h/2),width/2,round(6*h/20)) for i in white_keys if i.lower() in nf}
    iteration = 0
    for i in white_keys:
        if note_status[i]:
            Dr.rect(S,"gray",white_keys[i],border_radius=10)
            Dr.rect(S,"#000000",white_keys[i],border_radius=10,border_top_left_radius=4,border_top_right_radius=4,width = 1)
        else:
            #Dr.rect(S,colors[iteration],white_keys[i],border_radius=10)
            Dr.rect(S,"#F0F0F0",white_keys[i],border_radius=10,border_top_left_radius=4,border_top_right_radius=4)
            Dr.rect(S,"#000000",white_keys[i],border_radius=10,border_top_left_radius=4,border_top_right_radius=4,width = 1)
            S.blit(txt(i),(white_keys[i].left,white_keys[i].bottom - 40))
        iteration += 1

    iteration = 0
    for i in black_keys:
        if note_status[i]:
            Dr.rect(S,"pink",black_keys[i],border_radius=5)
        else:
            Dr.rect(S,"#222222",black_keys[i],border_bottom_left_radius=5,border_bottom_right_radius=5)
            Dr.rect(S,"#AAAAAA",black_keys[i],border_bottom_left_radius=5,border_bottom_right_radius=5, width = 2)
            S.blit(txt(i),(black_keys[i].left,black_keys[i].bottom-40))
        iteration += 1
    #print(note_keys)
#note

samplerate = 44100
defoctave = 4
def play_note(note = "A4",d = 10,A=6000):
    A = A
    f = nf[note]
    t1 = np.linspace(0,d,int(d*samplerate))
    ω = 2 * π * f
    y = A * np.sin (ω*t1[10:-10])
    sound = np.asarray([y,y]).T.astype(np.int16)
    sound = pygame.sndarray.make_sound(sound.copy())
    return sound
    #write("examplewav",samplerate,y.astype(np.int16))

note_sounds = { i:play_note(i) for i in note_status}
instruments = ["flute","piano","violin"]
inst_flute = {0 : 1, 1: 9, 2: 4, 3:2, 5: 0.3}
def press_action(pos,keycolor,timestamp,key):
    #color_switch(color_current)
    s = keycolor[pos]
    #print(s, nf[s])
    note_status[s] = True
    
    note_sounds[keycolor[pos]].play()
    if Editable:
        time_record[timestamp] = [s,0]
        timestamps[key] = timestamp

def lift_action(pos,keycolor,key,newtimestamp):
    #color_switch(color_current)
    s = keycolor[pos]
    note_status[s] = False
    note_sounds[keycolor[pos]].stop()
    if Editable:
        time_record[timestamps[key]][1] = newtimestamp-timestamps[key]


# work function
def work(t,speed,key,color,dur = 4,):
    global dead
    print(t,speed,key,dur)
    timepassed = time.time()-t
    h = S.get_height()
    left = color[key].left
    playcol = "orange"
    widthn = width
    if color == black_keys:
        widthn = width/2
        playcol = "pink"
    dist = speed * timepassed
    bar = pygame.Rect(left,dist,width,100)
    playnote = 0
    timeplayed = playstart = 0
    bar_height = dur*speed
    while timeplayed < dur and (not dead):
        playnote += 1
        if playnote == 1:
            playstart = time.time()
            note_status[key] = True
            note_sounds[key].play()
        timeplayed = time.time()-playstart
        

        '''dist = speed * timepassed
        if bar.bottom >= h/2:
            playnote+=1
            bar = pygame.Rect(left,dist,widthn, h/2 - bar.top)
            Dr.rect(S,playcol,bar,border_radius = -1)
            print(timeplayed)
            if playnote == 1:
                playstart = time.time() 
                note_sounds[key].play() 
            timeplayed = time.time() - playstart
        else:
            bar = pygame.Rect(left,dist,widthn, bar_height)
            Dr.rect(S,playcol,bar,border_radius =  4)
        timepassed = time.time() - t'''
    note_status[key] = False
    note_sounds[key].stop()

def multiwork(record):
    global Playpress
    st = time.time()
    it = 0
    for i in record:
        it+=   1
        if it == 1:
            st = time.time()
        key = record[i][0]
        col = white_keys if key[0].isupper() else black_keys
        ct = time.time()
        #print(ct)
        while time.time() - st < i:
            pass
        else:
            t1 = Thread(target = work, args = (time.time(),500,key,col,record[i][1]))
            t1.start()
    Playpress = False
    
def b(xcord,ycord,text, pressed):
    #stores the width of the
    # screen into a variable
    width = S.get_width()
    
    # stores the height of the
    # screen into a variable
    height = S.get_height()
    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
      
    # if mouse is hovered on a button it
    # changes to lighter shade 
    if xcord <= mouse[0] <= xcord + 140 and height/2 + ycord<= mouse[1] <= height/2 + ycord + 40:
        Dr.rect(S,(170,170,170),[xcord,height/2+ycord,140,40])
          
    elif pressed == True:
        Dr.rect(S,(255,0,0),[xcord,height/2+ycord,140,40])
    
    else:
        Dr.rect(S,(100,100,100),[xcord,height/2+ycord,140,40])
    # superimposing the text onto our button
    S.blit(txt(text, size = 35, color = "#ffffff") , (xcord + 5,height/2+ycord))

def b_record():
    b(0,20,"RECORD",Recpress)

def b_pause():
    b(0,80,"PAUSE",Pausepress)

def b_play():
    b(0,140,"PLAY",Playpress)
def b_save():
    b(0,200,"SAVE",Savepress)

def b_songs():
    b(0,260,"SONGS",Songspress)
def b_logout():
    b(0,-40,"LOGOUT",None)
'''class Button:
    def __init__(self,x = 150,y = 400,width = 100, height = 30, state = "passive",text = "LOGIN",**kwargs):
        self.TL = ()
        self.TR = ()
        self.BL = ()
        self.BR = ()
        self.cols = {}
        self.w1 = width
        self.h1 = height
        self.state = state
        self.text = text
        #self.txt = txt(self.text,font = r"E:\120204 Ashish Thannickal\Project Work\Homepage\BRADHITC.TTF", color = "black")
        self.txt = txt(self.text,font = r"D:\Music Synthesizer\Homepage\BRADHITC.TTF", color = "black")
        try:
            self.cols["passive"] = kwargs["c1"]
            self.cols["active"] = kwargs["c2"]
            self.cols["hover"] = kwargs["c3"]
        except:
            self.cols["passive"] = "pink"
            self.cols["active"] = "pink"
            self.cols["hover"] = "lavender"
        
        self.rect_w = width
        self.rect_h = height
        self.rect = pygame.rect.Rect(x,y,self.rect_w,self.rect_h)
        self.rect_bor = pygame.Rect(x,y,self.rect_w,self.rect_h)
        self.x = x
        self.y = y

    def draw(self):
        #Input Box
        self.rect = pygame.rect.Rect(self.x,self.y,self.rect_w,self.rect_h)
        self.rect_bor = pygame.Rect(self.x,self.y,self.rect_w,self.rect_h)
        self.bl = Dr.rect(S,color=self.cols[self.state],rect=self.rect,border_radius=10)
        self.bl_bor = Dr.rect(S,color="pink",rect=self.rect,width=3,border_radius=10)
        self.TL = self.bl.topleft
        self.TR = self.bl.topright
        self.BL = self.bl.bottomleft
        self.BR = self.bl.bottomright
        self.bl_txt = S.blit(self.txt, (self.TL[0]+10,self.TL[1]+5))

recordbutton1 = Button(x=0,y=200,text = "RECORD" ,c3 = (170,170,170),c1 = (100,100,100),c2 = (255,0,0))'''

#Loop
run = True
op = "+"
ite = 0
startmsg = True
Editable = False
start_time = time.time()
Recpress = Pausepress = Playpress = Savepress = Songspress =  False
while run:
    ite = eval(f"{ite}{op}1")
    if ite == len(colors):
        op = "-"
        ite -= 1
    if ite == 0:
        op = "+"
    S.fill((0,0,0))
    mytxt = txt("PIANO","Felix Titling", 60, colors[ite])
    mytxtw = mytxt.get_width()
    S.blit(mytxt,(S.get_width()//2 - mytxtw//2,S.get_height()/6))

    if startmsg:
        msg = txt("Use 'a' to ';' for white keys top row for black",size = 40, color = "light blue")
        msgw = msg.get_width()
        S.blit(msg,(S.get_width()//2 - msgw//2, S.get_height()//3))
        start_time = time.time()
    #print(pygame.event.get())
    #print(defoctave)
    for event in E.get():
        Sh = S.get_height()
        Sw = S.get_width()
        #print(event)
        #print("Semicolon",pygame.key.get_pressed()[pygame.K_SEMICOLON],end = "\r")
        if event.type == pygame.QUIT:
            dead = True
            run = False
            os._exit(0)
            
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            startmsg = False
            wk = list(white_keys)
            bk = list(black_keys)
            if event.key == pygame.K_a:
                press_action(0,wk,time.time()-start_time,pygame.K_a)
            if event.key == pygame.K_s:
                press_action(1,wk,time.time()-start_time,pygame.K_s)
            if event.key == pygame.K_d:
                press_action(2,wk,time.time()-start_time,pygame.K_d)
            if event.key == pygame.K_f:
                press_action(3,wk,time.time()-start_time,pygame.K_f)
            if event.key == pygame.K_g:
                press_action(4,wk,time.time()-start_time,pygame.K_g)
            if event.key == pygame.K_h:
                if len(wk)>5:
                    press_action(5,wk,time.time()-start_time,pygame.K_h)
            if event.key == pygame.K_j:
                if len(wk)>6:
                    press_action(6,wk,time.time()-start_time,pygame.K_j)
            if event.key == pygame.K_k:
                if len(wk)>7:
                    press_action(7,wk,time.time()-start_time,pygame.K_k)
            if event.key == pygame.K_l:
                if len(wk)>8:
                    press_action(8,wk,time.time()-start_time,pygame.K_l)
            if event.key == pygame.K_SEMICOLON:
                if len(wk)>9:
                    press_action(9,wk,time.time()-start_time,pygame.K_SEMICOLON)
            if event.key == pygame.K_w:
                press_action(0,bk,time.time()-start_time,pygame.K_w)
            if event.key == pygame.K_e:
                press_action(1,bk,time.time()-start_time,pygame.K_e)
            if event.key == pygame.K_t:
                press_action(2,bk,time.time()-start_time,pygame.K_t)
            if event.key == pygame.K_y:
                press_action(3,bk,time.time()-start_time,pygame.K_y)
            if event.key == pygame.K_u:
                press_action(4,bk,time.time()-start_time,pygame.K_u)
            if event.key == pygame.K_o:
                press_action(5,bk,time.time()-start_time,pygame.K_o)
            if event.key == pygame.K_p:
                press_action(6,bk,time.time()-start_time,pygame.K_p)

                    
            if event.key == pygame.K_DOWN:
                if defoctave >0:
                    defoctave -= 1
            if event.key == pygame.K_UP:
                if defoctave <7:
                    defoctave += 1


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                lift_action(0,wk,pygame.K_a,time.time()-start_time)
            if event.key == pygame.K_s:
                lift_action(1,wk,pygame.K_s,time.time()-start_time)
            if event.key == pygame.K_d:
                lift_action(2,wk,pygame.K_d,time.time()-start_time)
            if event.key == pygame.K_f:
                lift_action(3,wk,pygame.K_f,time.time()-start_time)
            if event.key == pygame.K_g:
                lift_action(4,wk,pygame.K_g,time.time()-start_time)
            if event.key == pygame.K_h:
                if len(wk)>5:
                    lift_action(5,wk,pygame.K_h,time.time()-start_time)
            if event.key == pygame.K_j:
                if len(wk)>6:
                    lift_action(6,wk,pygame.K_j,time.time()-start_time)
            if event.key == pygame.K_k:
                if len(wk)>7:
                    lift_action(7,wk,pygame.K_k,time.time()-start_time)
            if event.key == pygame.K_l:
                if len(wk)>8:
                    lift_action(8,wk,pygame.K_l,time.time()-start_time)
            if event.key == pygame.K_SEMICOLON:
                if len(wk)>9:
                    lift_action(9,wk,pygame.K_SEMICOLON,time.time()-start_time)
            if event.key == pygame.K_w:
                lift_action(0,bk,pygame.K_w,time.time()-start_time)
            if event.key == pygame.K_e:
                lift_action(1,bk,pygame.K_e,time.time()-start_time)
            if event.key == pygame.K_t:
                lift_action(2,bk,pygame.K_t,time.time()-start_time)
            if event.key == pygame.K_y:
                lift_action(3,bk,pygame.K_y,time.time()-start_time)
            if event.key == pygame.K_u:
                lift_action(4,bk,pygame.K_u,time.time()-start_time)
            if event.key == pygame.K_o:
                lift_action(5,bk,pygame.K_o,time.time()-start_time)
            if event.key == pygame.K_p:
                lift_action(6,bk,pygame.K_p,time.time()-start_time)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 0 <= mouse[0] <= 140 and Sh/2+20 <= mouse[1] <= Sh/2+60:
                Editable = True
                time_record = {}
                if Recpress == False:
                    Recpress = True
                else:
                    Recpress = False
                    Editable = False
                Playpress = False
                Pausepress = False
                
                #time_record = {}
                startmsg = True
            if 0 <= mouse[0] <= 140 and Sh/2+80 <= mouse[1] <= Sh/2+120:
                Recpress = False
                Pausepress = True
                Editable = False
                Pausepress = False
            if 0 <= mouse[0] <= 140 and Sh/2+140 <= mouse[1] <= Sh/2+160:
                Recpress = False
                Pausepress = False
                Playpress = True
                Editable = False
                d = time_record
                startmsg = True
                t = Thread(target=multiwork,args = (d,))
                t.start()
            if 0 <= mouse[0] <= 140 and Sh/2+180 <= mouse[1] <= Sh/2+220:
                Recpress=False
                Pausepress=False
                #Tk().wm_withdraw()
                win = Tk()
                win.wm_withdraw()
                answer = askyesno("Save recording","Do you wish to save the recording?")
                if answer == True:
                    from Constants import getuser
                    UN = getuser()
                    songname = askstring("Songname", "Enter Song Name:")
                    #to check for repetition
                    try:
                        #print(time_record)
                        Exe(f"insert into {UN}songs values (\"{songname}\",\"{time_record}\")")
                        MyDB.commit()
                    except:
                        answer1 = askyesno("Save recording","Song already exists. Replace the song?")
                        if answer1 == True:
                            Exe(f"update {UN}songs set recording = \"{time_record}\" where songname = \"{songname}\"")
                            MyDB.commit()
                    showinfo("Message",f"{songname} saved")
                win.destroy()
                Recpress = Pausepress = Playpress = Savepress = Songspress =  False
            if 0 <= mouse[0] <= 140 and Sh/2+240 <= mouse[1] <= Sh/2+300:
                from Constants import playsong,getuser
                Recpress = False
                Pausepress = False
                Playpress = False
                Editable = False
                try:
                    d = eval(playsong(getuser())[0])
                    #print(d)
                    startmsg = True
                    t = Thread(target=multiwork,args = (d,))
                    t.start()
                    time_record = {}
                except:
                    pass
                    #print("No Song Chosen")
                
            if 0 <= mouse[0] <= 140 and Sh/2-40 <= mouse[1] <= Sh/2:
                run=False
    mouse = pygame.mouse.get_pos()
    b_play()
    b_record()
    b_pause()
    b_save()
    b_songs()
    b_logout()
    #recordbutton1.draw()
    keys()
    button()
    D.update()

#import homepagescl
'''from cmath import rect
import pygame
import sys
  
  
# initializing the constructor
pygame.init()
  
# screen resolution
res = (720,720)
  
# opens up a window
screen = pygame.display.set_mode(res)
  
# white color
color = (255,255,255)
  
# light shade of the button
color_light = (170,170,170)
  
# dark shade of the button
color_dark = (100,100,100)
  
# stores the width of the
# screen into a variable
width = screen.get_width()
  
# stores the height of the
# screen into a variable
height = screen.get_height()
  
# defining a font
smallfont = pygame.font.SysFont('Corbel',35)
  
# rendering a text written in
# this font
text = smallfont.render('quit' , True , color)

while True:
      
    for ev in pygame.event.get():
          
        if ev.type == pygame.QUIT:
            pygame.quit()
              
        #checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:
              
            #if the mouse is clicked on the
            # button the game is terminated
            if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
                pygame.quit()
                  
    # fills the screen with a color
    screen.fill((60,25,60))
      
    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
      
    # if mouse is hovered on a button it
    # changes to lighter shade 
    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
        pygame.draw.rect(screen,color_light,[width/2,height/2,140,40])
          
    else:
        pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40])
      
    # superimposing the text onto our button
    screen.blit(text , (width/2+50,height/2))
      
    # updates the frames of the game
    pygame.display.update()'''