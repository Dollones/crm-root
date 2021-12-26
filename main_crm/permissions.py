from django.contrib.auth.mixins import AccessMixin


class SuperUserRequired(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OwnerRequired(AccessMixin):
    user_field = 'user'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_field_name = self.get_user_field()
        assert user_field_name, 'Должен быть указан user_field'

        if not request.user == getattr(self.object, user_field_name):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return getattr(self, 'object', None) or super().get_object()

    def get_user_field(self):
        return self.user_field
