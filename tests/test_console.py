#!/usr/bin/python3
"""A unit test module for the console (command interpreter).
"""
import json
import MySQLdb
import os
import sqlalchemy
import unittest
from io import StringIO
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from tests import clear_stream


class TestHBNBCommand(unittest.TestCase):
    """Represents the test class for the HBNBCommand class.
    """
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_create(self):
        """Tests the create command with the file storage.
        """
        with patch('sys.stdout', new=StringIO()) as output:
            conn = HBNBCommand()
            conn.onecmd('create City name="Texas"')
            mdl_id = output.getvalue().strip()
            clear_stream(output)
            self.assertIn('City.{}'.format(mdl_id), storage.all().keys())
            conn.onecmd('show City {}'.format(mdl_id))
            self.assertIn("'name': 'Texas'", output.getvalue().strip())
            clear_stream(output)
            conn.onecmd('create User name="James" age=17 height=5.9')
            mdl_id = output.getvalue().strip()
            self.assertIn('User.{}'.format(mdl_id), storage.all().keys())
            clear_stream(output)
            conn.onecmd('show User {}'.format(mdl_id))
            self.assertIn("'name': 'James'", output.getvalue().strip())
            self.assertIn("'age': 17", output.getvalue().strip())
            self.assertIn("'height': 5.9", output.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """Tests the create command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as output:
            conn = HBNBCommand()
            # creating a model with non-null attribute(s)
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                conn.onecmd('create User')
            # creating a User instance
            clear_stream(output)
            conn.onecmd('create User email="john25@gmail.com" password="123"')
            mdl_id = output.getvalue().strip()
            db_meta = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_meta.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(mdl_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('john25@gmail.com', result)
            self.assertIn('123', result)
            cursor.close()
            db_meta.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """Tests the show command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as output:
            conn = HBNBCommand()
            # showing a User instance
            obj = User(email="john25@gmail.com", password="123")
            db_meta = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_meta.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is None)
            conn.onecmd('show User {}'.format(obj.id))
            self.assertEqual(
                output.getvalue().strip(),
                '** no instance found **'
            )
            obj.save()
            db_meta = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_meta.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            clear_stream(output)
            conn.onecmd('show User {}'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('john25@gmail.com', result)
            self.assertIn('123', result)
            self.assertIn('john25@gmail.com', output.getvalue())
            self.assertIn('123', output.getvalue())
            cursor.close()
            db_meta.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """Tests the count command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as output:
            conn = HBNBCommand()
            db_meta = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_meta.cursor()
            cursor.execute('SELECT COUNT(*) FROM states;')
            result = cursor.fetchone()
            prev_count = int(result[0])
            conn.onecmd('create State name="Enugu"')
            clear_stream(output)
            conn.onecmd('count State')
            count = output.getvalue().strip()
            self.assertEqual(int(count), prev_count + 1)
            clear_stream(output)
            conn.onecmd('count State')
            cursor.close()
            db.close()
