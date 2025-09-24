from django.conf import settings
from django.db import models


class Course(models.Model):
    STATUS_ACTIVE = "active"
    STATUS_ARCHIVED = "archived"
    STATUS_DRAFT = "draft"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_ARCHIVED, "Archived"),
        (STATUS_DRAFT, "Draft"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_DRAFT)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.title


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="chapters")
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    learning_resource_url = models.URLField(null=True, blank=True)
    order_index = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["course", "order_index"]
        unique_together = ("course", "order_index")

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.course.title} — {self.title}"


class Test(models.Model):
    TYPE_MCQ = "mcq"
    TYPE_FILL_BLANK = "fillblank"

    TYPE_CHOICES = [
        (TYPE_MCQ, "Multiple Choice"),
        (TYPE_FILL_BLANK, "Fill in the Blank"),
    ]

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="tests")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    passing_score = models.PositiveIntegerField(null=True, blank=True)
    order_index = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["chapter", "order_index"]
        unique_together = ("chapter", "order_index")

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.chapter.title} ({self.type})"


class Question(models.Model):
    TYPE_MCQ = "mcq"
    TYPE_FILL_BLANK = "fillblank"

    TYPE_CHOICES = [
        (TYPE_MCQ, "Multiple Choice"),
        (TYPE_FILL_BLANK, "Fill in the Blank"),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    correct_answer_text = models.TextField(blank=True)
    order_index = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["test", "order_index"]
        unique_together = ("test", "order_index")

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"Question {self.pk}"


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=500)
    order_index = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["question", "order_index"]
        unique_together = ("question", "order_index")

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"Choice {self.pk}"


class UserCourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_dropped = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "course")
        ordering = ["-enrollment_date"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.user.username} in {self.course.title}"


class UserTest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tests")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="attempts")
    attempt_date = models.DateTimeField(auto_now_add=True)
    time_spent = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-attempt_date"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.user.username} - {self.test_id}"


class UserTestAnswer(models.Model):
    user_test = models.ForeignKey(UserTest, on_delete=models.CASCADE, related_name="answers")
    given_answer_text = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ["user_test"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"Answer {self.pk}"
