"""create company table

Revision ID: 82c1c9013bee
Revises: 504c89e07988
Create Date: 2022-12-16 22:25:15.692318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82c1c9013bee'
down_revision = '504c89e07988'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("company",
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('company_logo', sa.Integer,nullable=False),
    sa.Column('company_name', sa.String,nullable=False),
    sa.Column('company_website', sa.String,nullable=False),
    sa.Column('company_description', sa.String,nullable=False))

def downgrade() -> None:
    op.drop_table("company")
