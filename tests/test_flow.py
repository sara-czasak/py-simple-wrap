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
    run_with_delay,
    run_if,
    time_function_call,
    time_it,
    wait_until,
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
        monkeypatch.setattr(time, "perf_counter", lambda: next(times))

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


def test_run_with_delay():
    def sample_add(a, b):
        return a + b

    # Test that it successfully runs after a tiny delay and returns correct math
    result = run_with_delay(0.01, sample_add, 5, 5)
    assert result == 10


def test_run_if_runs_function_when_condition_is_true():
    assert run_if(True, max, 3, 8) == 8


def test_run_if_returns_default_when_condition_is_false():
    assert run_if(False, max, 3, 8, default_value=0) == 0


def test_run_if_does_not_call_function_when_condition_is_false():
    calls = []

    def record_call():
        calls.append("called")

    assert run_if(False, record_call) is None
    assert calls == []


def test_run_if_passes_keyword_arguments():
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    assert run_if(True, greet, "World", greeting="Hi") == "Hi, World!"


def test_wait_until_returns_true_when_condition_is_ready():
    calls = []

    def condition():
        calls.append(1)
        return len(calls) == 3

    assert wait_until(condition, timeout=1, interval=0) is True
    assert len(calls) == 3


def test_wait_until_returns_false_after_timeout(monkeypatch):
    times = iter([0, 0.2, 0.4, 0.6])
    sleep_calls = []

    monkeypatch.setattr(time, "time", lambda: next(times))
    monkeypatch.setattr(time, "sleep", lambda delay: sleep_calls.append(delay))

    assert wait_until(lambda: False, timeout=0.5, interval=0.1) is False
    assert sleep_calls == [0.1, 0.1]


def test_wait_until_checks_condition_after_timeout(monkeypatch):
    times = iter([0, 1])
    calls = []

    monkeypatch.setattr(time, "time", lambda: next(times))

    def condition():
        calls.append(1)
        return len(calls) == 1

    assert wait_until(condition, timeout=0.5, interval=0.1) is True
    assert len(calls) == 1


@pytest.mark.parametrize("runner", [run_py_file, run_py_file_safe])
def test_script_runner_executes_main_guard(runner, tmp_path, capsys):
    script = tmp_path / "guarded.py"
    script.write_text(
        "if __name__ == '__main__':\n"
        "    print('main entry point ran')\n",
        encoding="utf-8",
    )

    result = runner(str(script))

    assert "main entry point ran" in capsys.readouterr().out
    if runner is run_py_file_safe:
        assert result == (True, None)


@pytest.mark.parametrize("runner", [run_py_file, run_py_file_safe])
def test_script_runner_handles_errors_in_main_guard(runner, tmp_path):
    script = tmp_path / "broken_main.py"
    script.write_text(
        "if __name__ == '__main__':\n"
        "    raise ValueError('main entry point failed')\n",
        encoding="utf-8",
    )

    if runner is run_py_file:
        with pytest.raises(EasyFlowError, match="main entry point failed"):
            runner(str(script))
    else:
        assert runner(str(script)) == (False, "main entry point failed")



def test_time_it_preserves_metadata_and_signature(capsys):
    import inspect

    def calculate(value: int, *, offset: int = 1) -> int:
        """Calculate an adjusted value."""
        return value + offset

    timed = time_it(calculate)

    assert timed.__name__ == calculate.__name__
    assert timed.__qualname__ == calculate.__qualname__
    assert timed.__doc__ == calculate.__doc__
    assert timed.__annotations__ == calculate.__annotations__
    assert inspect.signature(timed) == inspect.signature(calculate)
    assert inspect.unwrap(timed) is calculate
    assert timed(2, offset=3) == 5
    assert "calculate took" in capsys.readouterr().out


@pytest.mark.parametrize("clock_shift", [-3600, 3600])
@pytest.mark.parametrize("decorated", [False, True])
def test_timing_helpers_ignore_wall_clock_adjustments(monkeypatch, capsys, clock_shift, decorated):
    wall_times = iter([10000.0, 10000.0 + clock_shift])
    elapsed_times = iter([20.0, 20.25])
    monkeypatch.setattr(time, "time", lambda: next(wall_times))
    monkeypatch.setattr(time, "perf_counter", lambda: next(elapsed_times))

    def calculate():
        return 42

    if decorated:
        assert time_it(calculate)() == 42
        assert capsys.readouterr().out == "calculate took 0.25s\n"
    else:
        assert time_function_call(calculate) == pytest.approx(0.25)
