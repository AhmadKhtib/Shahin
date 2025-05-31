from faker import Faker
import random
from datetime import datetime, timedelta
from models import session, Client, Device, Transaction

faker = Faker("ar_EG")

# Arabic name lists
first_names = [
    "محمد", "أحمد", "سارة", "فاطمة", "ليلى", "مريم", "نور", "آدم", "هالة", "رنا",
    "نورا", "ياسمين", "مها", "إيمان", "جميلة", "أماني", "عبير", "جود", "ميساء",
    "أنس", "أمير", "رامي", "جهاد", "هيثم", "علاء", "أيمن", "زيد", "حسام", "وسيم"
]

male_names = [
    "محمد", "أحمد", "خالد", "علي", "يوسف", "حسن", "محمود", "سعيد", "عمر", "فؤاد",
    "إبراهيم", "عبدالله", "رامي", "باسل", "عماد"
]

arabic_notes = [
    "تم الدفع", "لم يتم الدفع", "في انتظار الدفع", "الدفع عند التسليم",
    "تم التسليم", "يرجى مراجعة الزبون", "تم الصيانة", "الدفع نقداً"
]

device_types = {
    "جوال": ["شاومي", "سامسونج", "ايفون", "نوكيا", "اوبو", "هواوي", "بوكو"],
    "لابتوب": ["MSI", "HP", "ASUS", "LENOVO", "APPLE MAC", "Acer"],
    "باوربانك": ["5k", "10k", "15k", "20k", "30k"],
    "سماعة": ["ايربود", "سماعة صب"],
    "ايباد": ["سامسونج", "شاومي", "هواوي", "ايفون"],
    "بطارية": ["200A", "125A", "100A", "75A", "55A", "40A", "26A", "20A", "16A", "18A", "9A"],
    "كشاف": ["صغير", "وسط", "كبير"],
}

def generate_fake_data(num_clients=300):
    clients, devices, transactions = [], [], []
    used_names = set()

    for _ in range(num_clients):
        # Create a unique Arabic full name
        while True:
            first = random.choice(first_names)
            father = random.choice(male_names)
            full_name = f"{first} {father}"
            if full_name not in used_names:
                used_names.add(full_name)
                break

        client = Client(name=full_name)
        clients.append(client)

        for _ in range(random.randint(1, 3)):
            device_type = random.choice(list(device_types.keys()))
            brand = random.choice(device_types[device_type])
            device = Device(device_type=device_type, brand=brand, client=client)
            devices.append(device)

            for _ in range(random.randint(1, 2)):
                # Optional notes
                note = random.choice(arabic_notes) if random.randint(1, 10) == 1 else None
                transaction = Transaction(
                    amount=round(random.uniform(5.0, 50.0), 2),
                    time=datetime.now() - timedelta(days=random.randint(0, 90)),
                    NumberOfDevices=1,
                    notes=note,
                    client=client
                )
                transactions.append(transaction)

    return clients, devices, transactions

def preview_data(clients, devices, transactions):
    print("📊 معاينة أول 5 زبائن:\n")
    for i, client in enumerate(clients[:5]):
        print(f"👤 العميل {i+1}: {client.name}")
        client_devices = [d for d in devices if d.client == client]
        for d in client_devices:
            print(f"    📱 الجهاز: {d.device_type} - {d.brand}")
        client_transactions = [t for t in transactions if t.client == client]
        for t in client_transactions:
            time_str = t.time.strftime('%Y-%m-%d - %H:%M')
            note_str = f" | الملاحظة: {t.notes}" if t.notes else ""
            print(f"    💰 المبلغ: {t.amount} ₪ في {time_str}{note_str}")
        print("-" * 40)

def insert_into_db(clients, devices, transactions):
    session.add_all(clients + devices + transactions)
    session.commit()
    print(f"\n✅ تم إدخال {len(clients)} زبون، {len(devices)} جهاز، {len(transactions)} معاملة إلى قاعدة البيانات.")

if __name__ == "__main__":
    clients, devices, transactions = generate_fake_data(num_clients=300)
    preview_data(clients, devices, transactions)

    confirm = input("\nهل ترغب في إضافة هذه البيانات إلى قاعدة البيانات؟ (y/n): ")
    if confirm.strip().lower() == "y":
        insert_into_db(clients, devices, transactions)
    else:
        print("❌ تم إلغاء العملية.")
