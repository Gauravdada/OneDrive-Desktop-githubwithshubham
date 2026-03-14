#!/usr/bin/env python3
"""
Daily Routine App - A simple command-line application to manage your daily routine.

Features:
  - Add tasks with a scheduled time
  - View your daily routine sorted by time
  - Mark tasks as complete
  - Remove tasks
  - Data is saved automatically to a JSON file
"""

import json
import os
import sys

DATA_FILE = "routine_data.json"


def load_routine(filepath=DATA_FILE):
    """Load the routine from a JSON file. Returns a list of task dicts."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return json.load(f)


def save_routine(tasks, filepath=DATA_FILE):
    """Save the routine to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(tasks, f, indent=2)


def validate_time(time_str):
    """Validate that a time string is in HH:MM 24-hour format."""
    parts = time_str.split(":")
    if len(parts) != 2:
        return False
    try:
        hour, minute = int(parts[0]), int(parts[1])
    except ValueError:
        return False
    return 0 <= hour <= 23 and 0 <= minute <= 59


def add_task(tasks, time_str, description):
    """Add a new task to the routine."""
    if not validate_time(time_str):
        print("Invalid time format. Please use HH:MM (24-hour format).")
        return tasks
    if not description.strip():
        print("Task description cannot be empty.")
        return tasks
    task = {"time": time_str, "task": description.strip(), "done": False}
    tasks.append(task)
    tasks.sort(key=lambda t: t["time"])
    print(f"Added: [{time_str}] {description.strip()}")
    return tasks


def view_routine(tasks):
    """Display the daily routine sorted by time."""
    if not tasks:
        print("\nYour routine is empty. Add some tasks to get started!")
        return
    print("\n===== Your Daily Routine =====")
    print(f"{'#':<4} {'Time':<8} {'Status':<10} {'Task'}")
    print("-" * 45)
    for i, task in enumerate(tasks, 1):
        status = "Done" if task["done"] else "Pending"
        marker = "[x]" if task["done"] else "[ ]"
        print(f"{i:<4} {task['time']:<8} {marker} {status:<7} {task['task']}")
    done_count = sum(1 for t in tasks if t["done"])
    print("-" * 45)
    print(f"Progress: {done_count}/{len(tasks)} tasks completed")


def mark_done(tasks, task_number):
    """Mark a task as completed by its number (1-based)."""
    if task_number < 1 or task_number > len(tasks):
        print(f"Invalid task number. Choose between 1 and {len(tasks)}.")
        return tasks
    tasks[task_number - 1]["done"] = True
    print(f"Marked as done: {tasks[task_number - 1]['task']}")
    return tasks


def remove_task(tasks, task_number):
    """Remove a task by its number (1-based)."""
    if task_number < 1 or task_number > len(tasks):
        print(f"Invalid task number. Choose between 1 and {len(tasks)}.")
        return tasks
    removed = tasks.pop(task_number - 1)
    print(f"Removed: [{removed['time']}] {removed['task']}")
    return tasks


def reset_routine(tasks):
    """Reset all tasks to not done."""
    for task in tasks:
        task["done"] = False
    print("All tasks have been reset to pending.")
    return tasks


def print_menu():
    """Print the main menu."""
    print("\n===== Daily Routine App =====")
    print("1. View routine")
    print("2. Add task")
    print("3. Mark task as done")
    print("4. Remove task")
    print("5. Reset all tasks")
    print("6. Save and exit")
    print("=============================")


def main():
    """Main application loop."""
    tasks = load_routine()
    print("Welcome to the Daily Routine App!")

    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            view_routine(tasks)

        elif choice == "2":
            time_str = input("Enter time (HH:MM, 24-hour format): ").strip()
            description = input("Enter task description: ").strip()
            tasks = add_task(tasks, time_str, description)
            save_routine(tasks)

        elif choice == "3":
            view_routine(tasks)
            if tasks:
                try:
                    num = int(input("Enter task number to mark as done: ").strip())
                    tasks = mark_done(tasks, num)
                    save_routine(tasks)
                except ValueError:
                    print("Please enter a valid number.")

        elif choice == "4":
            view_routine(tasks)
            if tasks:
                try:
                    num = int(input("Enter task number to remove: ").strip())
                    tasks = remove_task(tasks, num)
                    save_routine(tasks)
                except ValueError:
                    print("Please enter a valid number.")

        elif choice == "5":
            tasks = reset_routine(tasks)
            save_routine(tasks)

        elif choice == "6":
            save_routine(tasks)
            print("Routine saved. Have a productive day!")
            break

        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()
