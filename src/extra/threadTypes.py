import typing
import queue

TaskType = typing.NewType(
    "TaskType",
    "queue.Queue[typing.Tuple[typing.Callable, typing.List]]",
)
