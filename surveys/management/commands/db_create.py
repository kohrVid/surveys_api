import psycopg2
from decouple import config
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Creates the Surveys API database'

    def handle(self, *args, **options):
        create_role = "CREATE ROLE {}".format(config("DATABASE_USER"))

        alter_role = "ALTER ROLE {} WITH SUPERUSER LOGIN CREATEDB;".format(
                config("DATABASE_USER"),
        )

        alter_role_password = "ALTER ROLE {} password '{}';".format(
                config("DATABASE_USER"),
                config("DATABASE_PASSWORD"),
        )

        create_db = "CREATE DATABASE {} WITH OWNER {} ENCODING 'UTF8';".format(
                config("DATABASE_NAME"),
                config("DATABASE_USER"),
        )

        conn = psycopg2.connect(
                "dbname={} user={}".format(
                    config("POSTGRES_DB"),
                    config("POSTGRES_USER"),
                )
        )

        conn.set_session(autocommit=True)
        curr = conn.cursor()

        try:
            curr.execute(create_role)
        except psycopg2.errors.DuplicateObject as err:
            print(err)
        finally:
            curr.execute(alter_role)
            curr.execute(alter_role_password)
            curr.execute(create_db)
            curr.close()
            conn.commit()
            conn.close()

        self.stdout.write(
                self.style.SUCCESS(
                    "Successfully created the {} database".format(config("DATABASE_NAME"))
                )
        )


