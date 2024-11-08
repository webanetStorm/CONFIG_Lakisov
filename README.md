# VirtualShell

VirtualShell — это командная оболочка, работающая с архивом `tar`. Эмулятор поддерживает команды для навигации, просмотра содержимого и работы с архивом.

## Постановка задачи
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата
tar. Эмулятор должен работать в режиме CLI.
Ключами командной строки задаются:
- Путь к архиву виртуальной файловой системы.
- Путь к лог-файлу.
Лог-файл имеет формат xml и содержит все действия во время последнего
сеанса работы с эмулятором.
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также
следующие команды:
1. du.
2. tree.
3. find.
Все функции эмулятора должны быть покрыты тестами, а для каждой из
поддерживаемых команд необходимо написать 3 теста.

## Установка и запуск

### Требования:
- Python 3.x
- Библиотеки: `tarfile`, `os`, `datetime`, `xml.etree.ElementTree`

### Запуск:
1. Убедитесь, что у вас есть tar-архив с именем `webanet.tar` в текущей директории или измените путь к файлу в коде.
2. Запустите скрипт через командную строку:
```bash
python main.py --hostname test_machine --tar_path system.tar --log_path log.xml
```

### Описание команд
-  Команда ls выводит список файлов и директорий в текущей директории внутри архива.

Пример: 
```bash
> ls
file1.txt
file2.txt
folder
```

- Команда cd изменяет текущую директорию.
   - cd <путь> - Переходил по указанному пути
   - cd / - Переходит в корневую директорию.
   - cd .. - Переходит на уровень выше.

Пример:
```bash
> cd folder
> ls
subfile1.txt
subfile2.txt
```

- Команда du выводит общий размер файлов в текущей директории или указанной. Если не указан путь, выводится размер текущей директории.
Выводится размер в байтах.

- Пример:

```bash
> du
500 байт
```

- Команда tree выводит древовидную структуру файлов и папок.

Пример:

```bash
> tree
folder/
    subfolder/
        file1.txt
        file2.txt
```

- Команда find ищет файл или папку по имени.

Пример:
```bash
> find file1.txt
folder/subfolder/file1.txt
```

- Команда exit завершает работу оболочки. Каждая выполненная команда записывается в файл log.xml. Формат лога:

```xml
<session>
    <command>[дата и время]: команда</command>
</session>
```

## Пример использования
```bash
> ls
folder
> cd folder
> ls
file1.txt
file2.txt
> du
250 байт
> tree
folder/
    file1.txt
    file2.txt
> exit
```

## Скриншот работы
![Пример работы](https://i.imgur.com/Fu1OFPZ.png)