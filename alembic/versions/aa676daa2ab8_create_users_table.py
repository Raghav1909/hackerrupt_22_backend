"""create users table

Revision ID: aa676daa2ab8
Revises: 
Create Date: 2022-12-16 20:53:11.140265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa676daa2ab8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('username', sa.String, unique=True, index=True,nullable=False),
    sa.Column('first_name', sa.String,nullable=True),
    sa.Column('last_name', sa.String,nullable= True),
    sa.Column('email', sa.String, unique=True, index=True,nullable=False),
    sa.Column('password', sa.String,nullable=False),
    sa.Column('is_admin', sa.Boolean, default=False),
    sa.Column('date_of_birth', sa.Date,nullable=True),
    sa.Column('phone_no', sa.String, unique=True,nullable=True),
    sa.Column('professional_summary', sa.String,nullable=True),
    )

def downgrade() -> None:
    op.drop_table("users")