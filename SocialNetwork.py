from abc import ABC, abstractmethod
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
class SocialNetwork:
    __instance = None
    @staticmethod
    def get_instance(name):
        if SocialNetwork is None:
            SocialNetwork(name)
        return SocialNetwork.__instance
    def __init__(self, name):
        if SocialNetwork.__instance is not None:
            raise Exception("SocialNetwork is a Singleton. Use get_instance() method!")
        else:
            SocialNetwork.__instance = self
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
        self.__followers = []
        self.__notif = []
        self.__posts_count = 0
    def get_name(self):
        return self.__user_name
    def get_password(self):
        return self.__password
    def is_logged_in(self) -> bool:
        return self.__logged_in
    def follow(self, other):
        check_if_user_logged_in(self)
        if self not in other.__followers:
            other.__followers.append(self)
            print(f"{self.__user_name} started following {other.get_name()}")
        else:
            print(f"{self.__user_name} already follows {other.get_name()}")
    def unfollow(self, other):
        check_if_user_logged_in(self)
        if self in other.__followers:
            other.__followers.remove(self)
            print(f"{self.__user_name} unfollowed {other.get_name()}")
    def add_notification(self, message: str, flag: bool = True):
        if flag:
            print(f"Notification to {self.__user_name}: {message}", end='')
        self.__notif.append(message)

    def log_out(self):
        self.__logged_in = False
    def log_in(self):
        self.__logged_in = True

    def publish_post(self, post_type: str, text, price: int = None, location: str = None):
        if post_type not in ['Text', 'Image', 'Sale']:
            raise Exception("Invalid post type. Must be Text/Image/Sale")
        check_if_user_logged_in(self)
        post = None
        if post_type == "Text":
            post = TextPost(self, text)
        elif post_type == "Image":
            post = ImagePost(self, text)
        elif post_type == "Sale":
            post = SalePost(self, text, price, location)
        for user in self.__followers: # Notify the followers
            user.add_notification(f"{self.__user_name} has a new post", False)
        self.__posts_count+=1
        print(post)
        return post
    def print_notifications(self):
        print(f"{self.__user_name}'s notifications:")
        for notif in self.__notif:
            print(f"{notif}")
    def __str__(self):
        return f"User name: {self.__user_name}, Number of posts: {self.__posts_count}, Number of followers: {len(self.__followers)}"
class Post(ABC):
    @abstractmethod
    def __init__(self, owner: User):
        self.__owner = owner
    def get_owner(self):
        return self.__owner
    def like(self, user: User):
        check_if_user_logged_in(user)
        if user != self.__owner:
            self.__owner.add_notification(f"{user.get_name()} liked your post")
            print()
    def comment(self, user: User, text: str):
        check_if_user_logged_in(user)
        self.__owner.add_notification(f"{user.get_name()} commented on your post")
        print(f": {text}")
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
        # image = mpimg.imread(self.__image_path)
        # plt.imshow(image)
        # plt.show()
        print(f"{self.get_owner().get_name()} posted a picture")
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
        if super().get_owner().get_password() != passw:
            raise Exception("Password does not match")
        if self.__sold:
            raise Exception("Item already sold!! Can't add discount")
        self.__price = self.__price * (1-(percent/100.0))
        print(f"Discount on {super().get_owner().get_name()}'s product! the new price is: {self.__price}")
    def sold(self, passw: str):
        if super().get_owner().get_password() != passw:
            raise Exception("Password does not match")
        self.__sold = True
        print(f"{super().get_owner().get_name()}'s product is sold")
    def __str__(self):
        status = "Sold!" if self.__sold else "For sale!"
        return (f"{self.get_owner().get_name()} posted a product for sale:\n"
                f"{status} {self.__item_name}, price: {self.__price}, pickup from: {self.__location}\n")
def check_if_user_logged_in(user: User):
    if (user.is_logged_in() == False):
        raise Exception(f"Error! {user.get_name()} is not logged in!")