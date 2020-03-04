import psycopg2
from decouple import config
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Deletes all rows in the Surveys API database'

    def handle(self, *args, **options):
        stored_proc = """
            CREATE OR REPLACE FUNCTION truncate_tables(username IN VARCHAR) RETURNS void AS $$
            DECLARE
              statements CURSOR FOR
                  SELECT
                    tablename
                  FROM pg_tables
                  WHERE tableowner = username
                    AND schemaname = 'public'
                    AND tablename NOT LIKE 'django_%';

            BEGIN
              FOR stmt IN statements LOOP
                EXECUTE 'TRUNCATE TABLE ' || quote_ident(stmt.tablename) ||
                ' CASCADE; ALTER SEQUENCE ' || stmt.tablename ||'_id_seq RESTART WITH 1;';
              END LOOP;
            END;
            $$ LANGUAGE plpgsql;
        """

        conn = psycopg2.connect(
                database=config("DATABASE_NAME"),
                user=config("DATABASE_USER")
        )

        curr = conn.cursor()
        curr.execute(stored_proc)
        curr.execute("SELECT truncate_tables(%s);", [config("DATABASE_USER")])
        conn.commit()
        curr.close()
        conn.close()

        self.stdout.write(
                self.style.SUCCESS(
                    "Successfully deleted all rows in the {} database".format(
                        config("DATABASE_NAME"),
                    )
                )
        )

