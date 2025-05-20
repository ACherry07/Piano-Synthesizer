import pygame
import os
import time
import threading
import mysql.connector

#SOUNDS
#https://soundcloud.com/ashamaluevmusic/sets/instrumental-background-music-for-videos
#https://www.ashamaluevmusic.com/summer-music

#MYSQL
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root", 
    passwd = "l9hfG&7a"
    )

mycursor = mydb.cursor()
try:
    mycursor.execute("create database synth")
    mycursor.execute("use synth")
    print(1)
except:
    mycursor.execute("use synth")
    print(2)



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

def valid(event,self):
    if event.unicode.isalnum() or event.unicode in ("_.") and self.type == "Name": return True
    elif event.unicode.isalnum() or event.unicode in (" ~`! @#$%^&*()_-+={[}]|\:;\"'<,>.?/") and self.type == "pwd": return True
    else: return False

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
                if valid(event,self) and event.key not in (pygame.K_RSHIFT,pygame.K_LSHIFT):
                    self.user_text = ut[:self.cursor_pos] + event.unicode + ut[self.cursor_pos:]
                    self.cursor_pos += 1
                elif valid(event,self) and MODSTATES & pygame.KMOD_SHIFT:
                    self.user_text = ut[:self.cursor_pos] + event.unicode + ut[self.cursor_pos:]
                    self.cursor_pos += 1


def backspace(self,t):
    if self.state == "active":
        if self.select_all_state =="passive":
            if t - self.backspace_time > 0.12:
                if self.cursor_pos >0:
                    # get text input from 0 to -1 i.e. end.
                    ut = self.user_text
                    self.user_text = ut[:self.cursor_pos-1] + ut[self.cursor_pos:]
                    
                    self.cursor_pos -= 1
                    self.backspace_time = t
        else:
            self.user_text = ""
            self.cursor_pos = 0

def delete(self,t):
    if self.state == "active":
        if self.select_all_state =="passive":
            if t - self.delete_time > 0.12:
                # get text input from 0 to -1 i.e. end.
                ut = self.user_text
                self.user_text = ut[:self.cursor_pos] + ut[self.cursor_pos+1:]
                self.delete_time = t
        else:
            self.user_text = ""
            self.cursor_pos = 0

def cursormove(self):
    if self.state == "active" and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            if self.cursor_pos >0:
                self.cursor_pos -= 1
                #print(self.cursor_pos)
        if event.key == pygame.K_RIGHT:
            if self.cursor_pos < len(self.user_text):
                self.cursor_pos += 1
                #print(input_name.cursor_pos)

def mousecursormove(self):
    k = self.cursor_positions.copy()
    k.append(mouse_pos[0])
    k.sort()
    self.cursor_pos = k.index(mouse_pos[0])

def tabaction():
    global now_active,now_activeindex
    if homepg.state == 2:
        if event.key == pygame.K_TAB and MODSTATES & pygame.KMOD_SHIFT:
            if now_activeindex in (0,None):
                now_activeindex = len(tabslist)
            try:
                now_active.state = "passive"
            except:
                pass
            now_activeindex -= 1
            now_active = tabslist[now_activeindex]
            if now_active != submit1:
                now_active.state = "active"
            else:
                now_active.state = "hover"

        else:
            if event.key == pygame.K_TAB:
                if now_activeindex in (len(tabslist)-1,None):
                    now_activeindex = -1
                try:
                    now_active.state = "passive"
                except:
                    pass
                now_activeindex += 1
                now_active = tabslist[now_activeindex]
                if now_active != submit1:
                    now_active.state = "active"
                else:
                    now_active.state = "hover"

def selectall(self):
    if self.state == "active" and isinstance(self,inputbox):
        if event.key == pygame.K_a and MODSTATES & pygame.KMOD_CTRL:
            self.select_all_state = "active"
        elif valid(event,self):
            self.select_all_state = "passive"
    else:
        self.select_all_state = "passive"

def f_submit():
    try:
        operation = "create table accounts (username varchar(30), password varchar(22))"
        mycursor.execute(operation)
        sql = "INSERT INTO accounts (username, password) VALUES (%s, %s)"
        val = (input_name.user_text.lower(), input_pwd.user_text)
        mycursor.execute(sql, val)
        mydb.commit()
        print(3)
    except:
        sql = "INSERT INTO accounts (username, password) VALUES (%s, %s)"
        val = (input_name.user_text.lower(), input_pwd.user_text)
        mycursor.execute(sql, val)
        mydb.commit()
        print(4)



class BGM:
    def __init__(self,track):
        from pygame import mixer
        self.mixer = mixer
        # Starting the mixer
        self.mixer.init()
        
        # Loading the song
        self.mixer.music.load(track)
        
        # Setting the volume
        self.mixer.music.set_volume(0.2)
    
    def play(self):
        # Start playing the song
        self.mixer.music.play()
    
    def end(self):
        self.mixer.music.stop()
        pass
Seawalk_bgm = BGM("D:\\Python Stuff\\Music Synthesizer\\Homepage\\Seawalk.mp3")

