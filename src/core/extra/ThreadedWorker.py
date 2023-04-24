import threading
import queue
import typing

from extra.threadTypes import TaskType


class ThreadedWorker(threading.Thread):
    def __init__(
        self,
        taskQueue: TaskType,
        failedTaskQueue: TaskType,
        messageOutput: typing.Callable[[typing.Any], None],
    ):
        threading.Thread.__init__(self)

        self.setDaemon(True)
        self.taskQueue = taskQueue
        self.failedTaskQueue = failedTaskQueue
        self.messageOutput = messageOutput

    def run(self) -> None:
        while True:
            try:
                task = self.taskQueue.get()
                (callback, args) = task
                result = callback(*args)
                print(args, result)
            except Exception as e:
                ...
                print(e)
                self.messageOutput(
                    f"Failed to execute {callback} with {args}. Task has been added to list"
                )

                self.failedTaskQueue.put(task)
            finally:
                self.taskQueue.task_done()
