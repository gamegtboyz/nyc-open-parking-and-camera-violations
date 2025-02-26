def load():
    # download the relevant library
    import pandas as pd
    from sqlalchemy import create_engine

    # import the connection_string set in config.db_config
    from config.db_config import connection_string

    # download the file from transformed data
    data = pd.read_csv('data/data.csv')

    # create database connection using connection string
    engine = create_engine(connection_string)

    # create the new table into the database
    table_name = 'opcv_data'

    # create the writing condition and results
    try:
        data.to_sql(table_name,engine,if_exists='replace',index=False)
        print(f"Data was loaded into '{table_name}' table successfully.")
    except Exception as e:
        print("Error: ", e)

    # after complete writing into the database, close the connection
    engine.dispose()