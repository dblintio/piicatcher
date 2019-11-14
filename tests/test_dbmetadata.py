from unittest import TestCase
from piicatcher.db.metadata import Column, Table, Schema


class DbMetadataTests(TestCase):

    data = {
        "no_pii": [
            ('abc', 'def'),
            ('xsfr', 'asawe')
        ],
        "partial_pii": [
            ('917-908-2234', 'plkj'),
            ('215-099-2234', 'sfrf')
        ],
        "full_pii": [
            ('Jonathan Smith', 'Virginia'),
            ('Chase Ryan', 'Chennai')
        ]
    }

    @staticmethod
    def data_generator(schema_name, table_name, column_list):
        for row in DbMetadataTests.data[table_name.get_name()]:
            yield row

    def test_negative_scan_column(self):
        col = Column('col')
        col.scan('abc')
        self.assertFalse(col.has_pii())

    def test_positive_scan_column(self):
        col = Column('col')
        col.scan('Jonathan Smith')
        self.assertTrue(col.has_pii())

    def test_null_scan_column(self):
        col = Column('col')
        col.scan(None)
        self.assertFalse(col.has_pii())

    def test_no_pii_table(self):
        schema = Schema('public')
        table = Table(schema, 'no_pii')
        table.add(Column('a'))
        table.add(Column('b'))

        table.scan(self.data_generator)
        self.assertFalse(table.has_pii())

    def test_partial_pii_table(self):
        schema = Schema('public')
        table = Table(schema, 'partial_pii')
        table.add(Column('a'))
        table.add(Column('b'))

        table.scan(self.data_generator)
        self.assertTrue(table.has_pii())
        cols = table.get_columns()
        self.assertTrue(cols[0].has_pii())
        self.assertFalse(cols[1].has_pii())

    def test_full_pii_table(self):
        schema = Schema('public')
        table = Table(schema, 'full_pii')
        table.add(Column('name'))
        table.add(Column('location'))

        table.scan(self.data_generator)
        self.assertTrue(table.has_pii())

        cols = table.get_columns()
        self.assertTrue(cols[0].has_pii())
        self.assertTrue(cols[1].has_pii())


class ShallowScan(TestCase):
    def test_no_pii_table(self):
        schema = Schema('public')
        table = Table(schema, 'no_pii')
        table.add(Column('a'))
        table.add(Column('b'))

        table.shallow_scan()
        self.assertFalse(table.has_pii())

    def test_partial_pii_table(self):
        schema = Schema('public')
        table = Table(schema, 'partial_pii')
        table.add(Column('fname'))
        table.add(Column('b'))

        table.shallow_scan()
        self.assertTrue(table.has_pii())
        cols = table.get_columns()
        self.assertTrue(cols[0].has_pii())
        self.assertFalse(cols[1].has_pii())

    def test_full_pii_table(self):
        schema = Schema('public')
        table = Table(schema, 'full_pii')
        table.add(Column('name'))
        table.add(Column('dob'))

        table.shallow_scan()
        self.assertTrue(table.has_pii())

        cols = table.get_columns()
        self.assertTrue(cols[0].has_pii())
        self.assertTrue(cols[1].has_pii())

