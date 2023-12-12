from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='Oleg',
            password='Oleg',
            chat_id='9183645'
        )

        self.habit = Habit.objects.create(
            place="Park",
            time='11:00',
            action="walking",
            period=7,
            duration_of_action=120,
            is_pleasant=False,
            is_public=False
        )

    def test_check_validation_choose_connected_habit_or_reward(self):
        """Тест валидатора choose_connected_habit_or_reward"""
        self.client.force_authenticate(user=self.user)

        data = {
            "place": "Park",
            "time": "11:00",
            "action": "walking",
            "period": 7,
            "duration_of_action": 120,
            "is_pleasant": True,
            "connected_habit": 1,
            "reward": "cookie",
            "is_public": False
        }

        response = self.client.post(
            reverse('habit:habit_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.json(),
                         {
                             "non_field_errors": [
                                 "Привычка может быть только либо со связанной привычкой, либо награждением!"
                             ]
                         }
                         )

    def test_check_validator_check_duration_of_action(self):
        """Тест валидатора check_duration_of_action"""
        self.client.force_authenticate(user=self.user)

        data = {
            "place": "Park",
            "time": "11:00",
            "action": "walking",
            "period": 7,
            "duration_of_action": 200,
            "is_pleasant": True,
            "reward": "cookie",
            "is_public": False
        }

        response = self.client.post(
            reverse('habit:habit_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.json(),
                         {
                             "duration_of_action": [
                                 "Время выполнения привычки не должно быть более 120 секунд(2 минут)!"
                             ]
                         }
                         )

    def test_check_validator_validate_just_pleasant_habit_in_connected_habit(self):
        """Тест валидатора validate_just_pleasant_habit_in_connected_habit"""
        self.client.force_authenticate(user=self.user)

        data = {
            "place": "Park",
            "time": "11:00",
            "action": "walking",
            "period": 7,
            "duration_of_action": 120,
            "is_pleasant": False,
            "connected_habit": self.habit.pk,
            "is_public": False
        }

        response = self.client.post(
            reverse('habit:habit_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.json(),
                         {
                             "non_field_errors": [
                                 "Связанной привычкой может быть только привычка, которая является приятной!"
                             ]
                         }
                         )

    def test_validator_validate_no_reward_or_connected_habit_for_pleasant(self):
        """Тест валидатора validate_no_reward_or_connected_habit_for_pleasant"""
        self.client.force_authenticate(user=self.user)

        data = {
            "place": "Park",
            "time": "11:00",
            "action": "walking",
            "period": 7,
            "duration_of_action": 120,
            "is_pleasant": True,
            "reward": "cookie",
            "is_public": False
        }

        response = self.client.post(
            reverse('habit:habit_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.json(),
                         {
                             "non_field_errors": [
                                 "У приятной привычки не может быть вознаграждения или связанной привычки!"
                             ]
                         }
                         )

    def test_validator_check_habit_frequency(self):
        """Тест валидатора check_habit_frequency"""
        self.client.force_authenticate(user=self.user)

        data = {
            "place": "Home",
            "time": "11:00",
            "action": "walking",
            "period": 9,
            "duration_of_action": 120,
            "is_pleasant": True,
            "is_public": False
        }

        response = self.client.post(
            reverse('habit:habit_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.json(),
                         {
                             "period": [
                                 "Нельзя выполнять привычку реже, чем 1 раз в неделю!"
                             ]
                         }
                         )

    def test_validator_check_habit_frequency_second_part(self):
        """Тест второй части валидатора check_habit_frequency """
        self.client.force_authenticate(user=self.user)

        data = {
            "place": "Home",
            "time": "11:00",
            "action": "walking",
            "period": 0,
            "duration_of_action": 120,
            "is_pleasant": True,
            "is_public": False
        }

        response = self.client.post(
            reverse('habit:habit_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.json(),
                         {
                             "period": [
                                 "Периодичность привычки не может равняться нулю!"
                             ]
                         }
                         )


class HabitDestroyTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='Oleg',
            password='Oleg',
            chat_id='91827465'
        )
        self.habit = Habit.objects.create(
            owner=self.user,
            place='Park',
            time='11:00:00',
            action='breathing',
            period=3,
            duration_of_action=60,
            is_pleasant=False
        )

    def test_habit_destroy_wrong_owner(self):
        """Тест на проверку удаления объекта чужим пользователем"""
        user = User.objects.create(
            username='not_owner',
            password='not_owner',
            chat_id='91827465'
        )
        self.client.force_authenticate(user=user)

        response = self.client.delete(
            reverse('habit:habit_delete',
                    args=[self.habit.pk]),

        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_habit_destroy(self):
        """Тест на удаление объекта владельцем"""
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse('habit:habit_delete',
                    args=[self.habit.pk]),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class HabitListTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='Oleg',
            password='Oleg',
            chat_id='918273645'
        )
        self.habit = Habit.objects.create(
            owner=self.user,
            place='Home',
            time='11:00:00',
            action='Test',
            period=3,
            duration_of_action=60,
            is_pleasant=False
        )

    def test_get_habit_list(self):
        """Тест на получения списка привычек владельца"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('habit:habit_list')
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.habit.id,
                        "place": self.habit.place,
                        "time": self.habit.time,
                        "action": self.habit.action,
                        "period": self.habit.period,
                        "duration_of_action": self.habit.duration_of_action,
                        "is_pleasant": self.habit.is_pleasant,
                        "connected_habit": self.habit.connected_habit,
                        "is_public": self.habit.is_public,
                        "last_reminder": self.habit.last_reminder,
                        "owner": self.habit.owner.pk,
                        "reward": self.habit.reward
                    }
                ]
            }
        )


class HabitRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='Oleg',
            password='Oleg',
            chat_id='918273645'
        )
        self.habit = Habit.objects.create(
            owner=self.user,
            place='Home',
            time='11:00:00',
            action='breathing',
            period=3,
            duration_of_action=60,
            is_pleasant=False
        )

    def test_habit_retrieve(self):
        """Тест на получение одной из привычек владельца"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('habit:habit_detail',
                    args=[self.habit.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_retrieve_wrong_owner(self):
        """Тест на проверку получения объекта чужим пользователем"""
        user = User.objects.create(
            username='not_owner',
            password='not_owner',
            chat_id='1239894'
        )
        self.client.force_authenticate(user=user)

        response = self.client.get(
            reverse('habit:habit_detail',
                    args=[self.habit.pk]),

        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class HabitUpdateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='Oleg',
            password='Oleg',
            chat_id='918273645'
        )
        self.habit = Habit.objects.create(
            owner=self.user,
            place='Home',
            time='11:00:00',
            action='breathing',
            period=3,
            duration_of_action=60,
            is_pleasant=False
        )

    def test_habit_update(self):
        """Тест на редакцию привычки владельцем"""
        self.client.force_authenticate(user=self.user)

        data = {
            "place": "Home"
        }

        response = self.client.patch(
            reverse('habit:habit_update',
                    args=[self.habit.pk]),
            data=data

        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_update_with_wrong_owner(self):
        user = User.objects.create(
            username='not_owner',
            password='not_owner',
            chat_id='909234'
        )
        self.client.force_authenticate(user=user)

        response = self.client.patch(
            reverse('habit:habit_update',
                    args=[self.habit.pk]),

        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PublicHabitListTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='Oleg',
            password='Oleg',
            chat_id='918273645'
        )
        self.habit = Habit.objects.create(
            owner=self.user,
            place='Home',
            time='11:00:00',
            action='breathing',
            period=3,
            duration_of_action=60,
            is_pleasant=False,
            is_public=True
        )

    def test_get_public_habit_list(self):
        """Test for getting list of habits"""
        response = self.client.get(
            reverse('habit:public_habit_list')
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.habit.id,
                        "place": self.habit.place,
                        "time": self.habit.time,
                        "action": self.habit.action,
                        "period": self.habit.period,
                        "duration_of_action": self.habit.duration_of_action,
                        "is_pleasant": self.habit.is_pleasant,
                        "connected_habit": self.habit.connected_habit,
                        "is_public": self.habit.is_public,
                        "last_reminder": self.habit.last_reminder,
                        "owner": self.habit.owner.pk,
                        "reward": self.habit.reward
                    }
                ]
            }
        )
