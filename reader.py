from datetime import datetime
import uuid
from model import Task, TaskStatus

class Reader:
    @staticmethod
    def read_status():
        prompt = ("1. To do\n"
                  "2. In Progress\n"
                  "3. Done\n"
                  "Enter your choice: ")
        while True:
            answer = str(input(prompt)).strip()
            match answer:
                case "1":
                    return TaskStatus.TODO
                case "2":
                    return TaskStatus.IN_PROGRESS
                case "3":
                    return TaskStatus.DONE
                case "-1":
                    return None
                case _:
                    print("Invalid choice. Try again.")

    @staticmethod
    def read_time(prompt: str):
        while True:
            raw_time = str(input(prompt)).strip()
            if raw_time == "-1":
                return None
            try:
                return datetime.strptime(raw_time, "%Y-%m-%d %H:%M")
            except ValueError:
                print(f"Invalid time format, try again.")
    @staticmethod
    def read_id(prompt: str):
        while True:
            raw_id = str(input(prompt)).strip()
            if raw_id == "-1":
                return None
            try:
                return uuid.UUID(raw_id)
            except ValueError:
                print(f"Invalid UUID format, try again.")
