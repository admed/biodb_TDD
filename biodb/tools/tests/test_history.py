from unittest.mock import Mock
from unittest.mock import MagicMock
from unittest.mock import patch
# from unittest.mock import create_autospec
from unittest import TestCase
from datetime import datetime

from tools.history import generate_versions
from tools.history import CustomHistory


def mock_custom_history(version_id=0):
    """Create mock object for CustomHistory (ch)

    Helper Function to generate mocked ch objects.
    Function is generating ch objects based on mocked DjangoSimpleHistory
    (sh) object.
    """
    # mock SimpleHistory (sh) object
    sh_mock = Mock()
    # add required attrobutes
    sh_mock.create_by = f"UserCreate{version_id}"
    sh_mock.modify_by = f"UserMod{version_id}"
    sh_mock.create_date = datetime.now()
    # mock sh method
    sh_mock.get_history_type_display = MagicMock(
        return_value="Created")
    # create a CustomHistory (ch) object based on sh_mock
    with patch('tools.history.CustomHistory', autospec=True):
        ch_mock = CustomHistory(sh_mock, version_id)
        ch_mock.version_id = version_id
    return ch_mock


class HistoryTestCase(TestCase):

    def setUp(self):
        # create the empty list for mocked CustomHistory(ch) objects
        self.mocklist = []

        # set the list of mocked CustomHistory(ch) objects
        for num in range(10):
            ch_mock = mock_custom_history(num)
            self.mocklist.append(ch_mock)

    @patch.object(CustomHistory, '__init__')
    def test_generate_versions(self, mock_historyinit):
        # set the default return for __init__
        # required for mock class
        mock_historyinit.return_value = None
        # set the reference as generate_versions
        reference = generate_versions
        # check generate_versions with empty list
        emptymocklist = []
        emptyversions = reference(emptymocklist)
        # assert that CustomHistory wasn't called
        self.assertFalse(mock_historyinit.called)
        # assert that function is returning empty list
        self.assertEqual(emptyversions, [])
        # check the generate_versions for list of 10 SimpleHistory objects
        versions = reference(self.mocklist)
        self.assertTrue(mock_historyinit.called)
        self.assertEqual(mock_historyinit.call_count, 10)
        # each object from a list shoud be a CustomHistory type
        for version in versions:
            self.assertTrue(isinstance(version, CustomHistory))

    @patch.object(CustomHistory, 'get_diff_objects')
    @patch.object(CustomHistory, 'get_differ_values')
    def test_custom_history(self, mock_get_differ_values,
                            mock_get_diff_objects):
        # set the default ch mock object
        reference = mock_custom_history()
        # check generate_versions with empty list
        diff_objects = reference.get_diff_objects()
        self.assertEqual(mock_get_diff_objects.call_count, 1)
        # check the differ values
        differ_values = reference.get_differ_values("fieldname")
        # verify
        mock_get_differ_values.assert_called_with("fieldname")
