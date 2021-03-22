#######################################################################################
# File:             menu.py
# Author:           Kevin Nunura and Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template Menu class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this Menu class, and use a version of yours instead.
# Important:        The server sends a object of this class to the client, so the client is
#                   in charge of handling the menu. This behaivor is strictly necesary since
#                   the client does not know which services the server provides until the
#                   clients creates a connection.
# Running:          This class is dependent of other classes.
# Usage :           menu = Menu() # creates object
#
########################################################################################

class Menu(object):
    def __init__(self, client):
        self.client = client

    def set_client(self, client):
        self.client = client

    def show_menu(self):
        menu = self.get_menu()
        return menu

    def get_menu(self):
        menu = "\n****** TCP CHAT ******\n" \
               "-----------------------\n" \
               "Options Available:\n" \
               "1. Get user list\n" \
               "2. Send a message\n" \
               "3. Get my messages\n" \
               "4. Create a new channel\n" \
               "5. Join an existing chat room\n" \
               "6. Disconnect from server\n\n" \
               "Your option here <number>: "

        return menu
