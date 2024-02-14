from abc import ABC, abstractmethod

from matplotlib import image as mpimg, pyplot as plt

import User


class Post(ABC):
    @abstractmethod
    def __init__(self, owner: User):
        self.__owner = owner

    def get_owner(self):
        return self.__owner

    def like(self, user: User):
        user.check_if_user_logged_in()
        if user != self.__owner:
            like_message = f"{user.get_name()} liked your post"
            self.__owner.update(like_message)
            print(f"notification to {self.__owner.get_name()}: {like_message}")

    def comment(self, user: User, text: str):
        user.check_if_user_logged_in()
        if user != self.__owner:
            comment_message = f"{user.get_name()} commented on your post"
            print(f"notification to {self.__owner.get_name()}: {comment_message}: {text}")


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
