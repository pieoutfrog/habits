from rest_framework import serializers

from habits.models import Habit
from habits.validators import check_habit_frequency, check_duration_of_action, choose_connected_habit_or_reward, \
    validate_just_pleasant_habit_in_connected_habit, validate_no_reward_or_connected_habit_for_pleasant


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычки"""
    period = serializers.IntegerField(validators=[check_habit_frequency])
    duration_of_action = serializers.IntegerField(validators=[check_duration_of_action])

    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        """Дополнительная валидация для сериализатора"""
        choose_connected_habit_or_reward(data.get('connected_habit'), data.get('reward'))
        validate_just_pleasant_habit_in_connected_habit(data.get('connected_habit'))
        validate_no_reward_or_connected_habit_for_pleasant(data)
        return data