#!/usr/bin/env python3

import libtmux
import os
from tqdm import trange
import argparse
import uuid



def get_env_name_by_num(num):
    return 'user-{}'.format(num)

def start(num_users, base_dir='./'):
    """
    Запустить $num_users ноутбуков. У каждого рабочая директория $base_dir+$folder_num
    """
    tmux_server = libtmux.Server()
    session_name = str(uuid.uuid4())
    session = tmux_server.new_session()

    for user_num in trange(num_users):
        # create tmux-window for each user
        window = session.new_window(window_name=f"window{num_users}")

        folder = f"folder_{num_users}"

        window.attached_pane.send_keys(f'cd {base_dir}')
        window.attached_pane.send_keys(f'mkdir folder_{user_num}')
        window.attached_pane.send_keys(f'cd folder_{user_num}')

        # start jupyter notebook
        cmd = 'jupyter notebook --ip {ip} --port {port} --no-browser --NotebookApp.token=\'{token}\' --NotebookApp.notebook_dir=\'{dir}\''.format(
            ip='0.0.0.0',
            port=10076 + user_num,
            token=str(uuid.uuid4()),
            dir=folder,
        )
        window.attached_pane.send_keys(cmd)



def stop(session_name, num):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    @:param num: номер окружения, кот. можно убить
    """
    tmux_server = libtmux.Server()
    session = tmux_server.get_by_id(f'${session_name}')
    session.kill_window(f'win{num}')


def stop_all(session_name):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    """
    tmux_server = libtmux.Server()
    session = tmux_server.get_by_id(f'${session_name}')
    session.kill_session()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd')
    parser.add_argument('argument_1')
    parser.add_argument('argument_2', nargs='?')
    args = parser.parse_args()

    if args.cmd == 'start':
        num_users = int(args.argument_1)
        if args.argument_2:
            base_dir = args.argument_2
            start(num_users, base_dir)
        else:
            start(num_users)
    elif args.cmd == 'stop':
        session_name = args.argument_1
        if args.argument_2:
            num = args.argument_2
            stop(session_name, num)
        else:
            raise ValueError()
    elif args.cmd == 'stop_all':
        session_name = args.argument_1
        stop_all(session_name)
    else:
        raise NameError()

if __name__ == "__main__":
    main()