import os
import unittest

from views import app, db
from config import basedir
from models import User

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

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

    # login helper function
    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password),
            follow_redirects=True)

    def register(self, name, email, password, confirm):
        return self.app.post('/register', data=dict(
            name=name, email=email, password=password, confirm=confirm),
            follow_redirects=True)

    # each test should start with 'test'
    def test_users_can_register(self):
        new_user = User("mherman", "michael@mherman.org", "michaelherman")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == 'mherman'

    def test_form_is_present_on_login_page(self):
        #import pdb;pdb.set_trace()
        response = self.app.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Please sign in to access your task list', 
            response.get_data())

    def test_users_cannot_login_unless_registered(self):
        #import pdb;pdb.set_trace()
        response = self.login('foo', 'bar')
        self.assertIn('Invalid username or password', response.get_data())

    def test_users_can_login(self):
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        response = self.login('Michael', 'python')
        self.assertIn('You are logged in.  Go Crazy.', response.get_data())

    def test_invalid_form_data(self):
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        response = self.login('alert("alert box!");', 'foo')
        self.assertIn('Invalid username or password', response.get_data())

    def test_form_is_present_on_register_page(self):
        response = self.app.get('/register')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Please register to start a task list', 
            response.get_data())

if __name__ == "__main__":
    unittest.main()