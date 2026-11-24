import shutil
from pathlib import Path

from alembic import command
from alembic.config import Config

from db.base import Base
from db.types import UTCDateTime

ENVIRONMENT = Path(__file__).resolve().parents[3] / "db" / "migrations"


# A revision generated from the models named db.types.UTCDateTime without importing it, so applying it failed, and the
# renderer that names the stored type instead holds only where the environment hands it to Alembic. The revision is
# generated over the suite's database, which holds no table, in a copy of the environment that holds no revision and
# runs no write hook, and is applied once it has been read.
def test_a_revision_generated_from_the_models_applies_and_names_only_what_the_database_stores(tmp_path: Path) -> None:
    scripts = tmp_path / "migrations"
    (scripts / "versions").mkdir(parents=True)
    for name in ("env.py", "script.py.mako"):
        shutil.copy(ENVIRONMENT / name, scripts / name)
    config = Config()
    config.set_main_option("script_location", str(scripts))

    command.revision(config, message="every table", autogenerate=True)
    revision = next((scripts / "versions").glob("*.py")).read_text(encoding="utf-8")
    stamps = sum(isinstance(column.type, UTCDateTime) for table in Base.metadata.tables.values() for column in table.columns)

    assert stamps > 0
    assert revision.count("sa.DateTime(timezone=True)") == stamps
    assert "db.types" not in revision
    command.upgrade(config, "head")
