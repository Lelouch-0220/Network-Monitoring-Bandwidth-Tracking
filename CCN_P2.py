import time
import psutil

def main():
    old_value = 0    

    while True:
        x = psutil.net_io_counters()
        print(x)
        time.sleep(1)
        new_value = x[0]+x[1]

        if old_value:
            send_stat(new_value - old_value)

        old_value = new_value

        time.sleep(1)

def convert_to_gbit(value):
    return value/1024./1024./1024.*8

def send_stat(value):
    print ("Bandwidth used: %0.3f" % convert_to_gbit(value))

main()