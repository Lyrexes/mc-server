#!/usr/bin/python3
import libtmux
import time
import argparse

SERVER  = libtmux.Server()
SESSION_NAME = "minecraft"
SERVER_JAR = "paper.jar"
RAM_IN_GB = 14

def get_window():
    return get_session().windows[0]

def get_session():
    return SERVER.find_where({ "session_name" : SESSION_NAME})

def get_pane():
    return get_window().panes[0]

def attach_session():
    get_session().attach_session()

def send_input(cmd: str):
    get_pane().send_keys(cmd)

def start_server():
    try:
        SERVER.new_session(SESSION_NAME, attach=False, 
            window_command=f"java -Xms{RAM_IN_GB}G -Xmx{RAM_IN_GB}G -jar {SERVER_JAR} --nogui")
    except:
        print("could not start server")

def stop_server():
    try:
        send_input("stop")
    except:
        print("could not stop server")

def restart_server():
    for i in range(10,0,-1):
        send_input(f"say Server restarts in {i}s")
        time.sleep(1)
    stop_server()
    time_sleep(10)
    start_server()

def open_console():
    try:
        attach_session()
    except:
        print(f"could not attach to session: {SESSION_NAME}")

def deamon_keep_server_up():
    if not SERVER.has_session(SESSION_NAME):
        start_server()

def parse_arguments():
    parser = argparse.ArgumentParser(
                    prog = 'mc-server',
                    description = '',
                    epilog = '--help to see all commands'
                )
    parser.add_argument('-r', '--restart', action='store_true',
     help="restarts server")
    parser.add_argument('-q', '--quit', action='store_true', 
     help="quits server")
    parser.add_argument('-s', '--start', action='store_true',
     help="starts server")
    parser.add_argument('v', '--view', action='store_true',
     help="view console")
    parser.add_argument('-d', '--deamon', action='store_true',
     help="deamon to keep server up if it crashes")
    return parser.parse_args()

def main():
    args = parse_arguments()
    if args.start:
        start_server()
    elif args.quit:
        stop_server()
    elif args.restart:
        restart_server()
    elif args.view:
        open_console()
    elif args.deamon:
        deamon_keep_server_up()

if __name__ == "__main__":
    main()
