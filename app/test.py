import unittest
import mysql.connector
from flask import Flask
from app import start_new_game, start_new_round, save_score  # Import the functions you need

class TestMySQLConnection(unittest.TestCase):

    def test_mysql_connection(self):
        # Configure your MySQL connection information here
        db_config = {
            "host": "127.0.0.1",
            "user": "root",
            "password": "",
            "database": "PlayerData"
        }

        try:
            # Try to establish a connection to the MySQL database
            connection = mysql.connector.connect(**db_config)

            # Check if the connection was successful
            self.assertTrue(connection.is_connected())

            # Close the connection
            connection.close()

        except mysql.connector.Error as err:
            # Handle any errors (e.g., wrong credentials)
            print(f"Error: {err}")
            self.fail("MySQL connection failed")

    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = "your_secret_key"

    def test_start_new_game(self):
        with self.app.test_request_context('/play'):
            with self.app.test_client() as client:
                with client.session_transaction() as session:
                    start_new_game()
                    self.assertEqual(session['score'], 0)
                    self.assertEqual(session['guessScore'], 0)
    def test_start_new_round(self):
        with self.app.test_request_context('/play'):
            with self.app.test_client() as client:
                with client.session_transaction() as session:
                    start_new_round()
                    self.assertIn('target_number', session)
                    self.assertIsInstance(session['target_number'], int)

    def test_save_score(self):
        with self.app.test_request_context('/endscreen'):
            with self.app.test_client() as client:
                with client.session_transaction() as session:
                    player_name = "TestPlayer"
                    score = 42
                    save_score(player_name, score)
                    # You can add assertions here to verify the score is saved correctly in the database

if __name__ == '__main__':
    unittest.main()
