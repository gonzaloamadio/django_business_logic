# -*- coding: utf-8 -*-
import string
from slugify import slugify


def slug_generator(postid,title):
    """
        Generation of slug.
    """
    return "{title_slug}-{hashid}".format(
            hashid=postid,
            title_slug=slugify(title[:128])
        )

