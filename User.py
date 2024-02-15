import Post
from ObserverDP import UserObserver, UserPublisher


class User(UserObserver, UserPublisher):

    def __init__(self, user_name: str, password: str):
        UserPublisher.__init__(self)
        UserObserver.__init__(self)
        self.__user_name = user_name
        self.__password = password
        self.__logged_in = True
        self.__posts_count = 0

    def get_name(self):
        return self.__user_name

    def get_password(self):
        return self.__password

    def is_logged_in(self) -> bool:
        return self.__logged_in

    def follow(self, other):
        self.check_if_user_logged_in()
        other.register(self)
        print(f"{self.__user_name} started following {other.get_name()}")

    def unfollow(self, other):
        self.check_if_user_logged_in()
        other.unregister(self)
        print(f"{self.__user_name} unfollowed {other.get_name()}")

    def log_out(self):
        self.__logged_in = False

    def log_in(self):
        self.__logged_in = True

    def publish_post(self, *args):
        self.check_if_user_logged_in()
        post_builder = Post.PostFactory()
        post = post_builder.create(self, args)
        self.__posts_count += 1
        self.notify(f"{self.__user_name} has a new post")
        print(post)
        return post

    def check_if_user_logged_in(self):
        if not self.is_logged_in():
            raise Exception(f"Error! {self.get_name()} is not logged in!")

    def print_notifications(self):
        print(f"{self.__user_name}'s notifications:")
        for notification in self._notifications:
            print(f"{notification}")

    def __str__(self):
        num_followers = len(self._subscribers)
        return (f"User name: {self.__user_name}, Number of posts: {self.__posts_count}, "
                f"Number of followers: {num_followers}")
