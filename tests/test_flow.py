"""Tests for easy_flow module."""

import time

import pytest

from py_simple_package.src.py_simple.easy_flow import (
    EasyFlowError,
    retry,
    run_py_file,
    run_py_file_safe,
    run_py_string,
    run_with_fallback,
    time_function_call,
    time_it,
)


class TestRunPyString:
    @pytest.mark.parametrize(
        "code_string,expected_output",
        [
            ("print('hello world')", "hello world\n"),
            ("a = 1 + 1\nprint(a)", "2\n"),
        ],
    )
    def test_runs_successfully(self, capsys, code_string, expected_output):
        run_py_string(code_string)
        captured = capsys.readouterr()
        assert captured.out == expected_output

    def test_script_error_raises(self):
        with pytest.raises(EasyFlowError) as exc_info:
            run_py_string("raise ValueError('boom')")
        assert "boom" in str(exc_info.value)


class TestEasyFlowError:
    def test_is_exception(self):
        """Tests if it is an exception."""
        assert issubclass(EasyFlowError, Exception)

    def test_stores_message(self):
        """Checks if the string provided is the same string outputted."""
        err = EasyFlowError("something is broken")
        assert err.message == "something is broken"
        assert str(err) == "something is broken"


class TestRunPyFile:
    def test_runs_successfully(self, tmp_path, capsys):
        """Checks if a file can run and let its output through."""
        script = tmp_path / "script.py"
        script.write_text("print('hello world')\n")

        run_py_file(str(script))

        captured = capsys.readouterr()
        assert "RUNNING:" in captured.out
        assert "hello world" in captured.out

    def test_missing_file_raises(self):
        """Should raise EasyFlowError for a file that doesn't exist."""
        with pytest.raises(EasyFlowError) as exc_info:
            run_py_file("does_not_exist.py")
        assert "does_not_exist.py" in str(exc_info.value)

    def test_script_error_raises(self, tmp_path):
        """Checks to see if an error within a script is correctly wrapped."""
        script = tmp_path / "broken.py"
        script.write_text("raise ValueError('boom')\n")

        with pytest.raises(EasyFlowError) as exc_info:
            run_py_file(str(script))
        assert "boom" in str(exc_info.value)


class TestRunPyFileSafe:
    def test_runs_successfully(self, tmp_path, capsys):
        """Checks if return is True, None and print progress on success."""
        script = tmp_path / "script.py"
        script.write_text("print('all good')\n")

        success, error = run_py_file_safe(str(script))

        assert success is True
        assert error is None
        captured = capsys.readouterr()
        assert "RUNNING:" in captured.out

    def test_missing_file_returns_error(self):
        """Checks if return is False, message if it failed."""
        success, error = run_py_file_safe("does_not_exist.py")
        assert success is False
        assert "does_not_exist.py" in error

    def test_script_error_returns_error(self, tmp_path):
        """Checks for something breaking within the file."""
        script = tmp_path / "broken.py"
        script.write_text("raise ValueError('boom')\n")

        success, error = run_py_file_safe(str(script))

        assert success is False
        assert "boom" in error


class TestTimeFunctionCall:
    def test_returns_a_float(self):
        """Checks if the output is a non-negative float."""
        duration = time_function_call(lambda: "done")
        assert isinstance(duration, float)
        assert duration >= 0

    def test_calls_function_with_args(self):
        """Ensures that functions with arguments work."""
        calls = []

        def add(a, b):
            calls.append((a, b))
            return a + b

        time_function_call(add, [2, 3])
        assert calls == [(2, 3)]

    def test_calls_function_with_no_args(self):
        """Checks that functions without arguments work."""
        calls = []

        def no_args():
            calls.append(True)

        time_function_call(no_args)
        assert calls == [True]

    def test_measures_elapsed_time(self, monkeypatch):
        """Checks to see if time difference is calculated correctly."""
        times = iter([100.0, 100.5])
        monkeypatch.setattr(time, "time", lambda: next(times))

        duration = time_function_call(lambda: None)
        assert duration == pytest.approx(0.5)

    def test_function_error_raises_easyflowerror(self):
        """Checks if exception are wrapped correctly."""

        def boom():
            raise ValueError("bad function")

        with pytest.raises(EasyFlowError) as exc_info:
            time_function_call(boom)
        assert "bad function" in str(exc_info.value)


