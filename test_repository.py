from datetime import datetime, timedelta
from model import TaskStatus, Task

def test_add_task(repository, db_session):
    task = Task(
        description="Testing",
        created_at= datetime.now(),
        schedule_for=datetime.now() + timedelta(days=1),
        status = TaskStatus.TODO
    )
    repository.add(task)
    task_in_db = db_session.get(Task, task.id)
    assert task_in_db is not None
    assert task_in_db.description == "Testing"
    assert task_in_db.status == TaskStatus.TODO

def test_get_task(repository, db_session):
    task = Task(
        description="Directly insterted",
        created_at=datetime.now(),
        schedule_for=datetime.now() + timedelta(days=1),
        status=TaskStatus.TODO
    )
    db_session.add(task)
    db_session.flush()
    task_in_db = repository.get(task.id)
    assert task_in_db is not None
    assert task_in_db.description == "Directly insterted"
    assert task_in_db.id == task.id

def test_get_not_found_task(repository):
    import uuid
    id = uuid.uuid4()
    fetched_task = repository.get(id)
    assert fetched_task is None

def test_get_all_tasks(repository, db_session):
    task1 = Task(
        description="first test task",
        created_at=datetime.now(),
        schedule_for=datetime.now() + timedelta(days=1),
        status=TaskStatus.TODO
    )
    task2 = Task(
        description="second test task",
        created_at=datetime.now(),
        schedule_for=datetime.now() + timedelta(days=1),
        status=TaskStatus.TODO
    )
    db_session.add(task1)
    db_session.add(task2)
    db_session.flush()

    tasks = repository.get_all()
    assert len(tasks) == 2

def test_delete_task(repository, db_session):
    task = Task(
        description="delete test task",
        created_at=datetime.now(),
        schedule_for=datetime.now() + timedelta(days=1),
        status=TaskStatus.TODO
    )
    db_session.add(task)
    db_session.flush()
    repository.delete(task)
    deleted_task = repository.get(task.id)
    assert deleted_task is None

def test_update_task(repository, db_session):
    task = Task(
        description="update test task",
        created_at=datetime.now(),
        schedule_for=datetime.now() + timedelta(days=1),
        status=TaskStatus.TODO
    )

    db_session.add(task)
    db_session.flush()
    task.status = TaskStatus.DONE
    repository.update()
    updated_task = db_session.get(Task, task.id)
    assert updated_task is not None
    assert updated_task.status == TaskStatus.DONE


