"""create jobs table

Revision ID: 504c89e07988
Revises: aa676daa2ab8
Create Date: 2022-12-16 22:12:07.093550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '504c89e07988'
down_revision = 'aa676daa2ab8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("jobs",
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('company_name', sa.String,nullable=False),
    sa.Column('job_title', sa.String,nullable=False),
    sa.Column('job_description', sa.String,nullable=False),
    sa.Column('applicant_count', sa.Integer,nullable=False),
    sa.Column('job_location', sa.String,nullable=False),
    sa.Column('job_salary', sa.String,nullable=False),
    sa.Column('date_posted', sa.Date,nullable=False),
    sa.Column('job_posted_date', sa.DateTime, server_default=sa.func.now()),
    sa.Column('job_closing date', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("jobs")