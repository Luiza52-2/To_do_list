import flet as ft
from db import main_db

def main(page: ft.Page):
    page.title = 'ToDo List'
    page.padding = 40
    page.bg_color = ft.colors.GREY_600
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)

    sort_option = ft.Dropdown(
        label="Сортировка",
        options=[
            ft.dropdown.Option("created_at DESC", "📅 Новые сверху"),
            ft.dropdown.Option("created_at ASC", "📅 Старые сверху"),
            ft.dropdown.Option("is_done ASC", "✅ Невыполненные сверху"),
            ft.dropdown.Option("is_done DESC", "✅ Выполненные сверху")
        ],
        value="created_at DESC",
        on_change=lambda e: load_tasks()
    )

    def load_tasks():
        task_list.controls.clear()
        tasks = main_db.get_tasks(sort_by=sort_option.value)
        for task_id, task_text, created_at, is_done in tasks:
            task_list.controls.append(create_task_row(task_id, task_text, created_at, is_done))
        page.update()

    def create_task_row(task_id, task_text, created_at, is_done):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)

        def enable_edit(e):
            task_field.read_only = False
            task_field.update()

        def save_edit(e):
            main_db.update_task_db(task_id, task_field.value)
            task_field.read_only = True
            page.update()

        def toggle_status(e):
            main_db.toggle_task_status(task_id, 1 if checkbox.value else 0)
            page.update()

        checkbox = ft.Checkbox(value=bool(is_done), on_change=toggle_status)

        return ft.Row([
            checkbox,
            ft.Column([
                ft.Text(created_at, size=12, color=ft.colors.GREY_300),
                task_field
            ], expand=True),
            ft.IconButton(ft.icons.EDIT, icon_color=ft.colors.YELLOW_400, on_click=enable_edit),
            ft.IconButton(ft.icons.SAVE, icon_color=ft.colors.GREEN_400, on_click=save_edit)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def add_task(e):
        if task_input.value:
            main_db.add_task_db(task_input.value)
            load_tasks()
            task_input.value = ""
            page.update()

    task_input = ft.TextField(hint_text="Добавьте задачу", expand=True, dense=True, on_submit=add_task)
    add_button = ft.ElevatedButton("Добавить", on_click=add_task, icon=ft.icons.ADD, icon_color=ft.colors.GREEN_400)

    page.add(
        ft.Column([
            ft.Row([task_input, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            sort_option,
            task_list
        ])
    )

    load_tasks()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)
