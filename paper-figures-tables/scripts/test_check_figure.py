"""Counterexamples to generic format and metadata-based hard failures."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
import unittest
from PIL import Image
from pypdf import PdfWriter
from pypdf.generic import DictionaryObject,NameObject,ArrayObject,DecodedStreamObject
from check_figure import check_figure

class FigureDiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.temp=TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def raster(self,name,size,dpi=None):
        path=self.root/name
        Image.new('RGB',size,'white').save(path,**({'dpi':dpi} if dpi else {}))
        return path

    def test_jpeg_and_low_metadata_dpi_do_not_invent_venue_requirement(self):
        path=self.raster('photo.jpg',(800,600),(72,72))
        issues,_=check_figure(path)
        self.assertNotIn('FAIL',[s for s,_ in issues])

    def test_final_pixel_density_overrides_low_embedded_dpi(self):
        path=self.raster('figure.png',(1200,900),(72,72))
        issues,info=check_figure(path,300,(4,3))
        self.assertNotIn('FAIL',[s for s,_ in issues])
        self.assertEqual([300,300],info['checked_dpi'])

    def test_high_metadata_dpi_cannot_hide_insufficient_final_pixels(self):
        path=self.raster('small.png',(300,300),(600,600))
        issues,_=check_figure(path,300,(3,3))
        self.assertIn('FAIL',[s for s,_ in issues])

    def test_both_axes_are_checked(self):
        path=self.raster('uneven.png',(600,600),(300,72))
        issues,_=check_figure(path,300)
        self.assertIn('FAIL',[s for s,_ in issues])

    def test_missing_metadata_uses_final_dimensions(self):
        path=self.raster('no-meta.png',(600,400))
        issues,info=check_figure(path,200,(3,2))
        self.assertNotIn('FAIL',[s for s,_ in issues])
        self.assertEqual('pixels_at_declared_final_size',info['resolution_basis'])

    def test_svg_with_raster_layer_is_not_a_format_failure(self):
        path=self.root/'mixed.svg'
        path.write_text('<svg xmlns="http://www.w3.org/2000/svg"><image href="data:image/png;base64,AAAA"/></svg>')
        issues,_=check_figure(path)
        self.assertNotIn('FAIL',[s for s,_ in issues])
        self.assertTrue(issues)  # image fidelity still requires actual rendering

    def test_bad_svg_and_corrupt_raster_fail(self):
        for name in ['bad.svg','bad.png']:
            path=self.root/name;path.write_text('not an image')
            self.assertIn('FAIL',[s for s,_ in check_figure(path)[0]])

    def test_type0_descendant_font_program_is_detected(self):
        writer=PdfWriter();page=writer.add_blank_page(width=100,height=100)
        program=DecodedStreamObject();program.set_data(b'font-program-fixture')
        descriptor=DictionaryObject({NameObject('/FontFile2'):writer._add_object(program)})
        descendant=DictionaryObject({NameObject('/Subtype'):NameObject('/CIDFontType2'),NameObject('/BaseFont'):NameObject('/FixtureFont'),NameObject('/FontDescriptor'):writer._add_object(descriptor)})
        font=DictionaryObject({NameObject('/Subtype'):NameObject('/Type0'),NameObject('/DescendantFonts'):ArrayObject([writer._add_object(descendant)])})
        page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):writer._add_object(font)})})
        path=self.root/'font.pdf';writer.write(path)
        self.assertEqual([],check_figure(path)[0])

    def test_invalid_dimensions_are_rejected(self):
        for target in [(0,1),(-1,1),(float('nan'),1)]:
            with self.assertRaises(ValueError):
                check_figure(self.root/'missing.png',300,target)

    def test_cli_strict_only_fails_definite_or_explicit_threshold_errors(self):
        path=self.raster('photo.jpg',(300,300),(72,72))
        script=Path(__file__).with_name('check_figure.py')
        base=[sys.executable,str(script),str(path),'--strict']
        self.assertEqual(0,subprocess.run(base,capture_output=True).returncode)
        self.assertEqual(2,subprocess.run(base+['--min-dpi','300','--width-in','3','--height-in','3'],capture_output=True).returncode)

if __name__=='__main__':
    unittest.main()
