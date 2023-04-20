

import netifaces
import subprocess
import string
import random



def get_int():
    interface = netifaces.interfaces()
    for intf in interface:
        if intf != 'lo':
            return intf
            

def get_mac():
    mac = netifaces.ifaddresses('eth0')[17][[0][0]]['addr']
    return mac 

def random_addr():
    
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
    
    mac = ""
    for i in range(6):
        for j in range(2):
            if i == 0:
                mac += random.choice("02468ACE")
            else:
                mac += random.choice(uppercased_hexdigits)
        mac += ":"
    return mac.strip(":")

def change_mac(interface, new_mac_address):
   
    subprocess.call(["sudo", "ifconfig", interface,"down"])
    subprocess.call(["sudo", "ifconfig", interface,"hw", "ether", new_mac_address])           
    subprocess.call(["sudo", "ifconfig", interface,"up"])
                     
def double_check(old_conf,new_conf):
    user_ans = input('\nDo you belive me or you need to check? y/n ')
    while True: 
        if user_ans == 'n':
            print(f"\nOLD:\n'{old_conf.stdout}\n\nNEW:\n{new_conf.stdout}\n")
            break
        elif user_ans == 'y':
            print('Thank you for trusting me\nhave a great day')
            break
        else:
            user_ans = input('\nReally? y/n ')  
            continue


def main():
    check = subprocess.run('ifconfig',stdout=subprocess.PIPE, text=True)
    intf = get_int()
    mac_addr = get_mac()
    random_mac_addr = random_addr()
    change_mac(intf, random_mac_addr)
    print(f'\nYour old mac address: {mac_addr}\nYour new mac address: {random_mac_addr}\n')
    after_check = subprocess.run('ifconfig',stdout=subprocess.PIPE, text=True)
    double_check(check,after_check)
    
   
    
main()