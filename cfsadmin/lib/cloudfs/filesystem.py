from private.filesystem_common import *
from private.cloudfs_paths import ExistValues, RestoreValue
from private.utils import set_debug

from errors import method_not_implemented
from container import Folder
from item import Item

class Filesystem(object):

    exists = ExistValues()

    def __init__(self, rest_interface):
            self.rest_interface = rest_interface

    def list(self, item, debug=False):
        """List contents of item if the item is a folder.

        :param item:    Folder to list the contents of.
        :param debug:   If true, will print the the request and response to stdout.

        :returns:   Dictionary representation of JSON response.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """
        path = item
        in_trash = False
        if isinstance(item, Item):
            path = item.url()
            in_trash = item.in_trash
        set_debug(self, debug)
        return list_items_from_path(self.rest_interface, path, in_trash)

    def root_container(self):
        """
        :return: A Folder representing the root of this users filesystem.
        """
        return self.root()

    def root(self):
        """
        :return: A Folder representing the root of this users filesystem.
        """
        return Folder.root_folder(self.rest_interface.get_copy())

    def list_trash(self, debug=False):
        """List the items in the trash.

        :param debug:   If true, will print the the request and response to stdout.
        :return:
        """
        set_debug(self, debug)
        result = self.rest_interface.list_trash(self.root_container().path())
        return create_items_from_json(self.rest_interface, result, None, True)

    def move(self, items, destination, exists=ExistValues.reuse, debug=False):
        """Move list of items to destination.

        :param items:       List of items to move.
        :param destination: Path or Folder to move the items to.
        :param exists:      How to handle if an item of the same name exists in the destination folder. Defaults to rename.
        :param debug:       If true, will print the the request and response to stdout.

        :returns:   Details of the new item(s) in a dictionary.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """
        return move_items(self.rest_interface, items, destination, exists, debug)

    def copy(self, items, destination, exists=ExistValues.reuse, debug=False):
        """Copy items to destination.

        :param items:       List of items to copy.
        :param destination: Path or Folder to copy the items to.
        :param exists:      How to handle if an item of the same name exists in the destination folder. Defaults to rename.
        :param debug:       If true, will print the the request and response to stdout.

        :returns:   Details of the new item(s) in a dictionary.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """
        return copy_items(self.rest_interface, items, destination, exists, debug)

    def restore(self, items, method=RestoreValue.fail, method_argument=None, debug=False):
        """Restore item(s) from trash.
        REST documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Recover%20Trash%20Item.html

        :param items:           Items or paths to restore.
        :param restore_method:  Determines method used to restore item.
        :param method_argument: Expected contents determined by value of restore_method
        :param debug:       If true, will print the the request and response to stdout.
        :return:    Items at new location.
        """
        set_debug(self, debug)
        results = []
        for item in items:
            path = item
            if isinstance(item, Item):
                path = item.path()
            results.append(self.rest_interface.restore_trash_item(path, method, method_argument))

        return results

    def list_shares(self, debug=False):
        set_debug(self, debug)
        result = self.rest_interface.list_shares()
        return create_items_from_json(self.rest_interface, result, None)

    def share_from_share_key(self, share_key, password=None, debug=False):
        from share import Share
        from errors import SharePasswordError
        try:
           return Share.share_from_share_key(self.rest_interface, share_key, password, debug)
        except SharePasswordError, e:
            raise SharePasswordError(e.request, e.response, e.message, e.INTERNAL_CODE)

    def create_share(self, items, debug=False):
        set_debug(self, debug)

        if not hasattr(items, '__iter__'):
            items = [items]

        items = map(lambda path: path.path() if isinstance(path, Item) else path, items)

        result = self.rest_interface.create_share(items)
        return create_items_from_json(self.rest_interface, result, None)[0]

    def file_history(self, item, debug=False):
        """NOT IMPLEMENTED: Get previous versions of item.
        REST documentation: https://www.bitcasa.com/cloudfs-api-docs/api/List%20History.html

        :param item:    Item to find previous versions.
        :param debug:   If true, will print the the request and response to stdout.
        :return:    List of previous versions of the item.
        """
        raise method_not_implemented(self, 'file_history')