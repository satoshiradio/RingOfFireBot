import config


class RingOfFire:
    def __init__(self):
        self.database = Database(config.DbConfig.SQLALCHEMY_DATABASE_URI)
    pass


def main():
    pass


if __name__ == "__main__":
    main()
