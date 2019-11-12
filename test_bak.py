import importlib.util
from importlib.machinery import SourceFileLoader
from unittest import mock


def load_module_from_file(name, path):
    """All this to replace the deprecated imp.load_source"""
    loader = SourceFileLoader(name, path)
    spec = importlib.util.spec_from_file_location(name, path, loader=loader)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


backup = load_module_from_file('bak', './bak')


def test_original_file_path_full():
    backup_path = '/path/to/file/foobar.baz.bak.20200314T151234'
    expected = '/path/to/file/foobar.baz'
    actual = backup.original_file_path(backup_path)
    assert expected == actual


def test_original_file_path_filename():
    backup_path = 'foobar.baz.bak.20200314T151234'
    expected = 'foobar.baz'
    actual = backup.original_file_path(backup_path)
    assert expected == actual


def test_original_file_path_multiple_baks():
    backup_path = 'foobar.baz.bak.20200314T151234.bak.20200314T151234'
    expected = 'foobar.baz'
    actual = backup.original_file_path(backup_path)
    assert expected == actual


def test_most_recent_backup_file():
    original_path = 'foobar.baz'
    files = [
        'foobar.baz',
        'foobar.baz.bak.20200314T151234',
        'foobar.baz.bak.20200314T151234.bak.20200314T151234',
        'foobar.baz.bak.20200314T151235',
        'foobar.baz.bak.20200314T151235.bak.20200314T151235',
    ]
    expected = 'foobar.baz.bak.20200314T151235.bak.20200314T151235'
    with mock.patch('os.listdir', return_value=files):
        actual = backup.most_recent_backup_file(original_path)
    assert expected == actual


def test_most_recent_backup_file_not_found():
    original_path = 'foobar.baz'
    files = [
        'foobar.baz',
        'foobar.baz.bak.200200314T151234',
        'foobar.baz.20200314T151234.bak.20200314T151234',
        'fooobar.baz.bak.20200314T151235',
        'foobar.baz.bak.20200314T151235.bak.20200314T1512356',
    ]
    expected = None
    with mock.patch('os.listdir', return_value=files):
        actual = backup.most_recent_backup_file(original_path)
    assert expected == actual
