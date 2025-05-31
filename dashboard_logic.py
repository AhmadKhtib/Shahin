import matplotlib.pyplot as plt
from sqlalchemy import create_engine, func, and_
from sqlalchemy.orm import sessionmaker
from models import Client, Device, Transaction
import os
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib
import shutil
matplotlib.use('Agg')

def reshape(text):
    return get_display(arabic_reshaper.reshape(text))

# Setup SQLite connection
engine = create_engine("sqlite:///hub01.db")
Session = sessionmaker(bind=engine)
session = Session()

# Chart output directory
output_dir = "dashboard_charts"
os.makedirs(output_dir, exist_ok=True)

def generate_total_income_chart(start_date, end_date, device_type):
    query = session.query(
        func.strftime('%Y-%m-%d', Transaction.time).label("day"),
        func.sum(Transaction.amount).label("total")
    ).join(Client)

    # ✅ Fix: Device filtering using subquery for client IDs
    if device_type != "الكل":
        subquery = session.query(Device.client_id).filter(Device.device_type == device_type).subquery()
        query = query.filter(Client.id.in_(subquery.select()))

    # ✅ Add optional date filters
    filters = []
    if start_date:
        filters.append(Transaction.time >= start_date)
    if end_date:
        filters.append(Transaction.time <= end_date)

    if filters:
        query = query.filter(and_(*filters))

    query = query.group_by("day").order_by("day")
    results = query.all()

    if not results:
        return None

    # Format and reduce data for chart readability
    dates = [datetime.strptime(r[0], '%Y-%m-%d').strftime('%d/%m') for r in results]
    totals = [r[1] for r in results]

    if len(dates) > 30:
        dates = dates[::7]
        totals = totals[::7]

    # Plot with Arabic labels
    plt.figure(figsize=(10, 4))
    plt.bar(dates, totals, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.title(reshape("إجمالي المبالغ حسب الفلترة"))
    plt.xlabel(reshape("التاريخ"))
    plt.ylabel(reshape("المبلغ (₪)"))
    plt.tight_layout()
    filepath = os.path.join(output_dir, "total_income.png")
    plt.savefig(filepath)
    plt.close()
    print(f"Filter — Device: {device_type}, Start: {start_date}, End: {end_date}")
    print(f"✅ Chart saved at: {filepath}")
    # Final path where matplotlib saves image
    plt.savefig(filepath)
    plt.close()

    # ✅ Copy to assets folder for Flet to load
    output_path = "assets/total_income.png"
    shutil.copy(filepath, output_path)

    return output_path