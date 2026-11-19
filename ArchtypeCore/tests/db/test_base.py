from app import models
from db.base import Base


# A check constraint passed to a column is built when the tables are created from the models and
# passed over when a migration is generated from them, so a database built by migrations accepted
# a status the model refuses. A constraint stands on the table, where the generator carries it.
def test_no_column_holds_a_constraint_a_generated_migration_would_pass_over() -> None:
    tables = Base.metadata.tables

    held = [f"{table.name}.{column.name}" for table in tables.values() for column in table.columns if column.constraints]

    assert models.User.__tablename__ in tables
    assert held == []
