from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from django.contrib.auth import get_user_model

from postings.models import BlogPost

User = get_user_model()

#automated
class BlogPostAPITestCase(APITestCase):
	def setUp(self):
		user_obj = User(username = 'test', email = 'test@test.com')
		user_obj.set_password("some random password")
		user_obj.save()
		blog_post = BlogPost.objects.create(
			user = user_obj,
			title = 'new title test',
			 content = 'some random contents here'
			 )
	def test_single_user(self):
		user_count = User.objects.count()
		self.assertEqual(user_count, 1)

	def test_single_post(self):
		post_count = BlogPost.objects.count()
		self.assertEqual(post_count, 1)

	def test_get_list(self):
		data = {}
		url = api_reverse("api-postings:post-create")
		response = self.client.get(url, data, format = 'json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		#print(response.data)

	def test_post_list(self):
		data = {"title":"some title", "content" : "some contents"}
		url = api_reverse("api-postings:post-create")
		response = self.client.post(url, data, format = 'json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
	

	def test_get_item(self):
		blog_post = BlogPost.objects.first()
		data = {}
		url = blog_post.get_api_url()
		response = self.client.get(url, data, format = 'json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		print(response.data)

	def test_update_item(self):
		blog_post = BlogPost.objects.first()
		url = blog_post.get_api_url()
		data = {"title":"some title", "content" : "some contents"}
		response = self.client.post(url, data, format = 'json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		response = self.client.put(url, data, format = 'json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		#print(response.data)


