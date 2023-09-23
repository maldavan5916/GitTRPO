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
        
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Руководство пользователя")
        help_menu.add_command(label="О программе")
        self.menu_bar.add_cascade(label="Сервис", menu=help_menu)

        file_menu.configure(bg='#555', fg='white')
        references_menu.configure(bg='#555', fg='white')
        tables_menu.configure(bg='#555', fg='white')
        reports_menu.configure(bg='#555', fg='white')
        help_menu.configure(bg='#555', fg='white')

        self.config(menu=self.menu_bar)
        
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill='both', expand=True)

        bg = tk.PhotoImage(file="res\\bg.png")
        self.lbl = ctk.CTkLabel(self.table_frame, image=bg, text='Студенческий отдел кадров', font=("Calibri", 40))
        self.lbl.pack(anchor='center', expand=1)
        
    def show_students_table(self):
        # Очищаем предыдущие виджеты (если есть)
        for widget in self.table_frame.winfo_children():
            widget.destroy()
if __name__ == "__main__":
    MainApp().mainloop()
