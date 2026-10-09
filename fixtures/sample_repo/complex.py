"""Complex module with high CC and security smells."""
import sqlite3


def complex_function(x, y, z, mode, flag, extra):
    """Deliberately complex function for radon testing."""
    result = 0
    if x > 0:
        if y > 0:
            if z > 0:
                result = x + y + z
            elif z < 0:
                result = x + y - z
            else:
                result = x + y
        elif y < 0:
            if z > 0:
                result = x - y + z
            else:
                result = x - y - z
        else:
            result = x
    elif x < 0:
        if mode == "add":
            result = abs(x) + y
        elif mode == "sub":
            result = abs(x) - y
        else:
            result = 0
    if flag:
        result *= 2
    if extra:
        result += extra
    return result


def unsafe_query(user_input: str) -> list:
    """Vulnerable to SQL injection — for semgrep testing."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    # BAD: string concatenation in SQL
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    cursor.execute(query)
    return cursor.fetchall()
