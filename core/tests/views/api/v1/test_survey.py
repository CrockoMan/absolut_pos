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
        self.survey_data = {
            'author': self.user.id,
            'name': 'Survey Without Author',
            'survey_date': '2026-01-01',
            "questions": [
                {
                    "text": "Любите томаты?",
                    "order": 0,
                    "questions": [
                        {
                            "text": "Нет15",
                            "order": 1
                        },
                        {
                            "text": "Да1",
                            "order": 2
                        },
                        {
                            "text": "Не знаю1",
                            "order": 3
                        }
                    ]
                },
            ]
        }

    def test_unauthenticated_user_cannot_list_surveys(self):
        # LIST - неаутентифицированный пользователь
        url = reverse('core:api:v1:survey-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_list_surveys(self):
        # LIST
        self.client.force_authenticate(user=self.user)
        url = reverse('core:api:v1:survey-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertTrue('results' in response_json)
        self.assertEqual(len(response_json['results']), 1)

    def test_authenticated_user_can_retrieve_survey(self):
        # GET
        self.client.force_authenticate(user=self.user)
        url = reverse('core:api:v1:survey-detail', args=[self.survey.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(response_json['id'], self.survey.id)
        self.assertEqual(response_json['name'], self.survey.name)

    def test_regular_user_cannot_update_survey(self):
        # Изменение обычным пользователем запрещено
        self.client.force_authenticate(user=self.user)
        url = reverse('core:api:v1:survey-detail', args=[self.survey.id])

        self.survey_data['author'] = self.user.id

        response = self.client.put(url, self.survey_data, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_regulatr_user_cant_create(self):
        # Обычный пользователь не может создать опрос

        self.client.force_authenticate(user=self.user)
        url = reverse('core:api:v1:survey-list')

        self.survey_data['author'] = self.user.id

        response = self.client.post(url, self.survey_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_user_can_create_survey(self):
        """пользователь может создать опрос"""
        user = UserFactory(role = UserRoleChoices.ROLE_SURVEY_ADMIN)
        self.client.force_authenticate(user=user)
        url = reverse('core:api:v1:survey-list')

        self.survey_data['author'] = user.id

        response = self.client.post(url, self.survey_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_json = response.json()
        self.assertEqual(response_json['name'], self.survey_data['name'])
        self.assertEqual(response_json['author'], user.id)
