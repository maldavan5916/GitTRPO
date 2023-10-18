import sqlite3, xlsxwriter, sys, os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
from DB import DB
import pandas as pd
from tkinter.messagebox import showerror, showinfo

POL_HEADERS = ["№", "Наименование пола"]
KURS_HEADERS = ["№", "Наименование курса"]
GRUOP_HEADERS = ["№", "Наименование группы"]
SPEC_HEADERS = ["№", "Наименование специальности"]
OTDELENIE_HEADERS = ["№", "Наименование отделения"]
VID_FINAN_HEADERS = ["№", "Наименование финансирования"]

STUDENTS_HEADERS = ["№", "Фамилия Имя Отчество студента", "Дата рождения", "номер телефона", 
                    "№ студенчиского билета", "Год поступления", "Год окончания",
                    "наименование кypca", "Группа", "Наименование отделение", "Наименование пола", "Вид финансирования", "Специальность"]
PARENTS_HEADERS = ["№", "Фамилия Имя Отчество родителя", "Номер телефона", "Фамилия Имя Отчество студента"]

class WindowMain(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Студенческий отдел кадров')
        self.wm_iconbitmap()
        self.iconphoto(True, tk.PhotoImage(file="res\\images\\icon.png"))
        self.last_headers = None

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
        references_menu.add_command(label="Группы", 
                                    command=lambda: self.show_table("SELECT * FROM gruop", GRUOP_HEADERS))
        references_menu.add_command(label="Специальность", 
                                    command=lambda: self.show_table("SELECT * FROM spec", SPEC_HEADERS))
        references_menu.add_command(label="Отделение", 
                                    command=lambda: self.show_table("SELECT * FROM otdelenie", OTDELENIE_HEADERS))
        references_menu.add_command(label="Вид финансирования", 
                                    command=lambda: self.show_table("SELECT * FROM vid_finan", VID_FINAN_HEADERS))
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
        reports_menu.add_command(label="Создать Отчёт", command=self.to_xlsx)
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
        search_frame.grid(row=1, column=0, pady=pad)
        self.search_entry = ctk.CTkEntry(search_frame, width=300)
        self.search_entry.grid(row=0, column=0, padx=pad)
        ctk.CTkButton(search_frame, text="Поиск", width=20, command=self.search).grid(row=0, column=1, padx=pad)
        ctk.CTkButton(search_frame, text="Искать далее", width=20, command=self.search_next).grid(row=0, column=2, padx=pad)
        ctk.CTkButton(search_frame, text="Сброс", width=20, command=self.reset_search).grid(row=0, column=3, padx=pad)

    def search_in_table(self, table, search_terms, start_item=None):
        table.selection_remove(table.selection())  # Сброс предыдущего выделения

        items = table.get_children('')
        start_index = items.index(start_item) + 1 if start_item else 0

        for item in items[start_index:]:
            values = table.item(item, 'values')
            for term in search_terms:
                if any(term.lower() in str(value).lower() for value in values):
                    table.selection_add(item)
                    table.focus(item)
                    table.see(item)
                    return item  # Возвращаем найденный элемент

    def reset_search(self):
        if self.last_headers:
            self.table.selection_remove(self.table.selection())
        self.search_entry.delete(0, 'end')

    def search(self):
        if self.last_headers:
            self.current_item = self.search_in_table(self.table, self.search_entry.get().split(','))

    def search_next(self):
        if self.last_headers:
            if self.current_item:
                self.current_item = self.search_in_table(self.table, self.search_entry.get().split(','), start_item=self.current_item)
    
    def to_xlsx(self):
        if self.last_headers == POL_HEADERS:
            sql_query = "SELECT * FROM pol"
            table_name = "pol"
        elif self.last_headers == KURS_HEADERS:
            sql_query = "SELECT * FROM kurs"
            table_name = "kurs"
        elif self.last_headers == GRUOP_HEADERS:
            sql_query = "SELECT * FROM gruop"
            table_name = "gruop"
        elif self.last_headers == SPEC_HEADERS:
            sql_query = "SELECT * FROM spec"
            table_name = "spec"
        elif self.last_headers == OTDELENIE_HEADERS:
            sql_query = "SELECT * FROM otdelenie"
            table_name = "otdelenie"
        elif self.last_headers == VID_FINAN_HEADERS:
            sql_query = "SELECT * FROM vid_finan"
            table_name = "vid_finan"
        elif self.last_headers == STUDENTS_HEADERS:
            sql_query = '''
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
            '''
            table_name = "students"
        elif self.last_headers == PARENTS_HEADERS:
            sql_query = '''
                    SELECT parents.id_parent, parents.FIO, parents.phone_nomber, students.FIO FROM parents
                    JOIN students ON parents.id_student = students.id_student
            '''
            table_name = "parents"
        else: return

        dir = sys.path[0] + "\\export"
        os.makedirs(dir, exist_ok=True)
        path = dir + f"\\{table_name}.xlsx"

        # Подключение к базе данных SQLite
        conn = sqlite3.connect("res\\students_bd.db")
        cursor = conn.cursor()
        # Получите данные из базы данных
        cursor.execute(sql_query)
        data = cursor.fetchall()
        # Создайте DataFrame из данных
        df = pd.DataFrame(data, columns=self.last_headers)
        # Создайте объект writer для записи данных в Excel
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        # Запишите DataFrame в файл Excel
        df.to_excel(writer, 'Лист 1', index=False)
        # Сохраните результат
        writer.close()

        showinfo(title="Успешно", message=f"Данные экспортированы в {path}")
    
    def add(self):
        if self.last_headers == POL_HEADERS:
            WindowDirectory("add", ("Пол", "pol", "id_pol", "name_pol"))
        elif self.last_headers == KURS_HEADERS:
            WindowDirectory("add", ("Kypc", "kurs", "id_kurs", "N_kurs"))
        elif self.last_headers == GRUOP_HEADERS:
            WindowDirectory("add", ("Группы", "gruop", "id_gruop", "name_gruop"))
        elif self.last_headers == SPEC_HEADERS:
            WindowDirectory("add", ("Специальность", "spec", "id_spec", "name_spec"))
        elif self.last_headers == OTDELENIE_HEADERS:
            WindowDirectory("add", ("Отделение", "otdelenie", "id_otdelenie", "name_otdelenie"))
        elif self.last_headers == VID_FINAN_HEADERS:
            WindowDirectory("add", ("Вид финансирования", "vid_finan", "id_finan", "name_finan"))
        elif self.last_headers == STUDENTS_HEADERS:
            WindowStudents("add")
        elif self.last_headers == PARENTS_HEADERS:
            WindowParents("add")
        else: return

        self.withdraw()

    def delete(self):
        if self.last_headers:
            select_item = self.table.selection()
            if select_item:
                item_data = self.table.item(select_item[0])["values"]
            else:
                showerror(title="Ошибка", message="He выбранна запись")
                return
        else:
            return

        if self.last_headers == POL_HEADERS:
            WindowDirectory("delete", ("Пол", "pol", "id_pol", "name_pol"), item_data)
        elif self.last_headers == KURS_HEADERS:
            WindowDirectory("delete", ("Kypc", "kurs", "id_kurs", "N_kurs"), item_data)
        elif self.last_headers == GRUOP_HEADERS:
            WindowDirectory("delete", ("Группы", "gruop", "id_gruop", "name_gruop"), item_data)
        elif self.last_headers == SPEC_HEADERS:
             WindowDirectory("delete", ("Специальность", "spec", "id_spec", "name_spec"), item_data)
        elif self.last_headers == OTDELENIE_HEADERS:
             WindowDirectory("delete", ("Отделение", "otdelenie", "id_otdelenie", "name_otdelenie"), item_data)
        elif self.last_headers == VID_FINAN_HEADERS:
             WindowDirectory("delete", ("Вид финансирования", "vid_finan", "id_finan", "name_finan"), item_data)
        elif self.last_headers == STUDENTS_HEADERS:
            WindowStudents("delete", item_data)
        elif self.last_headers == PARENTS_HEADERS:
            WindowParents("delete", item_data)
        else: return

        self.withdraw()

    def change(self):
        if self.last_headers:
            select_item = self.table.selection()
            if select_item:
                item_data = self.table.item(select_item[0])["values"]
            else:
                showerror(title="Ошибка", message="He выбранна запись")
                return
        else:
            return

        if self.last_headers == POL_HEADERS:
            WindowDirectory("change", ("Пол", "pol", "id_pol", "name_pol"), item_data)
        elif self.last_headers == KURS_HEADERS:
            WindowDirectory("change", ("Kypc", "kurs", "id_kurs", "N_kurs"), item_data)
        elif self.last_headers == GRUOP_HEADERS:
            WindowDirectory("change", ("Группы", "gruop", "id_gruop", "name_gruop"), item_data)
        elif self.last_headers == SPEC_HEADERS:
            WindowDirectory("change", ("Специальность", "spec", "id_spec", "name_spec"), item_data)
        elif self.last_headers == OTDELENIE_HEADERS:
            WindowDirectory("change", ("Отделение", "otdelenie", "id_otdelenie", "name_otdelenie"), item_data)
        elif self.last_headers == VID_FINAN_HEADERS:
            WindowDirectory("change", ("Вид финансирования", "vid_finan", "id_finan", "name_finan"), item_data)
        elif self.last_headers == STUDENTS_HEADERS:
            WindowStudents("change", item_data)
        elif self.last_headers == PARENTS_HEADERS:
            WindowParents("change", item_data)
        else: return
        
        self.withdraw()
    
    def show_table(self, sql_query, headers = None):
        # Очистка фрейма перед отображением новых данных
        for widget in self.table_frame.winfo_children(): widget.destroy()

        # Подключение к базе данных SQLite
        conn = sqlite3.connect("res\\students_bd.db")
        cursor = conn.cursor()

        # Выполнение SQL-запроса
        cursor.execute(sql_query)
        self.last_sql_query = sql_query

        # Получение заголовков таблицы и данных
        if headers == None: # если заголовки не были переданы используем те что в БД
            table_headers = [description[0] for description in cursor.description]
        else: # иначе используем те что передали
            table_headers = headers
            self.last_headers = headers
        table_data = cursor.fetchall()

        # Закрытие соединения с базой данных
        conn.close()
            
        canvas = ctk.CTkCanvas(self.table_frame, width=865, height=480)
        canvas.pack(fill="both", expand=True)

        x_scrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal", command=canvas.xview)
        x_scrollbar.pack(side="bottom", fill="x")

        canvas.configure(xscrollcommand=x_scrollbar.set)

        self.table = ttk.Treeview(self.table_frame, columns=table_headers, show="headings", height=23)
        for header in table_headers: 
            self.table.heading(header, text=header)
            self.table.column(header, width=len(header) * 10 + 15) # установка ширины столбца исходя длины его заголовка
        for row in table_data: self.table.insert("", "end", values=row)

        canvas.create_window((0, 0), window=self.table, anchor="nw")

        self.table.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    
    def update_table(self):
        self.show_table(self.last_sql_query, self.last_headers)

class WindowDirectory(ctk.CTkToplevel):
    def __init__(self, operation: str, table_info: tuple[str, str, str, str], data = None):
        super().__init__()

        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if data:
            self.id = data[0] # id в таблице спрвочнике
            self.value = data[1] # значение по id
        
        self.table_name_user = table_info[0]
        self.table_name_db = table_info[1]
        self.field_id = table_info[2]
        self.field_name = table_info[3]

        if operation == "add":
            self.title(f"Добавление записи в таблицу '{self.table_name_user}'")
            ctk.CTkLabel(self, text="Наименование: ").grid(row=0, column=0, pady=5, padx=5)
            self.add_enty = ctk.CTkEntry(self, width=200)
            self.add_enty.grid(row=0, column=1, pady=5, padx=5)
            ctk.CTkButton(self, text="Отмена", width=200, command=self.quit_win).grid(row=1, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Добавить", width=200, command=self.add).grid(row=1, column=1, pady=5, padx=5)
        
        elif operation == "delete":
            self.title(f"Удаление записи из таблицы '{self.table_name_user}'")
            ctk.CTkLabel(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы '{self.table_name_user}'?", 
                         width=125).grid(row=0, column=0, columnspan=2, pady=5, padx=5)
            ctk.CTkLabel(self, text=f"Значение: {self.value}", width=125).grid(row=1, column=0, 
                                                                                 columnspan=2, pady=5, padx=5)
            ctk.CTkButton(self, text="Да", command=self.delete, width=125).grid(row=2, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Нет", command=self.quit_win, width=125).grid(row=2, column=1, pady=5, padx=5)
            
        elif operation == "change":
            self.title(f"Изменение записи в таблице '{self.table_name_user}'")
            ctk.CTkLabel(self, text="текущее значение").grid(row=0, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text="Новое значение").grid(row=0, column=1, pady=5, padx=5)

            ctk.CTkLabel(self, text=f"{self.value}").grid(row=1, column=0, pady=5, padx=5)
            self.change_entry = ctk.CTkEntry(self, width=200)
            self.change_entry.grid(row=1, column=1, pady=5, padx=5)

            ctk.CTkButton(self, text="Отмена", width=200, command=self.quit_win).grid(row=2, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Сохранить", width=200, command=self.change).grid(row=2, column=1, pady=5, padx=5)

    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        new_value = self.add_enty.get()
        if new_value:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO {self.table_name_db} ({self.field_name}) VALUES (?)", (new_value,))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {self.table_name_db} WHERE {self.field_id} = ?", (self.id,))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))
    
    def change(self):
        new_value = self.change_entry.get()
        if new_value:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"UPDATE {self.table_name_db} SET {self.field_name} = ? WHERE {self.field_id} = ?", 
                               (new_value, self.id))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
             showerror(title="Ошибка", message="Заполните все поля")

