import unittest
from unittest.mock import patch, MagicMock
from main import ShellEmulator


class TestVirtualShell(unittest.TestCase):

    def setUp(self):
        self.shell = ShellEmulator('../system.tar', '../log.xml', 'test_machine')

    @patch('xml.etree.ElementTree.ElementTree.write')
    def test_log(self, mock_write):
        self.shell.log('test command')
        self.assertEqual(self.shell.log_element[0].text, 'test command')
        mock_write.assert_called_once_with(self.shell.log_path)

    @patch('main.print')
    def test_ls_root(self, mock_print):
        self.shell.ls(['dir1', 'dir2', 'file1', 'file2'], None)
        mock_print.assert_any_call('dir1')
        mock_print.assert_any_call('dir2')
        mock_print.assert_any_call('file1')
        mock_print.assert_any_call('file2')

    @patch('main.print')
    def test_ls_in_directory(self, mock_print):
        self.shell.ls(['dir1/file1', 'dir1/file2'], 'dir1')
        mock_print.assert_any_call('file1')
        mock_print.assert_any_call('file2')

    @patch('main.print')
    def test_ls_no_files(self, mock_print):
        self.shell.ls([], 'dir1')
        mock_print.assert_not_called()

    @patch('xml.etree.ElementTree.ElementTree.write')
    def test_cd_root(self, mock_write):
        self.shell.cd('/', ['dir1', 'dir2'])
        self.assertEqual(self.shell.current_path, '')

    @patch('xml.etree.ElementTree.ElementTree.write')
    def test_cd_parent_directory(self, mock_write):
        self.shell.current_path = 'dir1/dir2'
        self.shell.cd('..', ['dir1', 'dir2'])
        self.assertEqual(self.shell.current_path, 'dir1')

    @patch('main.print')
    def test_cd_nonexistent_directory(self, mock_print):
        self.shell.cd('dir3', ['dir1', 'dir2'])
        mock_print.assert_any_call('\033[31mcd : Не удается найти путь "/dir3", так как он не существует\033[0m')

    @patch('main.print')
    def test_rmdir_empty_directory(self, mock_print):
        self.shell.rmdir(['var/', 'var/log/'], 'var/log')
        mock_print.assert_any_call('Директория var/log удалена')

    @patch('main.print')
    def test_rmdir_non_empty_directory(self, mock_print):
        self.shell.rmdir(['var/', 'var/log/', 'var/log/file.log'], 'var/log')
        mock_print.assert_any_call('Ошибка: директория var/log не пуста')

    @patch('main.print')
    def test_rmdir_nonexistent_directory(self, mock_print):
        self.shell.rmdir(['var/'], 'var/log')
        mock_print.assert_any_call('Ошибка: директория var/log не найдена')

    @patch('main.print')
    def test_who_command(self, mock_print):
        self.shell.who()
        mock_print.assert_any_call('Пользователь на компьютере: test_machine')

    @patch('main.print')
    def test_who_command_different_hostname(self, mock_print):
        self.shell.hostname = 'new_host'
        self.shell.who()
        mock_print.assert_any_call('Пользователь на компьютере: new_host')

    @patch('main.print')
    def test_who_command_empty_hostname(self, mock_print):
        self.shell.hostname = ''
        self.shell.who()
        mock_print.assert_any_call('Пользователь на компьютере: ')

    @patch('main.print')
    def test_history_with_multiple_commands(self, mock_print):
        self.shell.log('ls')
        self.shell.log('cd var')
        self.shell.log('rmdir log')
        self.shell.history()
        mock_print.assert_any_call("История команд:")
        mock_print.assert_any_call("ls")
        mock_print.assert_any_call("cd var")
        mock_print.assert_any_call("rmdir log")

    @patch('main.print')
    def test_history_with_no_commands(self, mock_print):
        self.shell.history()
        mock_print.assert_any_call("История команд:")

    @patch('main.print')
    def test_history_with_single_command(self, mock_print):
        self.shell.log('who')
        self.shell.history()
        mock_print.assert_any_call("История команд:")
        mock_print.assert_any_call("who")


if __name__ == '__main__':
    unittest.main()
