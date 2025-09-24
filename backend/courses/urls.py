from django.urls import path

from . import views

urlpatterns = [
    # Courses
    path("courses/", views.CourseListView.as_view(), name="course-list"),
    path("courses/create/", views.CourseCreateView.as_view(), name="course-create"),
    path("courses/<int:pk>/", views.CourseDetailView.as_view(), name="course-detail"),
    path("courses/<int:pk>/update/", views.CourseUpdateView.as_view(), name="course-update"),
    path("courses/<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course-delete"),
    # Chapters
    path("chapters/", views.ChapterListView.as_view(), name="chapter-list"),
    path("chapters/create/", views.ChapterCreateView.as_view(), name="chapter-create"),
    path("chapters/<int:pk>/", views.ChapterDetailView.as_view(), name="chapter-detail"),
    path("chapters/<int:pk>/update/", views.ChapterUpdateView.as_view(), name="chapter-update"),
    path("chapters/<int:pk>/delete/", views.ChapterDeleteView.as_view(), name="chapter-delete"),
    # Tests
    path("tests/", views.TestListView.as_view(), name="test-list"),
    path("tests/create/", views.TestCreateView.as_view(), name="test-create"),
    path("tests/<int:pk>/", views.TestDetailView.as_view(), name="test-detail"),
    path("tests/<int:pk>/update/", views.TestUpdateView.as_view(), name="test-update"),
    path("tests/<int:pk>/delete/", views.TestDeleteView.as_view(), name="test-delete"),
    # Questions
    path("questions/", views.QuestionListView.as_view(), name="question-list"),
    path("questions/create/", views.QuestionCreateView.as_view(), name="question-create"),
    path("questions/<int:pk>/", views.QuestionDetailView.as_view(), name="question-detail"),
    path("questions/<int:pk>/update/", views.QuestionUpdateView.as_view(), name="question-update"),
    path("questions/<int:pk>/delete/", views.QuestionDeleteView.as_view(), name="question-delete"),
    # Question choices
    path("choices/", views.QuestionChoiceListView.as_view(), name="choice-list"),
    path("choices/create/", views.QuestionChoiceCreateView.as_view(), name="choice-create"),
    path("choices/<int:pk>/", views.QuestionChoiceDetailView.as_view(), name="choice-detail"),
    path("choices/<int:pk>/update/", views.QuestionChoiceUpdateView.as_view(), name="choice-update"),
    path("choices/<int:pk>/delete/", views.QuestionChoiceDeleteView.as_view(), name="choice-delete"),
    # User course enrollments
    path("user-courses/", views.UserCourseListView.as_view(), name="user-course-list"),
    path("user-courses/create/", views.UserCourseCreateView.as_view(), name="user-course-create"),
    path("user-courses/<int:pk>/", views.UserCourseDetailView.as_view(), name="user-course-detail"),
    # User tests
    path("user-tests/", views.UserTestListView.as_view(), name="user-test-list"),
    path("user-tests/create/", views.UserTestCreateView.as_view(), name="user-test-create"),
    path("user-tests/<int:pk>/", views.UserTestDetailView.as_view(), name="user-test-detail"),
    path("user-tests/<int:pk>/update/", views.UserTestUpdateView.as_view(), name="user-test-update"),
    path("user-tests/<int:pk>/delete/", views.UserTestDeleteView.as_view(), name="user-test-delete"),
    # User test answers
    path("user-test-answers/", views.UserTestAnswerListView.as_view(), name="user-test-answer-list"),
    path("user-test-answers/create/", views.UserTestAnswerCreateView.as_view(), name="user-test-answer-create"),
    path("user-test-answers/<int:pk>/", views.UserTestAnswerDetailView.as_view(), name="user-test-answer-detail"),
    path("user-test-answers/<int:pk>/update/", views.UserTestAnswerUpdateView.as_view(), name="user-test-answer-update"),
    path("user-test-answers/<int:pk>/delete/", views.UserTestAnswerDeleteView.as_view(), name="user-test-answer-delete"),
]
