from typing import Any, Dict

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork


class MoviesApiMixin:
    """
    Mixin for movie-related APIs to fetch and annotate movie data with genres,
    actors, directors, and writers using efficient database queries.
    """

    model = Filmwork
    http_method_names = ["get"]

    def get_queryset(self, external_id=None) -> QuerySet:
        """
        Fetches and annotates Model objects.

        Returns:
            QuerySet: Annotated queryset of objects.
        """

        if external_id is None:
            queryset = self.model.objects.all()
        else:
            queryset = self.model.objects.filter(id=external_id)

        queryset = (
            queryset.prefetch_related("genrefilmwork__genre", "personfilmwork__person")
            .values("id", "title", "description", "creation_date", "rating", "type")
            .annotate(
                genres=ArrayAgg("genrefilmwork__genre__name", distinct=True),
                actors=ArrayAgg(
                    "personfilmwork__person__full_name",
                    filter=Q(personfilmwork__role="actor"),
                    distinct=True,
                ),
                directors=ArrayAgg(
                    "personfilmwork__person__full_name",
                    filter=Q(personfilmwork__role="director"),
                    distinct=True,
                ),
                writers=ArrayAgg(
                    "personfilmwork__person__full_name",
                    filter=Q(personfilmwork__role="writer"),
                    distinct=True,
                ),
            )
        )

        return queryset

    def render_to_response(self, context, **response_kwargs):
        """
        Renders the context as a JSON response.

        Args:
            context (dict): The context containing the data to be rendered to JSON.

        Returns:
            JsonResponse: The HTTP response with the context rendered as JSON.
        """
        return JsonResponse(context, **response_kwargs)


class MoviesListApi(MoviesApiMixin, BaseListView):
    """API endpoint for listing movies with pagination."""

    paginate_by = 50

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """Includes pagination information in the context."""

        paginator, page, queryset, _ = self.paginate_queryset(
            self.get_queryset(), self.paginate_by
        )

        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": list(queryset),
        }

        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    """API endpoint for listing a single movie details."""

    def get_context_data(self, **kwargs):
        """Adds additional context for a single movie."""

        pk = self.kwargs.get("pk", None)
        movies = self.get_queryset(pk)
        context = get_object_or_404(movies)

        return context
