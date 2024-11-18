"""
This module provides a class `TableSelector` for selecting tables from a database connection.
"""

class TableSelector:
    """
    A class used to represent a Table Selector.

    ...

    Attributes
    ----------
    conn : DuckDb.Connection
        a DuckDb database connection
    categories : dict
        a dictionary that categorizes tables into 'original' and 'others'

    Methods
    -------
    get_all_tables():
        Retrieves all tables from the database and categorizes them.
    choose_category():
        Prompts the user to choose a category of tables.
    choose_table(category):
        Prompts the user to choose a table from the chosen category.
    """

    def __init__(self, conn):
        """
        Constructs all the necessary attributes for the TableSelector object.

        Parameters
        ----------
            conn : DuckDb.Connection
                a DuckDb database connection
        """
        self.conn = conn
        self.categories = {
            'original': [],
            'others': []
        }
        self.get_all_tables()

    def get_all_tables(self):
        """
        Retrieves all tables from the database and categorizes them into 'original' and 'others'.
        """
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA show_tables")
        rows = cursor.fetchall()
        tables = [row[0] for row in rows]

        self.categories['original'] = [
            table for table in tables
            if '_original' in table and 'tokmanni_original' not in table
        ]

        self.categories['others'] = [
            table for table in tables
            if table not in self.categories['original']
        ]

    def choose_category(self):
        """
        Prompts the user to choose a category of tables.

        Returns
        -------
        str
            The chosen category.
        """
        print("Choose a category:")
        for i, category in enumerate(self.categories.keys()):
            print(f"{i+1}. {category}")
        choice = int(input("Enter the number of your choice: "))
        return list(self.categories.keys())[choice-1]

    def choose_table(self, category):
        """
        Prompts the user to choose a table from the chosen category.

        Parameters
        ----------
        category : str
            The chosen category.

        Returns
        -------
        str
            The chosen table.
        """
        tables = self.categories[category]
        print("Choose a table:")
        for i, table in enumerate(tables):
            print(f"{i+1}. {table}")
        choice = int(input("Enter the number of your choice: "))
        return tables[choice-1]
