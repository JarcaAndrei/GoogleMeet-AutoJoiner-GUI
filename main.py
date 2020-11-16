from tkinter import Button, Tk, HORIZONTAL
from tkinter.ttk import Progressbar
import time
from time import gmtime,strftime
import threading
import os
import shutil
from threading import Thread, Event
import tkinter
import tkinter as tk
import progressbar
from tkinter import ttk  
from tkinter import *
import tkinter.messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import schedule
import datetime
from datetime import datetime
import signal
import sqlite3
# Options to allow chrome to use mic and cam etc
opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_experimental_option("excludeSwitches", ["enable-logging"])

# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
"profile.default_content_setting_values.media_stream_mic": 1, 
"profile.default_content_setting_values.media_stream_camera": 1,
"profile.default_content_setting_values.geolocation": 1, 
"profile.default_content_setting_values.notifications": 1 
})
def xpathfinder(path): #we need this function in case of a slow computer or some form of lag 
    while True:
        try:
            element=driver.find_element_by_xpath(path)
        except:
            time.sleep(2)
        else:
            return element
def gmail_login(sub,u,p,times):
    global driver
    driver = webdriver.Chrome(options=opt, executable_path=r'C:\webdrivers\chromedriver.exe') 
    driver.get("https://accounts.google.com/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1#identifier")
        # E-Mail:
    xpathfinder("//input[@name='identifier']").send_keys(u)
        # Next Button:
    xpathfinder("//*[@id='identifierNext']/div/button/div[2]").click()
        # Password:
    xpathfinder("//input[@name='password']").send_keys(p)
        # Next Button:
    xpathfinder("//*[@id='passwordNext']/div/button").click()
    time.sleep(2)
        # Opening Meet:    
    try:
        driver.get(sub)
    except:
        tkinter.messagebox.showwarning("Warning","Invalid link")
        return
    while True:
        try:
            driver.find_element_by_xpath("//*[@id='yDmH0d']/c-wiz/div/div/div[7]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span")
        except:
            curTime=strftime("%H:%M")
            if curTime==str(times):
                return
            driver.get(sub)
            time.sleep(5)
        else:
            break
    time.sleep(2)
    #muting mic and disabling cam with hotkeys
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('d').key_up(Keys.CONTROL).perform()
    ActionChains(driver).send_keys(Keys.ENTER)
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('e').key_up(Keys.CONTROL).perform()
    ActionChains(driver).send_keys(Keys.ENTER)
    #join button
    xpathfinder("//*[@id='yDmH0d']/c-wiz/div/div/div[7]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span").click() #mute,video
    time.sleep(60) # we need this sleep so that when the loop further down comes again, it will not open again
                    # the error case would be only if we have some sort of meeting that lasts 1 minute, but that's unrealistic 

