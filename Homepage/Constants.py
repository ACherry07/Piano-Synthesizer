import mysql.connector as M
from tkinter import *
from tkinter.messagebox import askyesno,showinfo
try:
    MyDB = M.connect(host="localhost",user="root",password="mysql", database = "Ashishproject")
except:
    MyDB = M.connect(host="localhost",user="root",password="l9hfG&7a", database = "Ashishproject")
MyC = MyDB.cursor()
Exe= MyC.execute
def getuser():
    global UN
    Exe("Select currentuser from currentuser")
    UN = MyC.fetchall()[0][0]
    print(UN)
    return UN
def playsong(UN):
    try:
        Exe(f"update currentuser set currentsong = NULL")
        MyDB.commit()
        Exe(f"Select Songname from {UN}songs")
        l = [i[0] for i in MyC.fetchall()]

        #Create an instance of tkinter frame
        win= Tk()
        #Define the size of window or frame
        #win.geometry("715x250")
        #Set the Menu initially
        menu= StringVar()
        menu.set("Select Song")
        #Create a dropdown Menu
        drop= OptionMenu(win, menu,*l)
        drop.pack()
        def selectbuttonaction():
            global song
            song = menu.get()
            print(song)
            win.destroy()
            if song != "Select Song":
                Exe(f"update currentuser set currentsong = '{song}'")
            MyDB.commit()
        def delbuttonaction():
            global song
            song = menu.get()
            print(song)
            answer1 = (askyesno("Delete Song","Are you sure you wish to delete?\n"+
            "This action cannot be undone!"))
            if answer1 == True:
                win.destroy()
                if song != "Select Song":
                    Exe(f"delete from {UN}songs where songname = '{song}'")
                MyDB.commit()
        songselbutton = Button(
            win,
            text = "Play Song",
            command = selectbuttonaction
            )
        songdelbutton = Button(
            win,
            text = "Delete Song",
            command = delbuttonaction
        )
        songselbutton.pack()
        songdelbutton.pack()
        win.mainloop()
        
        try:
            Exe(f"Select recording from {UN}songs where songname = (select currentsong from currentuser)")
            recording = MyC.fetchall()[0]
            Exe(f"update currentuser set currentsong = NULL")
            MyDB.commit()
            return recording
        except:
            pass
        
    except:
        win.wm_withdraw()
        showinfo("Message","No Saved Songs")
        win.destroy()