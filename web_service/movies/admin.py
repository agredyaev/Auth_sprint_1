from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    list_filter = ("name",)
    search_fields = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    list_filter = ("role",)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
        "created_at",
        "updated_at",
    )
    list_filter = ("type",)
    search_fields = (
        "title",
        "description",
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "full_name",
        "created_at",
        "updated_at",
    )
