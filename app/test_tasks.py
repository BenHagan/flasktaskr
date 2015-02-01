import os
import unittest

from views import app, db
from config import basedir
from models import User

TEST_DB = 'test.db'

class TestTasks(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.drop_all()

    def register(self, name="Michael", email="michael@realpython.com", 
        password="python", confirm="python"):
        return self.app.post('/register', data=dict(
            name=name, email=email, password=password, confirm=confirm),
            follow_redirects=True)

    def create_user(self, name="Michael", email="Michael@realpython.com", 
        password="python"):
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post('add/', data=dict(
            name='Go to the bank',
            due_date='02/05/2014',
            priority='1',
            posted_date='02/04/2014',
            status=1), follow_redirects=True)

    # login helper function
    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password),
            follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_logged_in_users_can_access_tasks_page(self):
        self.register('Fletcher', 'fletcher@realpython.com',
            'python101', 'python101')
        self.login('Fletcher', 'python101')
        response = self.app.get('/tasks')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Add a new task:', response.get_data())

    def test_not_logged_in_users_cannot_access_tasks_page(self):
        response = self.app.get('/tasks', follow_redirects=True)
        self.assertIn('You need to login first.', response.get_data())

    def test_users_can_add_tasks(self):
        self.create_user()
        self.login('Michael', 'python')
        self.app.get('/tasks', follow_redirects=True)
        response = self.create_task()
        self.assertIn(
            'New entry was successfully posted. Thanks.', response.get_data())

    def test_users_cannot_add_tasks_when_error(self):
        self.create_user()
        self.login('Michael', 'python')
        self.app.get('/tasks', follow_redirects=True)
        #import pdb;pdb.set_trace()
        response = self.app.post('/add/', data=dict(
            name='Go to the bank',
            due_date='',
            priority='1',
            posted_date='02/04/2014',
            status=1), follow_redirects=True)
        self.assertIn('This field is required.', response.get_data())

    def test_users_can_complete_tasks(self):
        self.create_user()
        self.login('Michael', 'python')
        self.app.get('/tasks', follow_redirects=True)
        self.create_task()
        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertIn('The task was marked as complete. Nice.', 
            response.get_data())

    def test_users_can_delete_tasks(self):
        self.create_user()
        self.login('Michael', 'python')
        self.app.get('/tasks', follow_redirects=True)
        self.create_task()
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn('The task was deleted', response.get_data())

    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.create_user()
        self.login('Michael', 'python')
        self.app.get('/tasks', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
        self.login('Fletcher', 'python101')
        self.app.get('/tasks', follow_redirects=True)
        response=self.app.get("complete/1/", follow_redirects=True)
        self.assertIn('You can only update tasks that belong to you',
         response.get_data())

    def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
        self.create_user()
        self.login('Michael', 'python')
        self.app.get('/tasks', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
        self.login('Fletcher', 'python101')
        self.app.get('/tasks', follow_redirects=True)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn(
            'You can only delete tasks that belong to you.', 
            response.get_data()
        )

if __name__ == "__main__":
    unittest.main()