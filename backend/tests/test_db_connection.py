import pytest
import os
from utilities.db_connection import get_db_connection
from unittest.mock import patch
import psycopg2

def test_missing_database_url(mocker):
    mocker.patch('os.environ.get', return_value=None)
    with pytest.raises(OSError):
        get_db_connection()

def test_incorrect_database_url_format(mocker):
    mocker.patch('os.environ.get', return_value='invalid_format_url')
    with pytest.raises(ValueError):
        get_db_connection()

def test_database_connection_failure(mocker):
    mocker.patch('os.environ.get', return_value='postgresql://username:password@host:5432/dbname')
    mocker.patch('psycopg2.connect', side_effect=psycopg2.Error)
    with pytest.raises(ConnectionError):
        get_db_connection()
    
def test_unexpected_error(mocker):
    mocker.patch('os.environ.get', side_effect=Exception("Unexpected error"))
    with pytest.raises(Exception):
        get_db_connection()