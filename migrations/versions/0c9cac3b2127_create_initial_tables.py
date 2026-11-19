"""create initial tables

Revision ID: 0c9cac3b2127
Revises: 
Create Date: 2026-10-31 16:59:39.122467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c9cac3b2127'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=150), nullable=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('firebase_uid', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_firebase_uid'), 'users', ['firebase_uid'], unique=True)

    # 2. resumes
    op.create_table(
        'resumes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('extracted_text', sa.Text(), nullable=True),
        sa.Column('file_type', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_resumes_id'), 'resumes', ['id'], unique=False)
    op.create_index(op.f('ix_resumes_user_id'), 'resumes', ['user_id'], unique=False)

    # 3. job_descriptions
    op.create_table(
        'job_descriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_job_descriptions_id'), 'job_descriptions', ['id'], unique=False)
    op.create_index(op.f('ix_job_descriptions_user_id'), 'job_descriptions', ['user_id'], unique=False)

    # 4. resume_analyses
    op.create_table(
        'resume_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('job_description_id', sa.Integer(), nullable=False),
        sa.Column('match_score', sa.Float(), nullable=False),
        sa.Column('text_similarity', sa.Float(), nullable=True),
        sa.Column('report', sa.JSON(), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='completed'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['job_description_id'], ['job_descriptions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_resume_analyses_id'), 'resume_analyses', ['id'], unique=False)
    op.create_index(op.f('ix_resume_analyses_job_description_id'), 'resume_analyses', ['job_description_id'], unique=False)
    op.create_index(op.f('ix_resume_analyses_resume_id'), 'resume_analyses', ['resume_id'], unique=False)

    # 5. recommendations
    op.create_table(
        'recommendations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('analysis_id', sa.Integer(), nullable=False),
        sa.Column('recommendation_type', sa.String(length=50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['analysis_id'], ['resume_analyses.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_recommendations_id'), 'recommendations', ['id'], unique=False)
    op.create_index(op.f('ix_recommendations_analysis_id'), 'recommendations', ['analysis_id'], unique=False)


def downgrade() -> None:
    op.drop_table('recommendations')
    op.drop_table('resume_analyses')
    op.drop_table('job_descriptions')
    op.drop_table('resumes')
    op.drop_table('users')
