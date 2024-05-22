from etl_service.models.mixins import IdMixin, UpdatedAtMixin


class StateModel(UpdatedAtMixin):
    """Defines state model"""

    pass


class UpdatedAtId(IdMixin, UpdatedAtMixin):
    """Defines updated_at_id model"""

    pass
