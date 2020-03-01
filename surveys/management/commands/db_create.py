import os
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


