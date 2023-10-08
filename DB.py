import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('res\\students_bd.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "kurs" (
                "id_kurs" INTEGER NOT NULL,
                "N_kurs" INTEGER NOT NULL,
                PRIMARY KEY("id_kurs" AUTOINCREMENT)
                )'''
        )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "gruop" (
                "id_gruop" INTEGER NOT NULL,
                "name_gruop" TEXT NOT NULL,
                PRIMARY KEY("id_gruop" AUTOINCREMENT)
                )'''
        )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "otdelenie" (
                "id_otdelenie" INTEGER NOT NULL,
                "name_otdelenie" TEXT NOT NULL,
                PRIMARY KEY("id_otdelenie" AUTOINCREMENT)
                )'''
        )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "pol" (
                "id_pol" INTEGER NOT NULL,
                "name_pol" TEXT NOT NULL,
                PRIMARY KEY("id_pol" AUTOINCREMENT)
                )'''
        )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "vid_finan" (
                "id_finan" INTEGER NOT NULL,
                "name_finan" TEXT NOT NULL,
                PRIMARY KEY("id_finan" AUTOINCREMENT)
                )'''
        )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "spec" (
                "id_spec" INTEGER NOT NULL,
                "name_spec" TEXT NOT NULL,
                PRIMARY KEY("id_spec" AUTOINCREMENT)
                )'''
        )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "students" (
                "id_student" INTEGER NOT NULL,
                "FIO" TEXT NOT NULL,
                "date_dr" DATE NOT NULL,
                "phone_nomber" TEXT NOT NULL,
                "y_post" DATE NOT NULL,
                "y_okon" DATE NOT NULL,
                "n_bilet" TEXT NOT NULL,
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
                "FIO" TEXT NOT NULL,
                "phone_nomber" TEXT NOT NULL,
                "id_student" INTEGER NOT NULL,
                PRIMARY KEY("id_parent" AUTOINCREMENT)
                )'''
        )

        self.conn.commit()

if __name__ == "__main__":
    db = DB()