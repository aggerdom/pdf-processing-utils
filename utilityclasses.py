from plumbum import local
import os
from glob import glob
from unipath import Path

class ShellUtilityWrapper(object):
    """docstring for ShellUtilityWrapper"""

    def __init__(self, shell_command, exe_location):
        """
        Parent class that is used for figuring out what plumbum command to provide for a class.
        """
        self.exe_location = exe_location
        # basic shell_command without arguments (ex: "ls")
        self.shell_command = shell_command
        if self.exe_location is None:
            self.cmd = local[shell_command]
            self.exe_location = str(self.shell_command)
        else:
            self.cmd = local[self.exe_location]

    def route_to_download_instructions(self,download_url):
        pass

    def __call__(self, *args, **kwargs):
        stdout_from_syscall = self.cmd(*args, **kwargs)
        return stdout_from_syscall


class GhostScript(ShellUtilityWrapper):
    """docstring for GhostScript"""

    def __init__(self, shell_command="gs", exe_location=None):
        ShellUtilityWrapper.__init__(self, shell_command, exe_location)

    def pdf_to_jpeg(self, pdf_filename, output_filename=None):
        if output_filename is None:
            # rename the filename from pdf to jpeg
            pass
        command = ["-sDEVICE=jpg",'-o',output_filename,pdf_filename]
        self(command)
        # raise NotImplementedError

    def jpeg_to_pdf(self,jpeg_filename, output_filename=None):
        """
        Takes the filename for a jpeg of a single page document and converts it to a single page pdf
        :param jpeg_filename: filename of jpeg image
        :type jpeg_filename: str
        :param output_filename: filename of pdf page being produced
        :type output_filename: str
        :return: output_filename (if successful)
        :rtype: str
        """
        raise NotImplementedError
        if output_filename is None:
            # Todo: jpeg to pdf filename logic
            raise NotImplementedError

    def pdf_to_png(self, pdf_filename, output_filename):
        raise NotImplementedError


class PdfTk(ShellUtilityWrapper):
    """
    Wrapper for the pdfTk commandline tool.
    ===============================================================================================
    SYNOPSIS
           pdftk <input PDF files | - | PROMPT>
                [ input_pw <input PDF owner passwords | PROMPT> ]
                [ <operation> <operation arguments> ]
                [ output <output filename | - | PROMPT> ]
                [ encrypt_40bit | encrypt_128bit ]
                [ allow <permissions> ]
                [ owner_pw <owner password | PROMPT> ]
                [ user_pw <user password | PROMPT> ]
                [ flatten ] [ need_appearances ]
                [ compress | uncompress ]
                [ keep_first_id | keep_final_id ] [ drop_xfa ] [ drop_xmp ]
                [ verbose ] [ dont_ask | do_ask ]
           Where:
                <operation> may be empty, or:
                [ cat | shuffle | burst | rotate |
                  generate_fdf | fill_form |
                  background | multibackground |
                  stamp | multistamp |
                  dump_data | dump_data_utf8 |
                  dump_data_fields | dump_data_fields_utf8 |
                  dump_data_annots |
                  update_info | update_info_utf8 |
                  attach_files | unpack_files ]
    ===============================================================================================
    """

    def __init__(self, shell_command="pdftk", exe_location=None):
        "pdftk_loc = None (if accessible from terminal) else fileloc"
        ShellUtilityWrapper.__init__(self, shell_command, exe_location)

    def burst_pdf(self, pdf_filename):
        """
        Break a multipage pdf into a seperate pdf for each page.

        Produces:
            ".\doc_data.txt" (contains metadata about pdf that was burst)
            ".\page_{pagenumber}.pdf" (a 1 page pdf for each page in the file)
        """
        self([pdf_filename, "burst"])

    def get_filenames_for_pages_from_burst_file(self, filedir=None):
        """Get a list of filenames created after calling `self.burst_pdf`"""
        glob_command = 'pg_*.pdf'
        if filedir is not None:
            glob_command = os.path.join(filedir, glob_command)
        found_pages = glob(glob_command)
        return found_pages

    def parse_doc_data(self, doc_data_filename):
        """Get metadata from "doc_data.txt" created when burst operation is called"""
        raise NotImplementedError("Need to write function to parse 'doc_data.txt'")
        metadata = {}
        with open(doc_data_filename) as f:
            pass

    def combine_pages(self,listofpages,output_filename=None):


