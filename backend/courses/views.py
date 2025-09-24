from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission

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
from .serializers import (
    ChapterSerializer,
    CourseSerializer,
    QuestionChoiceSerializer,
    QuestionSerializer,
    TestSerializer,
    UserCourseSerializer,
    UserTestAnswerSerializer,
    UserTestSerializer,
)


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (getattr(request.user, "role", None) == "admin" or request.user.is_staff)
        )


# Course Views
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]


class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]


class CourseUpdateView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class CourseDeleteView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


# Chapter Views
class ChapterListView(generics.ListAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Chapter.objects.select_related("course").all()
        course_id = self.request.query_params.get("course_id")
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset


class ChapterCreateView(generics.CreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class ChapterDetailView(generics.RetrieveAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [AllowAny]


class ChapterUpdateView(generics.UpdateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class ChapterDeleteView(generics.DestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


# Test Views
class TestListView(generics.ListAPIView):
    serializer_class = TestSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Test.objects.select_related("chapter").all()
        chapter_id = self.request.query_params.get("chapter_id")
        if chapter_id:
            queryset = queryset.filter(chapter_id=chapter_id)
        return queryset


class TestCreateView(generics.CreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class TestDetailView(generics.RetrieveAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [AllowAny]


class TestUpdateView(generics.UpdateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class TestDeleteView(generics.DestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


# Question Views
class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Question.objects.select_related("test").all()
        test_id = self.request.query_params.get("test_id")
        if test_id:
            queryset = queryset.filter(test_id=test_id)
        return queryset


class QuestionCreateView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class QuestionDetailView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]


class QuestionUpdateView(generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class QuestionDeleteView(generics.DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


# Question Choice Views
class QuestionChoiceListView(generics.ListAPIView):
    serializer_class = QuestionChoiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = QuestionChoice.objects.select_related("question").all()
        question_id = self.request.query_params.get("question_id")
        if question_id:
            queryset = queryset.filter(question_id=question_id)
        return queryset


class QuestionChoiceCreateView(generics.CreateAPIView):
    queryset = QuestionChoice.objects.all()
    serializer_class = QuestionChoiceSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class QuestionChoiceDetailView(generics.RetrieveAPIView):
    queryset = QuestionChoice.objects.all()
    serializer_class = QuestionChoiceSerializer
    permission_classes = [AllowAny]


class QuestionChoiceUpdateView(generics.UpdateAPIView):
    queryset = QuestionChoice.objects.all()
    serializer_class = QuestionChoiceSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class QuestionChoiceDeleteView(generics.DestroyAPIView):
    queryset = QuestionChoice.objects.all()
    serializer_class = QuestionChoiceSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


# Enrollment Views
class UserCourseListView(generics.ListAPIView):
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserCourse.objects.select_related("course").filter(user=self.request.user)


class UserCourseCreateView(generics.CreateAPIView):
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserCourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated]


# User Test Views
class UserTestListView(generics.ListAPIView):
    serializer_class = UserTestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserTest.objects.select_related("test").filter(user=self.request.user)


class UserTestCreateView(generics.CreateAPIView):
    queryset = UserTest.objects.all()
    serializer_class = UserTestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserTestDetailView(generics.RetrieveAPIView):
    queryset = UserTest.objects.all()
    serializer_class = UserTestSerializer
    permission_classes = [IsAuthenticated]


class UserTestUpdateView(generics.UpdateAPIView):
    queryset = UserTest.objects.all()
    serializer_class = UserTestSerializer
    permission_classes = [IsAuthenticated]


class UserTestDeleteView(generics.DestroyAPIView):
    queryset = UserTest.objects.all()
    serializer_class = UserTestSerializer
    permission_classes = [IsAuthenticated]


# User Test Answer Views
class UserTestAnswerListView(generics.ListAPIView):
    serializer_class = UserTestAnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = UserTestAnswer.objects.select_related("user_test").filter(user_test__user=self.request.user)
        user_test_id = self.request.query_params.get("user_test_id")
        if user_test_id:
            queryset = queryset.filter(user_test_id=user_test_id)
        return queryset


class UserTestAnswerCreateView(generics.CreateAPIView):
    queryset = UserTestAnswer.objects.all()
    serializer_class = UserTestAnswerSerializer
    permission_classes = [IsAuthenticated]


class UserTestAnswerDetailView(generics.RetrieveAPIView):
    queryset = UserTestAnswer.objects.all()
    serializer_class = UserTestAnswerSerializer
    permission_classes = [IsAuthenticated]


class UserTestAnswerUpdateView(generics.UpdateAPIView):
    queryset = UserTestAnswer.objects.all()
    serializer_class = UserTestAnswerSerializer
    permission_classes = [IsAuthenticated]


class UserTestAnswerDeleteView(generics.DestroyAPIView):
    queryset = UserTestAnswer.objects.all()
    serializer_class = UserTestAnswerSerializer
    permission_classes = [IsAuthenticated]
