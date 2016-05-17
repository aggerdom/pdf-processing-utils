from utilityclasses import GhostScript
import os
from unipath import Path
import unittest


class TestGhostScript(unittest.TestCase):
    def test_pdf_to_png(self):
        testdir = Path(r"C:\tmp\pdfprocessing\test")
        testdir.chdir()
        input_file = "testpdf.pdf"
        output_file = Path(r"C:\tmp\pdfprocessing\test\test_gs_pdf_to_png.png")
        gs = GhostScript()
        gs.pdf_to_png(input_file,output_file)
        self.assertTrue(output_file.exists(),"File")


