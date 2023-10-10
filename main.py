import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import sqlite3
from PIL import Image
from DB import DB
from tkinter.messagebox import showerror

POL_HEADERS = ["№", "Наименование пола"]
KURS_HEADERS = ["№", "Наименование курса"]
GRUOP_HEADERS = ["№", "Наименование группы"]
SPEC_HEADERS = ["№", "Наименование специальности"]
OTDELENIE_HEADERS = ["№", "Наименование отделения"]
VID_FINAN_HEADERS = ["№", "Наименование финансирования"]

STUDENTS_HEADERS = ["№", "ФИО студента", "Дата рождения", "№ телефона", 
                    "№ студенчиского билета", "Год поступления", "Год окончания",
                    "Kypc", "Группа", "Отделение", "Пол", "Вид финансирования", "Специальность"]
PARENTS_HEADERS = ["№", "ФИО родителя", "№ телефона", "ФИО студента"]

class WindowMain(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Студенческий отдел кадров')
        self.geometry('865x450')
        self.resizable(width=False, height=False)
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
        references_menu.add_command(label="Группа", 
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
        if self.last_headers == POL_HEADERS:
            WindowPol("add")
        elif self.last_headers == KURS_HEADERS:
            WindowKurs("add")
        elif self.last_headers == GRUOP_HEADERS:
            WindowGruop("add")
        elif self.last_headers == SPEC_HEADERS:
            WindowSpec("add")
        elif self.last_headers == OTDELENIE_HEADERS:
            WindowOtdelenie("add")
        elif self.last_headers == VID_FINAN_HEADERS:
            WindowVidFinan("add")
        elif self.last_headers == STUDENTS_HEADERS:
            WindowStudents("add")
        elif self.last_headers == PARENTS_HEADERS:
            WindowParents("add")
        else: return

        self.withdraw()

    def delete(self):
        select_item = self.table.selection()
        if select_item:
            item_data = self.table.item(select_item[0])["values"]
        else:
            showerror(title="Ошибка", message="He выбранна запись")
            return

        if self.last_headers == POL_HEADERS:
            WindowPol("delete", item_data)
        elif self.last_headers == KURS_HEADERS:
            WindowKurs("delete", item_data)
        elif self.last_headers == GRUOP_HEADERS:
            WindowGruop("delete", item_data)
        elif self.last_headers == SPEC_HEADERS:
            WindowSpec("delete", item_data)
        elif self.last_headers == OTDELENIE_HEADERS:
            WindowOtdelenie("delete", item_data)
        elif self.last_headers == VID_FINAN_HEADERS:
            WindowVidFinan("delete", item_data)
        elif self.last_headers == STUDENTS_HEADERS:
            WindowStudents("delete", item_data)
        elif self.last_headers == PARENTS_HEADERS:
            WindowParents("delete", item_data)
        else: return

        self.withdraw()

    def change(self):
        select_item = self.table.selection()
        if select_item:
            item_data = self.table.item(select_item[0])["values"]
        else:
            showerror(title="Ошибка", message="He выбранна запись")
            return

        if self.last_headers == POL_HEADERS:
            WindowPol("change", item_data)
        elif self.last_headers == KURS_HEADERS:
            WindowKurs("change", item_data)
        elif self.last_headers == GRUOP_HEADERS:
            WindowGruop("change", item_data)
        elif self.last_headers == SPEC_HEADERS:
            WindowSpec("change", item_data)
        elif self.last_headers == OTDELENIE_HEADERS:
            WindowOtdelenie("change", item_data)
        elif self.last_headers == VID_FINAN_HEADERS:
            WindowVidFinan("change", item_data)
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

        self.table = ttk.Treeview(self.table_frame, columns=table_headers, show="headings")
        for header in table_headers: 
            self.table.heading(header, text=header)
            self.table.column(header, width=len(header) * 10 + 15) # установка ширины столбца исходя длины его заголовка
        for row in table_data: self.table.insert("", "end", values=row)

        canvas.create_window((0, 0), window=self.table, anchor="nw")

        self.table.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    
    def update_table(self):
        self.show_table(self.last_sql_query, self.last_headers)

class WindowPol(ctk.CTkToplevel):
    def __init__(self, operation, data = None):
        super().__init__()

        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        self.data = data

        if operation == "add":
            self.title("Добавление записи")
            ctk.CTkLabel(self, text="Наименование пола: ").grid(row=0, column=0, pady=5, padx=5)
            self.add_enty = ctk.CTkEntry(self, width=200)
            self.add_enty.grid(row=0, column=1, pady=5, padx=5)
            ctk.CTkButton(self, text="Добавить", command=self.add).grid(row=1, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Отмена", command=self.quit_win).grid(row=1, column=1, pady=5, padx=5)
        
        elif operation == "delete" and self.data != None:
            self.title("Удаление записи")
            ctk.CTkLabel(self, text="Вы действиельно хотите удалить запись", width=125).grid(row=0, column=0, 
                                                                                             columnspan=2, pady=5, padx=5)
            ctk.CTkLabel(self, text=f"Значение: {self.data[1]}", width=125).grid(row=1, column=0, 
                                                                                 columnspan=2, pady=5, padx=5)
            ctk.CTkButton(self, text="Да", command=self.delete, width=125).grid(row=2, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Нет", command=self.quit_win, width=125).grid(row=2, column=1, pady=5, padx=5)
            
        elif operation == "change"and self.data != None:
            self.title("Изменение записи")
            ctk.CTkLabel(self, text="Наименование значения").grid(row=0, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text="текущее значение").grid(row=0, column=1, pady=5, padx=5)
            ctk.CTkLabel(self, text="Новое значение").grid(row=0, column=2, pady=5, padx=5)

            ctk.CTkLabel(self, text="Наименование пола").grid(row=2, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text=f"{self.data[1]}").grid(row=2, column=1, pady=5, padx=5)
            self.pol_entry = ctk.CTkEntry(self, width=200)
            self.pol_entry.grid(row=2, column=2, pady=5, padx=5)

            ctk.CTkButton(self, text="Отмена", command=self.quit_win).grid(row=3, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Сохранить", command=self.change).grid(row=3, column=2, pady=5, padx=5)

    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        new_pol = self.add_enty.get()
        if new_pol:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO pol (name_pol) VALUES (?)", (new_pol,))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))

    def delete(self):
        try:
            if self.data != None:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM pol WHERE id_pol = ?", (self.data[0],))
                conn.commit()
                conn.close()
                self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))
    
    def change(self):
        new_pol = self.pol_entry.get()
        if new_pol:
            try:
                if self.data != None:
                    conn = sqlite3.connect("res\\students_bd.db")
                    cursor = conn.cursor()
                    cursor.execute("UPDATE pol SET name_pol = ? WHERE id_pol = ?", (new_pol, self.data[0]))
                    conn.commit()
                    conn.close()
                    self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))

class WindowKurs(ctk.CTkToplevel):
    def __init__(self, operation, data = None):
        super().__init__()

        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        self.data = data

        if operation == "add":
            self.title("Добавление записи")
            ctk.CTkLabel(self, text="Наименование курса: ").grid(row=0, column=0, pady=5, padx=5)
            self.add_enty = ctk.CTkEntry(self, width=200)
            self.add_enty.grid(row=0, column=1, pady=5, padx=5)
            ctk.CTkButton(self, text="Добавить", command=self.add).grid(row=1, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Отмена", command=self.quit_win).grid(row=1, column=1, pady=5, padx=5)
        
        elif operation == "delete" and self.data != None:
            self.title("Удаление записи")
            ctk.CTkLabel(self, text="Вы действиельно хотите удалить запись", width=125).grid(row=0, column=0, 
                                                                                             columnspan=2, pady=5, padx=5)
            ctk.CTkLabel(self, text=f"Значение: {self.data[1]}", width=125).grid(row=1, column=0, 
                                                                                 columnspan=2, pady=5, padx=5)
            ctk.CTkButton(self, text="Да", command=self.delete, width=125).grid(row=2, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Нет", command=self.quit_win, width=125).grid(row=2, column=1, pady=5, padx=5)
            
        elif operation == "change"and self.data != None:
            self.title("Изменение записи")
            ctk.CTkLabel(self, text="Наименование значения").grid(row=0, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text="текущее значение").grid(row=0, column=1, pady=5, padx=5)
            ctk.CTkLabel(self, text="Новое значение").grid(row=0, column=2, pady=5, padx=5)

            ctk.CTkLabel(self, text="Наименование курса").grid(row=2, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text=f"{self.data[1]}").grid(row=2, column=1, pady=5, padx=5)
            self.kurs_entry = ctk.CTkEntry(self, width=200)
            self.kurs_entry.grid(row=2, column=2, pady=5, padx=5)

            ctk.CTkButton(self, text="Отмена", command=self.quit_win).grid(row=3, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Сохранить", command=self.change).grid(row=3, column=2, pady=5, padx=5)
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        new_kurs = self.add_enty.get()
        if new_kurs:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO kurs (N_kurs) VALUES (?)", (new_kurs,))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))

    def delete(self):
        try:
            if self.data != None:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM kurs WHERE id_kurs = ?", (self.data[0],))
                conn.commit()
                conn.close()
                self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))
    
    def change(self):
        new_kurs = self.kurs_entry.get()
        if new_kurs:
            try:
                if self.data != None:
                    conn = sqlite3.connect("res\\students_bd.db")
                    cursor = conn.cursor()
                    cursor.execute("UPDATE kurs SET N_kurs = ? WHERE id_kurs = ?", (new_kurs, self.data[0]))
                    conn.commit()
                    conn.close()
                    self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))

