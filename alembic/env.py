from __future__ import annotations

import sys
from pathlib import Path
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

# ---------------------------------------------------------
# Ensure project root is on sys.path so `import app...` works
# ---------------------------------------------------------
sys.path.append(str(Path(__file__).resolve().parents[1]))

# ---------------------------------------------------------
# Import your settings + metadata
# ---------------------------------------------------------
from app.core.config import get_settings  # noqa: E402
from app.db.base import Base  # noqa: E402
import app.db.models  # noqa: F401, E402  # IMPORTANT: registers models

# Alembic Config object (reads alembic.ini)
config = context.config

# Logging setup (optional)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------
# Metadata for 'autogenerate'
# ---------------------------------------------------------
target_metadata = Base.metadata


def get_url() -> str:
    """Load DB URL from Pydantic settings (.env)."""
    return get_settings().database_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (no DB connection)."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # detect column type changes
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (with DB connection)."""
    connectable = create_engine(
        get_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # detect column type changes
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
