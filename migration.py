from alembic import op
import sqlalchemy as sa
from sqlalchemy import String, Column
from sqlalchemy.sql import table, column

from alembic import context


# revision = '3ba2b522d10d'
# down_revision = None



# def upgrade():
#     schema_upgrades()
#     if context.get_x_argument(as_dictionary=True).get('data', None):
#         data_upgrades()
#
# def downgrade():
#     if context.get_x_argument(as_dictionary=True).get('data', None):
#         data_downgrades()
#     schema_downgrades()
#
# def schema_upgrades():
#     """schema upgrade migrations go here."""
#     op.create_table("my_table", Column('data', String))
#
# def schema_downgrades():
#     """schema downgrade migrations go here."""
#     op.drop_table("my_table")
#
# def data_upgrades():
#     """Add any optional data upgrade migrations here!"""
#
#     my_table = table('my_table',
#         column('data', String),
#     )
#
#     op.bulk_insert(my_table,
#         [
#             {'data': 'data 1'},
#             {'data': 'data 2'},
#             {'data': 'data 3'},
#         ]
#     )
#
# def data_downgrades():
#     """Add any optional data downgrade migrations here!"""
#
#     op.execute("delete from my_table")
#
#


def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))


def downgrade():
    op.drop_column('account', 'last_transaction_date')

upgrade()
downgrade()