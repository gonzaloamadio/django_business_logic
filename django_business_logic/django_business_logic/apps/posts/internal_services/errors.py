# -*- coding: utf-8 -*-
"""Define custom errors for this app."""


class Error(Exception):
    """Global error for this app. If we catch this, we will cath all childs.

    Usage::

        from errors import Error as PostsError

        try:
            # action on posts
        except PostsError:
            # Handle all errors from account
    """

    pass


class InvalidDateOrder(Error):
    """When date of end is before date of start."""

    pass


class InvalidCategories(Error):
    """When choosen categories does not match to same group.

    This should not occur, as they should be filtered in front end. But anyway we
    should take care of this.
    """

    def __init__(self, parent, son):
        self.parent = parent
        self.son = son

    def __str__(self):
        return 'Choosen categories does not belong together: {}, {}'.format(
            self.parent, self.son,
        )
