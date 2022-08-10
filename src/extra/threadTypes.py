import typing
import queue

TaskType = typing.NewType(
    "TaskType[(...) -> void, List]",
    "queue.Queue[typing.Tuple[typing.Callable, typing.List]]",
)
