import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import sqlite3
from PIL import Image

POL_HEADERS = ["ID", "Наименование"]
KURS_HEADERS = ["ID", "Наименование"]
GRUOP_HEADERS = ["ID", "Наименование"]
SPEC_HEADERS = ["ID", "Наименование"]
OTDELENIE_HEADERS = ["ID", "Наименование"]
VID_FINAIN_HEADERS = ["ID", "Наименование"]

STUDENTS_HEADERS = ["ID", "ФИО студента", "Дата рождения", "№ телефона", 
                    "Год поступления", "Год окончания", "№ студенчиского билета",
                    "Kypc", "Группа", "Отделение", "Пол", "Вид финансирования", "Специальность"]
PARENTS_HEADERS = ["ID", "ФИО родителя", "№ телефона", "ФИО студента"]

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Студенческий отдел кадров')
        self.geometry('865x450')
        self.resizable(width=False, height=False)

        # Создание фрейма для отображения таблицы
        self.table_frame = ctk.CTkFrame(self, width=700, height=400)
        self.table_frame.grid(row=0, column=0, padx=5, pady=5)

        # Загрузка фона
        bg = ctk.CTkImage(Image.open("res\\images\\bg.png"), size=(700, 400))
        lbl = ctk.CTkLabel(self.table_frame, image=bg, text='Таблица не открыта', font=("Calibri", 40))
        lbl.place(relwidth=1, relheight=1)

        # Создание меню
        self.menu_bar = tk.Menu(self, background='#555', foreground='white')

        # Меню "Файл"
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Выход", command=self.quit)
        self.menu_bar.add_cascade(label="Файл", menu=file_menu)

        # Меню "Справочники"
        references_menu = tk.Menu(self.menu_bar, tearoff=0)
        references_menu.add_command(label="Пол", 
                                    command=lambda: self.show_table("SELECT * FROM pol", POL_HEADERS))
        references_menu.add_command(label="Kypc", 
                                    command=lambda: self.show_table("SELECT * FROM kurs", KURS_HEADERS))
        references_menu.add_command(label="Группа", 
                                    command=lambda: self.show_table("SELECT * FROM gruop", GRUOP_HEADERS))
        references_menu.add_command(label="Специальность", 
                                    command=lambda: self.show_table("SELECT * FROM spec", SPEC_HEADERS))
        references_menu.add_command(label="Отделение", 
                                    command=lambda: self.show_table("SELECT * FROM otdelenie", OTDELENIE_HEADERS))
        references_menu.add_command(label="Вид финансирования", 
                                    command=lambda: self.show_table("SELECT * FROM vid_finan", VID_FINAIN_HEADERS))
        self.menu_bar.add_cascade(label="Справочники", menu=references_menu)

        # Меню "Таблицы"
        tables_menu = tk.Menu(self.menu_bar, tearoff=0)
        tables_menu.add_command(label="Студенты", command=lambda: self.show_table('''
                    SELECT students.id_student, students.FIO, students.date_dr, students.phone_nomber, students.n_bilet,
                        students.y_post, students.y_okon, kurs.N_kurs, gruop.name_gruop, otdelenie.name_otdelenie, pol.name_pol,
                        vid_finan.name_finan, spec.name_spec
                    FROM students
                    JOIN kurs ON students.id_kurs = kurs.id_kurs
                    JOIN gruop ON students.id_gruop = gruop.id_gruop
                    JOIN otdelenie ON students.id_otdelenie = otdelenie.id_otdelenie
                    JOIN pol ON students.id_pol = pol.id_pol
                    JOIN vid_finan ON students.id_finan = vid_finan.id_finan
                    JOIN spec ON students.id_spec = spec.id_spec
        ''', STUDENTS_HEADERS))
        tables_menu.add_command(label="Родители", command=lambda: self.show_table('''
                    SELECT parents.id_parent, parents.FIO, parents.phone_nomber, students.FIO FROM parents
                    JOIN students ON parents.id_student = students.id_student
        ''', PARENTS_HEADERS))
        self.menu_bar.add_cascade(label="Таблицы", menu=tables_menu)

        # Меню "Отчёты"
        reports_menu = tk.Menu(self.menu_bar, tearoff=0)
        reports_menu.add_command(label="Создать Отчёт")
        self.menu_bar.add_cascade(label="Отчёты", menu=reports_menu)

        # Меню "Сервис"
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Руководство пользователя")
        help_menu.add_command(label="O программе")
        self.menu_bar.add_cascade(label="Сервис", menu=help_menu)

        # Настройка цветов меню
        file_menu.configure(bg='#555', fg='white')
        references_menu.configure(bg='#555', fg='white')
        tables_menu.configure(bg='#555', fg='white')
        reports_menu.configure(bg='#555', fg='white')
        help_menu.configure(bg='#555', fg='white')

        # Установка меню в главное окно
        self.config(menu=self.menu_bar)

        btn_width = 150
        pad = 5

        # Создание кнопок и виджетов для поиска и редактирования данных
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=0, column=1)
        ctk.CTkButton(btn_frame, text="добавить", width=btn_width, command=self.add).pack(pady=pad)
        ctk.CTkButton(btn_frame, text="удалить", width=btn_width, command=self.delete).pack(pady=pad)
        ctk.CTkButton(btn_frame, text="изменить", width=btn_width, command=self.change).pack(pady=pad)

        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=1, column=0)
        self.search_entry = ctk.CTkEntry(search_frame, width=300)
        self.search_entry.grid(row=0, column=0, padx=pad)
        ctk.CTkButton(search_frame, text="Поиск", width=20).grid(row=0, column=1, padx=pad)
        ctk.CTkButton(search_frame, text="настроить поиск").grid(row=0, column=2, padx=pad)
    
    def add(self):
        pass

    def delete(self):
        pass

    def change(self):
        pass
    
    def show_table(self, sql_query, headers = None):
        # Очистка фрейма перед отображением новых данных
        for widget in self.table_frame.winfo_children(): widget.destroy()

        # Подключение к базе данных SQLite
        conn = sqlite3.connect("res\\students_bd.db")
        cursor = conn.cursor()

        # Выполнение SQL-запроса
        cursor.execute(sql_query)

        # Получение заголовков таблицы и данных
        if headers == None: # если заголовки не были переданы используем те что в БД
            table_headers = [description[0] for description in cursor.description]
        else: # иначе используем те что передали
            table_headers = headers
        table_data = cursor.fetchall()

        # Закрытие соединения с базой данных
        conn.close()
            
        canvas = ctk.CTkCanvas(self.table_frame, width=865, height=480)
        canvas.pack(fill="both", expand=True)

        x_scrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal", command=canvas.xview)
        x_scrollbar.pack(side="bottom", fill="x")

        canvas.configure(xscrollcommand=x_scrollbar.set)

        table = ttk.Treeview(self.table_frame, columns=table_headers, show="headings")
        for header in table_headers: table.heading(header, text=header)
        for row in table_data: table.insert("", "end", values=row)

        canvas.create_window((0, 0), window=table, anchor="nw")

        table.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

if __name__ == "__main__":
    MainApp().mainloop()