class WindowGruop(ctk.CTkToplevel):
    def __init__(self, operation, data = None):
        super().__init__()

        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        self.data = data

        if operation == "add":
            self.title("Добавление записи")
            ctk.CTkLabel(self, text="Наименование группы: ").grid(row=0, column=0, pady=5, padx=5)
            self.add_enty = ctk.CTkEntry(self, width=200)
            self.add_enty.grid(row=0, column=1, pady=5, padx=5)
            ctk.CTkButton(self, text="Добавить", command=self.add).grid(row=1, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Отмена", command=self.quit_win).grid(row=1, column=1, pady=5, padx=5)
        
        elif operation == "delete" and self.data != None:
            self.title("Удаление записи")
            ctk.CTkLabel(self, text="Вы действиельно хотите удалить запись", width=125).grid(row=0, column=0, 
                                                                                             columnspan=2, pady=5, padx=5)
            ctk.CTkLabel(self, text=f"Значение: {self.data[1]}", width=125).grid(row=1, column=0, 
                                                                                 columnspan=2, pady=5, padx=5)
            ctk.CTkButton(self, text="Да", command=self.delete, width=125).grid(row=2, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Нет", command=self.quit_win, width=125).grid(row=2, column=1, pady=5, padx=5)
            
        elif operation == "change"and self.data != None:
            self.title("Изменение записи")
            ctk.CTkLabel(self, text="Наименование значения").grid(row=0, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text="текущее значение").grid(row=0, column=1, pady=5, padx=5)
            ctk.CTkLabel(self, text="Новое значение").grid(row=0, column=2, pady=5, padx=5)

            ctk.CTkLabel(self, text="Наименование группы").grid(row=2, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text=f"{self.data[1]}").grid(row=2, column=1, pady=5, padx=5)
            self.gruop_entry = ctk.CTkEntry(self, width=200)
            self.gruop_entry.grid(row=2, column=2, pady=5, padx=5)

            ctk.CTkButton(self, text="Отмена", command=self.quit_win).grid(row=3, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Сохранить", command=self.change).grid(row=3, column=2, pady=5, padx=5)
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        new_gruop = self.add_enty.get()
        if new_gruop:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO gruop (name_gruop) VALUES (?)", (new_gruop,))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))

    def delete(self):
        try:
            if self.data != None:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM gruop WHERE id_gruop = ?", (self.data[0],))
                conn.commit()
                conn.close()
                self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))
    
    def change(self):
        new_kurs = self.gruop_entry.get()
        if new_kurs:
            try:
                if self.data != None:
                    conn = sqlite3.connect("res\\students_bd.db")
                    cursor = conn.cursor()
                    cursor.execute("UPDATE gruop SET name_gruop = ? WHERE id_gruop = ?", (new_kurs, self.data[0]))
                    conn.commit()
                    conn.close()
                    self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))

