from utils.validators import validate_password_length, validate_email, validate_password, parse_command_arg

# Метод validate_password_length
def test_valid_length_in_range():
    length, error = validate_password_length("12")
    assert length == 12
    assert error is None

def test_length_below_minimum():
    length, error = validate_password_length("3")
    assert length is None
    assert error is not None

def test_length_at_upper_boundary():
    length, error = validate_password_length("128")
    assert length == 128
    assert error is None

def test_length_above_maximum():
    length, error = validate_password_length("129")
    assert length is None
    assert error is not None

def test_length_not_a_number():
    length, error = validate_password_length("abc")
    assert length is None
    assert error is not None

# Метод validate_email
def test_is_email_valid():
    valid, error = validate_email("example@gmail.com")
    assert valid is True
    assert error is None

def test_is_email_empty():
    valid, error = validate_email("")
    assert valid is False
    assert error is not None

def test_is_email_not_valid():
    valid, error = validate_email("example.com")
    assert valid is False
    assert error is not None

def test_is_email_contains_exclude_char():
    valid, error = validate_email("\n")
    assert valid is False
    assert error is not None

# Метод validate_password
def test_is_password_valid():
    valid, error = validate_password("qwertyuiop")
    assert valid is True
    assert error is None

def test_is_password_empty():
    valid, error = validate_password("")
    assert valid is False
    assert error is not None

def test_is_password_contains_exclude_char():
    valid, error = validate_password("\n")
    assert valid is False
    assert error is not None

# Метод parse_command_arg
def test_is_parse_command_arg_valid():
    arg = parse_command_arg("/password qwerty")
    assert arg is not None

def test_is_parse_command_arg_none():
    arg = parse_command_arg(None)
    assert arg is None

def test_is_parse_command_arg_not_has_args():
    arg = parse_command_arg("/password")
    assert arg is None