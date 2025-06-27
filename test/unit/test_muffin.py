import builtins
import io
import sys
from unittest import mock

import pytest

from muffinscript.errors import MuffinScriptSyntaxError
from muffinscript.muffin import main


def test_main_print(monkeypatch, capsys):
    """Test happy path printing."""
    monkeypatch.setattr(sys, "argv", ["muffin", "test.ms"])
    mock_file = io.StringIO('foo = "hello world"\np(foo)\n')
    monkeypatch.setattr(builtins, "open", lambda *a, **kw: mock_file)

    main()

    captured = capsys.readouterr()
    assert "hello world" in captured.out


def test_main_print_empty_file(monkeypatch, capsys):
    """Test we print nothing if the file is empty."""
    monkeypatch.setattr(sys, "argv", ["muffin", "test.ms"])
    mock_file = io.StringIO("\n")
    monkeypatch.setattr(builtins, "open", lambda *a, **kw: mock_file)

    main()

    captured = capsys.readouterr()
    assert "" in captured.out


def test_main_print_only_variable(monkeypatch, capsys):
    """Test we print nothing if the file only has a variable in it."""
    monkeypatch.setattr(sys, "argv", ["muffin", "test.ms"])
    mock_file = io.StringIO('foo = "hello world"\n')
    monkeypatch.setattr(builtins, "open", lambda *a, **kw: mock_file)

    main()

    captured = capsys.readouterr()
    assert "" in captured.out


def test_main_tokenizer_error(monkeypatch, capsys):
    """Test we throw a tokenizer error."""
    monkeypatch.setattr(sys, "argv", ["muffin", "test.ms"])
    mock_file = io.StringIO("!!!\n")
    monkeypatch.setattr(builtins, "open", lambda *a, **kw: mock_file)

    with mock.patch("muffinscript.lexer.tokenize", side_effect=MuffinScriptSyntaxError("", 1)):
        with pytest.raises(SystemExit):
            main()
        captured = capsys.readouterr()
        assert "\x1b[31mSYNTAX ERROR\x1b[0m - Unsupported statement | line: 1\n" in captured.out


def test_main_parser_error(monkeypatch, capsys):
    """Test we throw a parser error."""
    monkeypatch.setattr(sys, "argv", ["muffin", "test.ms"])
    mock_file = io.StringIO("p(foo\n")
    monkeypatch.setattr(builtins, "open", lambda *a, **kw: mock_file)

    with mock.patch("muffinscript.parser.parse_tokens", side_effect=MuffinScriptSyntaxError("", 1)):
        with pytest.raises(SystemExit):
            main()
        captured = capsys.readouterr()
        assert "\x1b[31mSYNTAX ERROR\x1b[0m - Unsupported statement | line: 1\n" in captured.out
