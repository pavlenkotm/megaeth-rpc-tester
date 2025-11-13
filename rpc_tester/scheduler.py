"""
Test scheduling system for automated periodic testing.

Schedule and run RPC tests at specified intervals.
"""

import asyncio
import json
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class ScheduleType(Enum):
    """Types of schedules."""

    ONCE = "once"
    INTERVAL = "interval"
    DAILY = "daily"
    WEEKLY = "weekly"
    CRON = "cron"


@dataclass
class ScheduledTask:
    """Scheduled test task."""

    task_id: str
    name: str
    schedule_type: ScheduleType
    config: Dict[str, Any]
    test_config: Dict[str, Any]
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    run_count: int = 0


class TestScheduler:
    """Schedule and manage periodic RPC tests."""

    def __init__(self):
        """Initialize scheduler."""
        self.tasks: Dict[str, ScheduledTask] = {}
        self.running = False
        self._scheduler_task: Optional[asyncio.Task] = None
        self.callbacks: List[Callable] = []

    def add_interval_task(
        self, task_id: str, name: str, interval_seconds: int, test_config: Dict[str, Any]
    ):
        """
        Add task that runs at regular intervals.

        Args:
            task_id: Unique task identifier
            name: Task name
            interval_seconds: Interval in seconds
            test_config: Test configuration
        """
        task = ScheduledTask(
            task_id=task_id,
            name=name,
            schedule_type=ScheduleType.INTERVAL,
            config={"interval_seconds": interval_seconds},
            test_config=test_config,
            next_run=datetime.now(),
        )
        self.tasks[task_id] = task

    def add_daily_task(self, task_id: str, name: str, run_time: time, test_config: Dict[str, Any]):
        """
        Add task that runs daily at specific time.

        Args:
            task_id: Unique task identifier
            name: Task name
            run_time: Time to run (datetime.time object)
            test_config: Test configuration
        """
        task = ScheduledTask(
            task_id=task_id,
            name=name,
            schedule_type=ScheduleType.DAILY,
            config={"run_time": run_time.isoformat()},
            test_config=test_config,
            next_run=self._calculate_next_daily_run(run_time),
        )
        self.tasks[task_id] = task

    def add_weekly_task(
        self, task_id: str, name: str, weekday: int, run_time: time, test_config: Dict[str, Any]
    ):
        """
        Add task that runs weekly on specific day.

        Args:
            task_id: Unique task identifier
            name: Task name
            weekday: Day of week (0=Monday, 6=Sunday)
            run_time: Time to run
            test_config: Test configuration
        """
        task = ScheduledTask(
            task_id=task_id,
            name=name,
            schedule_type=ScheduleType.WEEKLY,
            config={"weekday": weekday, "run_time": run_time.isoformat()},
            test_config=test_config,
            next_run=self._calculate_next_weekly_run(weekday, run_time),
        )
        self.tasks[task_id] = task

    def add_once_task(self, task_id: str, name: str, run_at: datetime, test_config: Dict[str, Any]):
        """
        Add task that runs once at specific time.

        Args:
            task_id: Unique task identifier
            name: Task name
            run_at: When to run
            test_config: Test configuration
        """
        task = ScheduledTask(
            task_id=task_id,
            name=name,
            schedule_type=ScheduleType.ONCE,
            config={"run_at": run_at.isoformat()},
            test_config=test_config,
            next_run=run_at,
        )
        self.tasks[task_id] = task

    def remove_task(self, task_id: str):
        """Remove scheduled task."""
        if task_id in self.tasks:
            del self.tasks[task_id]

    def enable_task(self, task_id: str):
        """Enable task."""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = True

    def disable_task(self, task_id: str):
        """Disable task."""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = False

    def add_callback(self, callback: Callable):
        """
        Add callback to be called when task runs.

        Callback signature: async def callback(task: ScheduledTask, results: Any)
        """
        self.callbacks.append(callback)

    async def start(self):
        """Start scheduler."""
        if self.running:
            print("Scheduler already running")
            return

        self.running = True
        self._scheduler_task = asyncio.create_task(self._run_scheduler())
        print("Scheduler started")

    async def stop(self):
        """Stop scheduler."""
        self.running = False

        if self._scheduler_task:
            self._scheduler_task.cancel()
            try:
                await self._scheduler_task
            except asyncio.CancelledError:
                pass

        print("Scheduler stopped")

    async def _run_scheduler(self):
        """Main scheduler loop."""
        while self.running:
            try:
                # Check for tasks that need to run
                now = datetime.now()
                tasks_to_run = []

                for task in self.tasks.values():
                    if not task.enabled:
                        continue

                    if task.next_run and now >= task.next_run:
                        tasks_to_run.append(task)

                # Run tasks
                for task in tasks_to_run:
                    asyncio.create_task(self._execute_task(task))

                # Sleep for a short interval
                await asyncio.sleep(1)

            except Exception as e:
                print(f"Scheduler error: {e}")

    async def _execute_task(self, task: ScheduledTask):
        """Execute scheduled task."""
        print(f"Running scheduled task: {task.name}")

        try:
            # Execute test (placeholder - would call actual test runner)
            results = await self._run_test(task.test_config)

            # Update task
            task.last_run = datetime.now()
            task.run_count += 1

            # Calculate next run
            task.next_run = self._calculate_next_run(task)

            # Disable once tasks
            if task.schedule_type == ScheduleType.ONCE:
                task.enabled = False

            # Call callbacks
            for callback in self.callbacks:
                try:
                    await callback(task, results)
                except Exception as e:
                    print(f"Callback error: {e}")

        except Exception as e:
            print(f"Task execution error: {e}")

    async def _run_test(self, test_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run test with given configuration.

        This is a placeholder - would integrate with actual test runner.
        """
        # Placeholder implementation
        await asyncio.sleep(0.1)
        return {
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "config": test_config,
        }

    def _calculate_next_run(self, task: ScheduledTask) -> Optional[datetime]:
        """Calculate next run time for task."""
        if task.schedule_type == ScheduleType.INTERVAL:
            interval = task.config["interval_seconds"]
            return datetime.now() + timedelta(seconds=interval)

        elif task.schedule_type == ScheduleType.DAILY:
            run_time = time.fromisoformat(task.config["run_time"])
            return self._calculate_next_daily_run(run_time)

        elif task.schedule_type == ScheduleType.WEEKLY:
            weekday = task.config["weekday"]
            run_time = time.fromisoformat(task.config["run_time"])
            return self._calculate_next_weekly_run(weekday, run_time)

        elif task.schedule_type == ScheduleType.ONCE:
            return None  # One-time tasks don't recur

        return None

    @staticmethod
    def _calculate_next_daily_run(run_time: time) -> datetime:
        """Calculate next daily run time."""
        now = datetime.now()
        next_run = datetime.combine(now.date(), run_time)

        if next_run <= now:
            next_run += timedelta(days=1)

        return next_run

    @staticmethod
    def _calculate_next_weekly_run(weekday: int, run_time: time) -> datetime:
        """Calculate next weekly run time."""
        now = datetime.now()
        days_ahead = weekday - now.weekday()

        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7

        next_run = datetime.combine(now.date(), run_time) + timedelta(days=days_ahead)

        return next_run

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of scheduled task."""
        if task_id not in self.tasks:
            return None

        task = self.tasks[task_id]

        return {
            "task_id": task.task_id,
            "name": task.name,
            "schedule_type": task.schedule_type.value,
            "enabled": task.enabled,
            "last_run": task.last_run.isoformat() if task.last_run else None,
            "next_run": task.next_run.isoformat() if task.next_run else None,
            "run_count": task.run_count,
        }

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get status of all tasks."""
        return [self.get_task_status(task_id) for task_id in self.tasks.keys()]

    def save_schedule(self, file_path: str):
        """
        Save schedule to file.

        Args:
            file_path: Path to save file
        """
        data = []

        for task in self.tasks.values():
            task_data = {
                "task_id": task.task_id,
                "name": task.name,
                "schedule_type": task.schedule_type.value,
                "config": task.config,
                "test_config": task.test_config,
                "enabled": task.enabled,
            }
            data.append(task_data)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    def load_schedule(self, file_path: str):
        """
        Load schedule from file.

        Args:
            file_path: Path to schedule file
        """
        with open(file_path, "r") as f:
            data = json.load(f)

        for task_data in data:
            schedule_type = ScheduleType(task_data["schedule_type"])

            task = ScheduledTask(
                task_id=task_data["task_id"],
                name=task_data["name"],
                schedule_type=schedule_type,
                config=task_data["config"],
                test_config=task_data["test_config"],
                enabled=task_data.get("enabled", True),
            )

            # Calculate next run
            if schedule_type == ScheduleType.INTERVAL:
                task.next_run = datetime.now()
            elif schedule_type == ScheduleType.DAILY:
                run_time = time.fromisoformat(task.config["run_time"])
                task.next_run = self._calculate_next_daily_run(run_time)
            elif schedule_type == ScheduleType.WEEKLY:
                weekday = task.config["weekday"]
                run_time = time.fromisoformat(task.config["run_time"])
                task.next_run = self._calculate_next_weekly_run(weekday, run_time)
            elif schedule_type == ScheduleType.ONCE:
                run_at = datetime.fromisoformat(task.config["run_at"])
                task.next_run = run_at if run_at > datetime.now() else None

            self.tasks[task.task_id] = task
