import json # import for processiong jsons
import unittest # import for creating unittests

# import the "flask app" from "project" folder. The app is defined in  project/__init__.py
# In this test class we are going to use the flask test_client method for testing a flask app
# for that reason we need to import the app itself
# Take into account that this is a simulated request test. We DON'T need the app running for passing these tests
from project import app 


# Define the class that extends from unittest.TestCase class. This allows to generate tests
class TestApp(unittest.TestCase):

    # define class property token to store the necessary token that will be obtained in test_1 
    token=''
    
    # define the function for getting the token. It declares the parameter self for accessing class properties, like the assert methods
    def test_1_getToken(self): 
        # get the test client from flask app
        tester = app.test_client(self) 
        
        # set the email and password to be sent to get the token
        user_data = {"email":"jd@myinsuranceapp.com","password":"passwordjd"} 
        
        # send a POST request to address "/api/v1/token" with the json with user_data to get the token
        # Look at README.md to understand why we send to that address
        response = tester.post('/api/v1/token',content_type='application/json', json = user_data)
        
        # converts the response info into objects
        data=json.loads(response.text)
        
        # print fo humans to see the data
        print(f"post token: {data}")

        # asserts that the reponse code is 200 (OK)
        # remember that this class extends from unittest.TestCase, where the "assert..." methods are available 
        self.assertEqual(response.status_code, 200)
        
        # if response code is 200, we have a valid token, then store it in the class propertie
        if response.status_code==200:
            TestApp.token=data['token']
        


    # define a function for validating the endpoint /api/v1/users/<id>/products. 
    # This function will need of a token for accessing to the endpoint, since it is in restricted area
    # we are goint to check that if we send a valid token, we receive a valid response, with status 200 and an array of products
    def test_2_get_user_products_valid_token(self):
        tester = app.test_client(self)
        
        # print fo humans to see the stored token
        print(f"token: {self.token}")

        # define the header to be sent with the request
        headers = {"Authorization": f"Bearer {TestApp.token}"}

        # send a GET request to the endpoint, indicating that json is expected as a response data and
        # adding the previous defined headers
        # take into account that the endpoint is: /api/v1/users/<id>/products
        # here we are replacing "<id>" by a concrete user id, that is the user with id="1"
        response = tester.get('/api/v1/users/1/products', content_type='application/json', headers=headers)

        # see previous function comments for this part
        data=json.loads(response.text)        
        print(f"get_user_products: {data}")
        self.assertEqual(response.status_code, 200)

        # here we verify that the length of the array data is greater than 0, since the user 1, has at least one product assigned
        self.assertTrue(len(data)>0)
    
    # define a function for validating that if we send a INAVLID/FAKE token, we receive a 4xx response
    # since the token is not valid, we should not get access to the restricted area
    def test_3_get_user_products_invalid_token(self):
        tester = app.test_client(self)
        
        # this is a fake/invalid token, so it smust not work for accessing restricted area
        ivalid_fake_token='CfDJ8OW5OI0CPGJBgSNlGwO0x4YF7qbYKVv7KOO-N0eFtDUzXOrL7F9Xd9W1otVi4ueJOkAmAhuoHFWNkqRaFD7zvAMHMSKncl6Vo5QXKmpvy6vqxOKxSURdIey8aZPRi3Nnhp2p9la-Al5xrVKz0lignRdcCHf3O7pF9zv_sNx_c_T7pUe3WsxaJEPX3t_9FO2Wjw'

        headers = {"Authorization": f"Bearer {ivalid_fake_token}"}
        response = tester.get('/api/v1/users/1/products', content_type='application/json', headers=headers)
        data=json.loads(response.text)
        print(f"get_user_products: {data}")

        # we expect the response code to be some 4XX code, that means that the request is invalid
        # this is true, since we send a invalida token
        self.assertTrue(response.status_code > 400)

    