class WindowSpec(ctk.CTkToplevel):
    def __init__(self, operation, data = None):
        super().__init__()

        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        self.data = data

        if operation == "add":
            self.title("Добавление записи")
            ctk.CTkLabel(self, text="Наименование специальности: ").grid(row=0, column=0, pady=5, padx=5)
            self.add_enty = ctk.CTkEntry(self, width=200)
            self.add_enty.grid(row=0, column=1, pady=5, padx=5)
            ctk.CTkButton(self, text="Добавить", command=self.add).grid(row=1, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Отмена", command=self.quit_win).grid(row=1, column=1, pady=5, padx=5)
        
        elif operation == "delete" and self.data != None:
            self.title("Удаление записи")
            ctk.CTkLabel(self, text="Вы действиельно хотите удалить запись", width=125).grid(row=0, column=0, 
                                                                                             columnspan=2, pady=5, padx=5)
            ctk.CTkLabel(self, text=f"Значение: {self.data[1]}", width=125).grid(row=1, column=0, 
                                                                                 columnspan=2, pady=5, padx=5)
            ctk.CTkButton(self, text="Да", command=self.delete, width=125).grid(row=2, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Нет", command=self.quit_win, width=125).grid(row=2, column=1, pady=5, padx=5)
            
        elif operation == "change"and self.data != None:
            self.title("Изменение записи")
            ctk.CTkLabel(self, text="Наименование значения").grid(row=0, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text="текущее значение").grid(row=0, column=1, pady=5, padx=5)
            ctk.CTkLabel(self, text="Новое значение").grid(row=0, column=2, pady=5, padx=5)

            ctk.CTkLabel(self, text="Наименование специальности").grid(row=2, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text=f"{self.data[1]}").grid(row=2, column=1, pady=5, padx=5)
            self.spec_entry = ctk.CTkEntry(self, width=200)
            self.spec_entry.grid(row=2, column=2, pady=5, padx=5)

            ctk.CTkButton(self, text="Отмена", command=self.quit_win).grid(row=3, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Сохранить", command=self.change).grid(row=3, column=2, pady=5, padx=5)
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        new_spec = self.add_enty.get()
        if new_spec:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO spec (name_spec) VALUES (?)", (new_spec,))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))

    def delete(self):
        try:
            if self.data != None:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM spec WHERE id_spec = ?", (self.data[0],))
                conn.commit()
                conn.close()
                self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))
    
    def change(self):
        new_kurs = self.spec_entry.get()
        if new_kurs:
            try:
                if self.data != None:
                    conn = sqlite3.connect("res\\students_bd.db")
                    cursor = conn.cursor()
                    cursor.execute("UPDATE spec SET name_spec = ? WHERE id_spec = ?", (new_kurs, self.data[0]))
                    conn.commit()
                    conn.close()
                    self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))

