from Tkinter import *
import Camera3
import smtplib
from PIL import ImageTk, Image
import smtp3
import Client

WINDOW_NAME = 'PURE_SECURE'
LABEL1 = 'EMAIL'
LABEL2 = 'PASSWORD'
LABEL3 = '''STEP 1'''
BUTTON1 = '''I'M A NEW USER!'''
MSG = '''sign up in order to have access to your data online'''

# ERRORS
ERROR1 = "Enter email"
ERROR2 = "Enter password"
ERROR3 = "Enter email and password"
ERROR4 = "Password must be at least 8 characters long"
ERROR5 = "note: you have another account connected to this email."
ERROR6 = "email address is illegal"

# MAIL
SUBJECT = "Welcome to Pure_Secure!"
BODY = "you have successfully signed in"

# RGB colors
GRAY85 = '#d9d9d9'
GRAY64 = '#a3a3a3'
BLACK = '#000000'
WHITE = '#ffffff'

WINDOW_SIZE = "416x328+569+161"
X1 = '0.15'
X2 = '0.40'
Y1 = '0.40'
Y2 = '0.55'

BUTTON_X1 = '0.31'
BUTTON_Y = '0.75'
BUTTON_HEIGHT = '35'
BUTTON_WIDTH = '150'

FONT10 = "-family {Segoe UI} -size 10 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"
FONT9 = "-family {Segoe UI} -size 12 -weight bold -slant roman"  \
            " -underline 0 -overstrike 0"


class HandleGUI:

    def __init__(self, master):

        self.master = master
        master.geometry(WINDOW_SIZE)
        master.title(WINDOW_NAME)
        master.configure(background=WHITE)

        self.message1 = Message(master)
        self.message1.place(relx=0.13, rely=0.1, relheight=0.20, relwidth=0.8)
        self.message1.configure(font=FONT10, background=WHITE)
        self.message1.configure(text=MSG)
        self.message1.configure(width=220)

        # empty label
        self.label4 = Label(master)
        self.label4.place(relx=0.13, rely=0.28, height=27, relwidth=1)
        self.label4.configure(font=FONT10, background=WHITE, fg='red', anchor=W)

        # step1 label
        self.label3 = Label(master)
        self.label3.place(relx=0.13, rely=0.08, height=27, width=56)
        self.label3.configure(font=FONT9, background=WHITE)
        self.label3.configure(text=LABEL3)

        # Email Label
        self.label1 = Label(master, text=LABEL1)
        self.create_label(self.label1, X1, Y1, 0.1, 40)

        # Password Label
        self.label2 = Label(master, text=LABEL2)
        self.create_label(self.label2, X1, Y2, 0.1, 68)

        # Email Entry
        self.entry1 = Entry(master)
        self.entry1.place(relx=X2, rely=Y1, relheight=0.1, relwidth=0.45)
        self.entry1.configure(background=WHITE, disabledforeground=GRAY64)
        self.entry1.configure(foreground=BLACK, width=185)

        # Password Entry
        self.entry2 = Entry(master)
        self.entry2.place(relx=X2, rely=Y2, relheight=0.1, relwidth=0.45)
        self.entry2.configure(background=WHITE, disabledforeground=GRAY64)
        self.entry2.configure(foreground=BLACK, width=185)

        # New User Button
        self.button1 = Button(master, command=self._new_user_btn, text=BUTTON1)
        self.create_button(self.button1, BUTTON_X1)

    @staticmethod
    def create_label(label, x, y, h, w):
        label.place(relx=x, rely=y, relheight=h, width=w)
        label.configure(background=WHITE)
        label.configure(disabledforeground=GRAY64)
        label.configure(foreground=BLACK)

    @staticmethod
    def create_button(button, x):
        button.place(relx=x, rely=BUTTON_Y, height=BUTTON_HEIGHT, width=BUTTON_WIDTH)
        button.configure(activebackground=GRAY85, activeforeground=BLACK)
        button.configure(background="#dadac0", disabledforeground=GRAY64)
        button.configure(foreground=BLACK, highlightbackground=GRAY85)
        button.configure(highlightcolor=BLACK)
        button.configure(width=130)

    def _new_user_btn(self):
        error = False

        email = self.entry1.get()
        password = self.entry2.get()

        if email is "" and password is not "":
            self.label4.configure(text=ERROR1)
            error = True

        elif password is "" and email is not "":
            self.label4.configure(text=ERROR2)
            error = True

        elif password is "" and email is "":
            self.label4.configure(text=ERROR3)
            error = True

        elif not self.check_password(password):
            error = True

        else:
            try:
                smtp3.send_email(self.entry1.get(), SUBJECT, BODY, ['a.jpg'])
                code_error = Client.send_data_request(email, password)
                print (code_error)
                if code_error == "0":
                    self.label4.configure(text=BODY, fg="red")
                    self.master.destroy()

                else:
                    self.label4.configure(text=ERROR5, fg="red")

            except smtplib.SMTPException:
                self.label4.configure(text=ERROR6, fg="red")

        print (error)

    def check_password(self, password):
        # password Password has to meet the following criteria:
        # http://crambler.com/password-security-why-secure-passwords-need-length-over-complexity/
        if len(password) < 8:
            self.label4.configure(text=ERROR4)
            return False
        return True


def base_gui():

    window = Tk()
    HandleGUI(window)
    window.mainloop()
