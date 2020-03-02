import psycopg2
from decouple import config
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Deletes all rows in the Surveys API database'

    def handle(self, *args, **options):
        truncate_tables = """
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
                ' CASCADE; ALTER TABLE ' || quote_ident(stmt.tablename) ||
                  ' ALTER COLUMN id RESTART WITH 1;';
              END LOOP;
            END;
            $$ LANGUAGE plpgsql;
        """


        clean_db = "{} SELECT truncate_tables('{}');".format(
                truncate_tables,
                config("DATABASE_NAME"),
        )

        conn = psycopg2.connect(
                "dbname={} user={}".format(
                    config("POSTGRES_DB"),
                    config("POSTGRES_USER"),
                )
        )

        conn.set_session(autocommit=True)
        curr = conn.cursor()
        curr.execute(clean_db)
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

