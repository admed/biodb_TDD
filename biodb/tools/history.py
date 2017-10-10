""""Tools to generate historical review."""
from collections import namedtuple


class CustomHistory():
    """Contains tools for display object history data in table.

    Wrapper for DjangoSimpleHistory - Application that track changes to
    instances of models and maintain a log of the changes.

    This class provides the wrapper for each SimpleHistory instance containing
    additional attrs and methods allowing to compare different versions
    and changes in github like style.
    """

    def __init__(self, SimpleHistObj, version_id, exclude=None):

        # get extra attr with version number
        self.version_id = version_id

        # store some of SimpleHistObj attrs
        # self.created_by = SimpleHistObj.create_by
        self.modify_by = SimpleHistObj.modify_by or SimpleHistObj.create_by
        self.modify_date = SimpleHistObj.modify_date
        # modyfication type "Created", "Changed", "Deleted"
        self.modify_type = SimpleHistObj.get_history_type_display()

        # store SimpleHistObj as current version
        self.curr_ver = SimpleHistObj
        # set self exclude as input kwarg or empty list if None
        if not exclude:
            self.exclude = []
        else:
            self.exclude = exclude

    def return_previous_version(self):
        """Return previous version of object or None"""
        # get previous version
        try:
            pr_ver = self.curr_ver.get_previous_by_history_date()

        # if DoesNotExist exception or different create_date
        # there is no previous version
        except self.curr_ver.DoesNotExist:
            return None
        if pr_ver.create_date != self.curr_ver.create_date:
            return None
        # return previous version
        return pr_ver

    def get_differ_fields(self):
        """Return list of model fields containing changes."""
        # create empty list for diff fileds
        diff_fields = []
        # get previous versions
        pr_ver = self.return_previous_version()
        # if there isn't previous version return empty list
        if not pr_ver:
            return diff_fields
        # get all field names in set
        fields = self.curr_ver.instance.get_fields(self.exclude)
        # search for differ fields
        for field in fields:
            # if field differ from curren version add it to list
            if getattr(self.curr_ver, field) != getattr(pr_ver, field):
                diff_fields.append(field)
        return diff_fields

    def get_differ_values(self, field):
        """ Get current and previous value for a given field."""
        # get previous versions
        pr_ver = self.return_previous_version()
        if not pr_ver:
            return ("", "")
        # set new and old values
        new_value = getattr(self.curr_ver, field) or ""
        old_value = getattr(pr_ver, field) or ""
        # return set of values
        return (old_value, new_value)

    def get_diff_objects(self):
        """Create difference objects for all diferent field for the instance.

        Function is returning list of difference objects conteining attributes:
        field name, new_value, old_value
        """
        # create empty list
        diff_objects = []
        # create object conteinter
        DiffField = namedtuple("DiffField",  # pylint: disable-msg=C0103
                               ["field", "new_value", "old_value"])
        # get list of differ fields
        fields = self.get_differ_fields()
        # for each field get differ values and write all to diff object
        for field in fields:
            # get diff values (old & new)
            old_value, new_value = self.get_differ_values(field)
            # create diff object
            diff_object = DiffField(field, new_value, old_value)
            # add object to list
            diff_objects.append(diff_object)
        # return list of diff objects
        return diff_objects


def generate_versions(history_objects, exclude=None):
    """Transform model.history.all() into CustomHistory instances list.

        Pass version_id number to CustomHistory constructor."""

    return [CustomHistory(version, version_id=idx)
            for idx, version in enumerate(reversed(history_objects), 1)]
