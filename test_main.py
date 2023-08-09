#
# Demonstrate 6 different ways to unit test the 'main.send_message' function and assert that it invokes the 'send'
# method of the 'main.DemoApiClient' class.
#
# In the first 3 tests, only the `send` method is mocked (aka monkey-patched). In particular the '__init__', 'connect',
# and 'close' methods from the 'main.DemoApiClient' class are still executed.
#
# In the last 3 tests, the whole 'main.DemoApiClient' class is mocked (aka monkey-patched). In particular no methods
# from this class are executed anymore.
#
# Of course in real-life we would have only one test and 'DemoApiClient' would be replaced by areal API like
# 'twilio.rest.Client'.
#
# By default pytest hides the logging output. To prevent this, run the tests with:
#
#     pytest --log-cli-level=DEBUG
#
# The output should look similar to this:
#
#     ============================= test session starts =============================
#     collecting ... collected 6 items
#
#     test_main.py::test_send_message_with_decorator_and_mock_method
#     -------------------------------- live log call --------------------------------
#     DEBUG    DemoApiClient:main.py:10 __init__
#     DEBUG    DemoApiClient:main.py:16 connect
#     DEBUG    DemoApiClient:main.py:19 close
#     PASSED                                                                   [ 16%]
#     test_main.py::test_send_message_with_context_manager_and_mock_method
#     -------------------------------- live log call --------------------------------
#     DEBUG    DemoApiClient:main.py:10 __init__
#     DEBUG    DemoApiClient:main.py:16 connect
#     DEBUG    DemoApiClient:main.py:19 close
#     PASSED                                                                   [ 33%]
#     test_main.py::test_send_message_with_fixture_and_mock_method
#     -------------------------------- live log call --------------------------------
#     DEBUG    DemoApiClient:main.py:10 __init__
#     DEBUG    DemoApiClient:main.py:16 connect
#     DEBUG    DemoApiClient:main.py:19 close
#     PASSED                                                                   [ 50%]
#     test_main.py::test_send_message_with_decorator_and_mock_class PASSED     [ 66%]
#     test_main.py::test_send_message_with_context_manager_and_mock_class PASSED [ 83%]
#     test_main.py::test_send_message_with_fixture_and_mock_class PASSED       [100%]
#
#     ============================== 6 passed in 0.07s ==============================
#

from unittest.mock import patch

import pytest

from main import send_message


# ---------------------------------------------------------------------------------------------------------------------
# Patching a single method.
# ---------------------------------------------------------------------------------------------------------------------

@patch("main.DemoApiClient.send")
def test_send_message_with_decorator_and_mock_method(mock_method):
    # The send method is patched until the function terminates.

    send_message("foo")
    mock_method.assert_called_with("foo")


def test_send_message_with_context_manager_and_mock_method():
    # The send method is not patched yet.

    with patch("main.DemoApiClient.send") as mock_method:
        # The send method is patched until the with block terminates.

        send_message("foo")
        mock_method.assert_called_with("foo")

    # The send method is not patched anymore.


@pytest.fixture
def mock_send():
    with patch("main.DemoApiClient.send") as mock_method:
        yield mock_method


def test_send_message_with_fixture_and_mock_method(mock_send):
    # The send method is patched until the function terminates.

    send_message("foo")
    mock_send.assert_called_with("foo")


# ---------------------------------------------------------------------------------------------------------------------
# Patching a whole class.
# ---------------------------------------------------------------------------------------------------------------------

@patch("main.DemoApiClient")
def test_send_message_with_decorator_and_mock_class(mock_class):
    # The main.DemoApiClient class is patched until the function terminates.

    send_message("foo")
    mock_class().connect.assert_called()
    mock_class().send.assert_called_with("foo")
    mock_class().close.assert_called()


def test_send_message_with_context_manager_and_mock_class():
    # The main.DemoApiClient class is not patched yet.

    with patch("main.DemoApiClient") as mock_class:
        # The main.DemoApiClient class is patched until the with block terminates.

        send_message("foo")
        mock_class().connect.assert_called()
        mock_class().send.assert_called_with("foo")
        mock_class().close.assert_called()

    # The main.DemoApiClient class is not patched anymore.


@pytest.fixture
def mock_api():
    with patch("main.DemoApiClient") as mock_class:
        yield mock_class


def test_send_message_with_fixture_and_mock_class(mock_api):
    # The main.DemoApiClient class is patched until the function terminates.

    send_message("foo")
    mock_api().connect.assert_called()
    mock_api().send.assert_called_with("foo")
    mock_api().close.assert_called()
