"""
Routine Convert - folder hierarchy methods


Summary
-------
Routine convert will be looking in a specific folder hierarchy.  This aids in the creation of that structure, so that
users can start placing in media to have it ready for conversion!


Description
--------
Hierarchy (object):     class containing methods for creating/organizing media paths
"""
import os
import settings as st


class Hierarchy:
    # Put together all paths specified in settings (as properties)
    @property
    def disc_paths(self) -> dict:
        return {df: os.path.join(st.root_dir, df) for df in st.disc_formats}

    @property
    def media_paths(self) -> dict:
        return {mc_key: [os.path.join(dp, mc_val) for dp in self.disc_paths.values()]
                for mc_key, mc_val in st.media_categories.items()}

    @property
    def process_paths(self) -> dict:
        return {pd_key: [os.path.join(mp, pd_val) for v in self.media_paths.values() for mp in v]
                for pd_key, pd_val in st.process_dirs.items()}

    def source_paths(self):
        """
        Return process folder for source (files that need to be converted)
        """
        return self.process_paths[st.source_key]

    def output_paths(self):
        """
        Return process folder for output/converted (target path for new, compressed media file)
        """
        return self.process_paths[st.output_key]

    def old_source_paths(self):
        """
        Return process folder for original source (where to keep source files, after they are converted)
        """
        return self.process_paths[st.old_source_key]

    @staticmethod
    def path_list_to_string(path_list: list) -> str:
        """
        Summary
        ---
        Given the path_list, iterate through paths to format them with the intent to output in a log.

        :param path_list:
        :return: (str) a formatted string for printing paths nicely
        """
        path_str = '\n'
        for p in path_list:
            path_str += f'\t\t\t{p}\n'

        return path_str

    def create_media_tree(self):
        """
        Summary
        ---
        Make folder tree based on folder paths in the settings module

        :return: None
        """
        # If paths do not exist, make directories!
        for paths in self.process_paths.values():
            for p in paths:
                if os.path.exists(p) is False:
                    os.makedirs(p)

        # Output path locations for the user
        msg = (
            f'\n>>> ROOT Media path created at ->\t{st.root_dir}\n'
            f'{st.NEW_LINE_SEP}\n'
            f'>>> Place files you want TO CONVERT in:\t{self.path_list_to_string(self.source_paths())}\n'
            f'>>> Your converted files will be put in:\t{self.path_list_to_string(self.output_paths())}\n'
            f'>>> After converted, your original files will move to:'
            f'\t{self.path_list_to_string(self.old_source_paths())}\n'
        )
        print(msg)


if __name__ == "__main__":
    # For running this as a script in CLI, to make folder tree
    hi = Hierarchy()
    hi.create_media_tree()
