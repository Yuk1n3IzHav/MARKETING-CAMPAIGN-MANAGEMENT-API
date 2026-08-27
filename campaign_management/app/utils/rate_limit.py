from time import time

login_attempts = {}


def check_login_rate_limit(identifier: str, limit: int, window_seconds: int):
    now = time()

    attempts = login_attempts.get(identifier, [])

    attempts = [attempt for attempt in attempts if now - attempt < window_seconds]

    if len(attempts) >= limit:
        login_attempts[identifier] = attempts

        return False

    attempts.append(now)

    login_attempts[identifier] = attempts

    return True
