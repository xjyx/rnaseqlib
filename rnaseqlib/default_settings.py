##
## Setting of default settings for pipeline
##
import os
import sys
import time

def set_settings_value(settings_info, section,
                       param, value):
    """
    Set settings value if there isn't a value already.
    """
    if section not in settings_info:
        return settings_info
    # If parameter does not have a value already, set it
    if param not in settings_info[section]:
        settings_info[section][param] = value
    return settings_info


def set_default_rnaseq_settings(settings_info):
    """
    Default settings that are RNA-Seq specific.
    """
    if settings_info["mapping"]["paired"]:
        # Compute mate inner dist based on read length
        mate_inner_dist = \
            settings_info["mapping"]["paired_end_frag"] - \
            (2 * settings_info["mapping"]["readlen"])
        settings_info = set_settings_value(settings_info,
                                           "mapping",
                                           "mate_inner_dist",
                                           mate_inner_dist)
    return settings_info


def set_default_riboseq_settings(settings_info):
    """
    Default settings that are Ribo-Seq specific.
    """
    return settings_info


def set_default_clipseq_settings(settings_info):
    """
    Default settings that are CLIP-Seq specific.
    """
    return settings_info


def section_error(section):
    print "Error in settings: cannot find %s section." \
        %(section)
    sys.exit(1)


def param_error(param, sect):
    print "Error in settings: cannot find parameter %s in section %s." \
        %(param, sect)
    sys.exit(1)


def check_settings(settings_info):
    """
    Error-check the settings.
    """
    required_sections = ["pipeline", "pipeline-files",
                         "mapping", "data"]
    # Check that the major sections are in place
    for section in required_sections:
        if section not in settings_info:
            section_error(section)
    ##
    ## Check that the major parameters are in place
    ##
    # Mapping from section to list of required parameters
    required_params = {"mapping": ["readlen"],
                       "pipeline-files": ["init_dir"]}
    for sect, sect_params in required_params.iteritems():
        for param in sect_params:
            if param not in settings_info[sect]:
                param_error(param, sect)
    # Check that paired-end specific parameters are correct
    if ("paired" in settings_info["mapping"]) and \
        settings_info["mapping"]["paired"]:
        if "paired_end_frag" not in settings_info["mapping"]:
            print "Error: Need \'paired_end_frag\' to be set for paired " \
                  "samples. Is your data paired-end?"
            sys.exit(1)
            

def set_default_settings(settings_info):
    """
    Set default global settings and data type
    specific settings.
    """
    if "data_type" not in settings_info["pipeline"]:
        print "Error: Need \'data_type\' to be set in [pipeline]."
        sys.exit(1)
    data_type = settings_info["pipeline"]["data_type"]
    if "paired" not in settings_info["mapping"]:
        # Not paired-end by default, only if no setting was given
        settings_info["mapping"]["paired"] = False
    if data_type == "rnaseq":
        settings_info = set_default_rnaseq_settings(settings_info)
    elif data_type == "riboseq":
        settings_info = set_default_riboseq_settings(settings_info)
    elif data_type == "clipseq":
        settings_info = set_default_clipseq_settings(settings_info)
    elif data_type == "selex":
        raise Exception, "Not implemented."
    else:
        print "Unknown data type %s." \
            %(data_type)
        sys.exit(1)
    # Set general default settings
    if "prefilter_miso" not in settings_info["settings"]:
        # By default, set it so that MISO events are not
        # prefiltered
        settings_info["settings"]["prefilter_miso"] = False
    return settings_info
