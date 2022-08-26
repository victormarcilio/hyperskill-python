from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, Date
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta, datetime

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(VARCHAR)
    deadline = Column(Date)


def menu():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add a task")
    print("6) Delete a task")
    print("0) Exit")
    return input()

def print_tasks_with_deadlines(tasks):
    count = 1
    for task in tasks:
        day, month = task.deadline.strftime('%d %b').split()
        day = int(day)
        print(f"{count}. {task.task}. {day} {month}")
        count += 1

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

while True:
    choice = menu()
    if choice == '0':
        break
    if choice == '1':
        rows = session.query(Task).all()
        print("Today:")
        if len(rows):
            for row in rows:
                print(f"{row.id}. {row.task}")
        else:
            print("Nothing to do!")
    elif choice == '2':
        day = datetime.today()
        for _ in range(7):
            print(day.strftime('%A %d %b'))
            tasks = session.query(Task).filter(Task.deadline == day.date()).all()
            day = day + timedelta(days=1)
            count = 1
            for task in tasks:
                print(f"{count}. {task.task}")
                count += 1
            print()
    elif choice == '3':
        tasks = session.query(Task).order_by(Task.deadline).all()
        print("All tasks: ")
        print_tasks_with_deadlines(tasks)
    elif choice == '4':
        tasks = session.query(Task).filter(Task.deadline < datetime.today().date()).all()
        print("Missed tasks:")
        print_tasks_with_deadlines(tasks)
        if len(tasks) == 0:
            print('All tasks have been completed!')
        print()
    elif choice == '5':
        description = input('Enter a task')
        deadline = input('Enter a deadline').split('-')
        deadline = [int(i) for i in deadline]
        task_to_add = Task(task=description, deadline=date(*deadline))
        session.add(task_to_add)
        session.commit()
        print('The task has been added!')
    elif choice == '6':
        tasks = session.query(Task).order_by(Task.deadline).all()
        if not tasks:
            print("Nothing to delete")
            continue

        print('Choose the number of the task you want to delete:')
        print_tasks_with_deadlines(tasks)
        opt = int(input())
        session.delete(tasks[opt - 1])
        session.commit()
        print("The task has been deleted!\n")
print("Bye!")
