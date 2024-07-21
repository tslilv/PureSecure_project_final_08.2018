from tkinter import *
import Camera3
import smtplib
import smtp3

WINDOW_NAME = 'PURE_SECURE'
LABEL1 = 'Email'
LABEL2 = 'Set the timer'
BUTTON = 'Activate!'

# RGB colors
GRAY85 = '#d9d9d9'
GRAY64 = '#a3a3a3'
BLACK = '#000000'
WHITE = '#ffffff'

WINDOW_SIZE = "333x286+473+180"
X1 = '0.15'
X2 = '0.40'
Y1 = '0.40'
Y2 = '0.55'

BUTTON_X = '0.42'
BUTTON_Y = '0.76'
BUTTON_HEIGHT = '35'
BUTTON_WIDTH = '60'

font11 = "-family {Segoe UI} -size 12 -weight normal -slant " \
         "roman -underline 0 -overstrike 0"
font12 = "-family {Segoe UI} -size 12 -weight bold -slant " \
         "roman -underline 0 -overstrike 0"

# ERRORS
ERROR1 = "Enter email"
ERROR2 = "Enter min:sec"
ERROR3 = "Enter numbers only"
ERROR4 = "try again"

# MAIL
SUBJECT = "Welcome to Pure_Secure!"
BODY = "you have successfully signed in"


class HandleGUI:

    def __init__(self, master):

        self.email = ""

        # set tkinter master root
        self.master = master
        master.geometry(WINDOW_SIZE)
        master.title(WINDOW_NAME)
        master.configure(background=GRAY85)

        # "Email label"
        self.label1 = Label(master, text=LABEL1)
        self.create_label(self.label1, 0.2, 0.14, 21, 45)
        self.label1.configure(font=font11)

        # "Set the timer label"
        self.label2 = Label(master, text=LABEL2)
        self.create_label(self.label2, 0.2, 0.47, 16, 95)
        self.label2.configure(font=font11)

        self.entry1 = Entry(master)
        self.entry1.place(relx=0.21, rely=0.24, relheight=0.1, relwidth=0.58)
        self.entry1.configure(background="white")
        self.entry1.configure(disabledforeground=GRAY64)
        self.entry1.configure(foreground=BLACK)
        self.entry1.configure(insertbackground="black")
        self.entry1.configure(width=194)

        self.entry2 = Entry(master)
        self.entry2.insert(END, "min")
        self.entry2.place(relx=0.21, rely=0.56, relheight=0.1, relwidth=0.25)
        self.entry2.configure(background="white")
        self.entry2.configure(disabledforeground=GRAY64)
        self.entry2.configure(foreground=BLACK)
        self.entry2.configure(insertbackground="black")
        self.entry2.configure(width=84)

        self.entry3 = Entry(master)
        self.entry3.insert(END, "sec")
        self.entry3.place(relx=0.54, rely=0.57, relheight=0.1, relwidth=0.25)
        self.entry3.configure(background="white")
        self.entry3.configure(disabledforeground="#a3a3a3")
        self.entry3.configure(foreground=BLACK)
        self.entry3.configure(insertbackground="black")
        self.entry3.configure(width=84)

        self.label4 = Label(master)
        self.label4.place(relx=0.20, rely=0.35, height=15, width=70)
        self.label4.configure(background="#d9d9d9")
        self.label4.configure(disabledforeground=GRAY64)
        self.label4.configure(foreground=BLACK)
        self.label4.configure(text='')
        self.label4.configure(width=54)

        self.label3 = Label(master)
        self.label3.place(relx=0.48, rely=0.56, height=29, width=21)
        self.label3.configure(background=GRAY85)
        self.label3.configure(disabledforeground=GRAY64)
        self.label3.configure(font=font12)
        self.label3.configure(foreground=BLACK)
        self.label3.configure(text=''':''')
        self.label3.configure(width=21)

        self.label5 = Label(master)
        self.label5.place(relx=0.20, rely=0.675, height=15, width=120)
        self.label5.configure(background=GRAY85)
        self.label5.configure(disabledforeground=GRAY64)
        self.label5.configure(foreground=BLACK)
        self.label5.configure(text='')

        self.label6 = Label(master)
        self.label6.place(relx=0.05, rely=0.05, height=15, width=120)
        self.label6.configure(background=GRAY85)
        self.label6.configure(disabledforeground=GRAY64)
        self.label6.configure(foreground=BLACK, font=font12)
        self.label6.configure(text="")
        self.label6.configure(width=54)

        self.button1 = Button(master, text=BUTTON, command=self.activate)
        self.create_button(self.button1)

    @staticmethod
    def create_label(label, x, y, h, w):
        label.place(relx=x, rely=y, height=h, width=w)
        label.configure(background=GRAY85)

    @staticmethod
    def create_button(button):
        button.place(relx=BUTTON_X, rely=BUTTON_Y, height=BUTTON_HEIGHT, width=BUTTON_WIDTH)
        button.configure(activebackground=GRAY85, activeforeground=BLACK)
        button.configure(background=GRAY85, disabledforeground=GRAY64)
        button.configure(foreground=BLACK, highlightbackground=GRAY85)
        button.configure(highlightcolor=BLACK)

    def activate(self):
        error = False

        self.email = self.entry1.get()
        if self.email is "":
            self.label4.configure(text=ERROR1, fg="red")
            error = True

        if self.entry2.get() is "" or self.entry3.get() is "":
            self.label5.configure(text=ERROR2, fg="red")
            error = True

        if not self.represents_int(self.entry2.get()) and not self.represents_int(self.entry3.get()):
            self.label5.configure(text=ERROR3, fg="red")
            error = True

        if not error:
            try:
                smtp3.send_email(self.email, SUBJECT, BODY, ['a.jpg'])
                self.countdown(int(self.entry2.get())*60+int(self.entry3.get()))
            except smtplib.SMTPException:
                self.label4.configure(text=ERROR4, fg="red")

    @staticmethod
    def represents_int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def countdown(self, count):
        # change text in label

        self.label6['text'] = "starts in..." + str(count)

        if count > 0:
            # call countdown again after 1000ms (1s)
            self.master.after(1000, self.countdown, count-1)

        if count == 0:
            self.master.destroy()
            Camera3.main(self.email)


def base_gui():

    window = Tk()
    HandleGUI(window)
    window.mainloop()
