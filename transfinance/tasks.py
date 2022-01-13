from datetime import datetime, timedelta
from queue import Queue
from threading import Thread
from time import sleep
from typing import Callable, Optional, Iterable, Dict


ONE_MINUTE = timedelta(seconds=60)


class Task:
    def __init__(
        self,
        function: Callable,
        args: Optional[Iterable] = None,
        kwargs: Optional[Dict] = None,
    ) -> None:
        self._function = function
        self._args = args or []
        self._kwargs = kwargs or {}

    def run(self) -> None:
        self._function(*self._args, **self._kwargs)


class TaskQueue(Thread):
    def __init__(self, limit: int = 100) -> None:
        super().__init__()
        self._limit_per_minute = limit
        self._tasks: Queue[Task] = Queue()

    def run(self) -> None:
        start = datetime.today()
        processed = 0
        while True:
            if self._tasks.empty():
                sleep(1)
                continue
            now = datetime.today()
            duration = now - start
            if duration > ONE_MINUTE:
                start += ONE_MINUTE
                processed = 0
                continue
            if processed == self._limit_per_minute:
                remainder = ONE_MINUTE - duration
                sleep(remainder.total_seconds())
                continue

            task = self._tasks.get()
            task.run()
            processed += 1

    def add_tasks(self, *tasks: Task) -> None:
        for task in tasks:
            self._tasks.put(task)


request_queue = TaskQueue()
request_queue.start()
