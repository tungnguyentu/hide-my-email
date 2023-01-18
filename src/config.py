from environs import Env

env = Env()
env.read_env()


class Settings:
    SQLALCHEMY_DATABASE_URI = env.str("SQLALCHEMY_DATABASE_URI")
    RANDOM_WORDS = env.list("RANDOM_WORDS")
    LIMIT_PROXIES = env.int("LIMIT_PROXIES")
    JWT_EXP = env.int("JWT_EXP")
    JWT_ALG = env.str("ALGORITHM")
    JWT_SECRET = env.str("SECRET_KEY")
    NO_REPLY_SENDER = env.str("NO_REPLY_EMAIL")
    NO_REPLY_PASSWORD = env.str("NO_REPLY_EMAIL_PASSWORD")
    SMTP_HOST = env.str("SMTP_HOST")
    HOST = env.str("HOST")
    SECRET_KEY_SIGNUP = env.str("SECRET_KEY_SIGNUP")
    DEFAULT_RANDOM_EMAIL_PASS = env.str("DEFAULT_RANDOM_EMAIL_PASS")