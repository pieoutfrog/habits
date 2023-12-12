from rest_framework.serializers import ValidationError


def choose_connected_habit_or_reward(connected_habit, reward):
    """Проверка на одновременный выбор связанной привычки и указания вознаграждения(что-то одно)"""
    if connected_habit and reward:
        raise ValidationError('Привычка может быть только либо со связанной привычкой, либо награждением!')


def check_duration_of_action(duration):
    """Проверка на выполнение привычки(должно быть не более 120 секунд)"""
    if duration > 120:
        raise ValidationError('Время выполнения привычки не должно быть более 120 секунд(2 минут)!')


def validate_just_pleasant_habit_in_connected_habit(connected_habit):
    """В связанные привычки могут попадать только привычки с признаком приятной привычки."""
    if connected_habit and not connected_habit.is_pleasant:
        raise ValidationError('Связанной привычкой может быть только привычка, которая является приятной!')


def validate_no_reward_or_connected_habit_for_pleasant(data):
    """У приятной привычки не может быть вознаграждения или связанной привычки."""
    is_pleasant = data.get('is_pleasant')
    reward = data.get('reward')
    connected_habit = data.get('connected_habit')

    if is_pleasant and (reward or connected_habit):
        raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки!')


def check_habit_frequency(period):
    """Проверка периодичности привычки(не реже, чем 1 раз в 7 дней) или периодичность не может равняться нулю"""
    if period > 7:
        raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в неделю!')

    if period == 0:
        raise ValidationError('Периодичность привычки не может равняться нулю!')
