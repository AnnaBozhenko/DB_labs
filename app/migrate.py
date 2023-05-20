# import names of files for migration
from dump import migration2_name, migration3_name, migration4_name, migration5_name, migration6_name, migration7_name, migration8_name, migration9_name, migration10_name, migration11_name

migration_files = [migration2_name, migration3_name, migration4_name, migration5_name, migration6_name, migration7_name, migration8_name, migration9_name, migration10_name, migration11_name]


from dump import transaction

@transaction
def migrate(conn):
    """migrate schema"""
    with conn.cursor() as cur:
        for file_name in migration_files:
            with open(file_name) as f:
                queries = [el for el in f.read().split(";") if el != ""]
                [cur.execute(query) for query in queries]
                conn.commit()


if __name__ == "__main__":
    migrate()
    