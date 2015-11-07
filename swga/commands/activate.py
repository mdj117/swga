import swga.database
import swga.primers
from swga.commands import Command


def main(argv, cfg_file):
    cmd = Command('activate', cfg_file=cfg_file)
    cmd.parse_args(argv)

    swga.database.init_db(cmd.primer_db)

    primers = swga.primers.read_primer_list(
        cmd.input,
        cmd.fg_genome_fp,
        cmd.bg_genome_fp
    )
    
    try:
        swga.primers.update_Tms(primers)
        swga.primers.update_locations(primers, cmd.fg_genome_fp)
        n_activated = swga.primers.activate(primers)
        swga.message("Marked {} primers as active.".format(n_activated))
    except AttributeError as e:
        swga.warn("Error updating database: '{}'".format(e.message))
        swga.warn(
            "Sometimes this happens if you're using a database created with "
            "an older version of swga. Please try creating a new workspace "
            "with `swga init` in another folder and adding these primers to "
            "that database instead."
        )
        raise e


