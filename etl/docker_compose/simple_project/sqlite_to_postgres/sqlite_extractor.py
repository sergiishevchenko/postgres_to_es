from logger import get_logger


logger = get_logger(__name__)


class SQLiteLoader:
    '''Class for extraction data from SQLite DB.'''

    def __init__(self, connection, table_name, table_model, page_size):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.table_name = table_name
        self.table_model = table_model
        self.page_size = page_size
        self.cursor.execute(f'SELECT * FROM {self.table_name}')

    def extract_movies(self):
        '''Method of extraction data from SQLite DB'''

        logger.info('Running extract_movies() method')

        while True:
            page_rows = self.cursor.fetchmany(size=self.page_size)
            if not page_rows:
                break
            page = []
            for row in page_rows:
                data = self.table_model(*row)
                page.append(data)
            yield page

    def __del__(self):
        self.cursor.close()