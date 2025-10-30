import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# -----------------------------
# 1️⃣ Setup Python path
# -----------------------------
# Add project root to sys.path so we can import seed.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# -----------------------------
# 2️⃣ Load dotenv
# -----------------------------
from dotenv import load_dotenv
load_dotenv()  # will load DATABASE_URL from .env

# -----------------------------
# 3️⃣ Import your SQLAlchemy Base
# -----------------------------
from seed import Base

# -----------------------------
# 4️⃣ Alembic config
# -----------------------------
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for 'autogenerate' support
target_metadata = Base.metadata

# -----------------------------
# 5️⃣ Migration functions
# -----------------------------
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = os.getenv("DATABASE_URL")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    from sqlalchemy import create_engine

    connectable = create_engine(os.getenv("DATABASE_URL"), poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# -----------------------------
# 6️⃣ Run migration
# -----------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
