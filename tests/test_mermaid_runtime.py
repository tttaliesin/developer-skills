import importlib.util
from pathlib import Path
import tempfile
import unittest
import sys

PACKAGE = Path(__file__).resolve().parents[1] / 'skills/design-doc-mermaid/scripts'
sys.path.insert(0, str(PACKAGE))
from mermaid_runtime import DiagramError, extract_blocks, render, convert_markdown


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.renderer = self.root / 'mmdc'
        self.renderer.write_text('''#!/usr/bin/env python3
import sys
from pathlib import Path
if '--version' in sys.argv:
 print('11.test');sys.exit(0)
src=Path(sys.argv[sys.argv.index('-i')+1]).read_text()
out=Path(sys.argv[sys.argv.index('-o')+1])
out.write_text('partial')
if 'BROKEN' in src:
 print('Parse error on line 1',file=sys.stderr);sys.exit(1)
if 'BROWSER_FAIL' in src:
 print('Failed to launch the browser process',file=sys.stderr);sys.exit(1)
out.write_text('<svg xmlns="http://www.w3.org/2000/svg"><text>'+src+'</text></svg>')
''')
        self.renderer.chmod(0o755)

    def source(self, text):
        p = self.root / 'source.mmd';p.write_text(text);return p

    def test_fences_and_duplicate_occurrences(self):
        text='````text\n```mermaid\nignored\n```\n````\n~~~mermaid\nflowchart TD; A-->B\n~~~\n```mermaid\nflowchart TD; A-->B\n```\n'
        blocks=extract_blocks(text)
        self.assertEqual([b.index for b in blocks],[1,2])
        self.assertEqual([b.content for b in blocks],['flowchart TD; A-->B\n']*2)
        self.assertNotEqual(blocks[0].start,blocks[1].start)

    def test_list_container_fence_rejected(self):
        with self.assertRaises(DiagramError):
            extract_blocks('- Item\n\n  ```mermaid\n  graph TD\n  A-->B\n  ```\n')

    def test_outside_block_line_endings_preserved(self):
        src=self.root/'doc.md';src.write_bytes(b'Before\r\n\r\n```mermaid\r\nflowchart TD\r\n```\r\n\r\nAfter\r\n')
        out=self.root/'result.md'
        convert_markdown(src,out,self.root/'images',mmdc=str(self.renderer))
        self.assertTrue(out.read_bytes().startswith(b'Before\r\n\r\n'))
        self.assertTrue(out.read_bytes().endswith(b'\r\nAfter\r\n'))

    def test_unclosed_block_rejected(self):
        with self.assertRaises(DiagramError):extract_blocks('```mermaid\nflowchart TD\n')

    def test_render_failure_preserves_existing_output(self):
        out=self.root/'existing.svg';out.write_text('trusted')
        with self.assertRaises(DiagramError) as error:
            render(self.source('BROKEN'),out,mmdc=str(self.renderer),overwrite=True)
        self.assertEqual(error.exception.code,'SYNTAX_ERROR')
        self.assertEqual(out.read_text(),'trusted')

    def test_browser_failure_is_not_syntax(self):
        with self.assertRaises(DiagramError) as error:
            render(self.source('BROWSER_FAIL'),self.root/'out.svg',mmdc=str(self.renderer))
        self.assertEqual(error.exception.code,'BROWSER_ERROR')

    def test_missing_renderer_creates_no_output(self):
        with self.assertRaises(DiagramError) as error:
            render(self.source('flowchart TD'),self.root/'out.svg',mmdc=str(self.root/'absent'))
        self.assertEqual(error.exception.code,'TOOL_MISSING')
        self.assertFalse((self.root/'out.svg').exists())

    def test_existing_output_requires_explicit_overwrite(self):
        out=self.root/'existing.svg';out.write_text('trusted')
        with self.assertRaises(DiagramError):
            render(self.source('flowchart TD'),out,mmdc=str(self.renderer))
        self.assertEqual(out.read_text(),'trusted')

    def test_duplicate_blocks_link_distinct_existing_images(self):
        src=self.root/'doc.md';src.write_text('```mermaid\nflowchart TD; A-->B\n```\n'*2)
        out=self.root/'result.md'
        result=convert_markdown(src,out,self.root/'images',mmdc=str(self.renderer))
        self.assertEqual(len(result['images']),2)
        self.assertNotEqual(result['images'][0],result['images'][1])
        for image in result['images']:
            self.assertTrue(Path(image).is_file())
            self.assertIn(Path(image).name,out.read_text())
        self.assertEqual(src.read_text(),'```mermaid\nflowchart TD; A-->B\n```\n'*2)

    def test_later_failure_preserves_document_and_images(self):
        src=self.root/'doc.md';src.write_text('```mermaid\nflowchart TD\n```\n```mermaid\nBROKEN\n```\n')
        out=self.root/'result.md';out.write_text('trusted doc')
        images=self.root/'images';images.mkdir();(images/'old.svg').write_text('trusted image')
        with self.assertRaises(DiagramError):convert_markdown(src,out,images,mmdc=str(self.renderer),overwrite=True)
        self.assertEqual(out.read_text(),'trusted doc')
        self.assertEqual(list(images.iterdir()),[images/'old.svg'])
        self.assertEqual((images/'old.svg').read_text(),'trusted image')

    def test_symlink_output_not_followed(self):
        victim=self.root/'victim';victim.write_text('private')
        out=self.root/'out.svg';out.symlink_to(victim)
        with self.assertRaises(DiagramError):render(self.source('flowchart TD'),out,mmdc=str(self.renderer),overwrite=True)
        self.assertEqual(victim.read_text(),'private')


if __name__=='__main__':unittest.main()
