import abc


class AppLogger(abc.ABC):
    @abc.abstractmethod
    def __init__(self) -> None:
        ...

    @abc.abstractmethod
    async def info(self, message: str) -> None:
        ...

    @abc.abstractmethod
    async def warning(self, message: str) -> None:
        ...

    @abc.abstractmethod
    async def error(self, message: str) -> None:
        ...

    @abc.abstractmethod
    async def critical(self, message: str) -> None:
        ...

    @abc.abstractmethod
    async def fatal(self, message: str) -> None:
        ...