class TextHP:

    def __init__(self):
        self.hpstate = 1
        self.th1 = 60
        self.text = txt("MUSIC SYNTHESIZER",
                        font = "D:/Python Stuff/Music Synthesizer/Homepage/Another Danger - Demo.otf",  
                        size = self.th1, 
                        color = "#eeeeee")
        self.th = self.text.get_height()
        self.tw = self.text.get_width()
        self.rect = self.text.get_rect()
        self.font = "D:/Python Stuff/Music Synthesizer/Homepage/Another Danger - Demo.otf"
        self.TL = ()
        self.TR = ()
        self.BL = ()
        self.BR = ()
        
    def draw(self,i=0,hpstate=1):
        global sizeiteration
        self.hpstate = hpstate
        self.th1 = int(60 * (Sw/Sw_org))
        if time.time()%0.05 > 0.03:
            sizeiteration += 1
        self.th2 = max(self.th1 - i,40)
        if self.hpstate == 2:
            self.font = "D:\Python Stuff\Music Synthesizer\Homepage\BRADHITC.TTF"
            self.th2 = 35
        self.text = txt("MUSIC SYNTHESIZER",
                        font = self.font,  
                        size = self.th2, 
                        color = "#eeeeee")
        self.th = self.text.get_height()
        self.tw = self.text.get_width()
        self.rect = self.text.get_rect()
        self.y = Sh/2-self.th/2
        if self.hpstate == 2:
            self.y = 40
        self.bl = S.blit(self.text ,(Sw/2-self.tw/2,self.y))
        self.TL = self.bl.topleft
        self.TR = self.bl.topright
        self.BL = self.bl.bottomleft
        self.BR = self.bl.bottomright
TxHP = TextHP()


class underline:
    def __init__(self,len=20,x=20,y=20):
        self.length = len
        self.x = x
        self.y = y
    
    def draw(self,len=20,x=20,y=20):
        self.length = len
        self.x = x
        self.y = y
        Dr.line(S,"#dddddd",(self.x,self.y),(self.x + self.length,self.y),8)
        pass
HPunderline = underline()

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
        self.select_all_state = "passive"
        #pwd
        self.hidepwd_img = pygame.image.load(r"D:\Python Stuff\Music Synthesizer\Homepage\Hidepwd.png")
        self.hidepwd_img = pygame.transform.scale(self.hidepwd_img,(33,33))
        self.showpwd_img = pygame.image.load(r"D:\Python Stuff\Music Synthesizer\Homepage\Showpwd.png")
        self.showpwd_img = pygame.transform.scale(self.showpwd_img,(33,33))
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
        
        #highlighting text
        if self.select_all_state == "active":
            highlightrect = self.user_txt1.get_rect(topleft = (self.TL[0]+7,self.TL[1]+3))
            Dr.rect(S,"light blue",highlightrect)

        #Getting cursor positions
        self.cursor_positions = []
        for i in range(len(self.user_text)):
            if self.type == "pwd":
                pos = txt("•"*len(self.user_text[:i]),size = 28)
            else:
                pos = txt(self.user_text[:i],size = 28)
            self.cursor_positions.append(pos.get_width() + self.TL[0] + 10)
        #print(self.cursor_positions)


        #Blitting text
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


class Submitbutton:
    def __init__(self,x = 250,y = 400,width = 100, height = 30, state = "passive",**kwargs):
        self.TL = ()
        self.TR = ()
        self.BL = ()
        self.BR = ()
        self.cols = {}
        self.w1 = width
        self.h1 = height
        self.state = state
        self.text = kwargs["text"]
        self.txt = txt(self.text,font = r"D:\Python Stuff\Music Synthesizer\Homepage\BRADHITC.TTF", color = "black")
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

submit1 = Submitbutton(text = "LOGIN")



class BGimg:
    def __init__(self,img):
        self.img = pygame.image.load(img)
        self.img_scaled = pygame.transform.scale(self.img,(Sw_org,Sh_org))
        pass
    def draw(self):
        self.img_scaled = pygame.transform.scale(self.img,(Sw,Sh))
        self.imgsrf = self.img_scaled.convert()
        S.blit(self.imgsrf,(0,0))
bg_img1 = BGimg(r"D:\Python Stuff\Music Synthesizer\Homepage\musicnote.jpg")



class HP:
    def __init__(self):
        self.state = False
    def action(self):
        if self.state == 1:
            TxHP.draw(i=sizeiteration,hpstate=self.state)
            HPunderline.draw(TxHP.tw,TxHP.BL[0],TxHP.BL[1])
            timer1 = Timer(time.time())
            timer1.draw()
        if self.state == 2:
            bg_img1.draw()
            TxHP.draw(hpstate=self.state)
            input_name.draw()
            input_pwd.draw()
            submit1.draw()
            timer1 = Timer(time.time())
            timer1.draw()
        if self.state == 0:
            self.txt = "DATA SUBMITTED"
            Seawalk_bgm.end()
            S.blit(txt(self.txt),(40,40))


        

run = True
starttime = time.time()
homepg = HP()
iteration = 0
sizeiteration = 0
tabslist = [input_name,input_pwd,submit1]
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
        homepg.state = 2
    else:
        Seawalk_bgm.end()
        homepg.state = 0
    if submit1.state == "active":
        homepg.state = 0
    homepg.action()
    try:
        1
        #print(input_name.user_text[input_name.cursor_pos-1])
    except:
        pass

    KEYSTATES = pygame.key.get_pressed()
    MODSTATES = pygame.key.get_mods()
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

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            input_name.select_all_state = "passive"
            input_pwd.select_all_state = "passive"
            mousecursormove(input_name)
            mousecursormove(input_pwd)
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
            if submit1.rect.collidepoint(mouse_pos):
                submit1.state = "active"
                now_active = submit1
                now_activeindex = tabslist.index(submit1)
                f_submit()
            else:
                submit1.state = "passive"
            
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
            if submit1.rect.collidepoint(mouse_pos):
                if submit1.state == "passive":
                    submit1.state = "hover"
            else:
                if submit1.state == "hover":
                    submit1.state = "passive"
        
        if event.type == pygame.KEYDOWN:
            
            gettxt(input_name)
            gettxt(input_pwd)
            cursormove(input_name)
            cursormove(input_pwd)
            tabaction()
            selectall(input_name)
            selectall(input_pwd)
    #print(input_pwd.pwd_img_state)
    #print(homepg.state)
    iteration += 1        
    D.update()