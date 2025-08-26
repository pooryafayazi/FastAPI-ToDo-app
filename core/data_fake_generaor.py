from core.db import SessionLocal
from sqlalchemy.orm import Session
from users.models import UserModel
from tasks.models import TaskModel
from faker import Faker

fake = Faker()


def seed_user(db):
    user = UserModel(username=fake.user_name())
    user.set_password("12345678")
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"✅ User created with Username: {user.username} and ID: {user.id}")
    return user


def seed_tasks(db, user, count: int = 10):
    tasks_list = []
    for _ in range(count):
        tasks_list.append(
            TaskModel(
                user_id=user.id,
                title=fake.sentence(nb_words=6),
                description=fake.text(),
                is_completed=fake.boolean(),
            )
        )

    db.add_all(tasks_list)
    db.commit()
    print(f"✅ Added {count} tasks for user id {user.id}")

   
""" 
def main():
    db = SessionLocal()
    try:
        user = seed_user(db)
        seed_tasks(db, user, count=10)
    finally:
        db.close()


if __name__ == "__main__":
    main()
"""


if __name__ == "__main__":
    db = SessionLocal()
    user = seed_user(db)
    seed_tasks(db, user, count=10)
    db.close()

# uv run python data_fake_generaor.py