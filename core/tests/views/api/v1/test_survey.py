from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from core.choices.role import UserRoleChoices
from core.tests.factories.survey import SurveyFactory
from core.tests.factories.user import UserFactory


class SurveyAPITestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.survey = SurveyFactory()

    def test1(self):
        # LIST
        self.client.force_authenticate(user=self.user)
        url = reverse('core:api:v1:survey-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertTrue('results' in response_json)
        self.assertEqual(len(response_json['results']), 1)

    def test2(self):
        # GET
        self.client.force_authenticate(user=self.user)
        url = reverse('core:api:v1:survey-detail', args=[self.survey.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(response_json['id'], self.survey.id)
        self.assertEqual(response_json['name'], self.survey.name)

    def test3(self):
        # Изменение обычным пользователем запрещено
        self.client.force_authenticate(user=self.user)
        url = reverse('core:api:v1:survey-detail', args=[self.survey.id])

        updated_data = {
            'name': 'Test',
            "author": self.user.id,
        }

        response = self.client.put(url, updated_data, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
