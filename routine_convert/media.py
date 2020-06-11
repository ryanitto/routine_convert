"""
Routine Convert - media objects


Summary
-------
Classes for media.  These will be used to contain metadata, file information and other information
about its type.  When time comes to convert media, it's quite helpful to know if it's a DVD vs. Blu-Ray,
in order for the correct conversion preset to be used (h265 codec with specific compression settings).


Description
--------
Media (object):     base class for media; largely used for storing information from ffprobe and IMDb
Movie (Media):      subclass for movies
Show (Media):       subclass for TV shows
"""
import datetime
import json
import subprocess
import os

import settings as st


class Media:
    """
    Summary
    ---
    Media class that contains data about a movie file (preferably either an .mp4 or .mkv file).  Helpful metadata,
    such as title, year, disc format (DVD/blu-ray), duration, etc can be useful when converting the media and
    organizing it on a file system.
    """
    source_title = ''
    year = ''
    disc_format = ''
    media_category = ''

    filename = ''
    nb_streams = 0
    nb_programs = 0
    format_name = ''
    format_long_name = ''
    start_time = ''
    duration = ''
    size = ''
    bit_rate = ''
    probe_score = 0
    encoder = ''
    creation_time = ''

    # tags = {}   # for debugging

    def __init__(self, media_file):
        self.set_attrs_from_probe(self._probe_media_to_dict(media_file))

    def __repr__(self):
        """
        Summary
        ---
        Return media title.  Include year if it has a value.

        :return: None
        """
        return '__'.join([
            str(self.__class__.__name__),
            self.title + (f' ({self.year})' if self.year else '')
        ])

    @property
    def title(self):
        # If the source file contains title metadata, go ahead and return
        if self.source_title:
            return self.source_title
        # Otherwise, make one from the filename itself
        else:
            return self.basename.title()

    @title.setter
    def title(self, name):
        self.source_title = name

    @property
    def basename(self):
        return str(os.path.basename(self.filename).split('_t')[0])

    @staticmethod
    def _probe_media_to_dict(file_):
        """
        Use FFPROBE to retrieve metadata contained in file.

        :return: (dict) output_dict (FFPROBE format data)
        """
        output_dict = {}

        probe_args = str(st.SPC_SEP.join(
            [st.FFPROBE,
             '-i', f'"{file_}"',
             '-print_format', 'json',
             '-pretty', '-show_format'
             ]
        ))
        out = subprocess.check_output(probe_args, stderr=subprocess.PIPE)
        out_to_json = json.loads(out)
        if out_to_json:
            output_dict = out_to_json[st.FFPROBE_FMT_STR]
            nested_dicts = {k: v for k, v in output_dict.items() if isinstance(v, dict) for k, v in v.items()}
            output_dict.update(nested_dicts)
        return output_dict

    def set_attrs_from_probe(self, probe_dict):
        """
        Summary
        ---
        The result from the probe of the media file (JSON) will be used to set class attributes.  Check to
        see if data in the JSON file matches a class variable.

        :return: None
        """
        for k, v in probe_dict.items():
            if hasattr(self, k):
                setattr(self, k, v)

    @property
    def duration_to_minutes(self):
        """
        Summary
        ---
        Get the duration in minutes by converting the HH:MM:SS.FFF.. time format retrieved from probing media.

        :return: (int) total length of media in minutes
        """
        dur_to_time = datetime.datetime.strptime(self.duration, '%H:%M:%S.%f0') - datetime.datetime(1900, 1, 1)
        return round(dur_to_time.total_seconds() / 60)


class Movie(Media):
    """
    Summary
    ---
    Movie type.  Contains all movie-specific class variables or methods to assist in converting a motion picture.
    """
    media_category = st.movie_cat


class Show(Media):
    """
    Summary
    ---
    TV show type.  Contains all specific class variables or methods to assist in converting a TV show.
    """
    media_category = st.show_cat

    show_title = ''
    season = 0
    episode_title = ''
    episode_num = 0

    @property
    def title(self):
        return self.show_title

    @title.setter
    def title(self, name):
        """
        Summary
        ---
        TV shows can contain redundant words (like including "disc" or "season" in the name itself). When
        setting the title, to save time, clear out some of these words if possible.

        While doing so, this is the step to filter out unique things like "episode number" into the class
        member variable.  This will come in handy, later, when comparing data on IMDb.

        :type name: (str) full title of episode/show name
        """
        # TODO: TV shows don't have consistent naming :(, need a better way to clear out words like "season" or
        #  "disc" consistently.  If possible?
        name = name.lower().replace('disc', '')
        name = name.lower().replace('season', '')
        name = st.SPC_SEP.join([x for x in name.split(st.SPC_SEP) if x.isalnum()]).title()
        self.show_title = name

    @staticmethod
    def make_episode_tagged(show_name, season, show_num, episode_titlename=None):
        """
        Create episode tag to insert in filename, as a suffix

        :param show_name: (str): name of the show (e.g.  "The Simpsons")
        :param season: (int): season number (e.g. 4)
        :param show_num: (int): show number (e.g. 12)
        :param episode_titlename: (str): title of the episode (e.g.  "Marge vs. the Monorail")
        :return: (str): episode
        """
        # Combined title (e.g. "The Simpsons_s01e01")
        episode = st.USCORE_SEP.join([str(show_name), 's{:02d}e{:02d}'.format(season, show_num)])

        if episode_titlename and type(episode_titlename) is str:
            episode = st.WIDE_DASH_SEP.join([episode, episode_titlename])

        return episode