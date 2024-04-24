from mixins import UpdatedAtMixin, IdMixin


class StateModel(UpdatedAtMixin):
    """Defines state model"""
    pass


class UpdatedAtId(UpdatedAtMixin, IdMixin):
    """Defines updated_at_id model"""
    pass
