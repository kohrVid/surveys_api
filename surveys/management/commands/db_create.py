import psycopg2
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Creates the Surveys API database'

    def handle(self, *args, **options):
        create_role = "CREATE ROLE {}".format("surveys_api")

        alter_role = "ALTER ROLE {} WITH SUPERUSER LOGIN CREATEDB;".format(
                "surveys_api",
                )

        alter_role_password = "ALTER ROLE {} password '{}';".format(
                "surveys_api",
                "password",
                )

        create_db = "CREATE DATABASE {} WITH OWNER {} ENCODING 'UTF8';".format(
                "surveys_api",
                "surveys_api",
                )

        conn = psycopg2.connect("dbname=postgres user=postgres")
        conn.set_session(autocommit=True)
        curr = conn.cursor()
        curr.execute(create_role)
        curr.execute(alter_role)
        curr.execute(alter_role_password)
        curr.execute(create_db)
        conn.commit()
        curr.close()
        conn.close()

        self.stdout.write(
                self.style.SUCCESS(
                    "Successfully created the {} database".format("surveys_api")
                    )
            )


