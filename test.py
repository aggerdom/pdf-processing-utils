from utilityclasses import GhostScript,PdfTk,Convert
import os
from unipath import Path
import unittest
import tempfile
from ocrmethods import convert_image
import shutil
from ocrmethods import get_text_from_image

testdir = Path(r"C:\tmp\pdfprocessing\tests")
testdir.chdir()
convert = Convert()



class TestPIL(unittest.TestCase):
    def test_id_times_roman(self):
        convert(r"C:\tmp\pdfprocessing\tests\test_pdf_page_tnr_noimage.pdf",
                r"C:\tmp\pdfprocessing\tests\test_pdf_page_tnr_noimage.tif")


class TestGhostScript(unittest.TestCase):
    def setUp(self):
        self.gs = GhostScript()
        self.testdir = testdir
        self.tempdir = tempfile.TemporaryDirectory()
        # print("creating tempdir: {}".format(os.path.abspath(self.tempdir.name)))

    def test_pdf_to_png(self):
        input_file = os.path.abspath("test_pdf_page_tnr_noimage.pdf")
        output_filename = "test_gs_pdf_to_png.png"
        output_file = os.path.join(self.tempdir.name,output_filename)
        self.gs.pdf_to_png(input_file,output_file)
        self.assertTrue(os.path.exists(output_file),"png file was not created")

    def test_png_to_pdf(self):
        pass

    def test_jpeg_to_pdf(self):
        pass

    def test_merge(self):
        list_of_pdfs = [r"C:\tmp\pdfprocessing\tests\pg_000{}.pdf".format(i) for i in range(1,5)]
        merged_loc = os.path.join(testdir,"merged_pdf.pdf")
        self.gs.merge_pdfs(list_of_pdfs,merged_loc)
        self.assertTrue(os.path.exists(merged_loc))
        self.addCleanup(os.remove,merged_loc)

    def tearDown(self):
        pass
        # for f in self.files_to_remove:
        #     os.remove(f)

