#######################################################################
# File:             client.py
# Author:           Kevin Nunura
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Class to handle communication from ClientHandler
#                   With respects to menu selection. This class is to
#                   the client.py what ClientHelper is to server.py.
# Running:          Python 2: python client.py
#                   Python 3: python3 client.py
#
########################################################################
class ClientHelper(object):

    def __init__(self, client_instance):
        self.client = client_instance

    def run(self):
        self.process_server_data()

    def process_server_data(self):
        while True:
            server_data_request = self.process_menu()
            if "close_connection" in server_data_request:
                self.client.close()
                break
            elif server_data_request:
                for key in server_data_request.keys():
                    # listen and respond for the number of fields requested
                    self.listen_and_respond()
            self.process_server_response(server_data_request)

    # Prints out menu and asks for option input.
    # Sends option selected to server/ClientHandler
    # Receives data fields sent by server and returns it
    def process_menu(self):
        menu = self.client.receive()
        option_selected = int(input(menu))
        self.client.send({'option_selected': option_selected})

        data_field = self.client.receive()
        return data_field

    # Prints all responses from ClientHandler after ClientHandler
    # is done processing the selected option
    def process_server_response(self, server_request):
        server_response = self.client.receive()
        print(server_response)
        # If option selected deals with chatrooms, then
        # continuously loop response until "bye is typed.
        if "room_id" in server_request:


            while True:
                answer = self.listen_and_respond()
                if "bye" in answer:
                    break
        else:
            return

    # Receive question, answer, and send answer to server
    def listen_and_respond(self):
        request_question = self.client.receive()
        answer = input(request_question)
        self.client.send(answer)
        return answer
