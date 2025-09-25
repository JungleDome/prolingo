from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from .models import (
    Course, Chapter, Test, Question, Option,
    UserCourse, UserChapter, UserTestResult, UserAnswer
)
from .serializers import (
    CourseSerializer, ChapterSerializer, TestSerializer, QuestionSerializer, OptionSerializer,
    UserCourseSerializer, UserChapterSerializer, UserTestResultSerializer, UserAnswerSerializer
)
from users.permissions import IsAdminRole, IsOwnerOrAdmin
from users.models import User
from server.schema import extend_schema_with_tags

# Course CRUD Views
@extend_schema_with_tags("Courses")
class CourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Course.objects.all().order_by('-created_date')
        # anonymous users => only active courses
        if not getattr(self.request.user, "is_authenticated", False):
            return qs.filter(status='active')
        # admins/staff see all
        if getattr(self.request.user, 'role', None) == 'admin' or self.request.user.is_staff:
            return qs
        # authenticated non-admins see active and drafts they created
        return qs.filter(Q(status='active') | Q(created_by=self.request.user))

@extend_schema_with_tags("Courses")
class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

@extend_schema_with_tags("Courses")
class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

@extend_schema_with_tags("Courses")
class CourseUpdateView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

@extend_schema_with_tags("Courses")
class CourseDeleteView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

