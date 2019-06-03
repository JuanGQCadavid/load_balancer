import json
import sys

def main():
    pass


def menu_dialog():
    print('*'*50)
    print('Welcome to load Balancer')
    print("* press (1) for server's farm")
    print("* press (2) for start the service")
    print("* press (3) for exit")

    key_press = int(input('\t\t:'))

    if (key_press == '1'):
        server_farm()
    elif(key_press == '2'):
        start_load_balancer()
    elif(key_press == '3'):
        print("See ya later")
        sys.exit(0)
    else:
        print(key_press,' is not a valid input')
        return menu_dialog

def server_farm_dialog():
    print('-'*25,'SERVER FARM','-'*25)
    print('Commands: status | config | help | exit')

    command_line = input('$: ')
    command_line_splited = command_line.split(' ')

    if len(command_line_splited) == 1:
        if command_line_splited[0] == 'status':
            pass
        elif command_line_splited[0] == 'help':
            pass
        elif command_line_splited[0] == 'exit':
            return menu_dialog;
        else:
            print(command_line, ' [ERR] Command not found')
            return server_farm_dialog()
    else:
        if command_line_splited[0] == 'status':
            pass
        elif command_line_splited[0] == 'config':
            if command_line_splited[1] == 'add':
                pass
            elif command_line_splited[1] == 'edit':
                pass
            elif command_line_splited[1] == 'remove':
                pass
            else:
                print(command_line_splited[1], ' [ERR] Command not found')
                return server_farm_dialog()
        else:
            print(command_line, ' [ERR] Command not found')
            return server_farm_dialog()

        
    

def server_farm():
    print()
    pass

def start_load_balancer():
    pass

if __name__ == '__main__':
    main