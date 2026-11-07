from datetime import datetime, timedelta
import uuid
from model import Task, TaskStatus
from reader import Reader
from repository import TaskRepository


class TaskApp:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def add_task(self):
        print("Please, enter following values")
        description = input("Description: ")
        created_at = datetime.now()
        schedule_for = datetime.now() + timedelta(days=1)
        wish = input("Do you wish to enter schedule timedate(default - 1 day)?[y/n]: ")
        if wish.strip().lower() == "y":
            schedule_for = Reader.read_time("schedule for[YYYY-MM-DD HH:MM]: ")
        status = TaskStatus.TODO
        task = Task(description=description, created_at=created_at, schedule_for=schedule_for, status=status)
        self.repository.add(task)
        return task.id

    def change_status_by_id(self, id_to_change):
        if id_to_change is None:
            return
        if isinstance(id_to_change, uuid.UUID):
            task = self.repository.get(id_to_change)
            if not task:
                print(f"Task with id {id_to_change} not found.")
                return
            print("Please, enter new status:")
            new_status = Reader.read_status()
            if new_status is None:
                return

            task.status = new_status
            self.repository.update()
            print(f"Task with id {id_to_change} changed.")

    def change_status(self):
        id_to_change = Reader.read_id("id of task you want to change: ")
        self.change_status_by_id(id_to_change)

    def delete_task(self):
        id_to_delete = Reader.read_id("id of task you want to delete: ")
        if id_to_delete is None:
            return
        if isinstance(id_to_delete, uuid.UUID):
            task = self.repository.get(id_to_delete)
            if not task:
                print(f"Task with id {id_to_delete} not found.")
                return
            self.repository.delete(task)
            print(f"Task with id {id_to_delete} deleted.")

    def change_task(self):
        id_to_change = Reader.read_id("id of task you want to change: ")
        if id_to_change is None:
            return
        if isinstance(id_to_change, uuid.UUID):
            task = self.repository.get(id_to_change)
            if not task:
                print(f"Task with id {id_to_change} not found.")
                return
            prompt = ("1. Description\n"
                      "2. Created at\n"
                      "3. Schedule for\n"
                      "4. Status:\n"
                      "5. Quit\n"
                      "Enter your choice: ")
            running = True
            while running:
                choice = str(input(prompt))
                match choice:
                    case "1":
                        new_description = input("Description: ")
                        task.description = new_description
                        self.repository.update()
                        running = False
                    case "2":
                        new_created_at = Reader.read_time("created at: ")
                        task.created_at = new_created_at
                        self.repository.update()
                        running = False
                    case "3":
                        new_scheduled_for = Reader.read_time("Scheduled for: ")
                        task.schedule_for = new_scheduled_for
                        self.repository.update()
                        running = False
                    case "4":
                        self.change_status_by_id(id_to_change)
                        running = False
                    case "5":
                        running = False
                    case _:
                        print("Invalid choice. Try again.")

    def display_task(self):
        id_to_display = Reader.read_id("id of task you want to display: ")
        if id_to_display is None:
            return
        if isinstance(id_to_display, uuid.UUID):
            task = self.repository.get(id_to_display)
            if not task:
                print(f"Task with id {id_to_display} not found.")
            print(task)

    def display_all_tasks(self):
        tasks = self.repository.get_all()
        for task in tasks:
            print(task)
            print('-'*40)

    def filter_by_status(self):
        print("Please, enter status to filter by: ")
        target_status = Reader.read_status()
        tasks = self.repository.filter_by_status(target_status)
        for task in tasks:
            print(task)
            print('-'*40)

