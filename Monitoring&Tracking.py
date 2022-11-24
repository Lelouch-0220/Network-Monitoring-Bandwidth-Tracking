import os
import sys
import socket
import datetime
import time
import psutil


FILE = os.path.join(os.getcwd(), "networkinfo.log")
 
# creating log file in the currenty directory
# ??getcwd?? get current directory,
# os function, ??path?? to specify path

hostname = socket.gethostname() #Client Host Name
ip_address = socket.gethostbyname(hostname) #Client IP


def ping():
    # to ping a particular IP
    try:
        socket.setdefaulttimeout(3)
         
        # if data interruption occurs for 3
        # seconds, <except> part will be executed
 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # AF_INET: address family
        # SOCK_STREAM: type for TCP
 
        host = "8.8.8.8"
        port = 53
 
        server_address = (host, port)
        s.connect(server_address)
 
    except OSError as error:
        return False
        # function returns false value
        # after data interruption
 
    else:
        s.close()
        # closing the connection after the
        # communication with the server is completed
        return True
 
 
def calculate_time(start, stop):
   
    # Calculate time internet was unavailable for
    difference = stop - start
    seconds = float(str(difference.total_seconds()))
    return str(datetime.timedelta(seconds=seconds)).split(".")[0]
 
def first_check():
    # to check if the system was already
    # connected to an internet connection
 
    if ping():
        # if ping returns true
        live = "\nCONNECTION ACQUIRED\n"
        print(live)
        print(f"Hostname: {hostname}")
        print(f"Client IP: {ip_address}\n")
        connection_acquired_time = datetime.datetime.now()
        acquiring_message = "c=Connection acquired at: " + \
            str(connection_acquired_time).split(".")[0]
        print(acquiring_message)
 
        with open(FILE, "a") as file:
           
            # writes into the log file
            file.write(live)
            file.write(f"Hostname: {hostname}\n")
            file.write(f"Client IP: {ip_address}\n")
            file.write(acquiring_message)
 
        return True
 
    else:
        # if ping returns false
        not_live = "\nCONNECTION NOT ACQUIRED\n"
        print(not_live)
 
        with open(FILE, "a") as file:
           
            # writes into the log file
            file.write(not_live)
        return False

def convert_to_gbit(value): #Converting value to readable
    return value/1024./1024./1024.*8        

def main():
   
    # main function to call functions
    old_bytes = 0    #For Bandwidth Calculation
    monitor_start_time = datetime.datetime.now()
    monitoring_date_time = "Monitoring started at: " + \
        str(monitor_start_time).split(".")[0]
 
    if first_check():
        # if true
        print(monitoring_date_time)
        print("--------------------\n")
        # monitoring will only start when
        # the connection will be acquired
 
    else:
        # if false
        while True:
           
            # infinite loop to see if the connection is acquired
            if not ping():
                 
                # if connection not acquired
                time.sleep(1)
            else:
                 
                # if connection is acquired
                first_check()
                print(monitoring_date_time)
                break
 
    with open(FILE, "a") as file:
       
        # write into the file as a into networkinfo.log,
        # "a" - append: opens file for appending,
        # creates the file if it does not exist
        file.write("\n")
        file.write(monitoring_date_time + "\n")
        file.write("--------------------\n")
 
    while True:

        # infinite loop, as we are monitoring
        # the network connection till the machine runs
        z = psutil.net_io_counters() #psutil library = tuple of bytes sent/recieved and packets s/r
        print(z)
        if ping():
             
            # if true: the loop will execute after every 5 seconds
            z = psutil.net_io_counters()
            print(z[2])
            time.sleep(3)
 
        else:
            # if false: fail message will be displayed
            
            down_time = datetime.datetime.now()
            x = down_time - monitor_start_time 
            
            
            time.sleep(1)
            new_bytes = z[0]+z[1]
            value = new_bytes-old_bytes

            fail_msg = "Disconnected at: " + str(down_time).split(".")[0]
            used_msg = "Internet was used for: " + str(x).split(".")[0]

            print(fail_msg)
            print(used_msg)
 
            with open(FILE, "a") as file:
                # writes into the log file
                file.write(fail_msg + "\n")
                file.write(used_msg + "\n")
                file.write("\nBandwidth used: %0.3f" % convert_to_gbit(value) + "\n")
                file.write("--------------------\n")
 
            while not ping():
               
                # infinite loop, will run till ping() return true
                time.sleep(1) 
 
            up_time = datetime.datetime.now()

            # after loop breaks, connection restored
            uptime_message = "Connected Again at: " + str(up_time).split(".")[0]
 
            down_time = calculate_time(down_time, up_time)
            unavailablity_time = "Client was disconnected for: " + down_time
            
            print(uptime_message)
            print(unavailablity_time)
            
 
            with open(FILE, "a") as file:
                 
                # log entry for connection restoration time,
                # and unavailability time
                file.write(uptime_message + "\n")
                file.write(unavailablity_time + "\n")           
                file.write("--------------------\n")


main()

#Change .log file to excel
#Include a function which disconnects the internet if Bandwidth usage crosses a limit

