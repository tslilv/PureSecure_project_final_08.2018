# -*- coding: utf-8 -*-
import socket
import time
import os


IP = '127.0.0.1'
PORT = 80

MSG = "SAVE /DB/{0}/{1}/{2} PURE_SECURE0.1\\r\\n" \
      "content-type: {3}\\r\\n" \
      "content-len: {4}\\r\\n"

DATA_REQUEST = "DATA {0}/{1}"


class Client():

    def __init__(self, user, data):
        self.user = user
        self.data = data
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((IP, PORT))

    def send_save_message(self):


        msg = MSG.format(self.user, time.strftime("%d-%m-%Y"),
                         time.strftime("%H-%M-%S")+'.jpg', "img", len(self.data))
        self.client.send(msg)

        response = self.client.recv(1024)
        # print "ww"
        # if response == len(self.data):
        #     print "send"
        if response:
            self.client.send(self.data)
        self.client.close()

    def send_data_message(self, username, password):
        """"
        send data request to server
        return bool TRUE if saved in database successfully
        otherwise, return FALSE
        """

        msg = DATA_REQUEST.format(username, password)
        self.client.send(msg)

        response = self.client.recv(1024)
        self.client.close()
        return response


def get_content(filename):
        """
        get name of a file
        open, read and copy the file content
        return the content of the file if exists
        otherwise, return an empty string
        """

        if os.path.exists(filename):
            file1 = open(filename, 'rb')
            content = file1.read()
            file1.close()
        else:
            return ""
        return content


def send_save_request(user, img):
    """
    Add Documentation here
    """
    data = get_content(img)
    client = Client(user, data)
    client.send_save_message()


def send_data_request(user, password):

    client = Client(user, "")
    return client.send_data_message(user, password)


if __name__ == '__main__':
    main("user", "a.jpg")