class TestTimeIt:
    def test_returns_original_result(self):
        """Should return whatever the wrapped function returns."""

        @time_it
        def add(a, b):
            return a + b

        assert add(2, 3) == 5

    def test_prints_timing(self, capsys):
        """Should print the function's name and elapsed time."""

        @time_it
        def add(a, b):
            return a + b

        add(2, 3)

        captured = capsys.readouterr()
        assert "add took" in captured.out

    def test_supports_args_and_kwargs(self):
        """Should forward both positional and keyword arguments."""

        @time_it
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"

        assert greet("World", greeting="Hi") == "Hi, World!"


class TestRetry:
    def test_succeeds_on_first_try(self, monkeypatch):
        """Checks what happens if things runs smoothly."""
        monkeypatch.setattr(time, "sleep", lambda s: None)
        calls = []

        def always_works():
            calls.append(1)
            return "success"

        result = retry(always_works)
        assert result == "success"
        assert len(calls) == 1

    def test_succeeds_after_some_failures(self, monkeypatch):
        """Checks if it retries, failure then success."""
        monkeypatch.setattr(time, "sleep", lambda s: None)
        calls = []

        def fails_twice_then_works():
            calls.append(1)
            if len(calls) < 3:
                raise ValueError("not yet")
            return "success"

        result = retry(fails_twice_then_works, attempts=5)
        assert result == "success"
        assert len(calls) == 3

    def test_raises_after_all_attempts_fail(self, monkeypatch):
        """Tests if max failure limit is reach."""
        monkeypatch.setattr(time, "sleep", lambda s: None)
        calls = []

        def always_fails():
            calls.append(1)
            raise ValueError("nope")

        with pytest.raises(ValueError, match="nope"):
            retry(always_fails, attempts=3)
        assert len(calls) == 3

    def test_waits_between_attempts(self, monkeypatch):
        """Ensure delays are taken between attempts."""
        sleep_calls = []
        monkeypatch.setattr(time, "sleep", lambda s: sleep_calls.append(s))

        def always_fails():
            raise ValueError("nope")

        with pytest.raises(ValueError):
            retry(always_fails, attempts=3, delay=2)

        assert sleep_calls == [2, 2]

    def test_default_attempts_and_delay(self, monkeypatch):
        """Checks default settings."""
        sleep_calls = []
        monkeypatch.setattr(time, "sleep", lambda s: sleep_calls.append(s))
        calls = []

        def always_fails():
            calls.append(1)
            raise ValueError("nope")

        with pytest.raises(ValueError):
            retry(always_fails)

        assert len(calls) == 3
        assert sleep_calls == [1, 1]

    def test_zero_attempts_returns_none(self, monkeypatch):
        """Checks the loop never runs when attempts is zero."""
        monkeypatch.setattr(time, "sleep", lambda s: None)
        calls = []

        def never_called():
            calls.append(1)
            return "unreachable"

        assert retry(never_called, attempts=0) is None
        assert calls == []

    def test_single_attempt_raises_without_sleeping(self, monkeypatch):
        """Checks a lone failing attempt raises and never waits."""
        sleep_calls = []
        monkeypatch.setattr(time, "sleep", lambda s: sleep_calls.append(s))

        def always_fails():
            raise ValueError("nope")

        with pytest.raises(ValueError):
            retry(always_fails, attempts=1)

        assert sleep_calls == []


def test_run_with_fallback():
    assert run_with_fallback(int, 0, "invalid") == 0
    assert run_with_fallback(int, 0, "42") == 42
