import datetime
import io

from logger import get_logger
from sqlite_extractor import SQLiteLoader


logger = get_logger(__name__)


class PostgresSaver(SQLiteLoader):
    '''Class for saving data from SQLite DB to PostgreSQL DB.'''

    def save_all_data(self, data_from_sql):
        '''Saving all data method.'''

        # check running save_current_table() method
        logger.info('Running save_table_data() method')

        # set current time to start var
        start = datetime.datetime.now()

        for page in data_from_sql:
            page_values = '\n'.join([record.values for record in page])
            with io.StringIO(page_values) as result:
                self.cursor.copy_from(result, table=self.table_name, null='None', size=self.page_size)

        # display saving process time for every table
        logger.info('Saved data for ' + str(datetime.datetime.now() - start))