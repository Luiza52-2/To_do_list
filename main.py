import flet as ft
from db import main_db

def main(page: ft.Page):
    page.title = 'ToDo List'
    # page.padding = 40
    # page.bg_color = ft.colors.GREY_600
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_maximized = True

    task_list = ft.Column(spacing=10)

    task_input = ft.TextField(hint_text="Добавьте задачу", expand=True, dense=True)
    add_button = ft.ElevatedButton("Добавить", icon=ft.icons.ADD, icon_color=ft.colors.GREEN_400)
    clear_button = ft.ElevatedButton(
        "Очистить выполненные",
        icon=ft.icons.DELETE_SWEEP,
        icon_color=ft.colors.RED_300
    )

    sort_option = ft.Dropdown(
        label="Сортировка",
        options=[
            ft.dropdown.Option("created_at DESC", "📅 Новые сверху"),
            ft.dropdown.Option("created_at ASC", "📅 Старые сверху"),
            ft.dropdown.Option("is_done ASC", "✅ Невыполненные сверху"),
            ft.dropdown.Option("is_done DESC", "✅ Выполненные сверху")
        ],
        value="created_at DESC"
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
            load_tasks()

        def toggle_status(e):
            main_db.toggle_task_status(task_id, 1 if checkbox.value else 0)
            load_tasks()

        def delete_task(e):
            main_db.delete_task_db(task_id)
            load_tasks()

        checkbox = ft.Checkbox(value=bool(is_done), on_change=toggle_status)

        return ft.Row([
            checkbox,
            ft.Column([
                ft.Text(created_at, size=12, color=ft.colors.GREY_400),
                task_field
            ], expand=True),
            ft.IconButton(ft.icons.EDIT, icon_color=ft.colors.YELLOW_400, on_click=enable_edit),
            ft.IconButton(ft.icons.SAVE, icon_color=ft.colors.GREEN_400, on_click=save_edit),
            ft.IconButton(ft.icons.DELETE, icon_color=ft.colors.RED_400, on_click=delete_task)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def add_task(e):
        if task_input.value:
            main_db.add_task_db(task_input.value)
            task_input.value = ""
            load_tasks()

    def clear_completed_tasks(e):
        main_db.delete_completed_tasks()
        load_tasks()

    def sort_changed(e):
        load_tasks()

    
    add_button.on_click = add_task
    task_input.on_submit = add_task
    clear_button.on_click = clear_completed_tasks
    sort_option.on_change = sort_changed

    
    content = ft.Container(
        content=ft.Column([
            ft.Row([task_input, add_button, clear_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            sort_option,
            task_list
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        alignment=ft.alignment.center
    )

    background_image = ft.Image(
        src='/home/user/Desktop/to_do_list/pexels-lum3n-44775-399161.jpg',
        fit=ft.ImageFit.FILL,
        width=page.width,
        height=page.height
    )

    background = ft.Stack([background_image, content])

    def on_resize(e):
        background_image.width = page.width
        background_image.height = page.height
        background.update()

    page.add(background)
    page.on_resize = on_resize

    load_tasks()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)
