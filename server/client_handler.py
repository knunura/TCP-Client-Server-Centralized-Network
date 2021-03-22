#######################################################################
# File:             client_handler.py
# Author:           Kevin Nunura and Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template ClientHandler class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client handler class, and use a version of yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################
import pickle
from menu import Menu
from datetime import datetime
import threading
import time


class ClientHandler(object):
    """
    The ClientHandler class provides methods to meet the functionality and services provided
    by a server. Examples of this are sending the menu options to the client when it connects,
    or processing the data sent by a specific client to the server.
    """

    def __init__(self, server_instance, clientsocket, addr):
        """
        Class constructor already implemented for you
        :param server_instance: normally passed as self from server object
        :param clientsocket: the socket representing the client accepted in server side
        :param addr: addr[0] = <server ip address> and addr[1] = <client id>
        """
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.client_name = None
        self.server = server_instance
        self.clientsocket = clientsocket
        self.print_lock = threading.Lock()  # creates the print lock
        self.server.send_client_id(self.clientsocket, self.client_id)
        self.unread_messages = [[None for col in range(3)] for row in range(5)]
        self.chatroom_id = None

    def get_client_name(self):
        return self.client_name

    def get_client_id(self):
        return self.client_id

    def get_chatroom_id(self):
        return self.chatroom_id

    def get_clientsocket(self):
        return self.clientsocket

    def run(self):
        self.process_client_data()

    def set_message(self, timestamp, sender, message):
        for i in range(len(self.unread_messages)):
            if not self.unread_messages[i][0]:
                self.unread_messages[i][0] = timestamp
                self.unread_messages[i][1] = sender
                self.unread_messages[i][2] = message
                break

    # This function processes all data being sent from client.
    def process_client_data(self):
        while True:
            #client_data is data being received from client.
            client_data = self.server.receive(self.clientsocket)
            if not client_data:
                print("No data received...")
                break
            # If Client sends an option, process it
            if 'option_selected' in client_data:
                self.process_options(client_data)
            # The first data being sent from client should be their personal details
            else:
                clientname = client_data['client_name']
                clientid = client_data['clientid']
                self.client_name = clientname
                self.client_id = clientid
                print("Client " + self.client_name + " with clientid: " + str(self.client_id) +
                      " has connected to this server.")
            self._sendMenu()

    # This function sends the Menu string
    def _sendMenu(self):
        time.sleep(1)   #Recommended by Professor
        menu = Menu(self.clientsocket)
        menuOptions = menu.show_menu()
        self.server.send(self.clientsocket, menuOptions)

    # This function runs other functions pertaining to the client's input.
    def process_options(self, data):
        if 'option_selected' in data.keys() and 1 <= data['option_selected'] <= 6:  # validates a valid option selected
            option = data['option_selected']
            self.server_log(option)
            if option == 1:
                self._send_user_list()
            elif option == 2:
                self._save_message()
            elif option == 3:
                self._send_messages()
            elif option == 4:
                self._create_chat()
            elif option == 5:
                self._join_chat()
            elif option == 6:
                self._disconnect_from_server()
        else:
            print("The option selected is invalid")

    # This function logs to the server depending on what option clients have selected.
    def server_log(self, option):
        id = self.client_name + ":" + str(self.client_id) + "..."
        self.print_lock.acquire()
        if option == 1:
            print("Sent user list to " + id)
        elif option == 2:
            print("Message sent by " + id)
        elif option == 3:
            print("Sent unread messages to " + id)
        elif option == 4:
            print("Chat room [" + str(self.chatroom_id) + "] created by " + id)
        elif option == 5:
            print("Chat room [" + str(self.chatroom_id) + "] joined by " + id)
        elif option == 6:
            print(self.client_name + " disconnected from the server...")
        self.print_lock.release()

    # This function sends a list of users in the server to the requester.
    def _send_user_list(self):
        data_fields = ""
        # Send empty field to client so client only waits to receive final response.
        self.server.send(self.clientsocket, data_fields)
        # Compute response for option 1 and send to Client
        response = "Users in the server: "
        clients = self.server.get_clients()
        for value in clients.values():
            name = value.get_client_name()
            id = value.get_client_id()
            response += name + ":" + str(id) + " "
        self.server.send(self.clientsocket, response)

    # This function saves a message in the unread_messages[] of the recipient's clinethandler.
    def _save_message(self):
        data_fields = {"message": None, "recipient_id": None}
        # Send dict data field to client so client knows how many times to listen for
        self.server.send(self.clientsocket, data_fields)
        self.server.send(self.clientsocket, "What is your message: ")
        data_fields["message"] = self.server.receive(self.clientsocket)
        self.server.send(self.clientsocket, "What is the recipient id: ")
        data_fields["recipient_id"] = int(self.server.receive(self.clientsocket))

        date = datetime.now()
        timestamp = str(date.year) + "-" + str(date.month) + "-" + str(date.day) + " " + str(date.hour) + ":" + str(
            date.minute)

        # Get client_handler dictionary from server
        clients = self.server.get_clients()
        try:
            # Get client_handler object specific to recipientid
            clienthandler_object = clients.get(data_fields["recipient_id"])
            clienthandler_object.set_message(timestamp, self.client_name, data_fields["message"])
            self.server.send(self.clientsocket, "Message was sent!")
        except:
            self.server.send(self.clientsocket, "Recipient not found!")

    # This function sends the unread inbox to the Client requesting it.
    def _send_messages(self):
        data_fields = ""
        self.server.send(self.clientsocket, data_fields)

        # Loop through own messages and compile a response with all messages. Rest inbox before sending response.
        try:
            my_messages = "My messages:\n"
            for i in range(len(self.unread_messages)):
                if self.unread_messages[i][0]:
                    my_messages += self.unread_messages[i][0] + ": " + self.unread_messages[i][2] + " (from: " + \
                                self.unread_messages[i][1] + ")\n"

            self.unread_messages = [[None] * 3] * 5
            self.server.send(self.clientsocket, my_messages)
        except:
            self.server.send(self.clientsocket, "No messages...")

    # This function creates a chatroom and allows creator to start the conversation. Typing bye quits chatroom.
    def _create_chat(self):
        data_fields = {"room_id": None}
        self.server.send(self.clientsocket, data_fields)

        self.server.send(self.clientsocket, "Enter the chat room id: ")
        room_id = self.server.receive(self.clientsocket)
        self.chatroom_id = room_id
        log = "\n---------------Chat Room " + room_id + "---------------\n" \
                                                        "Type bye to close the chat room.\n" \
                                                        "Waiting for users...\n"
        self.server.send(self.clientsocket, log)

        self.server.send(self.clientsocket, ">>")
        self.loop_in_chat()

    # This function allows clients to join a chatroom and speak after creator speaks. Typing bye quits chatroom.
    def _join_chat(self):
        data_fields = {"room_id": None}
        self.server.send(self.clientsocket, data_fields)

        self.server.send(self.clientsocket, "Enter the chat room id to join: ")
        room_id = self.server.receive(self.clientsocket)

        self.chatroom_id = room_id  # implement invalid chatroom validation
        log = "\n---------------Chat Room " + room_id + "---------------\n"
        self.server.send(self.clientsocket, log)

        self.loop_in_chat()

    # This function has anyone in the chatroom continuously loop in the chat until they type
    # "Bye" somewhere in their message.
    def loop_in_chat(self):
        while True:
            self.print_lock.acquire()
            message = self.client_name + ": " + self.server.receive(self.clientsocket) + "\n>> "

            # Get all clients from server's client handler dictionary and send a message to each clientsocket of each
            # client that is connected to sames chat room.
            clients = self.server.get_clients()
            for client in clients.values():
                client_chatroom_id = client.get_chatroom_id()
                client_id = client.get_client_id()
                if client_chatroom_id == self.chatroom_id and client_id != self.client_id:
                    self.server.send(client.get_clientsocket(), message)

            if "bye" in message:
                break
            self.print_lock.release()

    # This function deletes the clients data from the server
    def delete_client_data(self):  #
        clients = self.server.get_clients()
        for key in clients.keys():
            if key == self.client_id:
                del clients[key]
                break

    # This function deletes client's data, then disconnects client from server.
    def _disconnect_from_server(self):
        self.delete_client_data()
        data_fields = {"close_connection": None}
        self.server.send(self.clientsocket, data_fields)
        exit()
