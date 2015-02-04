import os
import unittest

from project import app, db, bcrypt
from config import basedir
from project.models import User

TEST_DB = 'test.db'

class TestUsers(unittest.TestCase):

        # executed prior to each test
    def setUp(self):
        app.config['DEBUG'] = False
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
        return self.app.post('/users/', data=dict(name=name, password=password),
            follow_redirects=True)

    def register(self, name="Michael", email="michael@realpython.com", 
        password="python", confirm="python"):
        return self.app.post('/users/register/', data=dict(
            name=name, 
            email=email, 
            password=password, 
            confirm=confirm),
            follow_redirects=True)

    def logout(self):
        return self.app.get('/users/logout', follow_redirects=True)

    def create_user(self, name="Michael", email="Michael@realpython.com", 
        password="python"):
        new_user = User(
            name=name, 
            email=email, 
            password=bcrypt.generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()


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
        response = self.app.get('/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn('Please sign in to access your task list', 
            response.get_data())

    def test_users_cannot_login_unless_registered(self):
        #import pdb;pdb.set_trace()
        response = self.login('foo', 'bar')
        self.assertIn('Invalid username or password', response.get_data())

    def test_users_can_login(self):
        self.register()
        response = self.login('Michael', 'python')
        self.assertIn('You are logged in.  Go Crazy.', response.get_data())

    def test_invalid_form_data(self):
        self.register()
        response = self.login('alert("alert box!");', 'foo')
        self.assertIn('Invalid username or password', response.get_data())

    def test_form_is_present_on_register_page(self):
        response = self.app.get('/users/register/')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Please register to start a task list', 
            response.get_data())

    def test_user_registration(self):
        self.app.get('/users/register/', follow_redirects=True)
        response = self.register()
        assert 'Thanks for registering.  Please login' in response.get_data()

    def test_duplicate_user_registration_throws_error(self):
        #self.app.get('/register', follow_redirects=True)
        self.register()

        #self.app.get('/register', follow_redirects=True)
        response = self.register()

        self.assertIn(
            'Oh no! That username and/or email already exists.',
            response.get_data())

    def test_logged_in_users_can_logout(self):
        self.register('Fletcher', 'fletcher@realpython.com',
            'python101', 'python101')
        self.login('Fletcher', 'python101')
        response = self.logout()
        self.assertIn('You are logged out. Bye. :(', response.get_data())

    def test_not_logged_in_user_cant_logout(self):
        response = self.logout()
        self.assertNotIn('You are logged out. Bye. :(', response.get_data())

    def test_default_user_role(self):
        db.session.add(
            User(
                "Johnny",
                "john@doe.com",
                "johnny"
                )
            )
        db.session.commit()

        users = db.session.query(User).all()
        print users
        for user in users:
            self.assertEquals(user.role, 'user')

    def test_404_error(self):
        response = self.app.get('/this-route-does-not-exist')
        self.assertEquals(response.status_code, 404)
        self.assertIn('Sorry. There\'s nothing here.', response.data)

    def test_500_error(self):
        bad_user = User(
            name = 'Jeremy',
            email = 'jeremy@realpython.com',
            password = 'django'
            )
        db.session.add(bad_user)
        db.session.commit()
        response = self.login('Jeremy', 'django')
        self.assertEquals(response.status_code, 500)
        self.assertNotIn('ValueError: Invalid salt', response.data)
        self.assertIn('Something went terribly wrong.', response.data)



if __name__ == "__main__":
    unittest.main()