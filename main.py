import tkinter as tk
import customtkinter as ctk
import sqlite3

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Студенческий отдел кадров')
        self.geometry('700x600')

        self.menu_bar = tk.Menu(self, background='#555', foreground='white')

        # Создаем пункты меню
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Открыть")
        file_menu.add_command(label="Сохранить")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)
        self.menu_bar.add_cascade(label="Файл", menu=file_menu)

        references_menu = tk.Menu(self.menu_bar, tearoff=0)
        references_menu.add_command(label="Пол")
        references_menu.add_command(label="Курс")
        references_menu.add_command(label="Группа")
        references_menu.add_command(label="Специальность")
        references_menu.add_command(label="Отделение")
        references_menu.add_command(label="Вид финансирования")
        self.menu_bar.add_cascade(label="Справочники", menu=references_menu)

        tables_menu = tk.Menu(self.menu_bar, tearoff=0)
        tables_menu.add_command(label="Студенты", command=self.show_students_table)
        tables_menu.add_command(label="Родители")
        self.menu_bar.add_cascade(label="Таблицы", menu=tables_menu)

        reports_menu = tk.Menu(self.menu_bar, tearoff=0)
        reports_menu.add_command(label="Создать Отчёт")
        self.menu_bar.add_cascade(label="Отчёты", menu=reports_menu)

        file_menu.configure(bg='#555', fg='white')
        references_menu.configure(bg='#555', fg='white')
        tables_menu.configure(bg='#555', fg='white')
        reports_menu.configure(bg='#555', fg='white')

        self.config(menu=self.menu_bar)
        
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill='both', expand=True)
        
    def show_students_table(self):
        # Очищаем предыдущие виджеты (если есть)
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Создаем соединение с базой данных
        conn = sqlite3.connect('students_bd.db')
        cursor = conn.cursor()

        # Выполняем SQL-запрос для выборки данных из таблицы students
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()

        # Закрываем соединение с базой данных
        conn.close()

         # Выводим заголовки таблицы
        headers = ["ID", "ФИО", "Дата рождения", "Телефон", "Дата поступления", "Дата окончания", "Номер билета", "Курс", "Группа", "Отделение", "Пол", "Финансирование", "Специальность"]
        for col, header in enumerate(headers):
            label_frame = ctk.CTkFrame(self.table_frame)
            label_frame.grid(row=0, column=col, padx=5, pady=5, sticky='nsew')
            
            label = ctk.CTkLabel(label_frame, text=header)
            label.pack(padx=5, pady=5, fill='both', expand=True)

        # Выводим данные
        for row_num, row_data in enumerate(data, start=1):
            for col, cell_data in enumerate(row_data):
                label_frame = ctk.CTkFrame(self.table_frame)
                label_frame.grid(row=row_num, column=col, padx=5, pady=5, sticky='nsew')
                
                label = ctk.CTkLabel(label_frame, text=str(cell_data))
                label.pack(padx=5, pady=5, fill='both', expand=True)
if __name__ == "__main__":
    MainApp().mainloop()
