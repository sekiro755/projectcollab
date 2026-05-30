import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test_add_existing_user(setup_database, connection):
    add_user('testuser', 'testuser@example.com', 'password123')
    add_user('testuser', 'another@example.com', 'password456')
    cursor = connection.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE username='testuser';"
        )
    count = cursor.fetchone()[0]

    assert count == 1

def test_authenticate_user_success(setup_database, connection):
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user
    assert authenticate_user('testuser', 'password123') is True 

def test_display_users(setup_database, connection):
    add_user('user1', 'user1@example.com', 'password1')
    add_user('user2', 'user2@example.com', 'password2')
    cursor = connection.cursor()
    cursor.execute("SELECT username, email FROM users")
    users = cursor.fetchall()
    assert len(users) == 2, "Должно отображаться два пользователя."
    assert ('user1', 'user1@example.com') in users
    assert ('user2', 'user2@example.com') in users


# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""