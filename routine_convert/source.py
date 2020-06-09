"""
Routine Convert - source objects


Summary
-------
Common variables to be used throughout module should live in this spot.


Description
--------
SourceFiles (object):     Class for organizing and fetching media information.  Primarily, there are operations
for looking up media filepaths on a user's hard drive.  Additionally, being able to look up data on IMDb to be
used with associated media will come in handy.  IMDb is useful because we can pull not just metadata down but
a poster URL, so we can download a poster as a JPG and include that in a movie directory.
"""
import os
import re

import imdb

import media as me
import settings as st


class SourceFiles(object):
    media_on_disk = []

    # OPTIONAL: Added files to convert
    movie_files = []

    # Media type and it's associated class.
    # Example: since TV shows have additional info than movies, different subclasses will be used for them
    media_types = {
        'Movies': me.Movie,
        'TV Shows': me.Show
    }

    # Instance IMDb package (to grab movie or TV show info)
    # (http://www.imdb.com)
    ia = imdb.IMDb()

    @staticmethod
    def make_title(sentence):
        """
        Reformat a title.  To address titles that may all contain uppercase characters, use a regex pattern to replace
        all uppercase characters with lowercase.  Then, identify beginning letters (in "group 0") and capitalize them.

        Example:
        BEFORE  > DR. STRANGELOVE - OR HOW I LEARNED TO STOP WORRYING AND LOVE THE BOMB
        AFTER   > Dr. Strangelove - Or How I Learned To Stop Worrying And Love The Bomb

        :return: (str) reformatted title
        """
        return re.sub(r"\w+[A-Za-z]+('[A-Za-z]+)?", lambda m: m.group(0).capitalize(), sentence)

    def _get_media_on_disk(self):
        """
        Walk from root directory down media paths that exist.  Return found files as media objects.

        Warning:  It is time consuming to perform multiple walks on the OS!!!  So, limit use of this method.

        :return: (list) media_objects
        """
        media_objects = []

        for df in st.DISC_FORMATS.values():
            # Initial sub-folder (disc format) off of the "media root" folder
            # ex:
            #
            #       C:\Media_Root
            #           \DVD        <-
            #           \Blu-Ray    <-
            #
            disc_type_path = os.path.join(st.root_dir, df)
            if os.path.exists(disc_type_path):
                media_objects += self._get_media_objects_from_directory(disc_type_path, disc_format=df)
            else:
                raise FileExistsError('Media directory does not exist for in directory: {}'.format(disc_type_path))

        return media_objects

    def _get_media_objects_from_directory(self, dir_, disc_format=''):
        """
        Given the dir arg, perform an os.walk operation on the path.  Return any media objects found, by their subclass,
        if the last index exists (the last index only exists when a file is found from the walk method).

        :param dir_: (str) directory to begin search
        :param disc_format: (optional -> str) if supplied, add disc format to class property
        :return: found_media
        """
        found_media = []

        for media_type_as_name, media_obj in self.media_types.items():
            # Look in media sub-folder, which will be underneath a disc format folder
            # ex:
            #
            #       C:\Media_Root
            #           \DVD
            #              \TV Shows    <-
            #              \Movies      <-
            #           \Blu-Ray
            #              \TV Shows    <-
            #              \Movies      <-
            #
            full_media_path = os.path.join(dir_, media_type_as_name)

            for fm in os.walk(full_media_path):
                for base_m in fm[-1]:
                    found_file = os.path.normpath(os.path.join(fm[0], base_m))

                    # Use associated class, for the sub-folder name (Movies -> Movie class, TV Shows -> Show class...)
                    media = media_obj(found_file)
                    if disc_format:
                        media.disc_format = disc_format
                    found_media.append(media)

        return found_media

    def media_grabber(self, *args, **kwargs):
        """
        Summary
        ---
        Wrapper to use for class properties that contain media.  This is a helpful function when calling other class
        properties that are looking up existing media in the class (movies or shows, for example).

        :param args: collection of arguments to
        :param kwargs:
        :return:
        """
        def wrapper(cls):
            media = cls.media_on_disk
            if media:
                pass
            else:
                media = cls._get_media_on_disk()
            return media
        return wrapper

    @property
    @media_grabber
    def media(self):
        return self.media_on_disk

    @media.setter
    def media(self, refresh):
        """
        Summary
        ---
        If media property is set to a value, perform another fetch of media on disk.

        :return: None
        """
        if refresh:
            self.media_on_disk = self._get_media_on_disk()

    @property
    def movies(self):
        return [m for m in self.media if isinstance(m, me.Movie)]

    @property
    def shows(self):
        return [m for m in self.media if isinstance(m, me.Show)]

    def _set_metadata_from_imdb(self, media):
        """
        Given Media class arg, lookup title on IMDb.  Determine if the titles given in the title can be
        found from an IMDb lookup.  Any valid matches found will fill in metadata found from the IMDb title.

        Based on the media instance, determine the subtype and perform lookup if unique
        (for example, if it's a TV show we need to search it differently vs. a movie)

        :param media: (Media) class object
        :return: (Media instance)
        """
        if media:
            # TODO: Identify movie with year.  First result is best guess, based on popularity (usually).  That
            #  can get subjective with remakes/reboots.
            if isinstance(media, me.Movie):
                title_search = self.ia.search_movie(media.title)
                if title_search:
                    id = title_search[0].getID()
                    movie = self.ia.get_movie(id)
                    # print(movie.infoset2keys)
                    print(movie.current_info)
                    print(movie.get('runtimes'))

            # TODO: TV show titles can be tricky, when organized on the hard drive straight from
            #  disc. Seems like there's not really a standard way to do it.  May have to instruct user
            #  on how to organize shows so they are identified right.
            if isinstance(media, me.Show):
                title_search = self.ia.search_movie(media.title)
                if title_search:
                    id = title_search[0].getID()
                    show = self.ia.get_episode(id)
                    # print(show.infoset2keys)
                    print(show.current_info)
                    # print(show.get('runtimes'))

        return media

    def lookup_all_media_on_imdb(self):
        """
        Summary
        ---
        Go through all media in class and set all metadata.

        :return: None
        """
        for m in self.media:
            self._set_metadata_from_imdb(m)

