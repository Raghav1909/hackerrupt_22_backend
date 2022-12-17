"""create work experience table

Revision ID: d62e3eccd3fb
Revises: 9d1c51516839
Create Date: 2022-12-16 23:37:14.601327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd62e3eccd3fb'
down_revision = '9d1c51516839'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'work_experience',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('start_date', sa.DateTime, nullable=False),
        sa.Column('end_date', sa.DateTime, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('work_experience')
