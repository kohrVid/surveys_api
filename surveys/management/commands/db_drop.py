import psycopg2
from decouple import config
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Drops the Surveys API database'

    def handle(self, *args, **options):
        drop_database = "DROP DATABASE {};".format(config("DATABASE_NAME"))
        drop_role = "DROP ROLE {}".format(config("DATABASE_USER"))

        conn = psycopg2.connect("dbname=postgres user=postgres")
        conn.set_session(autocommit=True)
        curr = conn.cursor()
        curr.execute(drop_database)
        curr.execute(drop_role)
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

