import psycopg2

class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(database="postgres",host = "127.0.0.1", port = "5432", user="postgres")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print("Opened database successfully")

        except:
            print("Cannot connect to datase")

    def create_table(self):
        create_table_command = """CREATE TABLE public."Klausur"
                                (
                                    "Titel" character varying(50) COLLATE pg_catalog."default" NOT NULL,
                                    "pNr" integer NOT NULL,
                                    CONSTRAINT exam_pkey PRIMARY KEY ("pNr")
                                )
                                WITH (
                                    OIDS = FALSE
                                )
                                TABLESPACE pg_default;

                                ALTER TABLE public."Klausur"
                                    OWNER to postgres;



                                CREATE TABLE public."Notenliste"
                                (
                                    "Note" float NOT NULL,
                                    "pNr" integer NOT NULL,
                                    "matNr" integer NOT NULL,
                                    CONSTRAINT "Notenliste_pkey" PRIMARY KEY ("pNr", "matNr")
                                )
                                WITH (
                                    OIDS = FALSE
                                )
                                TABLESPACE pg_default;

                                ALTER TABLE public."Notenliste"
                                    OWNER to postgres;



                                CREATE TABLE public."Student"
                                (
                                    "matNr" integer NOT NULL,
                                    "Name" character varying(50) COLLATE pg_catalog."default" NOT NULL,
                                    "birDate" date,
                                    CONSTRAINT student_pkey PRIMARY KEY ("matNr")
                                )
                                WITH (
                                    OIDS = FALSE
                                )
                                TABLESPACE pg_default;

                                ALTER TABLE public."Student"
                                    OWNER to postgres;	"""

        self.cursor.execute(create_table_command)

    def get_matrikelnummer(self):
        get_matrikeln = "SELECT \"matNr\" from \"Student\""
        self.cursor.execute(get_matrikeln)
        matrikels = self.cursor.fetchall()

        matrikels = [matrikel[0] for matrikel in matrikels]

        return matrikels

    def get_klausurnummer(self):
        get_klausuren = "SELECT \"pNr\" from \"Klausur\";"
        self.cursor.execute(get_klausuren)
        klausuren = self.cursor.fetchall()

        klausuren = [klausur[0] for klausur in klausuren]

        return klausuren

    def create_student(self, info):
        create_student_mat = "INSERT INTO \"Student\"(\"matNr\", \"Name\", \"birDate\") VALUES ({}, '{}', to_timestamp('{}', 'dd-mm-yyyy'));".format(info[0], info[1], info[2])
        self.cursor.execute(create_student_mat)

    def drop_student(self, info):
        drop_student_mat = "DELETE FROM \"Student\" WHERE \"matNr\" = {};".format(info)
        self.cursor.execute(drop_student_mat)

    def create_klausur(self, info):
        create_klausur_mat = "INSERT INTO \"Klausur\"(\"Titel\", \"pNr\") VALUES ('{}', {});".format(info[1], info[0])
        self.cursor.execute(create_klausur_mat)

    def drop_klausur(self, info):
        drop_klausur_mat = "DELETE FROM \"Klausur\" WHERE \"pNr\" = {};".format(info)
        self.cursor.execute(drop_klausur_mat)

    def insert_note(self, info):
        insert_note = "INSERT INTO \"Notenliste\"(\"Note\", \"pNr\", \"matNr\") VALUES ({}, {}, {});".format(info[0], info[1], info[2])
        self.cursor.execute(insert_note)

    def delete_note(self, info):
        delete_note = "DELETE FROM \"Notenliste\" WHERE \"pNr\" = {} AND \"matNr\" = {};".format(info[0], info[1])
        self.cursor.execute(delete_note)

        return self.cursor.statusmessage

    def get_all_noten_by_student(self, info):
        get_all_notes = "SELECT  \"Student\".\"matNr\", \"Name\", \"birDate\" , c.\"Titel\",  a.\"Note\", c.\"Datum\", c.\"pNr\" FROM \"Student\" INNER JOIN (SELECT * FROM \"Notenliste\") a ON \"Student\".\"matNr\" = a.\"matNr\" INNER JOIN (SELECT * FROM \"Klausur\") c ON a.\"pNr\" = c.\"pNr\" WHERE \"Student\".\"matNr\" = {};".format(info)

        self.cursor.execute(get_all_notes)

        notenspiegel_inklv_stammdaten = self.cursor.fetchall()

        if len(notenspiegel_inklv_stammdaten) == 0:
            only_stammdaten_stat = "SELECT * FROM \"Student\" WHERE \"matNr\" = {}".format(info)
            self.cursor.execute(only_stammdaten_stat)

            only_stammdaten = self.cursor.fetchall()

            only_stammdaten.insert(0, "Keine Note(n)")

            print(only_stammdaten)

            return only_stammdaten

        else:

            notenspiegel_inklv_stammdaten.insert(0, "Note(n) vorhanden")

            print(notenspiegel_inklv_stammdaten)

            return notenspiegel_inklv_stammdaten


if __name__== '__main__':
    database_connection = DatabaseConnection()
    #database_connection.get_all_noten_by_student(33)
    #database_connection.create_table()
    #database_connection.insert_new()
    #database_connection.create_student(info=gui.app.student_anlegen())
    #database_connection.get_matrikelnummer()

    # database_connection.create_table()
    # database_connection.insert_new()
    # database_connection.query_all()
    # database_connection.update_record()
    # database_connection.drop_table()
