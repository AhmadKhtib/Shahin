import flet as ft
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from models import Transaction, Client, session

def main(page: ft.Page,container: ft.Column):
    
    

    # Dropdowns for day, month, and year
    day_input = ft.Dropdown(
        label="اليوم",
        options=[ft.dropdown.Option(str(i)) for i in range(1, 32)],  # Days 1-31
        width=100,
        label_style=ft.TextStyle(color="black"),
        text_style=ft.TextStyle(color="black"),
    )
    month_input = ft.Dropdown(
        label="الشهر",
        options=[ft.dropdown.Option(str(i)) for i in range(1, 13)],  # Months 1-12
        width=100,
        label_style=ft.TextStyle(color="black"),
        text_style=ft.TextStyle(color="black"),
    )
    year_input = ft.Dropdown(
        label="السنة",
        options=[ft.dropdown.Option(str(i)) for i in range(2025, 2030)],  # Years 2000-2030
        width=100,
        label_style=ft.TextStyle(color="black"),
        text_style=ft.TextStyle(color="black"),
    )

    # Result display
    result_text = ft.Text(value="", selectable=True, color=ft.colors.BLACK, text_align="center", size=20)
    result_text.width = 300  # Set width for the result text

    def search_transactions(e):
        try:
            # Get user input
            search_day = int(day_input.value)
            search_month = int(month_input.value)
            search_year = int(year_input.value)

            # Validate the inputs
            if not (1 <= search_day <= 31 and 1 <= search_month <= 12 and search_year > 0):
                raise ValueError("تأكد من إدخال يوم وشهر وسنة صحيحة.")

            # Format the date as day_month_year
            search_date = f"{search_year:04d}-{search_month:02d}-{search_day:02d}"

            # Query to group by date and include client information
            try:
                daily_totals_with_clients = session.query(
                    func.date(Transaction.time).label('day'),  # Extract only the date part
                    func.sum(Transaction.amount).label('total_amount'),
                    func.group_concat(Client.name, ', ').label('clients')
                ).join(Client, Transaction.client_id == Client.id)\
                 .filter(func.date(Transaction.time) == search_date)\
                 .group_by('day').all()

                # Check if results are found
                if daily_totals_with_clients:
                    # Display the results
                    result = ""
                    for day, total_amount, clients in daily_totals_with_clients:
                        result += f"التاريخ:\n {day}\n"
                        result += f"إجمالي المبلغ:\n {total_amount}\n"
                        result += f"العملاء:\n {clients}\n\n"
                    result_text.value = result
                else:
                    result_text.value = "لا توجد معاملات في هذا التاريخ."

            except SQLAlchemyError as e:
                result_text.value = f"حدث خطأ أثناء الاستعلام عن البيانات: {e}"

        except ValueError as ve:
            result_text.value = f"خطأ في الإدخال: {ve}"
        except Exception as ex:
            result_text.value = f"حدث خطأ غير متوقع: {ex}"

        page.update()

    # Search button
    search_button = ft.ElevatedButton(text="بحث", on_click=search_transactions)

    # Layout
    container.controls.append(
        (ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("البحث عن المعاملات اليومية", style="headlineMedium", color="Black", text_align="center"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Center the text horizontally
                ),
                ft.Row(
                    [day_input, month_input, year_input],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                ft.Row(
                    [search_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                ft.Row(
                    [result_text],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    ))
