import pygame
import os
import time
import threading
import mysql.connector as M
from Constants import *
#SOUNDS
#https://soundcloud.com/ashamaluevmusic/sets/instrumental-background-music-for-videos
#https://www.ashamaluevmusic.com/summer-music

pygame.init()


#USEFUL CONSTANTS
D = pygame.display
S = D.set_mode((800,600),pygame.RESIZABLE)
Sh_org = S.get_height()
Sw_org = S.get_width()
E = pygame.event
Dr = pygame.draw


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
def eventcheck(tabslist):
     if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if input_name.rect.collidepoint(mouse_pos):
                input_name.state = "active"
                now_active = input_name
                now_activeindex = tabslist.index(input_name)
            else:
                input_name.state = "passive"
            if input_pwd.rect.collidepoint(mouse_pos):
                input_pwd.state = "active"
                now_active = input_pwd
                now_activeindex = tabslist.index(input_pwd)
            else:
                input_pwd.state = "passive"
            if input_pwd.pwd_rect.collidepoint(mouse_pos):
                input_pwd.state = "active"
                if input_pwd.pwd_img_state == "hidden":
                    input_pwd.pwd_img_state = "visible"
                else:
                    input_pwd.pwd_img_state = "hidden"

                 
     if event.type == pygame.MOUSEMOTION:
        
        mouse_pos = pygame.mouse.get_pos()
        if input_name.rect.collidepoint(mouse_pos):
            if input_name.state == "passive":
                input_name.state = "hover"
        else:
            if input_name.state == "hover":
                input_name.state = "passive"
        if input_pwd.rect.collidepoint(mouse_pos):
            if input_pwd.state == "passive":
                input_pwd.state = "hover"
        else:
            if input_pwd.state == "hover":
                input_pwd.state = "passive"

     if event.type == pygame.KEYDOWN:
        
        gettxt(input_name)
        gettxt(input_pwd)
        cursormove(input_name)
        cursormove(input_pwd)
        tabaction()
            
def uservalidation():
    un = input_name.user_text
    pwd = input_pwd.user_text
    Exe("Select * from users where username = %s",(un,))
    try:
        L_details = MyC.fetchall()[0]
    except:
        #print("Unavailable now")
        from tkinter import Tk
        from tkinter.messagebox import showerror
        Tk().wm_withdraw()
        showerror("Error","Invalid username")
        return

    if L_details[1] == pwd:
        print(1)
        Exe("Delete from currentuser")
        print("Done")
        Exe(f"Insert into currentuser values('{un}',null)")
        MyDB.commit()
        submit1.state = "active"
        
    else:
        from tkinter import Tk
        from tkinter.messagebox import showerror
        Tk().wm_withdraw()
        showerror("Error","Invalid password")

def usercreation():
    un = input_name.user_text
    pwd = input_pwd.user_text
    try:
        Exe("Insert into users values(%s,%s)",(un,pwd))
        MyDB.commit()
    except:
        #print("Username already exists")
        from tkinter import Tk
        from tkinter.messagebox import showerror
        Tk().wm_withdraw()
        showerror("Error","Username already exists")
        #S.blit(txt("Username already exists", color = "red"),(40,600))
        return
    Exe("Delete from currentuser")
    Exe(f"Insert into currentuser values('{un}',null)")
    MyDB.commit()
    Exe(f"Create table {un}songs(songname varchar(30) primary key, recording text)")
    homepg.state = 0

        
def gettxt(self):
    if self.state == "active":
        # Check for backspace
        '''if event.key == pygame.K_BACKSPACE:

            # get text input from 0 to -1 i.e. end.
            ut = self.user_text
            self.user_text = ut[:self.cursor_pos-1] + ut[self.cursor_pos:]
            self.cursor_pos -= 1'''

        # Unicode standard is used for string
        # formation
        if len(self.user_text)<self.maxlen[self.type] :
            if event.key not in (pygame.K_LEFT ,pygame.K_RIGHT, pygame.K_BACKSPACE,pygame.K_DELETE,pygame.K_TAB):
                ut = self.user_text
                if event.unicode.isalnum() or event.unicode in ("_"):
                    self.user_text = ut[:self.cursor_pos] + event.unicode + ut[self.cursor_pos:]
                    self.cursor_pos += 1
                    
