import flet as ft
#from flet import c
from Additon import more_data
from models import session
from datetime import datetime


def main(page: ft.Page, container: ft.Column):
    
    page.vertical_alignment='center'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    app=more_data(session=session)
    client_name=ft.TextField(label="اسم الزبون",
                            value="" ,
                             text_align='center' ,
                             width=300, color='black',
                             label_style=ft.TextStyle(color="black"),
                             text_style=ft.TextStyle(color="black"))
    
    Amount=ft.TextField(label="المبلغ",
                                     value=0 ,
                                     text_align='center' ,
                                     width=300, color='black',
                                     label_style=ft.TextStyle(color="black"),
                                     text_style=ft.TextStyle(color="black"))

    number_of_devices=ft.TextField(label='عدد الاجهزة مع الزبون',
                                   value="0",
                                    text_align='center',
                                    width=300, color='black',
                                    label_style=ft.TextStyle(color="black"),
                                    text_style=ft.TextStyle(color="black"))
    note = ft.TextField(
                    label=f'اضافة ملاحظة',
                    value=None,
                    width=300,
                    text_align='center', color='black',
                    label_style=ft.TextStyle(color="black"),
                    text_style=ft.TextStyle(color="black")
                )

    # Container for dynamic device inputs
    devices_container = ft.Column([], alignment=ft.MainAxisAlignment.CENTER)
    
    def clear_content(e):
        note.value=''
        note.update()

        client_name.value=''
        client_name.update()

        number_of_devices.value=0
        number_of_devices.update()
        Amount.value=0
        Amount.update()
        
    def get_brand_options(device_type_value):
        if device_type_value == "جوال":
            return [
                ft.dropdown.Option("شاومي"),
                ft.dropdown.Option("سامسونج"),
                ft.dropdown.Option("ايفون"),
                ft.dropdown.Option("نوكيا"),
                ft.dropdown.Option("اوبو"),
                ft.dropdown.Option("هواوي"),
                ft.dropdown.Option("بوكو"),
            ]
        elif device_type_value == "لابتوب":
            return [
                ft.dropdown.Option("MSI"),
                ft.dropdown.Option("HP"),
                ft.dropdown.Option("ASUS"),
                ft.dropdown.Option("LENOVO"),
                ft.dropdown.Option("APPLE MAC"),
                ft.dropdown.Option("Acer"),
            ]
        elif device_type_value == "باوربانك":
            return [
                ft.dropdown.Option("5k"),
                ft.dropdown.Option("10k"),
                ft.dropdown.Option("15k"),
                ft.dropdown.Option("20k"),
                ft.dropdown.Option("30k"),
            ]
        elif device_type_value == "سماعة":
            return [
                ft.dropdown.Option("ايربود"),
                ft.dropdown.Option("سماعة صب"),
            ]
        elif device_type_value == "ايباد":
            return [
                ft.dropdown.Option("سامسونج"),
                ft.dropdown.Option("شاومي"),
                ft.dropdown.Option("هواوي"),
                ft.dropdown.Option("ايفون"),
            ]
        elif device_type_value == "بطارية":
            return [
                ft.dropdown.Option("200A"),
                ft.dropdown.Option("125A"),
                ft.dropdown.Option("100A"),
                ft.dropdown.Option("75A"),
                ft.dropdown.Option("55A"),
                ft.dropdown.Option("40A"),
                ft.dropdown.Option("26A"),
                ft.dropdown.Option("20A"),
                ft.dropdown.Option("16A"),
                ft.dropdown.Option("18A"),
                ft.dropdown.Option("9A"),
            ]
        elif device_type_value == "كشاف":
            return [
                ft.dropdown.Option("صغير"),
                ft.dropdown.Option("وسط"),
                ft.dropdown.Option("كبير"),
            ]
        else:
            return []

    # Store device inputs for saving data later
    device_inputs = {}

    def update_device_inputs(e):
        devices_container.controls.clear()  # Remove existing inputs
        device_inputs.clear()  # Clear stored inputs
        
        try:
            num_devices = int(number_of_devices.value)
            
            for i in range(num_devices):
                # Create new device_type dropdown for each device
                curr_device_type = ft.Dropdown(
                    label=f'نوع الجهاز {i+1}',
                    width=150,
                    options=[
                        ft.dropdown.Option("جوال"),
                        ft.dropdown.Option("لابتوب"),
                        ft.dropdown.Option("ايباد"),
                        ft.dropdown.Option("بطارية"),
                        ft.dropdown.Option("باوربانك"),
                        ft.dropdown.Option("سماعة"),
                        ft.dropdown.Option("كشاف"),
                    ],
                    label_style=ft.TextStyle(color='black'),
                    text_style=ft.TextStyle(color=ft.colors.SCRIM)
                )
                
                # Create new brand dropdown for each device
                curr_brand = ft.Dropdown(
                    label=f'اسم الشركة {i+1}',
                    width=150,
                    options=[],
                    label_style=ft.TextStyle(color='black'),
                    text_style=ft.TextStyle(color=ft.colors.SCRIM)
                )
                
                # Store the inputs for saving later
                device_inputs[i] = {
                    "device_type": curr_device_type,
                    "brand": curr_brand,
                    
                }
                
                # Connect the brand_options function to this specific device type dropdown
                def create_handler(brand_field):
                    def handler(e):
                        selected = e.control.value
                        brand_field.options = get_brand_options(selected)
                        brand_field.value = None
                        page.update()
                    return handler
                
                curr_device_type.on_change = create_handler(curr_brand)
                # Add the device inputs to the container
                devices_container.controls.append(ft.Row([curr_device_type,curr_brand], alignment='center'))
                # Add a divider between devices for better readability
                devices_container.controls.append(ft.Divider(height=1, thickness=0.1))
        
        except ValueError:
            number_of_devices.error_text = "يرجى إدخال رقم صحيح"
        
        page.update()

    def save_data(e):
        if not client_name.value:
            client_name.error_text = 'يرجى ادخال الاسم'
            page.update()
        else:
            # Save client info
            app.more_clients(
                client_name=client_name.value,
            )
            app.more_transaction(amount=Amount.value,NumberOfDevices=number_of_devices.value,time=datetime.now(),notes=note.value)
            
            # Save each device
            for i in device_inputs:
                device_data = device_inputs[i]
                app.more_devices(
                    device_type=device_data["device_type"].value,
                    brand=device_data["brand"].value,
                    
                )
            
            # Show success message 
            page.snack_bar = ft.SnackBar(
                content=ft.Text("تم حفظ البيانات بنجاح"),
                action="حسناً"
            )
            page.snack_bar.open = True
            page.update()

    # Add the page layout
    container.controls.append(
        ft.Column(
            [
                
                ft.Row([client_name], alignment='center'),
                ft.Row([number_of_devices], alignment='center'),
                ft.Row([Amount], alignment='center'),
                ft.Row([ft.ElevatedButton("مسح", on_click=clear_content)], alignment='center'),
                devices_container,
                ft.Row([note], alignment='center'),
                ft.Row([ft.ElevatedButton("حفظ", on_click=save_data)], alignment='center'),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            
        )
    )


    number_of_devices.on_blur = update_device_inputs
    number_of_devices.on_submit = update_device_inputs

    update_device_inputs(None)
