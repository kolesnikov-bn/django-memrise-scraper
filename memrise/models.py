from django.db import models


class Course(models.Model):
    id = models.IntegerField("Course memrise ID", primary_key=True)
    name = models.CharField("Course name", max_length=1024)
    url = models.CharField("Course's URL", max_length=1024)
    difficult = models.IntegerField("Number of difficult words in the course")
    num_things = models.IntegerField("Number of words in the course")
    num_levels = models.IntegerField("Number of levels in the course")
    difficult_url = models.CharField("Difficult's URL", max_length=1024)

    def __str__(self) -> str:
        return f"{self.name}"


class Level(models.Model):
    id = models.IntegerField("Memrise's level ID", primary_key=True)
    number = models.IntegerField("Number of level")
    name = models.CharField("Level name", max_length=1024)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.course}; Level-{self.number} [{self.name}]"


class Word(models.Model):
    id = models.IntegerField("Memrise's word ID", primary_key=True)
    word_a = models.CharField("Original word", max_length=1024)
    word_b = models.CharField("Translate", max_length=1024, null=True)
    level = models.ForeignKey("Level", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.word_a} --> {self.word_b}"