def backspace(self,t):
    if self.state == "active":
        if t - self.backspace_time > 0.12:
            if self.cursor_pos >0:
                # get text input from 0 to -1 i.e. end.
                ut = self.user_text
                self.user_text = ut[:self.cursor_pos-1] + ut[self.cursor_pos:]
                
                self.cursor_pos -= 1
                self.backspace_time = t

def delete(self,t):
    if self.state == "active":
        if t - self.delete_time > 0.12:
            # get text input from 0 to -1 i.e. end.
            ut = self.user_text
            self.user_text = ut[:self.cursor_pos] + ut[self.cursor_pos+1:]
            self.delete_time = t

def cursormove(self):
    if self.state == "active":
        if event.key == pygame.K_LEFT:
            if self.cursor_pos >0:
                self.cursor_pos -= 1
                #print(self.cursor_pos)
        if event.key == pygame.K_RIGHT:
            if self.cursor_pos < len(self.user_text):
                self.cursor_pos += 1
                #print(input_name.cursor_pos)

def tabaction():
    global now_active,now_activeindex
    if KEYSTATES[pygame.K_LSHIFT] or KEYSTATES[pygame.K_RSHIFT]: 
        #print("yes")
        if event.key == pygame.K_TAB:
            if now_activeindex in (0,None):
                now_activeindex = len(homepg.tabslist)
            try:
                now_active.state = "passive"
            except:
                pass
            now_activeindex -= 1
            now_active = homepg.tabslist[now_activeindex]
            if type(now_active) != type(submit1):
                now_active.state = "active"
            else:
                now_active.state = "hover"

    else:
        if event.key == pygame.K_TAB:
            if now_activeindex in (len(homepg.tabslist)-1,None):
                now_activeindex = -1
            try:
                now_active.state = "passive"
            except:
                pass
            now_activeindex += 1
            now_active = homepg.tabslist[now_activeindex]
            if type(now_active) != type(submit1):
                now_active.state = "active"
            else:
                now_active.state = "hover"

class BGM:
    def __init__(self,track):
        from pygame import mixer
        self.mixer = mixer
        # Starting the mixer
        self.mixer.init()
        
        # Loading the song
        self.mixer.music.load(track)
        
        # Setting the volume
        self.mixer.music.set_volume(0.5)
    
    def play(self):
        # Start playing the song
        self.mixer.music.play()
    
    def end(self):
        self.mixer.music.stop()
        pass
#Seawalk_bgm = BGM("E:\\120204 Ashish Thannickal\\Project Work\\Homepage\\Seawalk.mp3")
Seawalk_bgm = BGM("D:\\Music Synthesizer\\Homepage\\Seawalk.mp3")

class TextHP:

    def __init__(self,i = 0,hpstate=1):
        global sizeiteration
        self.hpstate = hpstate
        self.th1 = int(60 * (Sw/Sw_org))
        if time.time()%0.05 > 0.03:
            sizeiteration += 1
        self.th2 = max(self.th1 - i,40)
        if self.hpstate == 2:
            self.th2 = 35
        self.text = txt("MUSIC SYNTHESIZER",
                        #font = "E:\\120204 Ashish Thannickal\\Project Work\\Homepage\\Another Danger - Demo.otf",  
                        font = "D:/Music Synthesizer/Homepage/Another Danger - Demo.otf",  
                        size = self.th2, 
                        color = "#eeeeee")
        self.th = self.text.get_height()
        self.tw = self.text.get_width()
        self.rect = self.text.get_rect()
        self.TL = ()
        self.TR = ()
        self.BL = ()
        self.BR = ()
        
    def draw(self):
        self.y = Sh/2-self.th/2
        if self.hpstate == 2:
            self.y = 40
        self.bl = S.blit(self.text ,(Sw/2-self.tw/2,self.y))
        self.TL = self.bl.topleft
        self.TR = self.bl.topright
        self.BL = self.bl.bottomleft
        self.BR = self.bl.bottomright
    