class WindowStudents(ctk.CTkToplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())

        conn = sqlite3.connect("res\\students_bd.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM kurs")
        kurs = []
        for item in cursor.fetchall():
            kurs.append(f"{item[0]}. {item[1]}")
        
        cursor.execute("SELECT * FROM gruop")
        gruop = []
        for item in cursor.fetchall():
            gruop.append(f"{item[0]}. {item[1]}")
        
        cursor.execute("SELECT * FROM otdelenie")
        otdelenie = []
        for item in cursor.fetchall():
            otdelenie.append(f"{item[0]}. {item[1]}")
        
        cursor.execute("SELECT * FROM pol")
        pol = []
        for item in cursor.fetchall():
            pol.append(f"{item[0]}. {item[1]}")
        
        cursor.execute("SELECT * FROM vid_finan")
        vid_finan = []
        for item in cursor.fetchall():
            vid_finan.append(f"{item[0]}. {item[1]}")
        
        cursor.execute("SELECT * FROM spec")
        spec = []
        for item in cursor.fetchall():
            spec.append(f"{item[0]}. {item[1]}")
        
        conn.close

        if select_row:
            self.select_row = select_row

        if operation == "add":
            self.title("Добавление в таблицу 'Студенты'")

            ctk.CTkLabel(self, text="ФИО").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.fio_entry = ctk.CTkEntry(self, width=300)
            self.fio_entry.grid(row=0, column=1)
            
            ctk.CTkLabel(self, text="Дата рождения").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.date_entry = ctk.CTkEntry(self, width=300)
            self.date_entry.grid(row=1, column=1)
            
            ctk.CTkLabel(self, text="№ телефона").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.phone_entry = ctk.CTkEntry(self, width=300)
            self.phone_entry.grid(row=2, column=1)
            
            ctk.CTkLabel(self, text="№ студенчиского билета").grid(row=3, column=0, padx=5, pady=5, sticky="w")
            self.n_bilet_entry = ctk.CTkEntry(self, width=300)
            self.n_bilet_entry.grid(row=3, column=1)
            
            ctk.CTkLabel(self, text="Год поступления").grid(row=4, column=0, padx=5, pady=5, sticky="w")
            self.y_post_entry = ctk.CTkEntry(self, width=300)
            self.y_post_entry.grid(row=4, column=1)
            
            ctk.CTkLabel(self, text="Год окончания").grid(row=5, column=0, padx=5, pady=5, sticky="w")
            self.y_okon_entry = ctk.CTkEntry(self, width=300)
            self.y_okon_entry.grid(row=5, column=1)
            '''=================================================================================='''
            ctk.CTkLabel(self, text="Kypc").grid(row=6, column=0, padx=5, pady=5, sticky="w")
            self.kurs_cb = ctk.CTkComboBox(self, width=300, values=kurs)
            self.kurs_cb.grid(row=6, column=1, pady=5, padx=5)

            ctk.CTkLabel(self, text="Группа").grid(row=7, column=0, padx=5, pady=5, sticky="w")
            self.gruop_cb = ctk.CTkComboBox(self, width=300, values=gruop)
            self.gruop_cb.grid(row=7, column=1, pady=5, padx=5)

            ctk.CTkLabel(self, text="Отделение").grid(row=8, column=0, padx=5, pady=5, sticky="w")
            self.otdelenie_cb = ctk.CTkComboBox(self, width=300, values=otdelenie)
            self.otdelenie_cb.grid(row=8, column=1, pady=5, padx=5)

            ctk.CTkLabel(self, text="Пол").grid(row=9, column=0, padx=5, pady=5, sticky="w")
            self.pol_cb = ctk.CTkComboBox(self, width=300, values=pol)
            self.pol_cb.grid(row=9, column=1, pady=5, padx=5)

            ctk.CTkLabel(self, text="Вид финансирования").grid(row=10, column=0, padx=5, pady=5, sticky="w")
            self.vid_finan_cb = ctk.CTkComboBox(self, width=300, values=vid_finan)
            self.vid_finan_cb.grid(row=10, column=1, pady=5, padx=5)

            ctk.CTkLabel(self, text="Специальность").grid(row=11, column=0, padx=5, pady=5, sticky="w")
            self.spec_cb = ctk.CTkComboBox(self, width=300, values=spec)
            self.spec_cb.grid(row=11, column=1, pady=5, padx=5)

            ctk.CTkButton(self, text="Отмена", command=self.quit_win, width=150
                          ).grid(row=12, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkButton(self, text="Добавить", command=self.add, width=150
                          ).grid(row=12, column=1, padx=5, pady=5, sticky="e")
        
        elif operation == "delete":
            self.title("Удаление из таблицы 'Студенты'")

            ctk.CTkLabel(self, text="Вы действитель хотите удалить запись\nИз таблицы студенты?"
                         ).grid(row=0, column=0, padx=5, pady=5, columnspan=2)
            ctk.CTkLabel(self, text=f"{self.select_row[0]}. {self.select_row[1]}"
                         ).grid(row=1, column=0, padx=5, pady=5, columnspan=2)
            
            ctk.CTkButton(self, text="Нет", width=100, command=self.quit_win).grid(row=2, column=0, pady=5, padx=5, sticky="w")
            ctk.CTkButton(self, text="Да", width=100, command=self.delete).grid(row=2, column=1, pady=5, padx=5, sticky="e")
        
        elif operation == "change":
            self.title("Изменение в таблице 'Студенты'")

            ctk.CTkLabel(self, text="Имя поля").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self, text="Текущее значение").grid(row=0, column=1, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self, text="Новое занчение").grid(row=0, column=2, padx=5, pady=5, sticky="w")

            ctk.CTkLabel(self, text="ФИО").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self, text=self.select_row[1]).grid(row=1, column=1, padx=5, pady=5, sticky="w")
            self.fio_entry = ctk.CTkEntry(self, width=300)
            self.fio_entry.grid(row=1, column=2)
            
            ctk.CTkLabel(self, text="Дата рождения").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self, text=self.select_row[2]).grid(row=2, column=1, padx=5, pady=5, sticky="w")
            self.date_entry = ctk.CTkEntry(self, width=300)
            self.date_entry.grid(row=2, column=2)
            
            ctk.CTkLabel(self, text="№ телефона").grid(row=3, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self, text=self.select_row[3]).grid(row=3, column=1, padx=5, pady=5, sticky="w")
            self.phone_entry = ctk.CTkEntry(self, width=300)
            self.phone_entry.grid(row=3, column=2)
            
            ctk.CTkLabel(self, text="№ студенчиского билета").grid(row=4, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self, text=self.select_row[4]).grid(row=4, column=1, padx=5, pady=5, sticky="w")
            self.n_bilet_entry = ctk.CTkEntry(self, width=300)
            self.n_bilet_entry.grid(row=4, column=2)
            
            ctk.CTkLabel(self, text="Год поступления").grid(row=5, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self, text=self.select_row[5]).grid(row=5, column=1, padx=5, pady=5, sticky="w")
            self.y_post_entry = ctk.CTkEntry(self, width=300)
            self.y_post_entry.grid(row=5, column=2)
            
            ctk.CTkLabel(self, text="Год окончания").grid(row=6, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self, text=self.select_row[6]).grid(row=6, column=1, padx=5, pady=5, sticky="w")
            self.y_okon_entry = ctk.CTkEntry(self, width=300)
            self.y_okon_entry.grid(row=6, column=2)
            '''=================================================================================='''
            ctk.CTkLabel(self, text="Kypc").grid(row=7, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self, text=self.select_row[7]).grid(row=7, column=1, padx=5, pady=5, sticky="w")
            self.kurs_cb = ctk.CTkComboBox(self, width=300, values=kurs)
            self.kurs_cb.grid(row=7, column=2, pady=5, padx=5)

            ctk.CTkLabel(self, text="Группа").grid(row=8, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self, text=self.select_row[8]).grid(row=8, column=1, padx=5, pady=5, sticky="w")
            self.gruop_cb = ctk.CTkComboBox(self, width=300, values=gruop)
            self.gruop_cb.grid(row=8, column=2, pady=5, padx=5)

            ctk.CTkLabel(self, text="Отделение").grid(row=9, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self, text=self.select_row[9]).grid(row=9, column=1, padx=5, pady=5, sticky="w")
            self.otdelenie_cb = ctk.CTkComboBox(self, width=300, values=otdelenie)
            self.otdelenie_cb.grid(row=9, column=2, pady=5, padx=5)

            ctk.CTkLabel(self, text="Пол").grid(row=10, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self, text=self.select_row[10]).grid(row=10, column=1, padx=5, pady=5, sticky="w")
            self.pol_cb = ctk.CTkComboBox(self, width=300, values=pol)
            self.pol_cb.grid(row=10, column=2, pady=5, padx=5)

            ctk.CTkLabel(self, text="Вид финансирования").grid(row=11, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self, text=self.select_row[11]).grid(row=11, column=1, padx=5, pady=5, sticky="w")
            self.vid_finan_cb = ctk.CTkComboBox(self, width=300, values=vid_finan)
            self.vid_finan_cb.grid(row=11, column=2, pady=5, padx=5)

            ctk.CTkLabel(self, text="Специальность").grid(row=12, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self, text=self.select_row[12]).grid(row=12, column=1, padx=5, pady=5, sticky="w")
            self.spec_cb = ctk.CTkComboBox(self, width=300, values=spec)
            self.spec_cb.grid(row=12, column=2, pady=5, padx=5)


            ctk.CTkButton(self, text="Отмена", command=self.quit_win, width=150
                          ).grid(row=13, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkButton(self, text="Сохранить", command=self.change, width=150
                          ).grid(row=13, column=2, padx=5, pady=5, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        new_FIO = self.fio_entry.get()
        new_date = self.date_entry.get()
        new_phone_nomber = self.phone_entry.get()
        new_n_bilet = self.n_bilet_entry.get()
        new_y_post = self.y_post_entry.get()
        new_y_okon = self.y_okon_entry.get()
        id_kurs = self.kurs_cb.get().split(".")[0]
        id_gruop = self.gruop_cb.get().split(".")[0]
        id_otdelenie = self.otdelenie_cb.get().split(".")[0]
        id_pol = self.pol_cb.get().split(".")[0]
        id_vid_finan = self.vid_finan_cb.get().split(".")[0]
        id_spec = self.spec_cb.get().split(".")[0]

        if "" not in (new_FIO, new_date, new_phone_nomber, new_n_bilet, new_y_post, new_y_okon):
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute(
                    f"""INSERT INTO students (FIO, date_dr, phone_nomber, y_post, y_okon, n_bilet,
                    id_kurs, id_gruop, id_otdelenie, id_pol, id_finan, id_spec) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                    (new_FIO, new_date, new_phone_nomber, new_n_bilet, new_y_post, new_y_okon, 
                     id_kurs, id_gruop, id_otdelenie, id_pol, id_vid_finan, id_spec))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")
    
    def delete(self):
        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM students WHERE id_student = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

    def change(self):
        new_FIO = self.fio_entry.get() or self.select_row[1]
        new_date = self.date_entry.get() or self.select_row[2]
        new_phone_nomber = self.phone_entry.get() or self.select_row[3]
        new_n_bilet = self.n_bilet_entry.get() or self.select_row[4]
        new_y_post = self.y_post_entry.get() or self.select_row[5]
        new_y_okon = self.y_okon_entry.get() or self.select_row[6]
        id_kurs = self.kurs_cb.get().split(".")[0]
        id_gruop = self.gruop_cb.get().split(".")[0]
        id_otdelenie = self.otdelenie_cb.get().split(".")[0]
        id_pol = self.pol_cb.get().split(".")[0]
        id_vid_finan = self.vid_finan_cb.get().split(".")[0]
        id_spec = self.spec_cb.get().split(".")[0]

        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE students SET (FIO, date_dr, phone_nomber, y_post, y_okon, n_bilet,
                id_kurs, id_gruop, id_otdelenie, id_pol, id_finan, id_spec) = (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
                WHERE id_student = {self.select_row[0]}
            ''', (new_FIO, new_date, new_phone_nomber, new_n_bilet, new_y_post, new_y_okon, 
                  id_kurs, id_gruop, id_otdelenie, id_pol, id_vid_finan, id_spec))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

class WindowParents(ctk.CTkToplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())

        conn = sqlite3.connect("res\\students_bd.db")
        cursor = conn.cursor()
        cursor.execute("SELECT students.id_student, students.FIO FROM students")
        students_id_fio = cursor.fetchall()
        conn.close

        strs_students_id_fio = []
        for item in students_id_fio:
            strs_students_id_fio.append(f"{item[0]}. {item[1]}")
        students_id_fio = strs_students_id_fio

        if select_row:
            self.select_id_p = select_row[0]
            self.select_fio_p = select_row[1]
            self.select_phone = select_row[2]
            self.select_fio_s = select_row[3]

        if operation == "add":
            self.title("Добаление")
            ctk.CTkLabel(self, text="Добаление в таблицу 'Родители'").grid(row=0, column=0, pady=5, padx=5, columnspan=2)
            ctk.CTkLabel(self, text="ФИО родителя").grid(row=1, column=0, pady=5, padx=5)
            self.fio_p = ctk.CTkEntry(self, width=300)
            self.fio_p.grid(row=1, column=1, pady=5, padx=5)

            ctk.CTkLabel(self, text="№ телефона").grid(row=2, column=0, pady=5, padx=5)
            self.phone = ctk.CTkEntry(self, width=300)
            self.phone.grid(row=2, column=1, pady=5, padx=5)

            ctk.CTkLabel(self, text="ФИО студента").grid(row=3, column=0, pady=5, padx=5)
            self.fio_s = ctk.CTkComboBox(self, width=300, values=students_id_fio)
            self.fio_s.grid(row=3, column=1, pady=5, padx=5)

            ctk.CTkButton(self, text="Отмена", width=100, command=self.quit_win).grid(row=4, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Добавить", width=100, command=self.add).grid(row=4, column=1, pady=5, padx=5, sticky="e")
        
        elif operation == "delete":
            self.title("Удаление")
            ctk.CTkLabel(self, text="Вы действиельно хотите\n удалить запись из таблицы 'Родители'?"
                         ).grid(row=0, column=0, pady=5, padx=5, columnspan=2)
            
            ctk.CTkLabel(self, text=f"{self.select_id_p}. {self.select_fio_p}"
                         ).grid(row=1, column=0, pady=5, padx=5, columnspan=2)

            ctk.CTkButton(self, text="Нет", width=100, command=self.quit_win).grid(row=2, column=0, pady=5, padx=5, sticky="w")
            ctk.CTkButton(self, text="Да", width=100, command=self.delete).grid(row=2, column=1, pady=5, padx=5, sticky="e")
        
        elif operation == "change":
            self.title("Изменение в таблице 'Родители'")
            ctk.CTkLabel(self, text="Назввание поля").grid(row=0, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text="Текущее значение").grid(row=0, column=1, pady=5, padx=5)
            ctk.CTkLabel(self, text="Новое занчение").grid(row=0, column=2, pady=5, padx=5)

            ctk.CTkLabel(self, text="ФИО родителя").grid(row=1, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text=self.select_fio_p).grid(row=1, column=1, pady=5, padx=5)
            self.fio_p = ctk.CTkEntry(self, width=300)
            self.fio_p.grid(row=1, column=2, pady=5, padx=5)

            ctk.CTkLabel(self, text="№ телефона").grid(row=2, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text=self.select_phone).grid(row=2, column=1, pady=5, padx=5)
            self.phone = ctk.CTkEntry(self, width=300)
            self.phone.grid(row=2, column=2, pady=5, padx=5)

            ctk.CTkLabel(self, text="ФИО студента").grid(row=3, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text=self.select_fio_s).grid(row=3, column=1, pady=5, padx=5)
            self.fio_s = ctk.CTkComboBox(self, width=300, values=students_id_fio)
            self.fio_s.grid(row=3, column=2, pady=5, padx=5)

            ctk.CTkButton(self, text="Отмена", width=100, command=self.quit_win).grid(row=4, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Сохранить", width=100, command=self.change).grid(row=4, column=2, pady=5, padx=5, sticky="e")

    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        new_FIO = self.fio_p.get()
        new_phone_nomber = self.phone.get()
        id_student = self.fio_s.get().split(".")[0]

        if new_FIO != "" and new_phone_nomber != "":
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO parents (FIO, phone_nomber, id_student) VALUES (?, ?, ?)", 
                            (new_FIO, new_phone_nomber, id_student))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM parents WHERE id_parent = ?", (self.select_id_p,))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

    def change(self):
        new_FIO = self.fio_p.get() or self.select_fio_p
        new_phone_nomber = self.phone.get() or self.select_phone
        id_student = self.fio_s.get().split(".")[0]

        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"""
                        UPDATE parents SET (FIO, phone_nomber, id_student) = (?, ?, ?) WHERE id_parent = {self.select_id_p}
                    """, (new_FIO, new_phone_nomber, id_student))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

if __name__ == "__main__":
    db = DB()
    win = WindowMain()
    win.mainloop()