from User import User


class SocialNetwork:
    __instance = None

    def __new__(cls, name):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, name):
        self.__name = name
        self.__users = []
        print(f"The social network {self.__name} was created!")

    def sign_up(self, user_name, password):
        if len(password) < 4 or len(password) > 8:
            raise Exception("The password must be between 4 and 8 characters.")
        for user in self.__users:
            if user.get_name() == user_name:
                raise Exception(f"The name '{user_name}' is already taken! Try another name.")
        user = User(user_name, password)
        self.__users.append(user)
        return user

    def log_out(self, user_name: str):
        for user in self.__users:
            if user.get_name() == user_name:
                user.log_out()
                print(f"{user_name} disconnected")

    def log_in(self, name: str, passw: str) -> None:
        for user in self.__users:
            if user.get_name() == name and user.get_password() == passw:
                user.log_in()
                print(f"{name} connected")

    def __str__(self):
        string = f"{self.__name} social network:\n"
        for user in self.__users:
            string += f"{user}\n"
        return string







