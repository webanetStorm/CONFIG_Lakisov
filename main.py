import xml.etree.ElementTree as ET
from datetime import datetime
import argparse
import tarfile
import os


class ShellEmulator:

    def __init__(self, tar_path, log_path, hostname, script_path=None):
        self.current_path = ''
        self.tar_path = tar_path
        self.log_path = log_path
        self.hostname = hostname
        self.script_path = script_path
        self.history_log = []
        self.log_element = ET.Element('session')

    def log(self, command):
        cmd = ET.SubElement(self.log_element, 'command')
        cmd.text = command
        ET.ElementTree(self.log_element).write(self.log_path)
        self.history_log.append(command)

    def ls(self, dir, path):
        current_dir = f'{path}/' if path else (f'{self.current_path}/' if self.current_path else '')
        for item in dir:
            if item.startswith(current_dir) and item != current_dir:
                relative_item = item[len(current_dir):]
                if '/' not in relative_item:
                    print(relative_item)
        self.log(f'[{datetime.now()}]: ls в ' + (self.current_path if self.current_path else 'корневой директории'))

    def cd(self, path, dir):
        if path == '/':
            self.current_path = ''
        elif path == '..':
            self.current_path = os.path.dirname(self.current_path)
        else:
            new_path = os.path.join(self.current_path, path)
            if any(item == new_path for item in dir):
                self.current_path = new_path
            else:
                self.throw(f'cd : Не удается найти путь "{self.current_path}/{new_path}", так как он не существует')
        self.log(f'[{datetime.now()}]: cd в {self.current_path}')

    def rmdir(self, dir, path):
        full_path = os.path.join(self.current_path, path).strip('/')

        if f"{full_path}/" in dir:
            if not any(item.startswith(f"{full_path}/") and item != f"{full_path}/" for item in dir):
                print(f'Директория {full_path} удалена')
            else:
                print(f'Ошибка: директория {full_path} не пуста')
        else:
            print(f'Ошибка: директория {full_path} не найдена')

        self.log(f'[{datetime.now()}]: rmdir для {full_path}')

    def who(self):
        print(f'Пользователь на компьютере: {self.hostname}')
        self.log(f'[{datetime.now()}]: who')

    def history(self):
        print('История команд:')
        for command in self.history_log:
            print(command)
        self.log(f'[{datetime.now()}]: history')

    def throw(self, message):
        message = f'\033[31m{message}\033[0m'
        print(message)

    def execute_script(self):
        if self.script_path:
            with open(self.script_path, 'r') as script_file:
                for line in script_file:
                    command = line.strip().split()
                    self.process_command(command)

    def process_command(self, command):
        with tarfile.open(self.tar_path, 'r') as tar:
            if command[0] == 'exit':
                return False
            elif command[0] == 'ls':
                self.ls(tar.getnames(), command[1] if len(command) > 1 else None)
            elif command[0] == 'cd' and len(command) >= 2:
                self.cd(command[1], tar.getnames())
            elif command[0] == 'rmdir' and len(command) >= 2:
                self.rmdir(tar.getnames(), command[1])
            elif command[0] == 'who':
                self.who()
            elif command[0] == 'history':
                self.history()
            else:
                self.throw(f'"{command[0]}" не является внутренней или внешней командой, исполняемой программой или пакетным файлом')
        return True


def main():
    parser = argparse.ArgumentParser(description='ShellEmulator CLI')
    parser.add_argument('--hostname', type=str, required=True, help='Имя компьютера для показа в приглашении к вводу')
    parser.add_argument('--tar_path', type=str, required=True, help='Путь к tar архиву виртуальной файловой системы')
    parser.add_argument('--log_path', type=str, required=True, help='Путь к лог-файлу')
    parser.add_argument('--script_path', type=str, help='Путь к стартовому скрипту')
    args = parser.parse_args()

    shell = ShellEmulator(args.tar_path, args.log_path, args.hostname, args.script_path)

    if args.script_path:
        shell.execute_script()

    while True:
        if not shell.process_command(input(f'\033[36m{shell.hostname}:{shell.current_path}> \033[0m').strip().split()):
            break


if __name__ == '__main__':
    main()
