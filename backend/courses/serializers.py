from rest_framework import serializers

from .models import (
    Chapter,
    Course,
    Question,
    QuestionChoice,
    Test,
    UserCourse,
    UserTest,
    UserTestAnswer,
)


class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = ["id", "question", "text", "order_index"]
        read_only_fields = ["id"]


class QuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "test",
            "text",
            "type",
            "correct_answer_text",
            "order_index",
            "choices",
        ]
        read_only_fields = ["id"]


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ["id", "chapter", "type", "passing_score", "order_index", "questions"]
        read_only_fields = ["id"]


class ChapterSerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = [
            "id",
            "course",
            "title",
            "description",
            "learning_resource_url",
            "order_index",
            "tests",
        ]
        read_only_fields = ["id"]


class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "description", "status", "chapters"]
        read_only_fields = ["id"]


class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourse
        fields = ["id", "user", "course", "enrollment_date", "is_dropped"]
        read_only_fields = ["id", "enrollment_date"]


class UserTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTest
        fields = ["id", "user", "test", "attempt_date", "time_spent"]
        read_only_fields = ["id", "attempt_date"]


class UserTestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTestAnswer
        fields = ["id", "user_test", "given_answer_text", "is_correct"]
        read_only_fields = ["id"]