# Chapter CRUD Views
@extend_schema_with_tags("Chapters")
class ChapterListView(generics.ListAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        qs = Chapter.objects.all()
        if course_id:
            qs = qs.filter(course_id=course_id).order_by('order_index')
        return qs

@extend_schema_with_tags("Chapters")
class ChapterCreateView(generics.CreateAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated]

@extend_schema_with_tags("Chapters")
class ChapterDetailView(generics.RetrieveAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated]

@extend_schema_with_tags("Chapters")
class ChapterUpdateView(generics.UpdateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

@extend_schema_with_tags("Chapters")
class ChapterDeleteView(generics.DestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

# Test CRUD Views
@extend_schema_with_tags("Tests")
class TestListView(generics.ListAPIView):
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chapter_id = self.request.query_params.get('chapter_id')
        qs = Test.objects.all()
        if chapter_id:
            qs = qs.filter(chapter_id=chapter_id)
        return qs

@extend_schema_with_tags("Tests")
class TestCreateView(generics.CreateAPIView):
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

@extend_schema_with_tags("Tests")
class TestDetailView(generics.RetrieveAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

@extend_schema_with_tags("Tests")
class TestUpdateView(generics.UpdateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

@extend_schema_with_tags("Tests")
class TestDeleteView(generics.DestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

# Question CRUD Views
@extend_schema_with_tags("Questions")
class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        test_id = self.request.query_params.get('test_id')
        qs = Question.objects.all()
        if test_id:
            qs = qs.filter(test_id=test_id)
        return qs

@extend_schema_with_tags("Questions")
class QuestionCreateView(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

@extend_schema_with_tags("Questions")
class QuestionDetailView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

@extend_schema_with_tags("Questions")
class QuestionUpdateView(generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

@extend_schema_with_tags("Questions")
class QuestionDeleteView(generics.DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

# Option CRUD Views
@extend_schema_with_tags("Options")
class OptionListView(generics.ListAPIView):
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        question_id = self.request.query_params.get('question_id')
        qs = Option.objects.all()
        if question_id:
            qs = qs.filter(question_id=question_id)
        return qs

@extend_schema_with_tags("Options")
class OptionCreateView(generics.CreateAPIView):
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated]

@extend_schema_with_tags("Options")
class OptionDetailView(generics.RetrieveAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated]

@extend_schema_with_tags("Options")
class OptionUpdateView(generics.UpdateAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

@extend_schema_with_tags("Options")
class OptionDeleteView(generics.DestroyAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

# Enrollment & Progress Views
@extend_schema_with_tags("User Courses")
class EnrollView(generics.CreateAPIView):
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print(f"Enrollment request data: {request.data}")  # Debug line
        
        # Check if user is already enrolled
        course_id = request.data.get('course')
        if course_id:
            existing_enrollment = UserCourse.objects.filter(
                user=request.user, 
                course_id=course_id
            ).first()
            if existing_enrollment:
                return Response(
                    {'detail': 'You are already enrolled in this course.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(f"Serializer errors: {serializer.errors}")  # Debug line
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema_with_tags("User Courses")
class UserCoursesListView(generics.ListAPIView):
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserCourse.objects.filter(user=self.request.user).select_related('course')

@extend_schema_with_tags("User Courses")
class UserCourseDetailView(generics.RetrieveAPIView):
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        course_id = self.kwargs.get('pk')
        return get_object_or_404(UserCourse, pk=course_id, user=self.request.user)

@extend_schema_with_tags("User Courses")
class UserCourseUpdateView(generics.UpdateAPIView):
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        course_id = self.kwargs.get('pk')
        return get_object_or_404(UserCourse, pk=course_id, user=self.request.user)

@extend_schema_with_tags("User Courses")
class UnenrollView(generics.DestroyAPIView):
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        course_id = self.kwargs.get('pk')
        return get_object_or_404(UserCourse, pk=course_id, user=self.request.user)

# UserChapter Management Views
@extend_schema_with_tags("User Chapters")
class UserChapterDetailView(generics.RetrieveAPIView):
    serializer_class = UserChapterSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        chapter_id = self.kwargs.get('chapter_id')
        chapter = get_object_or_404(Chapter, pk=chapter_id)
        obj, _ = UserChapter.objects.get_or_create(user=user, chapter=chapter)
        return obj

@extend_schema_with_tags("User Chapters")
class UserChapterUpdateView(generics.UpdateAPIView):
    serializer_class = UserChapterSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        chapter_id = self.kwargs.get('chapter_id')
        chapter = get_object_or_404(Chapter, pk=chapter_id)
        obj, _ = UserChapter.objects.get_or_create(user=user, chapter=chapter)
        return obj

# Test Results CRUD Views
@extend_schema_with_tags("User Test Results")
class UserTestResultListView(generics.ListAPIView):
    serializer_class = UserTestResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = UserTestResult.objects.all().order_by('-attempt_date')
        user_id = self.request.query_params.get('user_id')
        test_id = self.request.query_params.get('test_id')
        if user_id:
            qs = qs.filter(user_id=user_id)
        if test_id:
            qs = qs.filter(test_id=test_id)
        # normal users only see own results
        if getattr(self.request.user, 'role', None) != 'admin' and not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

@extend_schema_with_tags("User Test Results")
class UserTestResultCreateView(generics.CreateAPIView):
    serializer_class = UserTestResultSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema_with_tags("User Test Results")
class UserTestResultDetailView(generics.RetrieveAPIView):
    queryset = UserTestResult.objects.all()
    serializer_class = UserTestResultSerializer
    permission_classes = [IsAuthenticated]

@extend_schema_with_tags("User Test Results")
class UserTestResultUpdateView(generics.UpdateAPIView):
    queryset = UserTestResult.objects.all()
    serializer_class = UserTestResultSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

@extend_schema_with_tags("User Test Results")
class UserTestResultDeleteView(generics.DestroyAPIView):
    queryset = UserTestResult.objects.all()
    serializer_class = UserTestResultSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

# User Answers CRUD Views
@extend_schema_with_tags("User Answers")
class UserAnswerListView(generics.ListAPIView):
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = UserAnswer.objects.all()
        result_id = self.request.query_params.get('result_id')
        if result_id:
            qs = qs.filter(result_id=result_id)
        # restrict to owner unless admin
        if getattr(self.request.user, 'role', None) != 'admin' and not self.request.user.is_staff:
            qs = qs.filter(result__user=self.request.user)
        return qs

@extend_schema_with_tags("User Answers")
class UserAnswerCreateView(generics.CreateAPIView):
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated]

@extend_schema_with_tags("User Answers")
class UserAnswerDetailView(generics.RetrieveAPIView):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated]

@extend_schema_with_tags("User Answers")
class UserAnswerUpdateView(generics.UpdateAPIView):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

@extend_schema_with_tags("User Answers")
class UserAnswerDeleteView(generics.DestroyAPIView):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

# Admin Views for UserCourse
@extend_schema_with_tags("Admin Courses")
class AdminUserCourseListView(generics.ListAPIView):
    """Admin endpoint to view all user course enrollments"""
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    
    def get_queryset(self):
        return UserCourse.objects.all().select_related('user', 'course').order_by('-enrollment_date')

@extend_schema_with_tags("Admin Courses")
class AdminUserCourseCreateView(generics.CreateAPIView):
    """Admin endpoint to create user course enrollment"""
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    
    def perform_create(self, serializer):
        # Admin can specify any user
        serializer.save()

@extend_schema_with_tags("Admin Courses")
class AdminUserCourseUpdateView(generics.UpdateAPIView):
    """Admin endpoint to update user course enrollment"""
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

@extend_schema_with_tags("Admin Courses")
class AdminUserCourseDeleteView(generics.DestroyAPIView):
    """Admin endpoint to delete user course enrollment"""
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

@extend_schema_with_tags("Admin Courses")
class AdminUserCourseDetailView(generics.RetrieveAPIView):
    """Admin endpoint to view specific user course enrollment"""
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

# Admin Views for UserChapter
@extend_schema_with_tags("Admin Chapters")
class AdminUserChapterListView(generics.ListAPIView):
    """Admin endpoint to view all user chapter progress"""
    serializer_class = UserChapterSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    
    def get_queryset(self):
        return UserChapter.objects.all().select_related('user', 'chapter', 'chapter__course').order_by('-last_accessed')

@extend_schema_with_tags("Admin Chapters")
class AdminUserChapterCreateView(generics.CreateAPIView):
    """Admin endpoint to create user chapter progress"""
    serializer_class = UserChapterSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    
    def perform_create(self, serializer):
        # Admin can specify any user
        serializer.save()

@extend_schema_with_tags("Admin Chapters")
class AdminUserChapterUpdateView(generics.UpdateAPIView):
    """Admin endpoint to update user chapter progress"""
    queryset = UserChapter.objects.all()
    serializer_class = UserChapterSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

@extend_schema_with_tags("Admin Chapters")
class AdminUserChapterDeleteView(generics.DestroyAPIView):
    """Admin endpoint to delete user chapter progress"""
    queryset = UserChapter.objects.all()
    serializer_class = UserChapterSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

@extend_schema_with_tags("Admin Chapters")
class AdminUserChapterDetailView(generics.RetrieveAPIView):
    """Admin endpoint to view specific user chapter progress"""
    queryset = UserChapter.objects.all()
    serializer_class = UserChapterSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

# Admin Views for UserTestResult
@extend_schema_with_tags("Admin Test Results")
class AdminUserTestResultListView(generics.ListAPIView):
    """Admin endpoint to view all user test results"""
    serializer_class = UserTestResultSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    
    def get_queryset(self):
        return UserTestResult.objects.all().select_related(
            'user', 'test', 'test__chapter', 'test__chapter__course'
        ).order_by('-attempt_date')

@extend_schema_with_tags("Admin Test Results")
class AdminUserTestResultCreateView(generics.CreateAPIView):
    """Admin endpoint to create user test result"""
    serializer_class = UserTestResultSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    
    def perform_create(self, serializer):
        # Admin can specify any user
        serializer.save()

@extend_schema_with_tags("Admin Test Results")
class AdminUserTestResultUpdateView(generics.UpdateAPIView):
    """Admin endpoint to update user test result"""
    queryset = UserTestResult.objects.all()
    serializer_class = UserTestResultSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

@extend_schema_with_tags("Admin Test Results")
class AdminUserTestResultDeleteView(generics.DestroyAPIView):
    """Admin endpoint to delete user test result"""
    queryset = UserTestResult.objects.all()
    serializer_class = UserTestResultSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

@extend_schema_with_tags("Admin Test Results")
class AdminUserTestResultDetailView(generics.RetrieveAPIView):
    """Admin endpoint to view specific user test result"""
    queryset = UserTestResult.objects.all()
    serializer_class = UserTestResultSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

# Admin Views for UserAnswer
@extend_schema_with_tags("Admin Answers")
class AdminUserAnswerListView(generics.ListAPIView):
    """Admin endpoint to view all user answers"""
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    
    def get_queryset(self):
        return UserAnswer.objects.all().select_related(
            'result', 'result__user', 'result__test', 'result__test__chapter', 
            'result__test__chapter__course', 'question', 'question__test'
        ).order_by('-id')

@extend_schema_with_tags("Admin Answers")
class AdminUserAnswerCreateView(generics.CreateAPIView):
    """Admin endpoint to create user answer"""
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    
    def perform_create(self, serializer):
        # Admin can specify any result and question
        serializer.save()

@extend_schema_with_tags("Admin Answers")
class AdminUserAnswerUpdateView(generics.UpdateAPIView):
    """Admin endpoint to update user answer"""
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

@extend_schema_with_tags("Admin Answers")
class AdminUserAnswerDeleteView(generics.DestroyAPIView):
    """Admin endpoint to delete user answer"""
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

@extend_schema_with_tags("Admin Answers")
class AdminUserAnswerDetailView(generics.RetrieveAPIView):
    """Admin endpoint to view specific user answer"""
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

# Helper endpoint to mark chapter complete
@extend_schema(tags=["User Chapters"])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_chapter_complete(request, chapter_id):
    user = request.user
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    uc, _ = UserChapter.objects.get_or_create(user=user, chapter=chapter)
    uc.completed = True
    uc.last_accessed = timezone.now()
    uc.save()

    # update UserCourse progress_percent if enrolled
    try:
        uc_course = UserCourse.objects.get(user=user, course=chapter.course)
        total = chapter.course.chapters.count() or 1
        completed = UserChapter.objects.filter(user=user, chapter__course=chapter.course, completed=True).count()
        uc_course.progress_percent = round((completed / total) * 100, 2)
        if uc_course.progress_percent >= 100:
            uc_course.status = 'completed'
        uc_course.save()
    except UserCourse.DoesNotExist:
        pass

    return Response({'success': True, 'progress_percent': getattr(uc_course, 'progress_percent', None)})