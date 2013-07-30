# -*- coding: utf-8 -*-
"""
Content Organizer

This plugin will accomplish a few things:

	1. Rename your posts in a prettier former: YYYY-MM-DD-slug.ext
	2. Organize your posts in the content/ folder by yyyy/mm/YYYY-MM-DD-slug.EXT

Both these options can be turned off via your pelicanconf.py file (both default to False)

CO_RENAMER_ENABLE = False (set to True to enable)
CO_ORGANIZER_ENABLE = False (set to True to enable)

Some extra settings:

CO_RENAMER_GRACE = 15     # Amount of minutes to wait until the last modified timestamp before renaming content

========================

"""

from os import path, rename, stat
from time import strftime, strptime, time
import datetime
from pelican import signals

def _co_renamer(generator):
	renamer_grace = generator.settings.get('CO_RENAMER_GRACE', 0)

	for article in generator.articles:
		(a_filepath, a_filename) = path.split(article.source_path)
		a_extension = path.splitext(article.source_path)[1]
		a_date_struct = strptime(str(article.date), "%Y-%m-%d %H:%M:%S")
		a_difftime = int((time() - stat(article.source_path).st_mtime) / 60)
		a_new_filename = a_filepath + "/" + strftime("%Y-%m-%d-", a_date_struct) + article.slug + a_extension
		
		if not (article.source_path == a_new_filename) and (a_difftime > renamer_grace):
			rename(article.source_path, a_new_filename)


def _co_organizer(generator):
	print "Not yet complete"

def initialize(generator):
	renamer_enable = generator.settings.get('CO_RENAMER_ENABLE', False)
	organizer_enable = generator.settings.get('CO_ORGANIZER_ENABLE', False)
	
	if renamer_enable:
		_co_renamer(generator)
	
	if organizer_enable:
		_co_organizer(generator)

				
def register():
	signals.article_generator_finalized.connect(initialize)
