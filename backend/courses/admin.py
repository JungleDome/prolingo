from django.contrib import admin

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


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "status")
    search_fields = ("title", "description")
    list_filter = ("status",)


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order_index")
    list_filter = ("course",)
    ordering = ("course", "order_index")


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("id", "chapter", "type", "passing_score", "order_index")
    list_filter = ("type",)
    ordering = ("chapter", "order_index")
    search_fields = ("chapter__title",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "test", "type", "order_index")
    search_fields = ("text",)
    ordering = ("test", "order_index")


@admin.register(QuestionChoice)
class QuestionChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "order_index")
    ordering = ("question", "order_index")


@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "enrollment_date", "is_dropped")
    list_filter = ("is_dropped",)
    autocomplete_fields = ("user", "course")


@admin.register(UserTest)
class UserTestAdmin(admin.ModelAdmin):
    list_display = ("user", "test", "attempt_date", "time_spent")
    autocomplete_fields = ("user", "test")
    search_fields = ("user__username", "test__chapter__title")


@admin.register(UserTestAnswer)
class UserTestAnswerAdmin(admin.ModelAdmin):
    list_display = ("user_test", "is_correct")
    list_filter = ("is_correct",)
    autocomplete_fields = ("user_test",)
    search_fields = ("user_test__user__username",)