class WindowOtdelenie(ctk.CTkToplevel):
    def __init__(self, operation, data = None):
        super().__init__()

        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        self.data = data

        if operation == "add":
            self.title("Добавление записи")
            ctk.CTkLabel(self, text="Наименование отделения: ").grid(row=0, column=0, pady=5, padx=5)
            self.add_enty = ctk.CTkEntry(self, width=200)
            self.add_enty.grid(row=0, column=1, pady=5, padx=5)
            ctk.CTkButton(self, text="Добавить", command=self.add).grid(row=1, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Отмена", command=self.quit_win).grid(row=1, column=1, pady=5, padx=5)
        
        elif operation == "delete" and self.data != None:
            self.title("Удаление записи")
            ctk.CTkLabel(self, text="Вы действиельно хотите удалить запись", width=125).grid(row=0, column=0, 
                                                                                             columnspan=2, pady=5, padx=5)
            ctk.CTkLabel(self, text=f"Значение: {self.data[1]}", width=125).grid(row=1, column=0, 
                                                                                 columnspan=2, pady=5, padx=5)
            ctk.CTkButton(self, text="Да", command=self.delete, width=125).grid(row=2, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Нет", command=self.quit_win, width=125).grid(row=2, column=1, pady=5, padx=5)
            
        elif operation == "change"and self.data != None:
            self.title("Изменение записи")
            ctk.CTkLabel(self, text="Наименование значения").grid(row=0, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text="текущее значение").grid(row=0, column=1, pady=5, padx=5)
            ctk.CTkLabel(self, text="Новое значение").grid(row=0, column=2, pady=5, padx=5)

            ctk.CTkLabel(self, text="Наименование отделения").grid(row=2, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text=f"{self.data[1]}").grid(row=2, column=1, pady=5, padx=5)
            self.otdelenie_entry = ctk.CTkEntry(self, width=200)
            self.otdelenie_entry.grid(row=2, column=2, pady=5, padx=5)

            ctk.CTkButton(self, text="Отмена", command=self.quit_win).grid(row=3, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Сохранить", command=self.change).grid(row=3, column=2, pady=5, padx=5)
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        new_otdelenie = self.add_enty.get()
        if new_otdelenie:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO otdelenie (name_otdelenie) VALUES (?)", (new_otdelenie,))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))

    def delete(self):
        try:
            if self.data != None:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM otdelenie WHERE id_otdelenie = ?", (self.data[0],))
                conn.commit()
                conn.close()
                self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))
    
    def change(self):
        new_kurs = self.otdelenie_entry.get()
        if new_kurs:
            try:
                if self.data != None:
                    conn = sqlite3.connect("res\\students_bd.db")
                    cursor = conn.cursor()
                    cursor.execute("UPDATE otdelenie SET name_otdelenie = ? WHERE id_otdelenie = ?", (new_kurs, self.data[0]))
                    conn.commit()
                    conn.close()
                    self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))

