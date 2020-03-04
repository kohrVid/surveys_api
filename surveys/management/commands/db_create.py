import psycopg2
from psycopg2 import sql
from decouple import config
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates the Surveys API database'

    def handle(self, *args, **options):
        create_role = sql.SQL("CREATE ROLE {}").format(
                sql.Identifier(config("DATABASE_USER"))
        )

        alter_role = sql.SQL("ALTER ROLE {} WITH SUPERUSER LOGIN CREATEDB;").format(
                sql.Identifier(config("DATABASE_USER"))
        )

        alter_role_password = sql.SQL("ALTER ROLE {} password '{}';").format(
                sql.Identifier(config("DATABASE_USER")),
                sql.Identifier(config("DATABASE_PASSWORD")),
        )

        create_db = sql.SQL("CREATE DATABASE {} WITH OWNER {} ENCODING 'UTF8';").format(
                sql.Identifier(config("DATABASE_NAME")),
                sql.Identifier(config("DATABASE_USER")),
        )

        conn = psycopg2.connect(
                database=config("POSTGRES_DB"),
                user=config("POSTGRES_USER")
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


