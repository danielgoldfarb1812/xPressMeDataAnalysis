#על מנת ליצור תאריכים רנדומלים
import random
import string
#ספריה שמתחברת למונגודיבי
from pymongo import MongoClient
from datetime import datetime, timedelta

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["xPressMeDB"]

# 5 לולאות פור שמכניסות מידע אקראי לכל אוסף בדאטאבייס, עם תאריך יצירה רנדומלי
# הפעולה choice מחזירה רשימה של תווים אקראיים באורך 8 מהמחלקה string
# Generate random data for custom images
for _ in range(20):
    created_at = datetime(2023, random.randint(1, 12), random.randint(1, 28))
    image_data = {
        "name": ''.join(random.choices(string.ascii_letters, k=8)),
        "file_path": '/path/to/image/file',
        "size": random.randint(100, 500),
        "created_at": created_at
    }
    db.image_file.insert_one(image_data)

# Generate random data for custom sounds
for _ in range(20):
    created_at = datetime(2023, random.randint(1, 12), random.randint(1, 28))
    sound_data = {
        "name": ''.join(random.choices(string.ascii_letters, k=8)),
        "file_path": '/path/to/sound/file',
        "duration": random.randint(1, 10),
        "created_at": created_at
    }
    db.sound_file.insert_one(sound_data)

# Generate random data for custom boards
for _ in range(20):
    created_at = datetime(2023, random.randint(1, 12), random.randint(1, 28))
    buttons = []
    for _ in range(random.randint(4, 8)):
        button_data = {
            "text": ''.join(random.choices(string.ascii_letters, k=5)),
            "sound_id": random.randint(1, 20),
            "image_id": random.randint(1, 20)
        }
        buttons.append(button_data)

    board_data = {
        "name": ''.join(random.choices(string.ascii_letters, k=8)),
        "buttons": buttons,
        "created_at": created_at
    }
    db.communication_board.insert_one(board_data)

# Generate random data for users
for _ in range(20):
    created_at = datetime(2023, random.randint(1, 12), random.randint(1, 28))
    user_data = {
        "name": ''.join(random.choices(string.ascii_letters, k=8)),
        "email": ''.join(random.choices(string.ascii_letters, k=8)) + "@example.com",
        "password": ''.join(random.choices(string.ascii_letters + string.digits, k=8)),
        "created_at": created_at
    }
    db.user.insert_one(user_data)

# Generate random data for cases
for _ in range(20):
    created_at = datetime(2023, random.randint(1, 12), random.randint(1, 28))
    case_data = {
        "user_id": random.randint(1, 20),
        "subject": ''.join(random.choices(string.ascii_letters, k=10)),
        "message": ''.join(random.choices(string.ascii_letters + string.digits, k=20)),
        "status": random.choice(["open", "closed"]),
        "created_at": created_at
    }
    db.case.insert_one(case_data)
