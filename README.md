# TCP Centralized Client-Server Network 

## Kevin Nunura
    
## General Description
This project creates a network communication between multiple Clients and a Server. Our comminication uses threads in order to allow
    multiple clients to connect to our main Server. We use a ClientHandler class to manage communication from each Client to our Server
    to make our Server reusable. In the same manner, we use a ClientHelper to manage communication from each Client to our Server to keep
    our Client reusable. We have a Server, ClientHandler, and a Menu for our program on the Server side. We have a ClientHelper and a Client
    class in our Client side. Our Handlers and Helpers manage menu logic between our CLients and our Server.
    
## External Python modules/libraries
Requirements files included in each client and server folder.

## Build Instructions
1) Clone repository
2) Open up terminal on Linux
3) cd into repository

## Running Instructions

This project consist in two main entities, the server and the client. Server and client must be run in different machines located in the same LAN. (Local Area Network). There are other additional classes that must be in the following machines. 

The files client_handler.py, and menu.py must be located in the same directory as the server.py file.  

Additionally, This program must be compatible with the following OS architectures: Linux, Windows and macOS


1) Open a terminal in machine X and navigate to the directory where server.py is located. Then execute the following commands:

``` 
python3 server.py 
```
Take note of the server ip address in the LAN, so you can connect your clients to the server. 

2) Open a terminal in machine Y and navigate to the directory where client.py is located. Then execute the following commands:

``` 
python3 client.py 
```