class Login:
    def __init__(self,master):
        self.tablemaker() # creating tables in the database for account and for meetings
        self.master=master
        self.master.title("Auto-joiner")
        self.master.geometry("800x769+231+100")

        #self.master.geometry('750x300+0+0')
        self.master.config(bg='LightSkyBlue4')
        self.frame= Frame(self.master,bg='LightSkyBlue4')
        self.frame.pack()
        self.Username=StringVar()
        self.Password=StringVar()
        self.Del=StringVar()
        self.Title=Label(self.frame,text='Auto-Joiner',font=('arial',50,'bold'),bg='LightSkyBlue4',fg='gray20')
        self.Title.grid(row=0,column=0,columnspan=2)

        self.Logfr1=LabelFrame(self.frame,width=750,height=200,font=('arial',20,'bold'),relief='ridge',bg='cyan4',bd=10)
        self.Logfr1.grid(row=1,column=0)

        self.Logfr2=LabelFrame(self.frame,width=550,height=200,font=('arial',20,'bold'),relief='ridge',bg='cyan4',bd=10)
        self.Logfr2.grid(row=2,column=0)
        #
        self.User=Label(self.Logfr1,text='E-mail',font=('arial',20,'bold'),bd=22,bg='cyan4',fg='gray20')
        self.User.grid(row=0,column=0)
        self.txtUser=Entry(self.Logfr1,font=('arial',20,'bold'),bg='aquamarine3',textvariable=self.Username)#
        self.txtUser.grid(row=0,column=1)

        self.Pass=Label(self.Logfr1,text='Password',font=('arial',20,'bold'),bd=22,bg='cyan4',fg='gray20')
        self.Pass.grid(row=1,column=0)
        self.txtPass=Entry(self.Logfr1,font=('arial',20,'bold'),bg='aquamarine3',textvariable=self.Password,show="*")#
        self.txtPass.grid(row=1,column=1)

        

       ###
        conn=sqlite3.connect('timetable.db')
        c=conn.cursor()
        c.execute("SELECT *, oid FROM userpass ")
        records= c.fetchall()
        # stuff for remaining logged in
        for record in records:
            if record[2]==1:
                self.txtUser.insert(END, record[0])
                self.txtPass.insert(END, record[1])
                break
        flag=0
        # this will show the checkmark checked in case we previously chose to remain logged in
        for record in records:
            if record[2]==1:
                self.var = IntVar(value=1)
                flag=1
                break
        if flag==0:
            self.var=IntVar(value=0)
        conn.commit()
        conn.close()
        #other interface stuff
        self.checks=Checkbutton(self.Logfr1, text="Check in order to remain logged in",font=('arial',20,'bold'),bg='cyan4',fg='gray20', variable=self.var)
        self.checks.grid(row=2,column=0,columnspan=2)

        self.btnLog=Button(self.Logfr2,text='Login',font=('arial',20,'bold'), width=16,command=self.LoginSys)
        self.btnLog.grid(row=3,column=0,pady=20,padx=8)

        self.btnReset=Button(self.Logfr2,text='Register',font=('arial',20,'bold'), width=16,command=self.Register)
        self.btnReset.grid(row=3,column=1,pady=20,padx=8)

        self.btnExit=Button(self.Logfr2,text='Exit', font=('arial',20,'bold'),width=16,command=self.exit)
        self.btnExit.grid(row=4,column=1,pady=20,padx=8)

        self.btnQuery=Button(self.Logfr2,text='Show Accounts',font=('arial',20,'bold'), width=16,command=self.logQuery)
        self.btnQuery.grid(row=4,column=0,pady=20,padx=8)

        self.btnQuery=Button(self.Logfr2,text='Delete account',font=('arial',20,'bold'), width=16,command=self.delUser)
        self.btnQuery.grid(row=5,column=0,columnspan=2,pady=20,padx=8)

        self.box=Entry(self.Logfr2,font=('arial',20,'bold'),bg='aquamarine3',textvariable=self.Del,justify='center')
        self.box.grid(row=6,column=0, columnspan=2,pady=20,padx=8)

    def delUser(self):
        # deleting an account
        d=self.Del.get()
        conn= sqlite3.connect('timetable.db')
        c=conn.cursor()
        try:
            c.execute("DELETE from userpass WHERE oid=" +  d)
        except:
            return

        self.box.delete(0, END)

        conn.commit()
        conn.close()

    def tablemaker(self):
        conn= sqlite3.connect('timetable.db')
        c=conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS addresses (
                    day text,
                    name text,
                    starting_hour text,
                    ending_hour text,
                    link text
                    )""")

        c.execute("""CREATE TABLE IF NOT EXISTS userpass(
                    username text,
                    password text,
                    checker integer 
                    )""")
        # checker integer is for the -remain logged in- option
        conn.commit()
        conn.close()

    def LoginSys(self):
        u=self.Username.get()
        p=self.Password.get()
        conn=sqlite3.connect('timetable.db')
        c=conn.cursor()
        c.execute("SELECT *, oid FROM userpass ")
        records= c.fetchall()
        ok=0
        # this stuff is for the logged in thing and all the cases of putting an account and checking/not checking the box etc
        for record in records:
            if u==str(record[0]) and p==str(record[1]):
                if self.var.get()==1 and record[2]==0:
                    for sec_record in records:
                        if sec_record[2]==1:
                            record_id=sec_record[3]
                            c.execute("""UPDATE userpass SET 
                                        checker=:checker

                            WHERE oid= :oid""",
                            {
                            'checker': 0,
                            'oid': record_id
                            })
                            break
                    record_id=record[3]
                    c.execute("""UPDATE userpass SET 
                                checker=:checker

                    WHERE oid= :oid""",
                    {
                    'checker': 1,
                    'oid': record_id
                    })
                elif self.var.get()==0:
                    for sec_record in records:
                        if sec_record[2]==1:
                            record_id=sec_record[3]
                            c.execute("""UPDATE userpass SET 
                                        checker=:checker

                            WHERE oid= :oid""",
                            {
                            'checker': 0,
                            'oid': record_id
                            })
                            break
                
                conn.commit()
                conn.close()
                ok=1
                self.master.destroy()
                #we launch the actual thing 
                root=tkinter.Tk()
                app=App(root,u,p)
                root.mainloop()
                break
        if ok==0:
            conn.commit()
            conn.close()
            tkinter.messagebox.showwarning("Warning","Invalid Username or Password")
            self.Username.set("")
            self.Password.set("")
            self.txtUser.focus()
    def Register(self):
        self.newWin3=Toplevel(self.master)
        self.app=regWin(self.newWin3)
    def exit(self):
        self.exit=tkinter.messagebox.askyesno("Exit","Are you sure?")
        if self.exit>0:
            self.master.destroy()
        else:
            return
    def logQuery(self):
        self.add_query1=tk.Toplevel(self.master)
        self.add_query1.title("All accounts")
        self.add_query1.config(bg='cyan4')

        
        conn=sqlite3.connect('timetable.db')
        c=conn.cursor()

        c.execute("SELECT *,oid FROM userpass ")
        records= c.fetchall()
        
        self.Lbfr4=LabelFrame(self.add_query1,width=750,height=200,font=('arial',20,'bold'),relief='ridge',bg='cyan4',bd=10)
        self.Lbfr4.grid(row=1,column=2)
#-------------------------------------
        self.e=Entry(self.Lbfr4,width=12,bg='cyan4', fg='black', font=('Arial',20,'bold'),justify='center')
        self.e.grid(row=0,column=0)
        self.e.insert(END,"E-mail")
        self.e=Entry(self.Lbfr4,width=12,bg='cyan4', fg='black', font=('Arial',20,'bold'),justify='center')
        self.e.grid(row=0,column=1)
        self.e.insert(END,"Password")
        self.e=Entry(self.Lbfr4,width=12,bg='cyan4', fg='black', font=('Arial',20,'bold'),justify='center')
        self.e.grid(row=0,column=2)
        self.e.insert(END,"ID")
#-------------------------------------
        i=1
        temp=0
        for record in records:
            for j in range(3): 
                if j==2:
                    j=j+1
                self.e = Entry(self.Lbfr4, width=12,bg='cyan4', fg='black', font=('Arial',20,'bold'),justify='center') 
                  
                self.e.grid(row=i, column=temp) 
                self.e.insert(END, record[j]) 
                temp=temp+1
            i=i+1
            temp=0
        conn.commit()
        conn.close()
        
#

class regWin:
    def __init__(self,master):
        self.master=master
        self.master.title("Register")
        self.master.config(bg='LightSkyBlue4')
        self.frame= Frame(self.master,bg='LightSkyBlue4')
        self.frame.pack()
        self.Username=StringVar()
        self.Password=StringVar()

        self.Title=Label(self.frame,text='Register',font=('arial',50,'bold'),bg='LightSkyBlue4',fg='gray20')
        self.Title.grid(row=0,column=0,columnspan=2)

        self.Logfr1=LabelFrame(self.frame,width=750,height=200,font=('arial',20,'bold'),relief='ridge',bg='cyan4',bd=10)
        self.Logfr1.grid(row=1,column=0)

        #
        self.User=Label(self.Logfr1,text='Username',font=('arial',20,'bold'),bd=22,bg='cyan4',fg='gray20')
        self.User.grid(row=0,column=0)
        self.txtUser=Entry(self.Logfr1,font=('arial',20,'bold'),bg='aquamarine3',textvariable=self.Username)
        self.txtUser.grid(row=0,column=1,padx=10)

        self.Pass=Label(self.Logfr1,text='Password',font=('arial',20,'bold'),bd=22,bg='cyan4',fg='gray20')
        self.Pass.grid(row=1,column=0)
        self.txtPass=Entry(self.Logfr1,font=('arial',20,'bold'),bg='aquamarine3',textvariable=self.Password,show='*')
        self.txtPass.grid(row=1,column=1)

        self.btnLog=Button(self.Logfr1,text='Register',font=('arial',20,'bold'), width=16,command=self.Registered)
        self.btnLog.grid(row=3,column=0,columnspan=2,pady=20,padx=8)
    def Registered(self):
        u=self.Username.get()
        p=self.Password.get()
        conn= sqlite3.connect('timetable.db')
        c=conn.cursor()
        c.execute("INSERT INTO userpass VALUES (:username, :password, :checker)",
                {
                    'username': u,
                    'password': p,
                    'checker': 0
                })
        conn.commit()
        conn.close()
        self.master.destroy()

class App(Tk):
    def __init__(self,master,u,p):
        self.master=master
        self.u=u
        self.p=p

        self.master.title("Auto-joiner")
        self.master.config(bg='LightSkyBlue4')
        self.master.geometry("880x619+200+120")
        self.frame= Frame(self.master)
        self.frame.pack()
        self.frame.config(bg='LightSkyBlue4')
        self.trb=Label(self.frame,text='\n',font=('arial',20,'bold'),bg='LightSkyBlue4',fg='gray20')
        self.trb.grid(row=0,column=0)
        self.Logfr1=LabelFrame(self.frame,width=750,height=200,font=('arial',20,'bold'),relief='ridge',bg='cyan4',bd=10)
        self.Logfr1.grid(row=1,column=0)
#
#

        self.Title=Label(self.Logfr1,text='Meet Auto-Joiner',font=('arial',50,'bold'),bg='cyan4',fg='gray20')
        self.Title.grid(row=0,column=0,columnspan=2,ipadx=50)
        self.btn = Button(self.Logfr1, text='Start',font=('arial',15,'bold'), width=16, command=self.start)
        self.btn.grid(row=1,column=0,ipadx=30)

        self.progress = Progressbar(self.Logfr1, orient=HORIZONTAL,length=260,  mode='indeterminate')
        self.progress.grid(row=2,column=0,ipady=11)
        #btns and entries
        global delete_box
        delete_box=Entry(self.Logfr1,width=20,font=('arial',15,'bold'),bg='aquamarine3',justify='center')
        delete_box.grid(row=5,column=0,columnspan=3)

        delete_box_label= Label(self.Logfr1, text= "Input your ID in the box below in order to Delete/Edit a meeting\nYou can find the ID in the timetable for the desired day ",font=('arial',15,'bold'),bd=22,bg='cyan4',fg='black')
        delete_box_label.grid(row=4,column=0,columnspan=3)

        self.submit_btn= Button(self.Logfr1, text= "Schedule a meeting",font=('arial',15,'bold'), width=16, command=self.submit)
        self.submit_btn.grid(row=1, column=1,columnspan=2,  pady= 10, padx=30 , ipadx=34)

        self.query_btn= Button(self.Logfr1, text= "Timetable",font=('arial',15,'bold'), width=11, command=self.query)
        self.query_btn.grid(row=3, column=1, columnspan= 2,pady=0, ipadx=15)

        self.clicked_query=StringVar()
        self.currentDay=datetime.today().strftime("%A")
        self.clicked_query.set(self.currentDay)
        self.select_query=OptionMenu(self.Logfr1,self.clicked_query,"Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
        self.select_query.grid(row=2,column=1,columnspan=2,pady=10,ipadx=8,ipady=2)
        self.select_query.config(font=('arial',15,'bold'), width=10)
        self.select_query['menu'].config(font=('arial',15,'bold'))

        self.delete_btn= Button(self.Logfr1, text= "Delete a meeting",font=('arial',15,'bold'), width=16, command=self.delete)
        self.delete_btn.grid(row=6, column=1,columnspan=2,  ipadx=43)

        self.edit_btn= Button(self.Logfr1, text="Edit a meeting",font=('arial',15,'bold'), width=16, command=self.edit)
        self.edit_btn.grid(row=6,column=0,columnspan=1, pady=10, padx=18,ipadx=35)

        self.exit_btn= Button(self.Logfr1, text="Stop",font=('arial',15,'bold'), width=16, command=self.exit)
        self.exit_btn.grid(row=3,column=0, pady=10, padx=10,ipadx=30)
        self.t=0
    def exit(self):
        self.t=1
    def delete(self):
        conn= sqlite3.connect('timetable.db')
        c=conn.cursor()
        try:
            c.execute("DELETE from addresses WHERE oid=" +  delete_box.get())
        except:
            return

        delete_box.delete(0, END)

        conn.commit()
        conn.close()

    def edit(self):

        self.newWin1=Toplevel(self.master)
        self.app=editWin(self.newWin1)

    def submit(self):

        self.newWin2=Toplevel(self.master)
        self.app=submitWin(self.newWin2)

    def query(self):

        # shows all the records
        self.add_query=tk.Toplevel(self.master)
        self.add_query.config(bg='cyan4')
        self.add_query.title("Timetable")

        conn=sqlite3.connect('timetable.db')
        c=conn.cursor()
        c.execute("SELECT *,oid FROM addresses ORDER BY datetime(starting_hour) ASC")
        records= c.fetchall()
        record_id=self.clicked_query.get()

        self.Lbfr3=LabelFrame(self.add_query,width=750,height=200,font=('arial',20,'bold'),relief='ridge',bg='cyan4',bd=10)
        self.Lbfr3.grid(row=1,column=2)
#-------------------------------------
        self.e=Entry(self.Lbfr3,width=12,bg='cyan4', fg='black', font=('Arial',20,'bold'),justify='center')
        self.e.grid(row=0,column=1)
        self.e.insert(END,"Day")
        self.e=Entry(self.Lbfr3,width=12,bg='cyan4', fg='black', font=('Arial',20,'bold'),justify='center')
        self.e.grid(row=0,column=2)
        self.e.insert(END,"Name")
        self.e=Entry(self.Lbfr3,width=12,bg='cyan4', fg='black', font=('Arial',20,'bold'),justify='center')
        self.e.grid(row=0,column=3)
        self.e.insert(END,"Starting Hour")
        self.e=Entry(self.Lbfr3,width=12,bg='cyan4', fg='black', font=('Arial',20,'bold'),justify='center')
        self.e.grid(row=0,column=4)
        self.e.insert(END,"Ending Hour")
        self.e=Entry(self.Lbfr3,width=12,bg='cyan4', fg='black', font=('Arial',20,'bold'),justify='center')
        self.e.grid(row=0,column=5)
        self.e.insert(END,"Link")
        self.e=Entry(self.Lbfr3,width=12,bg='cyan4', fg='black', font=('Arial',20,'bold'),justify='center')
        self.e.grid(row=0,column=6)
        self.e.insert(END,"ID")
#-------------------------------------
        i=1
        temp=0
        for record in records:
            if record_id==record[0]:
                for j in range(1,7): 

                    self.e = Entry(self.Lbfr3, width=12,bg='cyan4', fg='black', font=('Arial',20,'bold'),justify='center') 
                    self.e.grid(row=i, column=j) 
                    self.e.insert(END, record[j-1])

                i=i+1
        conn.commit()
        conn.close()
    def start(self):
        def isAlive():
            try:
                driver.current_url
                return True
            except:
                return False
        def real_start():
            self.progress.start()
            #the actual thread starts here 
            conn=sqlite3.connect('timetable.db')
            c=conn.cursor()
            c.execute("SELECT *, oid FROM addresses ")
            records= c.fetchall()
            conn.commit()
            conn.close()
            ok=0
            while True:
                if self.t==1:
                    self.t=0
                    break
                curTime=strftime("%H:%M")
                dayy=datetime.today().strftime("%A")
                for record in records:
                    if str(record[2])==curTime and record[0]==dayy:
                        #if we got the starting hour and corect day:
                        ok=0
                        sub=str(record[4])
                        gmail_login(sub,self.u,self.p,record[3]) #
                    elif ok==0 and str(record[3])==curTime: # if during the previous meeting we get the ending hour, we need the ok variable to not
                        loop=1 # we have some problems here, because we either want to exit the meeting, due to a gap between meetings or a new meeting starts right after 
                            # and we need to synch this stuff
                        c=0
                        while loop:
                            # the loop will check if there are only 5 participants left and it'll exit and at the same time if another meeting has started
                            # if it exits before the time the next meeting has started, ok becomes 1 , loop 0 and we go back to the main if and will start from there again
                            if isAlive()==False:
                                ok=1
                                time.sleep(50)
                                break
                            try:
                                numOfParticipants=int(driver.find_element_by_xpath('/html/body/div[1]/c-wiz/div[1]/div/div[7]/div[3]/div[6]/div[3]/div/div[2]/div[1]/span/span/div/div/span[2]').get_attribute('innerHTML'))
                            except:
                                numOfParticipants=0
                            testing=0
                            if numOfParticipants<=5:
                                c=1
                            if c==1:
                                loop=0
                                ok=1
                                driver.close()
                                break
                            else:
                                d=strftime("%H:%M")
                                for idem in records:
                                    if str(idem[2])==d:
                                        loop=0
                                        ok=1
                                        driver.close()
                                        break
                                time.sleep(5) #increases the performance a bit
                time.sleep(5)
            #self.start_temp()

            
            ####fasffasgasg

        global submit_thread
        submit_thread = threading.Thread(target=real_start)
        submit_thread.daemon = True
        submit_thread.start()
        self.master.after(20, self.check_submit_thread)

    def check_submit_thread(self):
        if submit_thread.is_alive():
            self.master.after(20, self.check_submit_thread)
        else:
            self.progress.stop()

class editWin:
    def __init__(self,master):
        self.master=master
        self.master.title("Edit")
        self.master.config(bg='LightSkyBlue4')

        self.frame= Frame(self.master)
        self.frame.pack()

        self.Logfr1=LabelFrame(self.frame,width=750,height=200,font=('arial',20,'bold'),relief='ridge',bg='cyan4',bd=10)
        self.Logfr1.grid(row=1,column=0)
        conn= sqlite3.connect('timetable.db')
        c=conn.cursor()

        record_id= delete_box.get()
        try:
            c.execute("SELECT * FROM addresses WHERE oid= " + record_id )
        except:
            self.master.destroy()
            return
        records= c.fetchall()

        self.day_editor=Entry(self.Logfr1,font=('arial',20,'bold'),bg='aquamarine3',width=30)
        self.day_editor.grid(row=0, column=3, padx=10)
        self.name_editor=Entry(self.Logfr1,font=('arial',20,'bold'),bg='aquamarine3',width=30)
        self.name_editor.grid(row=1, column=3)
        self.shour_editor=Entry(self.Logfr1,font=('arial',20,'bold'),bg='aquamarine3',width=30)
        self.shour_editor.grid(row=2, column=3)
        self.fhour_editor=Entry(self.Logfr1,font=('arial',20,'bold'),bg='aquamarine3',width=30)
        self.fhour_editor.grid(row=3, column=3)
        self.link_editor=Entry(self.Logfr1,font=('arial',20,'bold'),bg='aquamarine3',width=30)
        self.link_editor.grid(row=4 , column=3)


        day_label_editor=Label(self.Logfr1,font=('arial',20,'bold'),bd=22,bg='cyan4',fg='black',text="Day")
        day_label_editor.grid(row=0, column=2, padx=40)
        name_label_editor=Label(self.Logfr1,font=('arial',20,'bold'),bd=22,bg='cyan4',fg='black',text="Name")
        name_label_editor.grid(row=1, column=2)
        shour_label_editor=Label(self.Logfr1,font=('arial',20,'bold'),bd=22,bg='cyan4',fg='black',text="Starting Hour")
        shour_label_editor.grid(row=2, column=2)
        fhour_finala_label_editor=Label(self.Logfr1,font=('arial',20,'bold'),bd=22,bg='cyan4',fg='black',text="Ending Hour")
        fhour_finala_label_editor.grid(row=3, column=2)
        link_label_editor=Label(self.Logfr1,font=('arial',20,'bold'),bd=22,bg='cyan4',fg='black',text="Link")
        link_label_editor.grid(row=4 , column=2)

        for record in records:
            self.day_editor.insert(0, record[0])
            self.name_editor.insert(0, record[1])
            self.shour_editor.insert(0, record[2])
            self.fhour_editor.insert(0, record[3])
            self.link_editor.insert(0, record[4])

        edit_btn= Button(self.Logfr1, text= "Save edit",font=('arial',20,'bold'), width=16, command=self.update)
        edit_btn.grid(row=6,column=2, columnspan=2, pady=10, padx=10, ipadx=100)
    def update(self):

        timeformat="%H:%M"
        try:
            validtime = datetime.strptime(self.shour_editor.get(), timeformat)
            validtime = datetime.strptime(self.fhour_editor.get(), timeformat)
        except:
            tkinter.messagebox.showwarning("Warning","Wrong starting/ending hour format, e.g.: '08:24' or '8:24'  ")
            self.master.focus()
            return

        conn= sqlite3.connect('timetable.db')
        c=conn.cursor()
        record_id=delete_box.get()
        c.execute("""UPDATE addresses SET 
            day=:day,
            name=:name,
            starting_hour=:starting_hour,
            ending_hour=:ending_hour,
            link=:link

            WHERE oid= :oid""",
            {
            'day': self.day_editor.get(),
            'name': self.name_editor.get(),
            'starting_hour': self.shour_editor.get(),
            'ending_hour': self.fhour_editor.get(),
            'link': self.link_editor.get(),
            'oid': record_id
            })
        conn.commit()
        conn.close()
        self.master.destroy()

class submitWin:
    def __init__(self,master):
        self.master=master
        self.master.title("Add")
        self.master.config(bg='LightSkyBlue4')
        self.frame= Frame(self.master,bg='LightSkyBlue4')
        self.frame.pack()

        self.Logfr1=LabelFrame(self.frame,width=750,height=200,font=('arial',20,'bold'),relief='ridge',bg='cyan4',bd=10)
        self.Logfr1.grid(row=1,column=0)

        self.clicked=StringVar()
        self.currentDay=datetime.today().strftime("%A")
        self.clicked.set(self.currentDay)
        self.drop_day=OptionMenu(self.Logfr1,self.clicked,"Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
        self.drop_day.grid(row=0,column=3)
        self.drop_day.config(font=('arial',15,'bold'), width=37,pady=3)
        self.drop_day['menu'].config(font=('arial',15,'bold'))
        self.name=Entry(self.Logfr1,width=30,font=('arial',20,'bold'),bg='aquamarine3')
        self.name.grid(row=1, column=3,padx=10)
        self.shour=Entry(self.Logfr1,width=30,font=('arial',20,'bold'),bg='aquamarine3')
        self.shour.grid(row=2, column=3)
        self.fhour=Entry(self.Logfr1,width=30,font=('arial',20,'bold'),bg='aquamarine3')
        self.fhour.grid(row=3, column=3)
        self.link=Entry(self.Logfr1,width=30,font=('arial',20,'bold'),bg='aquamarine3')
        self.link.grid(row=4 , column=3)

        self.day_label=Label(self.Logfr1,text="Day",font=('arial',20,'bold'),bd=22,bg='cyan4')
        self.day_label.grid(row=0, column=2, padx=40)
        self.name_label=Label(self.Logfr1,text="Name",font=('arial',20,'bold'),bd=22,bg='cyan4')
        self.name_label.grid(row=1, column=2)
        self.shour_label=Label(self.Logfr1,text="Starting Hour",font=('arial',20,'bold'),bd=22,bg='cyan4')
        self.shour_label.grid(row=2, column=2)
        self.fhour_label=Label(self.Logfr1,text="Ending Hour",font=('arial',20,'bold'),bd=22,bg='cyan4')
        self.fhour_label.grid(row=3, column=2)
        self.link_label=Label(self.Logfr1,text="Link",font=('arial',20,'bold'),bd=22,bg='cyan4')
        self.link_label.grid(row=4 , column=2)
        
        self.edit_btn= Button(self.Logfr1, text= "Add",font=('arial',20,'bold'), width=16, command=self.temp_submit)
        self.edit_btn.grid(row=6,column=2, columnspan=2, pady=10, padx=10, ipadx=100)
    def temp_submit(self):

        conn= sqlite3.connect('timetable.db')
        c=conn.cursor()
        shourTemp=self.shour.get()
        fhourTemp=self.fhour.get()
        if self.shour.get()=="" or self.fhour.get()=="":
            tkinter.messagebox.showwarning("Warning","You haven't input a starting or ending hour")
            self.master.focus()
            return
        if len(shourTemp)==4:
            shourTemp='0'+shourTemp
        if len(fhourTemp)==4:
            fhourTemp='0'+fhourTemp
        timeformat="%H:%M"
        try:
            validtime = datetime.strptime(shourTemp, timeformat)
            validtime = datetime.strptime(fhourTemp, timeformat)
        except:
            tkinter.messagebox.showwarning("Warning","Wrong starting/ending hour format, e.g.: '08:24' or '8:24'  ")
            self.master.focus()
            return

        c.execute("INSERT INTO addresses VALUES (:day, :name, :starting_hour, :ending_hour, :link)",
                {
                    'day': self.clicked.get(),
                    'name': self.name.get(),
                    'starting_hour': shourTemp,
                    'ending_hour': fhourTemp,
                    'link': self.link.get()
                })

        self.name.delete(0, END)
        self.shour.delete(0, END)
        self.fhour.delete(0, END)
        self.link.delete(0, END)
        conn.commit()
        conn.close()

def main():
    root=tkinter.Tk()
    app=Login(root)
    root.mainloop()


if __name__ == '__main__':
    main()
