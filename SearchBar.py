import flet as ft
from models import session, Client, Transaction, Device


def main(page: ft.Page, container: ft.Column):
    def on_search(e):
        query = search_box.value        
        results = session.query(Client).filter(Client.name.ilike(f'%{query}%')).all()
        result_list.controls.clear()
        
        for client in results:

            result_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        f" الاسم:\n {client.name}",
                        color="Black",
                        
                        text_align=ft.TextAlign.CENTER
                    ),
                    alignment=ft.alignment.center,  # Center alignment
                    rtl=True,
                    width=300,  # Adjusted width for better layout
                    height=50,  # Fixed height
                    bgcolor=ft.Colors.ORANGE,  # Background color
                    border_radius=ft.border_radius.all(15)  # Rounded corners
                    
                    
                )
            )

            # Get all devices linked to this client
            devices = session.query(Device).filter(Device.client_id == client.id).all()
            transactions = session.query(Transaction).filter(Transaction.client_id == client.id).all()
            if transactions:
                for transaction in transactions:
                    result_list.controls.append(
                        ft.Container(
                            content=ft.Text(f"عدد الاجهزة:\n {transaction.NumberOfDevices}",
                                             color="Black",
                                             text_align=ft.TextAlign.CENTER
                                     ),
                            alignment=ft.alignment.center,  # Center alignment
                            rtl=True,
                            width=300,
                            height=40, 
                            
                            )
                            )
                    result_list.controls.append(ft.Container(
                        content=ft.Text(f"المبلغ:\n {transaction.amount}",
                                         color=ft.colors.BLACK87,
                                         text_align=ft.TextAlign.CENTER),
                        alignment=ft.alignment.center,  # Center alignment
                        rtl=True,
                        width=300,  # Adjusted width for better layout
                        )
                        )
                   
                    result_list.controls.append(ft.Container(
                        content=ft.Text(f"رقم المعاملة:\n {transaction.id}",
                                        color=ft.colors.BLACK,
                                        text_align=ft.TextAlign.CENTER),
                        alignment=ft.alignment.center,  # Center alignment
                        rtl=True,
                        width=300,  # Adjusted width for better layout
                        
                        )
                        )
                    if transaction.notes:
                        result_list.controls.append(ft.Container(
                            content=ft.Text(f"ملاحظات :\n {transaction.notes} \nرقم الملاحظة :\n{transaction.id}",
                                            color=ft.colors.BLACK26,
                                            text_align=ft.TextAlign.CENTER),
                            alignment=ft.alignment.center,  # Center alignment
                            rtl=True,
                            bgcolor=ft.colors.GREY,
                            width=300,  
                            
                            )   
                            )
                        
                    else:
                        result_list.controls.append(
                            ft.Container(
                                content=ft.Text(f"ملاحظات \n: لا توجد ملاحظات",
                                                color=ft.colors.BLACK,
                                                text_align=ft.TextAlign.CENTER),
                                alignment=ft.alignment.center,  
                                
                                rtl=True,
                                width=300,  

                            )
                         )
                        
                    result_list.controls.append(ft.Container(
                        content=ft.Text(f"  تاريخ التسليم:\n {transaction.time}",
                                        color="Black",
                                        text_align=ft.TextAlign.CENTER),
                        alignment=ft.alignment.center,  # Center alignment
                        rtl=True,
                        width=300,

                    )
                        )
                    
            if devices:
                result_list.controls.append(ft.Container(
                    content=ft.Text("الاجهزة:",color="Black",
                                    text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,  
                    rtl=True,
                    width=300,  
                      
                )
                    )
                for device in devices:
                    
                    result_list.controls.append(ft.Container(
                        content=ft.Text(f"  نوع الجهاز :👈 {device.device_type}\n الماركة:👈 {device.brand}",
                                        color="Black",
                                        text_align=ft.TextAlign.CENTER),
                        alignment=ft.alignment.center,  
                        rtl=True,
                        width=300,  
                    )
                        )
            else:
                result_list.controls.append(
                    ft.Container(
                        content=ft.Text(
                            f"لا يوجد اجهزة ل\n{client.name}",
                            color=ft.colors.RED_100,
                            text_align=ft.TextAlign.CENTER
                        ),
                        alignment=ft.alignment.center,  
                        rtl=True,
                        width=300,
                        height=50,
                        border_radius=ft.border_radius.all(5)  
                    )
                )

        page.update()

    page.horizontal_alignment = ft.TextAlign.CENTER
    page.vertical_alignment = "RIGHT"
    
    page.padding = 20
    

    search_box = ft.TextField(label="ابحث عن الاسم", on_change=on_search ,color='black',label_style=ft.TextStyle(color='black'),text_align=ft.TextAlign.CENTER)
    result_list = ft.Column()
    
    

    container.controls.append(
        ft.Container(ft.Column(
            [
                ft.Container(  
                    content=search_box,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.WHITE,
                    padding=10,
                    rtl=True,
                    expand=True,
                    
                ),
                ft.Container(  
                    content=result_list,
                    alignment=ft.alignment.center,
                    expand=True,
                    #bgcolor=ft.Colors.WHITE,  # Optional: Background color for better visibility
                    padding=10,
                    rtl=True,
                ),
                
            ],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True
        ),
        
    )
    )
