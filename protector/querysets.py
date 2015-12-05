from django.db.models.query import QuerySet
from protector.internals import VIEW_PERMISSION_NAME, NULL_OWNER_TO_PERMISSION_OBJECT_ID, \
    NULL_OWNER_TO_PERMISSION_CTYPE_ID, _get_restriction_filter
from protector.helpers import filter_queryset_by_permission, get_view_permission


class PermissionQuerySet(QuerySet):
    """
        Queryset is used for filtering any queryset by user permissions on its objects
    """
    def filter_by_permission(self, user, permission):
        return filter_queryset_by_permission(self, user, permission)


class GenericUserToGroupQuerySet(QuerySet):
    def by_role(self, roles):
        utg_table_name = self.model._meta.db_table
        return self.extra(
            where=["{utg_table}.roles & %s".format(utg_table=utg_table_name)],
            params=[roles]
        )


class RestrictedQuerySet(PermissionQuerySet):
    """
        Queryset is used for filtering objects not visible to user
    """

    def visible(self, user=None):
        if user is None:
            return self.filter(restriction_id__isnull=True)
        if user.has_perm(VIEW_PERMISSION_NAME):
            return self
        if user.id is None:
            return self.filter(restriction_id__isnull=True)
        condition = self._get_visible_condition(user.id, get_view_permission().id)
        return self.extra(where=[condition])

    def _get_visible_condition(self, user_id, perm_id):
        condition = """
            {table_name!s}.restriction_id IS NULL OR
        """
        condition += _get_restriction_filter(self, user_id, perm_id)
        condition = condition.format(table_name=self.model._meta.db_table)
        return condition


class OwnerToPermissionQuerySet(QuerySet):
    def without_obj_perms(self):
        return self.filter(
            object_id=NULL_OWNER_TO_PERMISSION_OBJECT_ID,
            content_type_id=NULL_OWNER_TO_PERMISSION_CTYPE_ID
        )


class PermAnnotatedMixin(QuerySet):

    annotate_perms_for_user = None

    def annotate_perms(self, user):
        new_qset = self.all()
        new_qset.annotate_perms_for_user = user
        return new_qset

    def _fetch_all(self):
        super(PermAnnotatedMixin, self)._fetch_all()


class GenericGroupQuerySet(QuerySet):
    
    def update(self, *args, **kwargs):
        super(GenericGroupQuerySet, self).update(*args, **kwargs)
        to_update = {}
        for field, roles in self.model.MEMBER_FOREIGN_KEY_FIELDS:
            if field in kwargs:
                to_update[field]
                GenericUserToGroup.objects.filter(
                     
                )
