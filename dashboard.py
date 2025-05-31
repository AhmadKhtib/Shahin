import matplotlib.pyplot as plt
from sqlalchemy import func, create_engine
from sqlalchemy.orm import sessionmaker
from models import Client, Device, Transaction
import os
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib
matplotlib.use('Agg')

# Helper for proper Arabic rendering
def reshape(text):
    return get_display(arabic_reshaper.reshape(text))

# Setup DB
engine = create_engine("sqlite:///hub01.db")
Session = sessionmaker(bind=engine)
session = Session()

# Output directory
output_dir = "dashboard_charts"
os.makedirs(output_dir, exist_ok=True)

def generate_total_income_chart():
    results = session.query(
        func.strftime('%Y-%m-%d', Transaction.time).label("day"),
        func.sum(Transaction.amount).label("total")
    ).group_by("day").order_by("day").all()

    raw_dates = [r[0] for r in results]
    totals = [r[1] for r in results]

    # Optional: show fewer date labels
    if len(raw_dates) > 30:
        raw_dates = raw_dates[::7]
        totals = totals[::7]

    # Format to short dd/mm
    dates = [datetime.strptime(d, '%Y-%m-%d').strftime('%d/%m') for d in raw_dates]

    plt.figure(figsize=(10, 4))
    plt.bar(dates, totals, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.title(reshape("إجمالي المبالغ اليومية"))
    plt.xlabel(reshape("التاريخ"))
    plt.ylabel(reshape("المبلغ (₪)"))
    plt.tight_layout()
    filepath = os.path.join(output_dir, "total_income.png")
    plt.savefig(filepath)
    plt.close()
    return filepath

def generate_device_type_chart():
    results = session.query(
        Device.device_type, func.count(Device.device_type)
    ).group_by(Device.device_type).all()

    labels = [reshape(r[0]) for r in results]
    sizes = [r[1] for r in results]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title(reshape("توزيع أنواع الأجهزة"))
    filepath = os.path.join(output_dir, "device_types.png")
    plt.savefig(filepath)
    plt.close()
    return filepath

def generate_top_clients_chart():
    results = session.query(
        Client.name, func.sum(Transaction.amount)
    ).join(Transaction).group_by(Client.id).order_by(func.sum(Transaction.amount).desc()).limit(5).all()

    names = [reshape(r[0]) for r in results]
    totals = [r[1] for r in results]

    plt.figure(figsize=(8, 4))
    plt.barh(names, totals, color='green')
    plt.xlabel(reshape("إجمالي المبلغ (₪)"))
    plt.title(reshape("أفضل 5 زبائن حسب المبالغ"))
    plt.tight_layout()
    filepath = os.path.join(output_dir, "top_clients.png")
    plt.savefig(filepath)
    plt.close()
    return filepath

# Generate all charts
generate_total_income_chart()
generate_device_type_chart()
generate_top_clients_chart()

print("✅ Dashboard charts updated in folder: dashboard_charts")