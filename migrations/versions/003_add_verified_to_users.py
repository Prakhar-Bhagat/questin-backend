"""add is_verified to users

Revision ID: 003_add_verified_to_users
Revises: 002_add_name_to_users
Create Date: 2026-05-18
"""
from alembic import op
import sqlalchemy as sa

revision = "003_add_verified_to_users"
down_revision = "44c69e5d8a07"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("is_verified", sa.Boolean(), nullable=False, server_default="false"))
    op.add_column("users", sa.Column("verify_token", sa.String(200), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "verify_token")
    op.drop_column("users", "is_verified")