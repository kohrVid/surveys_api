import psycopg2
from psycopg2 import sql
from decouple import config
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Drops the Surveys API database'

    def handle(self, *args, **options):
        drop_database = sql.SQL("DROP DATABASE {};").format(
                sql.Identifier(config("DATABASE_NAME")),
        )

        drop_role = sql.SQL("DROP ROLE {};").format(
                sql.Identifier(config("DATABASE_USER")),
        )

        conn = psycopg2.connect(
                database=config("POSTGRES_DB"),
                user=config("POSTGRES_USER")
        )

        conn.set_session(autocommit=True)
        curr = conn.cursor()
        conn.cursor().execute(drop_database)
        conn.cursor().execute(drop_role)
        conn.commit()
        curr.close()
        conn.close()

        self.stdout.write(
                self.style.SUCCESS(
                    "Successfully dropped the {} database".format(
                        config("DATABASE_NAME"),
                    )
                )
        )

