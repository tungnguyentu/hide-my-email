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
