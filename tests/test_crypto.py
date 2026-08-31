from services.crypto import (
    DIGITS,
    analyze_password,
    build_alphabet,
    entropy,
    generate_password,
    make_hashes,
)


# Метод build_alphabet
def test_build_alphabet_all_enabled():
    alphabet = build_alphabet(True, True, True, False)
    assert len(alphabet) > 0
    assert any(ch.islower() for ch in alphabet)
    assert any(ch.isdigit() for ch in alphabet)
    assert any(ch in "!@#$%^&*()+_-=" for ch in alphabet)


def test_build_alphabet_exclude_similar():
    alphabet = build_alphabet(True, True, True, True)
    assert "I" not in alphabet
    assert "l" not in alphabet
    assert "1" not in alphabet
    assert "O" not in alphabet
    assert "0" not in alphabet


def test_build_alphabet_only_digits():
    alphabet = build_alphabet(False, True, False, False)
    assert alphabet == DIGITS


# Метод generate_password
def test_generate_password_length():
    alphabet = build_alphabet(True, True, True, False)
    password = generate_password(16, alphabet)
    assert len(password) == 16


def test_generate_password_symbols_from_alphabet():
    alphabet = build_alphabet(True, True, True, False)
    password = generate_password(32, alphabet)
    assert all(c in alphabet for c in password)


def test_generate_password_with_only_digits():
    alphabet = build_alphabet(False, True, False, False)
    password = generate_password(8, alphabet)
    assert password.isdigit()


# Метод make_hashes
def test_make_hashes_md5():
    hashes = make_hashes("hello")
    assert hashes["MD5"] == "5d41402abc4b2a76b9719d911017c592"


def test_make_hashes_sha1():
    hashes = make_hashes("hello")
    assert hashes["SHA-1"] == "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"


def test_make_hashes_sha256():
    hashes = make_hashes("hello")
    assert (
        hashes["SHA-256"]
        == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    )


# Метод entropy
def test_entropy_increases_with_length():
    ent_short = entropy("abcdef")
    ent_long = entropy("qwertyuiopasdfghjklzxcvbnm")
    assert ent_long > ent_short


# Метод analyze_password
def test_analyze_weak_password():
    res = analyze_password("123456")
    assert res["level"] == "Слабый"


def test_analyze_medium_password():
    res = analyze_password("abc12345")
    assert res["level"] == "Средний"


def test_analyze_strong_password():
    res = analyze_password("Password2@24!Str0ng")
    assert res["level"] == "Сильный"