class Deskew(object):
    """
    Wrapper for the deskew commandline tool.
    ===============================================================================================
    Deskew 1.10 (2014-03-03) by Marek Mauder
    http://galfar.vevb.net/deskew/
    Invalid parameters!
    Usage:
    deskew [-o output] [-a angle] [-t a|treshold] [-b color] [-r rect] [-f format] [-s info] input
        -o output:     Output image file (default: out.png)
        -a angle:      Maximal skew angle in degrees (default: 10)
        -t a|treshold: Auto threshold or value in 0..255 (default: a)
        -b color:      Background color in hex format RRGGBB (default: trns. black)
        -r rect:       Skew detection only in content rectangle (pixels):
                       left,top,right,bottom (default: whole page)
        -f format:     Force output pixel format (values: b1|g8|rgba32)
        -s info:       Info dump (any combination of):
                       s - skew detection stats, p - program parameters
        input:         Input image file

    Supported file formats
    Input:  BMP, JPG, PNG, JNG, GIF, DDS, TGA, PBM, PGM, PPM, PAM, PFM, PSD, TIF
    Output: BMP, JPG, PNG, JNG, GIF, DDS, TGA, PGM, PPM, PAM, PFM, PSD, TIF
    ================================================================================================
    """
    def __init__(self, shell_command="deskew", exe_location=None):
        """
        :param exe_loc: [None (if accessible from terminal) | The path of the executable]
        """
        ShellUtilityWrapper.__init__(self, shell_command, exe_location)
        self.project_url = "http://galfar.vevb.net/wp/projects/deskew/"

    def deskew_file(self,input_filename, output_filename=None, angle=None, threshhold=None, bg_color=None, pixel_format=None, rect=None, info=None):
        self.validate_input_filename(input_filename)
        self.validate_output_filename(output_filename)
        flag_val_pairs = {"-o": output_filename,
                          "-a": angle,
                          "-t": threshhold,
                          "-b": bg_color,
                          "-r": rect,
                          "-f": pixel_format,
                          "-s": info}
        flag_order = ["-o", "-a", "-t", "-b", "-r", "-f", "-s"]
        # Todo: Fileformat Validation
        # construct the parts of the command
        command = []
        for flag in flag_order:
            val = flag_val_pairs[flag]
            if val is not None:
                command.extend([flag, val])
        command.append(input_filename)
        # deskew the file
        self(*command)

    def validate_input_filename(self, input_filename):
        input_fileformat = Path(input_filename).ext
        valid_formats = (".bmp", ".jpg", ".png", ".jng", ".gif", ".dds",
                         ".tga", ".pbm", ".pgm", ".ppm", ".pam", ".pfm",
                         ".psd", ".tif")
        if input_filename not in valid_formats:
            error_message = "Deskew input file format error: {} is not one of these filetypes {}".format(
                input_filename, ",".join(valid_formats))
            raise ValueError(error_message)

    def validate_output_filename(self, output_filename):
        output_fileformat = Path(output_filename).ext
        valid_formats = (".bmp", ".jpg", ".png", ".jng", ".gif", ".dds",
                         ".tga", ".pgm", ".ppm", ".pam", ".pfm", ".psd",
                         ".tif")
        if output_fileformat not in valid_formats:
            error_message = "Deskew input file format error: {} is not one of these filetypes {}".format(
                output_filename, ",".join(valid_formats))
            raise ValueError(error_message)

class PdfXChangeViewer(object):
    """
    Automates OCRing a pdf and adding a textlayer using PdfXChangeViewer
    """
    raise NotImplementedError
    def __init__(self, arg):
        super(PdfXChangeViewer, self).__init__()
        self.arg = arg


def main():
    pdftk = PdfTk()

if __name__ == '__main__':
    main()
