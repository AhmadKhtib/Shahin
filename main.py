import flet as ft
from insertion import main as insertion_main
from SearchBar import main as search_bar_main
from Update_notes import main as update_main
from daily_transactions import main as daily_transactions_main
from dashboard_tab import main as dashboard_main

def main(page: ft.Page):
    
    page.title = 'نقطة شحن الخطيب'
    page.bgcolor = ft.colors.WHITE 
    
    # Columns for each tab
    insertion_column = ft.Column(
        [],
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
        )
    
    search_column = ft.Column(
        [],
        scroll=ft.ScrollMode.ALWAYS,
        expand=True, 
    )
    update_column = ft.Column(
        [],
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
        )

    daily_transactions_column = ft.Column(
        [],
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
        )
    dashboard_column = ft.Column(
        [], 
        scroll=ft.ScrollMode.ALWAYS,
        expand=True
        )

    
    t = ft.Tabs(
    
        animation_duration=300,
        label_color="black",  
        indicator_color="black",
        unselected_label_color='black',
        label_padding=10,

        tabs=[
            ft.Tab(text="الإدخال", content=ft.Container(insertion_column)),
            ft.Tab(text="البحث", content=ft.Container(search_column)),
            ft.Tab(text="تحديث المعاملات", content=update_column),
            ft.Tab(text="المعاملات اليومية", content=daily_transactions_column),
            ft.Tab(text="التحليلات", content=ft.Container(dashboard_column))
        ],
        expand=1,
)
    
    # Modules
    insertion_main(page, insertion_column)
    search_bar_main(page, search_column)
    update_main(page, update_column)
    daily_transactions_main(page, daily_transactions_column)
    dashboard_main(page, dashboard_column)

    page.add(t)
    
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")