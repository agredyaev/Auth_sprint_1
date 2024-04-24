import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    """Mixin that adds timestamp fields to a model, recording creation and last modification times."""

    created_at = models.DateTimeField(_("row_creation_datetime"), auto_now_add=True)
    updated_at = models.DateTimeField(_("row_modification_datetime"), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """Mixin that adds a UUID primary key field to a model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(TimeStampedMixin, UUIDMixin):
    # noinspection GrazieInspection
    """Genre represents a category of artistic composition, as in music or literature,
    characterized by similarities in form, style, or subject matter.
    """
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("genre")
        verbose_name_plural = _("genres")
        indexes = [
            models.Index(fields=["name", "description"], name="name_description_idx")
        ]


class Filmwork(TimeStampedMixin, UUIDMixin):
    """Filmwork represents a cinematic or television production or movie."""

    MOVIE = "movie"
    TV_SHOW = "tv_show"
    TYPE_CHOICES = [
        (MOVIE, _("Movie")),
        (TV_SHOW, _("TV Show")),
    ]

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.DateField(_("release_date"), blank=True, null=True)
    rating = models.FloatField(
        _("rating"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(
        _("type"), max_length=255, choices=TYPE_CHOICES, default=MOVIE
    )
    file_path = models.FileField(
        _("file"),
        blank=True,
        null=True,
        upload_to="movies/",
        help_text=_("Select a file to upload."),
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("film work")
        verbose_name_plural = _("film works")
        indexes = [models.Index(fields=["title", "rating"], name="title_rating_idx")]


class Gender(models.TextChoices):
    MALE = "male", _("male")
    FEMALE = "female", _("female")


class Person(TimeStampedMixin, UUIDMixin):
    """Person represents an individual involved in the creation or production of
    film works, such as actors, directors, or writers.
    """

    full_name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return str(self.full_name)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("person")
        verbose_name_plural = _("people")
        indexes = [models.Index(fields=["full_name"], name="full_name_idx")]


class GenreFilmwork(UUIDMixin):
    """
    Represents the association between Filmwork and Genre entities.
    This model is used to create a many-to-many relationship, where a single
    film work can be associated with multiple genres and vice versa.
    """

    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    genre = models.ForeignKey(
        "Genre", verbose_name=_("genre"), on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _("genre film work")
        verbose_name_plural = _("genre film works")
        indexes = [models.Index(fields=["created_at"], name="created_at_idx")]
        constraints = [
            models.UniqueConstraint(
                fields=["genre_id", "film_work_id"], name="unique_genre_id_film_work_id"
            )
        ]


class PersonFilmwork(UUIDMixin):
    """
    Represents a many-to-many relationship between a Person and a Filmwork,
    defining the role a person has in a particular film work.
    """

    ACTOR = "actor"
    DIRECTOR = "director"
    WRITER = "writer"
    TYPE_CHOICES = [
        (ACTOR, _("Actor")),
        (DIRECTOR, _("Director")),
        (WRITER, _("Writer")),
    ]

    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    person = models.ForeignKey(
        "Person", verbose_name=_("person"), on_delete=models.CASCADE
    )
    role = models.TextField(
        _("role"), blank=False, null=True, choices=TYPE_CHOICES, default=ACTOR
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _("person film work")
        verbose_name_plural = _("person film works")
        indexes = [
            models.Index(fields=["created_at", "role"], name="created_at_role_idx")
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["id", "person_id", "film_work_id"],
                name="unique_id_person_id_film_work_id",
            )
        ]
