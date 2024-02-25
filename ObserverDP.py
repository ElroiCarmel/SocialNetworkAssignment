from abc import ABC, abstractmethod


class Observer(ABC):
    """
    An Interface like class that defines an Observer type
    has to implement the update method
    """
    @abstractmethod
    def update(self, event: str) -> None:
        pass


class Publisher(ABC):

    def __init__(self):
        self._subscribers = set()

    @abstractmethod
    def register(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def unregister(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self, event: str) -> None:
        pass


class UserObserver(Observer):

    def __init__(self):
        self._notifications: list[str] = []

    def update(self, notification: str) -> None:
        self._notifications.append(notification)


class UserPublisher(Publisher):

    def register(self, observer: Observer) -> None:
        self._subscribers.add(observer)

    def unregister(self, observer: Observer) -> None:
        if observer in self._subscribers:
            self._subscribers.remove(observer)

    def notify(self, event: str) -> None:
        for observer in self._subscribers:
            observer.update(event)