class WindowVidFinan(ctk.CTkToplevel):
    def __init__(self, operation, data = None):
        super().__init__()

        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        self.data = data

        if operation == "add":
            self.title("Добавление записи")
            ctk.CTkLabel(self, text="Наименование финансирования: ").grid(row=0, column=0, pady=5, padx=5)
            self.add_enty = ctk.CTkEntry(self, width=200)
            self.add_enty.grid(row=0, column=1, pady=5, padx=5)
            ctk.CTkButton(self, text="Добавить", command=self.add).grid(row=1, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Отмена", command=self.quit_win).grid(row=1, column=1, pady=5, padx=5)
        
        elif operation == "delete" and self.data != None:
            self.title("Удаление записи")
            ctk.CTkLabel(self, text="Вы действиельно хотите удалить запись", width=125).grid(row=0, column=0, 
                                                                                             columnspan=2, pady=5, padx=5)
            ctk.CTkLabel(self, text=f"Значение: {self.data[1]}", width=125).grid(row=1, column=0, 
                                                                                 columnspan=2, pady=5, padx=5)
            ctk.CTkButton(self, text="Да", command=self.delete, width=125).grid(row=2, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Нет", command=self.quit_win, width=125).grid(row=2, column=1, pady=5, padx=5)
            
        elif operation == "change"and self.data != None:
            self.title("Изменение записи")
            ctk.CTkLabel(self, text="Наименование значения").grid(row=0, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text="текущее значение").grid(row=0, column=1, pady=5, padx=5)
            ctk.CTkLabel(self, text="Новое значение").grid(row=0, column=2, pady=5, padx=5)

            ctk.CTkLabel(self, text="Наименование финансирования").grid(row=2, column=0, pady=5, padx=5)
            ctk.CTkLabel(self, text=f"{self.data[1]}").grid(row=2, column=1, pady=5, padx=5)
            self.finan_entry = ctk.CTkEntry(self, width=200)
            self.finan_entry.grid(row=2, column=2, pady=5, padx=5)

            ctk.CTkButton(self, text="Отмена", command=self.quit_win).grid(row=3, column=0, pady=5, padx=5)
            ctk.CTkButton(self, text="Сохранить", command=self.change).grid(row=3, column=2, pady=5, padx=5)
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        new_vid_finan = self.add_enty.get()
        if new_vid_finan:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO vid_finan (name_finan) VALUES (?)", (new_vid_finan,))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))

    def delete(self):
        try:
            if self.data != None:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM vid_finan WHERE id_finan = ?", (self.data[0],))
                conn.commit()
                conn.close()
                self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))
    
    def change(self):
        new_kurs = self.finan_entry.get()
        if new_kurs:
            try:
                if self.data != None:
                    conn = sqlite3.connect("res\\students_bd.db")
                    cursor = conn.cursor()
                    cursor.execute("UPDATE vid_finan SET name_finan = ? WHERE id_finan = ?", (new_kurs, self.data[0]))
                    conn.commit()
                    conn.close()
                    self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))

class WindowStudents(ctk.CTkToplevel):
    def __init__(self, operation, data = None):
        super().__init__()

        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        self.data = data

        if operation == "add":
            self.add()
        elif operation == "delete":
            self.delete()
        elif operation == "change":
            self.change()
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        print(__class__, "add")

    def delete(self):
        print(__class__, "delete")
    
    def change(self):
        print(__class__, "change")

class WindowParents(ctk.CTkToplevel):
    def __init__(self, operation, data = None):
        super().__init__()

        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        self.data = data

        if operation == "add":
            self.add()
        elif operation == "delete":
            self.delete()
        elif operation == "change":
            self.change()
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        print(__class__, "add")

    def delete(self):
        print(__class__, "delete")
    
    def change(self):
        print(__class__, "change")

if __name__ == "__main__":
    db = DB()
    win = WindowMain()
    win.mainloop()