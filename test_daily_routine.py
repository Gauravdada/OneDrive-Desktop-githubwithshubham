"""Tests for the Daily Routine App."""

import json
import os
import tempfile
import unittest

from daily_routine import (
    add_task,
    load_routine,
    mark_done,
    remove_task,
    reset_routine,
    save_routine,
    validate_time,
    view_routine,
)


class TestValidateTime(unittest.TestCase):
    def test_valid_times(self):
        self.assertTrue(validate_time("00:00"))
        self.assertTrue(validate_time("06:30"))
        self.assertTrue(validate_time("12:00"))
        self.assertTrue(validate_time("23:59"))

    def test_invalid_times(self):
        self.assertFalse(validate_time("24:00"))
        self.assertFalse(validate_time("12:60"))
        self.assertFalse(validate_time("abc"))
        self.assertFalse(validate_time("12"))
        self.assertFalse(validate_time(""))
        self.assertFalse(validate_time("1:2:3"))


class TestAddTask(unittest.TestCase):
    def test_add_valid_task(self):
        tasks = []
        tasks = add_task(tasks, "08:00", "Morning exercise")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["time"], "08:00")
        self.assertEqual(tasks[0]["task"], "Morning exercise")
        self.assertFalse(tasks[0]["done"])

    def test_add_multiple_tasks_sorted(self):
        tasks = []
        tasks = add_task(tasks, "12:00", "Lunch")
        tasks = add_task(tasks, "06:00", "Wake up")
        tasks = add_task(tasks, "08:00", "Breakfast")
        self.assertEqual(tasks[0]["time"], "06:00")
        self.assertEqual(tasks[1]["time"], "08:00")
        self.assertEqual(tasks[2]["time"], "12:00")

    def test_add_invalid_time(self):
        tasks = []
        tasks = add_task(tasks, "25:00", "Invalid")
        self.assertEqual(len(tasks), 0)

    def test_add_empty_description(self):
        tasks = []
        tasks = add_task(tasks, "08:00", "   ")
        self.assertEqual(len(tasks), 0)


class TestMarkDone(unittest.TestCase):
    def test_mark_valid_task(self):
        tasks = [{"time": "08:00", "task": "Exercise", "done": False}]
        tasks = mark_done(tasks, 1)
        self.assertTrue(tasks[0]["done"])

    def test_mark_invalid_number(self):
        tasks = [{"time": "08:00", "task": "Exercise", "done": False}]
        tasks = mark_done(tasks, 0)
        self.assertFalse(tasks[0]["done"])
        tasks = mark_done(tasks, 5)
        self.assertFalse(tasks[0]["done"])


class TestRemoveTask(unittest.TestCase):
    def test_remove_valid_task(self):
        tasks = [
            {"time": "06:00", "task": "Wake up", "done": False},
            {"time": "08:00", "task": "Breakfast", "done": False},
        ]
        tasks = remove_task(tasks, 1)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["task"], "Breakfast")

    def test_remove_invalid_number(self):
        tasks = [{"time": "06:00", "task": "Wake up", "done": False}]
        tasks = remove_task(tasks, 3)
        self.assertEqual(len(tasks), 1)


class TestResetRoutine(unittest.TestCase):
    def test_reset_all(self):
        tasks = [
            {"time": "06:00", "task": "Wake up", "done": True},
            {"time": "08:00", "task": "Breakfast", "done": True},
        ]
        tasks = reset_routine(tasks)
        self.assertFalse(tasks[0]["done"])
        self.assertFalse(tasks[1]["done"])


class TestSaveAndLoad(unittest.TestCase):
    def test_save_and_load(self):
        tasks = [
            {"time": "06:00", "task": "Wake up", "done": False},
            {"time": "08:00", "task": "Breakfast", "done": True},
        ]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as tmp:
            filepath = tmp.name
        try:
            save_routine(tasks, filepath)
            loaded = load_routine(filepath)
            self.assertEqual(loaded, tasks)
        finally:
            os.unlink(filepath)

    def test_load_nonexistent(self):
        loaded = load_routine("/tmp/nonexistent_file_12345.json")
        self.assertEqual(loaded, [])


class TestViewRoutine(unittest.TestCase):
    def test_view_empty(self):
        # Should not raise
        view_routine([])

    def test_view_with_tasks(self):
        tasks = [
            {"time": "06:00", "task": "Wake up", "done": True},
            {"time": "08:00", "task": "Breakfast", "done": False},
        ]
        # Should not raise
        view_routine(tasks)


if __name__ == "__main__":
    unittest.main()
