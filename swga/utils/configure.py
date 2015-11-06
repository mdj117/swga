import os
import ConfigParser

import swga

# This is the name used by default when writing a config file post-init
default_config_file = 'parameters.cfg'


def parse_config(cfg_file, section):
    '''
    Parses a config file in the given section. Missing sections and values do
    not raise an error (but missing values may give a warning).

    Returns:
    - defaults: a dict of values in the given section
    '''
    config = ConfigParser.SafeConfigParser()
    defaults = {}
    if not os.path.isfile(cfg_file):
        swga.error(
            "Cannot find parameters file. Run `swga init` or specify options "+
            "manually.", exception=False)
        return {}
    with open(cfg_file) as cfg_file_fp:
        config.readfp(cfg_file_fp)
        try:
            defaults = dict(config.items(section))
        except ConfigParser.NoSectionError:
            defaults = {}
        return defaults