import flet as ft
from models import session, Transaction, Client ,Device

def main(page: ft.Page, container: ft.Column):
    page.vertical_alignment = "center"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def update_transaction(e):
        try:
            note_number = int(note_number_input.value)
            transaction_to_update = session.query(Transaction).filter(Transaction.id == note_number).first()

            if transaction_to_update:
                # Fetch the client name
                client = session.query(Client).filter(Client.id == transaction_to_update.client_id).first()
                if client:
                    client_name.value = f"اسم الزبون: {client.name}"
                    NumberOfDevices.value = f"عدد الاجهزة: {transaction_to_update.NumberOfDevices}"
                    # Fetch the devices linked to this client
                    ClientDevices = session.query(Device.device_type).filter(Device.client_id == client.id).all()
                    # Convert the list of devices to a string
                    devices.value = ', '.join([device.device_type for device in ClientDevices])

                else:
                    client_name.value = "اسم الزبون: غير موجود"

                # Update the current transaction details
                current_notes.value = f"المعاملة الحالية: {transaction_to_update.notes}"
                current_amount.value = f"المبلغ المدفوع: {transaction_to_update.amount}"

                # Update the UI
                client_name.update()
                current_notes.update()
                current_amount.update()

                def save_changes(e):
                    try:
                        new_note = new_note_input.value
                        new_amount = float(new_amount_input.value)
                        transaction_to_update.amount = new_amount
                        transaction_to_update.notes = new_note
                        session.commit()
                        result_message.value = "تم التحديث بنجاح."
                        result_message.color = ft.colors.WHITE

                        # Clear the input fields
                        new_note_input.value = ""
                        new_amount_input.value = 0
                        note_number_input.value = ""
                        client_name.value = ""
                        NumberOfDevices.value = ""
                        devices.value = ""
                        current_notes.value = ""
                        current_amount.value = ""

                        # Show the clear button after saving
                        clear_button.visible = True

                        # Update the UI
                        new_note_input.update()
                        new_amount_input.update()
                        note_number_input.update()
                        client_name.update()
                        NumberOfDevices.update()
                        devices.update()
                        current_notes.update()
                        current_amount.update()
                        save_button.update()
                        clear_button.update()
                    except Exception as ex:
                        result_message.value = f"خطأ أثناء التحديث: {ex}"
                        result_message.color = ft.colors.RED
                    result_message.update()

                save_button.on_click = save_changes
                new_note_input.visible = True
                new_amount_input.visible = True
                save_button.visible = True
                clear_button.visible = True
                page.update()
            else:
                result_message.value = f"لم يتم العثور على المعاملة بالرقم {note_number}."
                result_message.color = ft.colors.RED
                result_message.update()
        except ValueError:
            result_message.value = "الرجاء إدخال رقم صحيح."
            result_message.color = ft.colors.RED
            result_message.update()

    def clear_fields(e):
        # Clear all fields
        new_note_input.value = ""
        new_amount_input.value = ""
        note_number_input.value = ""
        client_name.value = ""
        current_notes.value = ""
        NumberOfDevices.value = ""
        devices.value = ""
        current_amount.value = ""
        new_note_input.visible = False
        new_amount_input.visible = False

        save_button.visible = False
        clear_button.visible = False
        page.update()

    def show_all_clients_with_notes(e):
        # Query all transactions with notes
        transactions_with_notes = session.query(Transaction).filter(Transaction.notes.isnot(None), Transaction.notes != "").all()
        clients_list.controls.clear()

        if transactions_with_notes:
            for transaction in transactions_with_notes:
                client = session.query(Client).filter(Client.id == transaction.client_id).first()
                if client:
                    clients_list.controls.append(ft.Text(f"رقم المعاملة: {transaction.id}", color='black'))
                    clients_list.controls.append(ft.Text(f"اسم العميل: {client.name}", color='black'))
                    clients_list.controls.append(ft.Text(f"المبلغ: {transaction.amount}", color='black'))
                    clients_list.controls.append(ft.Text(f"الملاحظة: {transaction.notes}", color='black'))
                    clients_list.controls.append(ft.Text("----------------------------", color='black'))
        else:
            clients_list.controls.append(ft.Text("لا توجد ملاحظات لأي عميل.", color='black'))

        clients_list.update()

    # UI Components
    note_number_input = ft.TextField(label="رقم الملاحظة", width=300, label_style=ft.TextStyle(color='black'),color='black')
    fetch_button = ft.ElevatedButton("بحث", on_click=update_transaction)
    client_name = ft.Text(color='black')  # Display the client name
    NumberOfDevices = ft.Text(color='black')
    devices = ft.Text(color='black')  
    current_notes = ft.Text(color='black')
    current_amount = ft.Text(color='black')
    new_note_input = ft.TextField(label="الملاحظة الجديدة", visible=False, width=300,label_style=ft.TextStyle(color="black"),
        text_style=ft.TextStyle(color="black"))
    new_amount_input = ft.TextField(label="المبلغ الجديد", value=0, visible=False, width=300,label_style=ft.TextStyle(color="black"),
        text_style=ft.TextStyle(color="black"))
    save_button = ft.ElevatedButton("حفظ التغييرات", visible=False)
    clear_button = ft.ElevatedButton("عرض اقل", visible=False, on_click=clear_fields)  # Initially hidden
    result_message = ft.Text(color='black')
    show_all_button = ft.ElevatedButton("عرض جميع العملاء الذين لديهم ملاحظات", on_click=show_all_clients_with_notes)
    clients_list = ft.Column()

    # Add components to the container
    container.controls.append(
        ft.Column(
            [
                note_number_input,
                fetch_button,
                client_name,
                NumberOfDevices,
                devices,
                current_notes,
                current_amount,
                new_note_input,
                new_amount_input,
                save_button,
                clear_button,  # Add the clear button here
                result_message,
                show_all_button,
                ft.Row(
                    [clients_list],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    
                ),
                
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
        )
    )