class underline:
    def __init__(self,len=20,x=20,y=20):
        self.length = len
        self.x = x
        self.y = y
    
    def draw(self):
        Dr.line(S,"#dddddd",(self.x,self.y),(self.x + self.length,self.y),8)
        pass


class Timer:
    def __init__(self,t):
        self.d = {}
        self.d["ss"] = t-starttime
        self.d["mm"] = int(self.d["ss"]//60)
        self.d["ss"] = round(self.d["ss"]%60,2)
        self.d["hh"] = int(self.d["mm"]//60)
        self.d["mm"] = self.d["mm"]%60
        self.txt = "{} : {} : {}".format(self.d["hh"],self.d["mm"],self.d["ss"])
        self.text = txt(self.txt,size = 40,color = "pink")
    def draw(self):
        self.bl = S.blit(self.text ,(0,0))
        pass


class inputbox:
    def __init__(self,x = 250,y = 100,width = 100, height = 35, state = "passive",**kwargs):
        self.TL = ()
        self.TR = ()
        self.BL = ()
        self.BR = ()
        self.cols = {}
        self.w1 = width
        self.h1 = height
        self.state = state
        self.user_text = ""
        self.backspace_time = time.time()
        self.delete_time = time.time()
        self.text_tit = ""
        self.tit_th = height
        self.tit_tw = 100
        self.text_rect = ()
        self.x = x
        self.y = y
        self.maxlen = {"Name":30,"pwd":22}
        
        #pwd
        #self.hidepwd_img = pygame.image.load(r"E:\120204 Ashish Thannickal\Project Work\Homepage\Hidepwd.png")
        self.hidepwd_img = pygame.image.load(r"D:\Music Synthesizer\Homepage\Hidepwd.png")
        self.hidepwd_img = pygame.transform.scale(self.hidepwd_img,(30,30))
        #self.showpwd_img = pygame.image.load(r"E:\120204 Ashish Thannickal\Project Work\Homepage\Showpwd.png")
        self.showpwd_img = pygame.image.load(r"D:\Music Synthesizer\Homepage\Showpwd.png")
        self.showpwd_img = pygame.transform.scale(self.showpwd_img,(30,30))
        self.pwd_img_state = "hidden"
        self.pwd_imgsrf = self.showpwd_img.convert()
        self.pwd_rect = pygame.rect.Rect(0,0,0,0)

        try:
            self.cols["passive"] = kwargs["c1"]
            self.cols["active"] = kwargs["c2"]
            self.cols["hover"] = kwargs["c3"]
        except:
            self.cols["passive"] = "gray"
            self.cols["active"] = "white"
            self.cols["hover"] = "purple"
        self.rect_w = width
        self.rect_h = height
        self.rect = pygame.rect.Rect(x,y,self.rect_w,self.rect_h)
        self.rect_bor = pygame.Rect(x,y,self.rect_w,self.rect_h)
        
        #Cursor
        self.cursor_pos = 0
        self.cursor_pos_coords = [0,0]
        self.cursor = pygame.Rect(self.rect.topright, (2, self.rect.height-2))

    def draw(self):
        #Input Box
        self.rect = pygame.rect.Rect(self.x,self.y,self.rect_w,self.rect_h)
        self.rect_bor = pygame.Rect(self.x,self.y,self.rect_w,self.rect_h)
        self.bl = Dr.rect(S,color=self.cols[self.state],rect=self.rect)
        #self.bl = Dr.rect(S,color="black",rect=self.rect)
        self.bl_bor = Dr.rect(S,color="#2949f3",rect=self.rect,width=3)
        self.TL = self.bl.topleft
        self.TR = self.bl.topright
        self.BL = self.bl.bottomleft
        self.BR = self.bl.bottomright

        #Input Text
        if self.type == "pwd":
            self.user_txt1 = txt("•"*len(self.user_text),size = 28)
            self.user_txt2 = txt("•"*len(self.user_text[:self.cursor_pos]),size = 28) 
            if self.pwd_img_state == "visible":
                self.user_txt1 = txt(self.user_text,size = 28)
                self.user_txt2 = txt(self.user_text[:self.cursor_pos],size = 28)
                self.pwd_imgsrf = self.hidepwd_img.convert()
                #self.pwd_img_state = "visible"
            else:
                self.pwd_imgsrf = self.showpwd_img.convert()
                #self.pwd_img_state = "hidden"
            self.pwd_rect = self.pwd_imgsrf.get_rect(topleft = (self.TR[0]+2,self.TL[1]))
            S.blit(self.pwd_imgsrf,(self.TR[0]+2,self.TL[1]))
        else:
            self.user_txt1 = txt(self.user_text,size = 28)
            self.user_txt2 = txt(self.user_text[:self.cursor_pos],size = 28)
        
        self.bl_txt = S.blit(self.user_txt1, (self.TL[0]+10,self.TL[1]+5))
        #print(self.bl_txt.width+20,self.rect_w)
        self.rect_w = max(self.bl_txt.width+20,self.w1)
        
        ###self.rect_h = max(self.bl_txt.height+20,self.h1)

        # Blit the  cursor
        if time.time() % 1 > 0.5 and self.state == "active":
            # bounding rectangle of the text
            text_rect = self.user_txt2.get_rect(topleft = (self.rect.x+10, self.rect.y + 5))

            # set cursor position
            self.cursor.midleft = text_rect.midright

            pygame.draw.rect(S, "Black", self.cursor)

        '''self.cursor_pos_coords[1] = self.TL[1]
        self.cursor_pos_coords[0] = self.TL[0] + *self.cursor_pos + 9'''

        #Title of IB
        S.blit(self.text_tit, (self.TL[0]-self.tit_tw-20,self.TL[1]))



    def set_type(self,type="name"):
        if type == "name":
            self.type = "Name"
            self.txt_tit = "USERNAME :"
            self.text_tit = txt(self.txt_tit,size = 38,color = "#abcdef",u = True)
            self.tit_th = self.text_tit.get_height()
            self.tit_tw = self.text_tit.get_width()
        if type == "pwd":
            self.type = "pwd"
            self.txt_tit = "PASSWORD :"
            self.text_tit = txt(self.txt_tit,size = 38,color = "#abcdef",u = True)
            self.tit_th = self.text_tit.get_height()
            self.tit_tw = self.text_tit.get_width()


input_name = inputbox()
input_name.set_type("name")
input_pwd = inputbox(250,250)
input_pwd.set_type("pwd")


class Button:
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

submit1 = Button()
submit2 = Button(text = "SUBMIT")
signup1 = Button(x=260,text = "SIGN UP")
back1 = Button(x = 260, text = "BACK")
class BGimg:
    def __init__(self,img):
        self.img = pygame.image.load(img)
        self.img_scaled = pygame.transform.scale(self.img,(Sw_org,Sh_org))
        pass
    def draw(self):
        self.img_scaled = pygame.transform.scale(self.img,(Sw,Sh))
        self.imgsrf = self.img_scaled.convert()
        S.blit(self.imgsrf,(0,0))
bg_img1 = BGimg(r"D:\Music Synthesizer\Homepage\musicnote.jpg")


class HP:
    def __init__(self):
        self.state = False
        self.tabslist = [input_name,input_pwd,submit1,signup1]
    def action(self):
        if self.state == 1:
            TxHP = TextHP(sizeiteration)
            TxHP.draw()
            unTxHP = underline(TxHP.tw,TxHP.BL[0],TxHP.BL[1])
            unTxHP.draw()
            timer1 = Timer(time.time())
            timer1.draw()
        if self.state == 2:
            bg_img1.draw()
            self.tabslist = [input_name,input_pwd,submit1,signup1]
            TxHP = TextHP(hpstate=self.state)
            TxHP.draw()
            input_name.draw()
            input_pwd.draw()
            submit1.draw()
            signup1.draw()
            timer1 = Timer(time.time())
            timer1.draw()
        if self.state == 3:
            bg_img1.draw()
            self.tabslist = [input_name,input_pwd,submit2,back1]
            TxHP = TextHP(hpstate=2)
            TxHP.draw()
            input_name.draw()
            input_pwd.draw()
            submit2.draw()
            back1.draw()
            timer1 = Timer(time.time())
            timer1.draw()    
        if self.state == 0:
            self.txt = f"You have succesfully logged out"
            S.blit(txt(self.txt),(40,40))
            Seawalk_bgm.end()
            import pygametrial
            


        

run = True
starttime = time.time()
homepg = HP()
iteration = 0
sizeiteration = 0
tabslist = [input_name,input_pwd,submit1,signup1]
tabstates = {"active":1,"passive":0}
now_active = None
now_activeindex = None
Seawalk_bgm.play()
while run:
    S.fill((0,0,0))
    Sh = S.get_height()
    Sw = S.get_width()

    '''x = input_pwd.hidepwd_img.convert()
    S.blit(x,(60,140))'''


    #HomePage
    if time.time()-starttime < 2:
        homepg.state = 1
    elif time.time()-starttime < 120:
        if homepg.state != 0:
            homepg.state = max(2,homepg.state)
    else:
        Seawalk_bgm.end()
    if submit1.state == "active":
        submit1.state="passive"
        homepg.state = 0
    if signup1.state == "active":
        homepg.state = 3
        signup1.state="passive"
        
    homepg.action()
    try:
        1
        #print(input_name.user_text[input_name.cursor_pos-1])
    except:
        pass

    KEYSTATES = pygame.key.get_pressed()
    if KEYSTATES[pygame.K_BACKSPACE]:
        backspace(input_name,time.time())
        backspace(input_pwd,time.time())
    elif KEYSTATES[pygame.K_DELETE]:
        delete(input_name,time.time())
        delete(input_pwd,time.time())
    for event in E.get():
        if event.type == pygame.QUIT:
            run = False
            os._exit(0)
        if homepg.state == 2:
            eventcheck(homepg.tabslist)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if submit1.rect.collidepoint(mouse_pos):
                    now_active = None
                    now_activeindex = None
                    uservalidation()
                else:
                    submit1.state = "passive"
                if signup1.rect.collidepoint(mouse_pos):
                    now_active = signup1
                    now_activeindex = homepg.tabslist.index(signup1)
                    homepg.state=3
                    signup1.state = "active"
                else:
                    signup1.state = "passive"
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if submit1.rect.collidepoint(mouse_pos):
                    if submit1.state == "passive":
                        submit1.state = "hover"
                else:
                    if submit1.state == "hover":
                        submit1.state = "passive"
                if signup1.rect.collidepoint(mouse_pos):
                    if signup1.state == "passive":
                        signup1.state = "hover"
                else:
                    if signup1.state == "hover":
                        signup1.state = "passive"
                
        if homepg.state == 3:
            eventcheck(homepg.tabslist)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if submit2.rect.collidepoint(mouse_pos):
                    now_active = None
                    now_activeindex = None
                    usercreation()
                else:
                    submit2.state = "passive"
                if back1.rect.collidepoint(mouse_pos):
                    homepg.state = 2
                else:
                    back1.state = "passive"
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if submit2.rect.collidepoint(mouse_pos):
                    if submit2.state == "passive":
                        submit2.state = "hover"
                else:
                    if submit2.state == "hover":
                        submit2.state = "passive"
                if back1.rect.collidepoint(mouse_pos):
                    if back1.state == "passive":
                        back1.state = "hover"
                else:
                    if back1.state == "hover":
                        back1.state = "passive"
        
    #print(input_pwd.pwd_img_state)
    #print(homepg.state)
    iteration += 1        
    D.update()
