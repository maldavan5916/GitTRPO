import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('students_bd.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "kurs" (
                "id_kurs" INTEGER NOT NULL,
                "N_kurs" INTEGER,
                PRIMARY KEY("id_kurs" AUTOINCREMENT)
                )'''
        )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "gruop" (
                "id_gruop" INTEGER NOT NULL,
                "name_gruop" TEXT,
                PRIMARY KEY("id_gruop" AUTOINCREMENT)
                )'''
        )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "otdelenie" (
                "id_otdelenie" INTEGER NOT NULL,
                "name_otdelenie" TEXT,
                PRIMARY KEY("id_otdelenie" AUTOINCREMENT)
                )'''
        )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "pol" (
                "id_pol" INTEGER NOT NULL,
                "name_pol" TEXT,
                PRIMARY KEY("id_pol" AUTOINCREMENT)
                )'''
        )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "vid_finan" (
                "id_finan" INTEGER NOT NULL,
                "name_finan" TEXT,
                PRIMARY KEY("id_finan" AUTOINCREMENT)
                )'''
        )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "spec" (
                "id_spec" INTEGER NOT NULL,
                "name_spec" TEXT,
                PRIMARY KEY("id_spec" AUTOINCREMENT)
                )'''
        )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "students" (
                "id_student" INTEGER NOT NULL,
                "FIO" TEXT,
                "date_dr" DATE,
                "phone_nomber" TEXT,
                "y_post" DATE,
                "y_okon" DATE,
                "n_bilet" TEXT,
                "id_kurs" INTEGER NOT NULL,
                "id_gruop" INTEGER NOT NULL,
                "id_otdelenie" INTEGER NOT NULL,
                "id_pol" INTEGER NOT NULL,
                "id_finan" INTEGER NOT NULL,
                "id_spec" INTEGER NOT NULL,

                PRIMARY KEY("id_student" AUTOINCREMENT)
                )'''
        )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "parents" (
                "id_parent" INTEGER NOT NULL,
                "FIO" TEXT,
                "phone_nomber" TEXT,
                "id_student" INTEGER,
                PRIMARY KEY("id_parent" AUTOINCREMENT)
                )'''
        )

        self.conn.commit()

db = DB()