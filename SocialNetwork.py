from abc import ABC, abstractmethod
from matplotlib import pyplot as plt
from matplotlib import image as mpimg


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
            if user.get_name() == name:
                if user.get_password() == passw:
                    user.log_in()
                    print(f"{name} connected")

    def __str__(self):
        string = f"{self.__name} social network:\n"
        for user in self.__users:
            string += f"{user}\n"
        return string


class User:
    def __init__(self, user_name: str, password: str):
        self.__user_name = user_name
        self.__password = password
        self.__logged_in = True
        # self.__followers = []
        self.__notifications = []
        self.__posts_count = 0
        self.__ns = NotificationService(self)

    def get_name(self):
        return self.__user_name

    def get_password(self):
        return self.__password

    def get_notification_service(self):
        return self.__ns

    def is_logged_in(self) -> bool:
        return self.__logged_in

    def follow(self, other):
        self.check_if_user_logged_in()
        other.__ns.add_subscriber(self)

    def unfollow(self, other):
        self.check_if_user_logged_in()
        other.__ns.remove_subscriber(self)

    def add_notification(self, message: str):
        self.__notifications.append(message)

    def log_out(self):
        self.__logged_in = False

    def log_in(self):
        self.__logged_in = True

    def publish_post(self, post_type: str, text, price: int = None, location: str = None):
        self.check_if_user_logged_in()
        post_builder = PostFactory()
        post = post_builder.create(self, post_type, text, price, location)
        self.__ns.new_post_update()
        self.__posts_count += 1
        print(post)
        return post

    def check_if_user_logged_in(self):
        if not self.is_logged_in():
            raise Exception(f"Error! {self.get_name()} is not logged in!")

    def print_notifications(self):
        print(f"{self.__user_name}'s notifications:")
        for notification in self.__notifications:
            print(f"{notification}")

    def __str__(self):
        num_followers = len(self.__ns.get_subscribers())
        return (f"User name: {self.__user_name}, Number of posts: {self.__posts_count}, "
                f"Number of followers: {num_followers}")


class Post(ABC):
    @abstractmethod
    def __init__(self, owner: User):
        self.__owner = owner

    def get_owner(self):
        return self.__owner

    def like(self, user: User):
        user.check_if_user_logged_in()
        if user != self.__owner:
            self.__owner.get_notification_service().notify_like(user)

    def comment(self, user: User, text: str):
        user.check_if_user_logged_in()
        if user != self.__owner:
            self.__owner.get_notification_service().notify_comment(user, text)


class TextPost(Post):
    def __init__(self, owner: User, content):
        super().__init__(owner)
        self.__content = content

    def __str__(self):
        return (f"{self.get_owner().get_name()} published a post:\n"
                f"\"{self.__content}\"\n")


class ImagePost(Post):
    def __init__(self, owner: User, image_path):
        super().__init__(owner)
        self.__image_path = image_path

    def display(self):
        image = mpimg.imread(self.__image_path)
        plt.imshow(image)
        plt.show()
        print("Shows picture")

    def __str__(self):
        return f"{self.get_owner().get_name()} posted a picture\n"


class SalePost(Post):
    def __init__(self, owner: User, item: str, price: int, location: str):
        super().__init__(owner)
        self.__item_name = item
        self.__price = price
        self.__location = location
        self.__sold = False

    def discount(self, percent: int, passw: str):
        if self.get_owner().get_password() != passw:
            raise Exception("Password does not match")
        if self.__sold:
            raise Exception("Item already sold!! Can't add discount")
        self.__price = self.__price * (1-(percent/100.0))
        print(f"Discount on {self.get_owner().get_name()} product! the new price is: {self.__price}")

    def sold(self, passw: str):
        if super().get_owner().get_password() != passw:
            raise Exception("Password does not match")
        self.__sold = True
        print(f"{super().get_owner().get_name()}'s product is sold")

    def __str__(self):
        status = "Sold!" if self.__sold else "For sale!"
        return (f"{self.get_owner().get_name()} posted a product for sale:\n"
                f"{status} {self.__item_name}, price: {self.__price}, pickup from: {self.__location}\n")


class PostFactory:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def create(self, owner: User, post_type: str, text, price: int = None, location: str = None):
        post = None
        if post_type == "Text":
            post = TextPost(owner, text)
        elif post_type == "Image":
            post = ImagePost(owner, text)
        elif post_type == "Sale":
            post = SalePost(owner, text, price, location)
        else:
            raise Exception("Invalid post type. Must be Text/Image/Sale")
        return post


class NotificationService:
    def __init__(self, publisher):
        self.__publisher: User = publisher
        self.__subscribers: list[User] = []

    def add_subscriber(self, user):
        if user not in self.__subscribers:
            self.__subscribers.append(user)
            print(f"{user.get_name()} started following {self.__publisher.get_name()}")

    def remove_subscriber(self, user):
        if user in self.__subscribers:
            self.__subscribers.remove(user)
            print(f"{user.get_name()} unfollowed {self.__publisher.get_name()}")

    def new_post_update(self):
        for subscriber in self.__subscribers:
            subscriber.add_notification(f"{self.__publisher.get_name()} has a new post")

    def notify_like(self, other: User):
        message = f"{other.get_name()} liked your post"
        self.__publisher.add_notification(f"{message}")
        print(f"notification to {self.__publisher.get_name()}: {message}")

    def notify_comment(self, other: User, comment: str):
        message = f"{other.get_name()} commented on your post"
        self.__publisher.add_notification(f"{message}")
        print(f"notification to {self.__publisher.get_name()}: {message}: {comment}")

    def get_subscribers(self):
        return self.__subscribers
