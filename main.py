import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import sqlite3
from PIL import Image

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Создание основного окна приложения
        self.title('Студенческий отдел кадров')
        self.geometry('1250x500')

        # Создание меню
        self.menu_bar = tk.Menu(self, background='#555', foreground='white')

        # Меню "Файл"
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Сохранить")
        file_menu.add_command(label="добавить запись")
        file_menu.add_command(label="удалить запись")
        file_menu.add_command(label="изменить запись")
        file_menu.add_command(label="Поиск")
        file_menu.add_command(label="Отмена")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)
        self.menu_bar.add_cascade(label="Файл", menu=file_menu)

        # Меню "Справочники"
        references_menu = tk.Menu(self.menu_bar, tearoff=0)
        references_menu.add_command(label="Пол", command=lambda: self.show_tabl("SELECT * FROM pol"))
        references_menu.add_command(label="Курс", command=lambda: self.show_tabl("SELECT * FROM kurs"))
        references_menu.add_command(label="Группа", command=lambda: self.show_tabl("SELECT * FROM gruop"))
        references_menu.add_command(label="Специальность", command=lambda: self.show_tabl("SELECT * FROM spec"))
        references_menu.add_command(label="Отделение", command=lambda: self.show_tabl("SELECT * FROM otdelenie"))
        references_menu.add_command(label="Вид финансирования", command=lambda: self.show_tabl("SELECT * FROM vid_finan"))
        self.menu_bar.add_cascade(label="Справочники", menu=references_menu)

        # Меню "Таблицы"
        tables_menu = tk.Menu(self.menu_bar, tearoff=0)
        tables_menu.add_command(label="Студенты", command=lambda: self.show_tabl("SELECT * FROM students"))
        tables_menu.add_command(label="Родители", command=lambda: self.show_tabl("SELECT * FROM parents"))
        self.menu_bar.add_cascade(label="Таблицы", menu=tables_menu)

        # Меню "Отчёты"
        reports_menu = tk.Menu(self.menu_bar, tearoff=0)
        reports_menu.add_command(label="Создать Отчёт")
        self.menu_bar.add_cascade(label="Отчёты", menu=reports_menu)

        # Меню "Сервис"
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Руководство пользователя")
        help_menu.add_command(label="О программе")
        self.menu_bar.add_cascade(label="Сервис", menu=help_menu)

        # Настройка цветов меню
        file_menu.configure(bg='#555', fg='white')
        references_menu.configure(bg='#555', fg='white')
        tables_menu.configure(bg='#555', fg='white')
        reports_menu.configure(bg='#555', fg='white')
        help_menu.configure(bg='#555', fg='white')

        # Установка меню в главное окно
        self.config(menu=self.menu_bar)

        # Создание фрейма для отображения таблицы и фона
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill='both', expand=True)

        # Загрузка фона
        bg = ctk.CTkImage(Image.open("res\\bg.png"), size=(3840, 2400))
        self.lbl = ctk.CTkLabel(self.table_frame, image=bg, text='Студенческий отдел кадров', font=("Calibri", 40))
        self.lbl.pack(anchor='center', expand=1)

    def show_tabl(self, sql_query):
        # Очистка фрейма перед отображением новых данных
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Подключение к базе данных SQLite
        conn = sqlite3.connect("res\\students_bd.db")
        cursor = conn.cursor()

        # Выполнение SQL-запроса
        cursor.execute(sql_query)

        # Получение заголовков таблицы и данных
        table_headers = [description[0] for description in cursor.description]
        table_data = cursor.fetchall()

        # Закрытие соединения с базой данных
        conn.close()

        # Создание виджета Treeview для отображения таблицы
        tree = ttk.Treeview(self.table_frame, columns=table_headers, show="headings")
        for header in table_headers:
            tree.heading(header, text=header)
            tree.column(header, width=100)  # Установите ширину столбца по своему усмотрению

        for row in table_data:
            tree.insert("", "end", values=row)

        tree.grid(row=0, column=0)

        # Создание кнопок и виджетов для поиска и редактирования данных
        btn_frame = ctk.CTkFrame(self.table_frame)
        btn_frame.grid(row=0, column=1)

        btn_width = 150
        pad = 5
        ctk.CTkButton(btn_frame, text="добавить запись", width=btn_width).pack(pady=pad)
        ctk.CTkButton(btn_frame, text="удалить запись", width=btn_width).pack(pady=pad)
        ctk.CTkButton(btn_frame, text="изменить запись", width=btn_width).pack(pady=pad)
        ctk.CTkButton(btn_frame, text="сохранить", width=btn_width).pack(pady=pad)
        ctk.CTkButton(btn_frame, text="отмена", width=btn_width).pack(pady=pad)

        search_frame = ctk.CTkFrame(self.table_frame)
        search_frame.grid(row=1, column=0)
        ctk.CTkEntry(search_frame, width=300).grid(row=0, column=0, padx=pad)
        ctk.CTkButton(search_frame, text="Поиск", width=20).grid(row=0, column=1, padx=pad)
        ctk.CTkButton(search_frame, text="настроить поиск").grid(row=0, column=2, padx=pad)

if __name__ == "__main__":
    MainApp().mainloop()
