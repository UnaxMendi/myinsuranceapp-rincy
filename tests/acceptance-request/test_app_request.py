# see the comments in acceptance-flask/test_app_flask_tester.py file first.
import json
import unittest
import requests # import the reques library for sending requests to real running endpoints

# as you can see we DON'T import the app from project, since we are going to test the running app
# for that reason, you must first start the app, before passing the test

class TestApp(unittest.TestCase):
    token=''

    # define a variable for the base API url to be tested. We will concat the endpoint to this.
    base_url='http://localhost:5000/api/v1'

    def test_1_getToken(self):
        # defines the url...in this case: will be: http://localhost:5000/api/v1/token
        url=f"{self.base_url}/token"
        test_data = {"email":"jd@myinsuranceapp.com","password":"passwordjd"}

        # here we are using the request library to send the POST request data to the url
        # this is really the only difference with the flask based tests
        response = requests.post(url, json=test_data)
        data=json.loads(response.text)
        print(f"post: {data}")
        self.assertEqual(response.status_code, 200)
        if response.status_code==200:
            TestApp.token=data['token']

    def test_2_get_user_products_valid_token(self):
        url=f"{self.base_url}/users/1/products"
        print(f"token: {self.token}")
        headers = {"Authorization": f"Bearer {TestApp.token}"}
        response = requests.get(url, headers=headers)
        data=json.loads(response.text)
        print(f"get_user_products: {data}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data)>0)

    def test_3_get_user_products_invalid_token(self):
        url=f"{self.base_url}/users/1/products"
        invalid_fake_token='CfDJ8OW5OI0CPGJBgSNlGwO0x4YF7qbYKVv7KOO-N0eFtDUzXOrL7F9Xd9W1otVi4ueJOkAmAhuoHFWNkqRaFD7zvAMHMSKncl6Vo5QXKmpvy6vqxOKxSURdIey8aZPRi3Nnhp2p9la-Al5xrVKz0lignRdcCHf3O7pF9zv_sNx_c_T7pUe3WsxaJEPX3t_9FO2Wjw'
        headers = {"Authorization": f"Bearer {invalid_fake_token}"}
        response = requests.get(url, headers=headers)
        data=json.loads(response.text)
        print(f"get_user_products: {data}")
        self.assertTrue(response.status_code > 400)