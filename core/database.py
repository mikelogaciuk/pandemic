from dataclasses import dataclass, field
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
import pyodbc
import cx_Oracle
import logging
import socket

@dataclass
class SqlServer:
    host_name: str
    database: str

    def info(self):
        return f'Connection to SQL Server host: {self.host_name} with database: {self.database} ' \
               f'has been prepared. Please use .query() method to push data into dataframe.'

    def resolve_host(self):
        try:
            socket.gethostbyname(self.host_name)
            return 1
        except socket.error:
            return 0

    def query(self, mssql_query):
        try:
            if self.resolve_host() == 1:
                engine = create_engine(
                    f"mssql+pyodbc://{self.host_name}/{self.database}?driver=SQL+Server+Native+Client+11.0",
                    fast_executemany=True)
                temp = pd.read_sql(mssql_query, engine)
                log.info(f'Data from server: {self.host_name} for: {self.database} database has been requested.')
                engine.dispose()
                return temp
            elif self.resolve_host() == 0:
                log.warning("Error while resolving hostname: {}".format(self.host_name))
        except SQLAlchemyError as err:
            log.warning(err)

    def fetch_table(self, table_name):
        try:
            if self.resolve_host() == 1:
                engine = create_engine(
                    f"mssql+pyodbc://{self.host_name}/{self.database}?driver=SQL+Server+Native+Client+11.0",
                    fast_executemany=True)
                temp = pd.read_sql_table(table_name, engine)
                log.info(
                    f"Data from server: {self.host_name} for whole table: {table_name} "
                    f"from database: {self.database} has been requested.")
                engine.dispose()
                return temp
            elif self.resolve_host() == 0:
                log.warning("Error while resolving hostname: {}".format(self.host_name))
        except SQLAlchemyError as err:
            log.warning(err)

    def push_data(self, data_source, data_target: str, database_schema: str):
        try:
            if self.resolve_host() == 1:
                if database_schema in ('staging'):
                    engine = create_engine(
                        f"mssql+pyodbc://{self.host_name}/{self.database}?driver=SQL+Server+Native+Client+11.0",
                        fast_executemany=True)
                    log.info(f"Data being pushed for: {data_target} in schema: {database_schema} "
                             f"into database: {self.database} at server: {self.host_name}.")
                    data_source.to_sql(data_target, con=engine,
                                  schema=database_schema, if_exists='replace', index=False)
                    log.info(f"Data has been pushed succesfully.")
                else:
                    log.warning(f"Error! Data insert for blocked schema: {database_schema} has been requested. "
                                f"Please review your schema settings. Only schema 'staging' is accepted.")
            elif self.resolve_host() == 0:
                log.warning("Error while resolving hostname: {}".format(self.host_name))
        except SQLAlchemyError as err:
            log.warning(err)
