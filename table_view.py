# ספרייה המשמשת לניתוח נתונים וסטטיסטיקה, וניתן לייצא דרכה לקבצי אקסל
import pandas as pd
from pymongo import MongoClient
from datetime import datetime, timedelta

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["xPressMeDB"]

# Get the current year
current_year = datetime.now().year


# Count statistics for each collection
# הפונקציה תפעל 5 פעמים (פעם אחת עבור כל אוסף) ותיצור סטטיסטיקה חודשית עבור כל אוסף
def count_statistics(collection_name):
    # יצירת רשימה של tuple
    statistics = []

    for month in range(1, 13):

        # טווח תאריכים שבהם נוצרו רשומות
        start_date = datetime(current_year, month, 1)
        end_date = start_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=32)

        # יצירת נתונים לכל tuple
        # count: כמה נוצרו בטווח התאריכים הנ"ל
        # month_name: באיזה חודש נוצרו
        count = db[collection_name].count_documents({"created_at": {"$gte": start_date, "$lt": end_date}})

        # המרה של מספר החודש לשם החודש
        month_name = start_date.strftime("%b")
        # הוספת הtuple לרשימת הסטטיסטיקות
        statistics.append((month_name, count))

    # לאחר בניית סטטיסטיקה לכל חודש - נחזיר את הרשימה שנוצרה
    return statistics


# Define the collection names
collection_names = ["image_file", "sound_file", "communication_board", "user", "case"]

# Export statistics for each collection to CSV
for collection_name in collection_names:
    # קריאה לפונקציה על מנת ליצור רשימת סטטיסטיקות חודשית עבור האוסף הנוכחי
    statistics = count_statistics(collection_name)
    # יצירת data frame עבור הרשימה, עם עמודות של "חודש" ו"כמות"
    df = pd.DataFrame(statistics, columns=["Month", "Count"])
    # יצירת שם עבור הקובץ אותו ניצור
    csv_file = f"{collection_name}_statistics.csv"
    # המרת הdata frame לקובץ (index=False) אומר שהשורות לא יהיו ממוספרות
    df.to_csv(csv_file, index=False)
    # הדפסת הודעה שהסטטיסטיקות יוצאו בהצלחה לקובץ שנוצר
    print(f"Statistics for {collection_name} exported to {csv_file}.")


