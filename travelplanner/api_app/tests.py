from django.test import TestCase
from rest_framework.test import APIClient
from api_app.models import CustomUser,Destination,TravelPlan,Activity,Comment
from django.urls import reverse
from rest_framework import status

# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'bio': 'This is a test bio that is sufficiently long.',
            'sex': 'M',
            'birthdate': '2000-01-01',
        }
        user=CustomUser.objects.create(**self.test_user)
        user.set_password(self.test_user['password'])
        user.save()


    def test_user_creation(self):
        self.test_user_1 = {
            'username': 'testusers',
            'email': 'testuser_1@example.com',
            'password': 'testpassword123',
            'bio': 'This is a test bio that is sufficiently long.',
            'sex': 'M',
            'birthdate': '1995-01-01',
        }
        response =self.client.post(reverse("CustomUserListView"),self.test_user_1)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(),2)

    def test_get_all_users(self):
        response = self.client.get(reverse("CustomUserListView"))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

    def test_login_user(self):
        response = self.client.post(reverse('user-login'), data={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_logout_user(self):
        response = self.client.post(reverse('user-login'), data={'username': 'testuser', 'password': 'testpassword'})
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(reverse('user-logout'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["message"],"Logged out successfully")
        self.assertNotIn('token',response.data)

class TestDestination(TestCase):
    def setUp(self):
        
        self.client = APIClient()
        self.test_user = {
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password': 'testpassword',#testpassword
                'bio': 'This is a test bio that is sufficiently long.',
                'sex': 'M',
                
                'birthdate': '2000-01-01',
            }
        self.user=CustomUser.objects.create(**self.test_user)
        
        self.user.set_password(self.test_user['password'])
       
        self.user.save()

        self.client.login(username='testuser', password='testpassword')

        self.destination_data={
            "user": self.user.id,
            "name": "testrecipe",
            "description": "a description long enough to pass the test",
            "country": "T",
            "best_time_to_visit": "Test Ingredients to pass the test",
            #"image": "imagepath.jpeg",
        }

    def test_destination_creation(self):
        response = self.client.post(reverse("DestinationListView"),self.destination_data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Destination.objects.count(),1)

    def test_get_all_destinations(self):
        response = self.client.post(reverse("DestinationListView"),self.destination_data)
        response_get = self.client.get(reverse('DestinationListView'))
        self.assertEqual(response_get.status_code,status.HTTP_200_OK)

    def test_create_invalid_destination(self):
        destination_data2={
            "user": self.user.id,
            "name": "testrecipe",
            "description": "a description long enough to pass the test",
            "country": "D",
            "best_time_to_visit": "Test Ingredients to pass the test",
            #"image": "imagepath.jpeg",
        }
        response = self.client.post(reverse("DestinationListView"),destination_data2)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

        

    def test_delete_destination(self):
        #response = self.client.post(reverse("DestinationListView"),self.destination_data)
        #destination = Destination.objects.first()
        #response_delete = self.client.delete(reverse("DestinationDetailView"),kwargs={"pk": destination.pk})
        #self.assertEqual(response_delete.status_code,status.HTTP_204_NO_CONTENT)
        
        # Create the destination object
        response = self.client.post(reverse("DestinationListView"), self.destination_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        login_response = self.client.post(reverse("user-login"),{
            "username" : "testuser",
            "password": "testpassword"})

        token = login_response.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token )
        


        # Retrieve the created destination instance
        destination = Destination.objects.first()
        self.assertIsNotNone(destination)  # Ensure the destination exists

        # Construct the URL with the primary key
        url = reverse("DestinationDetailView", kwargs={"pk": destination.pk})
        
        # Perform the delete request
        response_delete = self.client.delete(url)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)