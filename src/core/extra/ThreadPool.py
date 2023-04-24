import threading
import typing
import queue

from extra.ThreadedWorker import ThreadedWorker
from extra.threadTypes import TaskType


class ThreadPool:
    def __init__(
        self,
        size: int,
        taskQueue: TaskType,
        failedTaskQueue: TaskType,
        messageOutput: typing.Callable[[typing.Any], None],
    ):
        self.threads: typing.List[ThreadedWorker] = []
        for i in range(size):
            thread = ThreadedWorker(taskQueue, failedTaskQueue, messageOutput)
            self.threads.append(thread)
        ...

    def start(self) -> None:
        for i in self.threads:
            i.start()

    def __del__(self) -> None:
        for i in self.threads:
            del i
        ...
