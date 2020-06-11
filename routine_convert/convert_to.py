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

import settings as st
import source as sc


class Handbrake:
    # TODO: Movies working for now, TV shows still need work (some shows have a file per episode, some don't
    #  and instead... lump a few together in one file!)
    # source_files = sc.SourceFiles().media
    source_files = sc.SourceFiles().movies

    # A dictionary containing media objects (keys) and strings (values) to call in handbrake CLI.
    _clr_str_dict = {}

    @staticmethod
    def get_output_from_source_path(source: str) -> str:
        """
        Summary
        ---
        Given the source arg (filepath), return a string with the folder substituted for the "output" folder.

        :param source: str - filepath to the media location
        :return: str - output_folder
        """
        return source.replace(st.process_dirs[st.source_key], st.process_dirs[st.output_key])

    @staticmethod
    def get_processed_from_source_path(source: str) -> str:
        """
        Summary
        ---
        Given the source arg (filepath), return a string with the folder substituted for the "processed" folder.

        :param source: str - filepath to the media location
        :return: str - output_folder
        """
        return source.replace(st.process_dirs[st.source_key], st.process_dirs[st.old_source_key])

    def make_cli_str_from_media(self, media_list=None):
        """
        Summary
        ---
        Combine filenames and variables into a handbrake-ready string.  Reformat movie title
        to be in a more user-friendly name (best as possible).
        """
        if media_list:
            for m in media_list:
                output_media_name = m.title + f'.{st.ext}'
                output_dir = os.path.dirname(self.get_output_from_source_path(m.filename))
                media_out = os.path.join(output_dir, output_media_name)
                preset = st.presets[m.disc_format]

                cli_str = f'"{st.HB_BIN}" --preset-import-file "{st.PRESET_FILE}" ' \
                          f'-i "{m.filename}" --preset "{preset}" -o "{media_out}" -f "{st.container}"'

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
                enc_fail_msg = '=======================ENCODING FAILED========================='
                print(f"{enc_fail_msg}\n{m.filename}\n{enc_fail_msg}")
            else:
                # Move old source file
                os.rename(m.filename, self.get_processed_from_source_path(m.filename))
        else:
            print('>>> No files found to convert!\n'
                  'Make sure you have media placed in your "TO_CONVERT" folder(s).\n'
                  'If you do not have any folder structure set up, make sure to\n'
                  'run this batch file FIRST:\n\n\t'
                  r'\routine_convert\bin\create_paths.bat')

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
    # For running this as a script in CLI, to begin conversion
    hb = Handbrake()
    hb.run()
