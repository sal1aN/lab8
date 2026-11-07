from controller import TaskApp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base
from repository import TaskRepository

DATABASE_URL = 'postgresql+psycopg2://postgres:password123@localhost:5431/postgres'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)



def runner():
    with SessionLocal() as session:
        repository = TaskRepository(session)
        app = TaskApp(repository)
        prompt = ('1. Add Task\n'
                  '2. Remove Task\n'
                  '3. Show Task by Id\n'
                  '4. Show all tasks\n'
                  '5. Change Task Status\n'
                  '6. Change Task\n'
                  '7. Filter Tasks\n'
                  '8. Quit\n'
                  'Enter your choice: ')
        running = True
        while running:
            choice = input(prompt).strip()
            match choice:
                case '1':
                    app.add_task()
                case '2':
                    app.delete_task()
                case'3':
                    app.display_task()
                case '4':
                    app.display_all_tasks()
                case '5':
                    app.change_status()
                case '6':
                    app.change_task()
                case '7':
                    app.filter_by_status()
                case'8':
                    running = False
                case _:
                    print("Enter a valid choice")


if __name__ == '__main__':
    runner()



