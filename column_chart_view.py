import pandas as pd
# ספרייה לתצוגה גרפית של נתונים (אחרי עיבוד באמצעות pandas)
import matplotlib.pyplot as plt
# ספרייה המשמשת לפעולות מתמטיות עבור רשימות גדולות (למשל פעולות של סטטיסטיקה)
import numpy as np
from pymongo import MongoClient
from datetime import datetime, timedelta

# Connect to MongoDB
def connect_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["xPressMeDB"]
    return db

# Get the current year
def get_current_year():
    return datetime.now().year

# Count statistics for each month
def count_statistics(db, year):
    # יצירת dictionary עבור כל אוסף
    statistics = {
        # קבלת טווח תאריכים בהתאם לdata frame שנוצר (ציר X)
        "Month": pd.date_range(start=f"{year}-01", periods=12, freq="M").strftime("%b"),
        # כל אחד מהבאים מיוצג ע"י עמודה
        "Custom Images": [],
        "Custom Sounds": [],
        "Custom Boards": [],
        "Registered Users": [],
        "Tickets": []
    }

    # הפעולה זהה לפעולה מהקובץ table_view רק שפה הוא רץ על כל תא בdictionary שנוצר במקום על אוסף אחד בלבד
    for month in range(1, 13):
        start_date = datetime(year, month, 1)
        end_date = start_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=32)

        statistics["Custom Images"].append(db.image_file.count_documents({"created_at": {"$gte": start_date, "$lt": end_date}}))
        statistics["Custom Sounds"].append(db.sound_file.count_documents({"created_at": {"$gte": start_date, "$lt": end_date}}))
        statistics["Custom Boards"].append(db.communication_board.count_documents({"created_at": {"$gte": start_date, "$lt": end_date}}))
        statistics["Registered Users"].append(db.user.count_documents({"created_at": {"$gte": start_date, "$lt": end_date}}))
        statistics["Tickets"].append(db.case.count_documents({"created_at": {"$gte": start_date, "$lt": end_date}}))

    # החזרת הdata frame שנוצר
    return pd.DataFrame(statistics)

# הצגת המידע בתצוגה גרפית צבעונית
def plot_statistics(df):
    # Set the width of each bar
    bar_width = 0.15

    # Set the positions of the x-axis ticks
    r = np.arange(len(df["Month"]))

    # Plot the statistics as grouped bars
    plt.figure(figsize=(10, 6))
    for i, column in enumerate(df.columns[1:]):
        plt.bar(r + bar_width*i, df[column], width=bar_width, edgecolor='white', label=column)

    # Add x-axis ticks and labels
    plt.xlabel("Month")
    plt.ylabel("Count")
    plt.title("Statistics Over 12 Months of the Current Year")
    plt.xticks(r + bar_width*2, df["Month"])
    plt.legend()

    # Show the chart
    plt.tight_layout()
    plt.show()

# Main function
def main():
    # התחברות לדאטאבייס
    db = connect_mongodb()
    # שמירת השנה הנוכחית
    year = get_current_year()
    # יצירת הdata frame של הסטטיסטיקות
    statistics_df = count_statistics(db, year)
    # הצגת הסטטיסטיקות בגרף
    plot_statistics(statistics_df)

# Run the script
if __name__ == "__main__":
    main()
