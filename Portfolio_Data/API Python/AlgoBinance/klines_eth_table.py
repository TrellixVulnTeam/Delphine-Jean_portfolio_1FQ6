from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

def make_databsae():
    """
    Make the Postgres database and create the table
    :return: database connexion
    """

    dbname = 'KlinesEthDB'
    username = 'Delphine'
    tablename = 'klines_eth_table'

    engine = create_engine('postgresql+psycopg2://%slocalhost/%s'%(username,dbname))

    if not database_exists(engine.url):
        create_database(engine.url)

    conn = psycopg2.connect(database = dbname, user = username)

    curr = conn.cursor()
