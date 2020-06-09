"""
Routine Convert - RUN handbrake!


Summary
-------
Handbrake is the tool that will convert the collected media files.  All available information or properties
will be used to convert a movie.  And it's okay if we have just minimal information - the goal here is to
automate as much of the process as can be done.  In the case of multiple movies or TV show folders, this
saves a great deal of time of having to deal with that. :)


Description
--------
Handbrake (object):     class containing preset data, list of media objects to convert and methods to
determine file locations before/after converting (such as moving "source" files to a different folder
when finished converting, so we don't attempt to convert them the next time!)
"""
import os
import subprocess

import routine_convert.settings as st
import routine_convert.source as sc


class Handbrake(object):
    # A list containing calls to handbrake, to loop through
    _clr_str_dict = {}

    # File format
    container = "av_mkv"
    ext = "mkv"

    # Handbrake presets. The JSON preset file for Handbrake follows a convention of <category>/<preset-name>
    # - Category (e.g.  General, Web, Devices, Matroska...)
    # - Preset name (e.g.  Very Fast 1080p30, Android 1080p30...)
    presets = {
        "DVD": r'/'.join([
            "Ryan",  # category
            "(Ryan) Apple 480p - Surround - 265 (Very Slow)"  # preset name
        ]),
        "Blu-Ray": r'/'.join([
            "Ryan",  # category
            "(Ryan) Apple 1080p - Surround - 265 (Very Slow)"  # preset name
        ]),
    }

    process_dirs = {
        'source': 'TO_CONVERT',  # Media ready for conversion
        'output': 'CONVERTED',  # Completed converted files, for review
        'old_source': 'SOURCE_PROCESSED',  # Media source moved into folder, no longer queued
    }

    # source_files = sc.SourceFiles().media
    source_files = sc.SourceFiles().movies  # For now, just converting movies!

    # ======================================================================================
    def __init__(self):
        pass

    def get_output_from_source_path(self, source: str) -> str:
        """
        Summary
        ---
        Given the source arg (filepath), return a string with the folder substituted for the "output" folder.

        :param source: str - filepath to the media location
        :return: str - output_folder
        """
        return source.replace(self.process_dirs['source'], self.process_dirs['output'])

    def get_processed_from_source_path(self, source: str) -> str:
        """
        Summary
        ---
        Given the source arg (filepath), return a string with the folder substituted for the "processed" folder.

        :param source: str - filepath to the media location
        :return: str - output_folder
        """
        return source.replace(self.process_dirs['source'], self.process_dirs['old_source'])

    def make_cli_str_from_media(self, media_list=None):
        """
        Summary
        ---
        Combine filenames and variables into a handbrake-ready string.  Reformat movie title
        to be in a more user-friendly name (best as possible).
        """
        if media_list:
            for m in media_list:
                output_media_name = m.title + '.{}'.format(self.ext)
                output_dir = os.path.dirname(self.get_output_from_source_path(m.filename))
                media_out = os.path.join(output_dir, output_media_name)
                preset = self.presets[m.disc_format]

                cli_str = '"{}" --preset-import-file "{}" -i "{}" --preset "{}" -o "{}" -f "{}"'.format(
                    st.HB_BIN, st.PRESET_FILE, m.filename, preset, media_out, self.container
                )

                self._clr_str_dict[m] = cli_str
        return self._clr_str_dict

    def process_cli_strs(self):
        """
        Summary
        ---
        Run the created CLI string(s).  This is expected to kick off handbrake processes, one after another.

        :return: None
        """
        for m, v in self._clr_str_dict.items():
            # Convert movie
            process = subprocess.run(v, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)

            if process.returncode:
                print("=======================ENCODING FAILED=========================\n{}".format(k))
                print("=======================ENCODING FAILED=========================")
            else:
                # Move old source file
                os.rename(m.filename, self.get_processed_from_source_path(m.filename))

    def run(self):
        """
        Summary
        ---
        Kick-off the conversion!

        :return: None
        """
        self.make_cli_str_from_media(self.source_files)
        self.process_cli_strs()


if __name__ == "__main__":
    hb = Handbrake()
    hb.run()
