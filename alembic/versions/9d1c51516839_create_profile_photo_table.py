"""create profile photo table

Revision ID: 9d1c51516839
Revises: 82c1c9013bee
Create Date: 2022-12-16 22:36:50.290276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d1c51516839'
down_revision = '82c1c9013bee'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("profile_photos",
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'),nullable=False),
    sa.Column('photo', sa.String,nullable=False))


def downgrade() -> None:
    os.drop_table("profile_photos")
