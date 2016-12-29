from utilityclasses import GhostScript,PdfTk,Deskew

ghostscript = GhostScript()
pdftk = PdfTk()
deskew = Deskew()

def deskew_single_pdf_page(filename, output_filename=None):
    """
    Takes a single page pdf document, and deskews it.

    :param filename: Filename of pdf page to be deskewed
    :type filename: str
    :param output_filename: Desired filename for the deskewed pdf page
    :type output_filename: [NoneType|str]
    :return: filename of deskewed pdf page
    :rtype: str
    """
    # figure out output filename
    # convert the pdf page to jpeg
    jpeg_page_filename = ghostscript.pdf_to_jpeg(filename,output_filename)
    # Deskew the jpeg page
    deskewed_jpg_page_filename = deskew.deskew_file(jpeg_page_filename,output_filename=None)
    # Convert the deskewed jpg page back to pdf
    pdf_pagename = ghostscript.jpeg_to_pdf(deskewed_jpg_page_filename,output_filename=None)
    # return the name of the new pdf
    return pdf_pagename


def fix_skewed_pdf(pdf_filename, output_filename=None):
    """
    Takes a pdf file with skewed pages and returns a pdf file with the pages deskewed
    """
    # Burst the pdf
    pages = pdftk.burst_pdf(pdf_filename)
    # Recombine (concatenate) the deskewed pdf pages into a single document
    # Todo: Possibly set meta-data back to that of the original pdf
    # metadata = pdftk.parse_docdata
    deskewed_pages = []
    for page in pages:
        deskewed_page = deskew_single_pdf_page(page)
        deskewed_pages.append(deskewed_page)
    recombined_pdf_filename = pdftk.combine_pages(deskewed_pages)
    # Return the filename of the pdf
    return recombined_pdf_filename

