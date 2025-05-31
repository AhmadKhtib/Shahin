import flet as ft
import os
import pathlib
from datetime import datetime
from dashboard_logic import generate_total_income_chart

DEVICE_TYPES = [
    "الكل", "جوال", "لابتوب", "ايباد", "باوربانك", "سماعة", "بطارية", "كشاف"
]

def main(page: ft.Page, container: ft.Column):
    chart_dir = "dashboard_charts"
    chart_path = os.path.join(chart_dir, "total_income.png")

    # Title
    title = ft.Text("📊 لوحة التحكم التفاعلية", size=24, weight="bold", text_align="center", color=ft.colors.BLACK)

    # Date input fields
    start_date_picker = ft.TextField(label="من تاريخ (YYYY-MM-DD)")
    end_date_picker = ft.TextField(label="إلى تاريخ (YYYY-MM-DD)")

    start_date_section = ft.Column([
        ft.Text("من تاريخ", size=14, weight="bold"),
        start_date_picker
    ])

    end_date_section = ft.Column([
        ft.Text("إلى تاريخ", size=14, weight="bold"),
        end_date_picker
    ])

    # Device type filter
    device_dropdown = ft.Dropdown(
        label="نوع الجهاز",
        options=[ft.dropdown.Option(value) for value in DEVICE_TYPES],
        value="الكل",
        width=200,
        text_align=ft.TextAlign.CENTER,
    )

    # Chart image display (persistent object)
    chart_display = ft.Image(
        src=chart_path if os.path.exists(chart_path) else "",
        width=600,
        fit=ft.ImageFit.CONTAIN
    )

    # Status message
    status_text = ft.Text("", color=ft.colors.GREEN_900)

    def refresh_dashboard(e):
        start_date = None
        end_date = None

        if start_date_picker.value:
            try:
                start_date = datetime.strptime(start_date_picker.value, "%Y-%m-%d")
            except ValueError:
                status_text.value = "⚠️ تنسيق تاريخ البداية غير صالح"
                page.update()
                return

        if end_date_picker.value:
            try:
                end_date = datetime.strptime(end_date_picker.value, "%Y-%m-%d")
            except ValueError:
                status_text.value = "⚠️ تنسيق تاريخ النهاية غير صالح"
                page.update()
                return

        device_type = device_dropdown.value
        path = generate_total_income_chart(start_date, end_date, device_type)

        try:
            if path and os.path.exists(path):
                normalized_path = pathlib.Path(path).as_posix()
                chart_display.src = f"{normalized_path}?v={datetime.now().timestamp()}"
                chart_display.update()  # <- Crucial!
                status_text.value = f"✅ تم التحديث بنجاح ({device_type})"
            else:
                chart_display.src = ""
                chart_display.update()
                status_text.value = "⚠️ لا توجد بيانات مطابقة للفلترة المحددة"
        except Exception as ex:
            chart_display.src = ""
            chart_display.update()
            status_text.value = f"❌ خطأ أثناء التحديث: {ex}"

        page.update()


    # Layout setup
    container.controls.clear()
    container.controls.append(title)
    container.controls.append(
        ft.Row(
            [start_date_section, end_date_section, device_dropdown,
             ft.ElevatedButton("🔄 تحديث الرسم", on_click=refresh_dashboard)],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15
        )
    )
    container.controls.append(ft.Row([chart_display], alignment=ft.MainAxisAlignment.CENTER))
    container.controls.append(ft.Row([status_text], alignment=ft.MainAxisAlignment.CENTER))
    page.update()