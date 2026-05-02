import unittest
import tgstore 
import os
import io
import tempfile 

class Test1(unittest.TestCase):

    def test_save(self):
        tgst_h, tgst_path = tempfile.mkstemp()
        try:
            os.close(tgst_h)
            header = {
                'content-type': 'plain/text',
                'tags': [ 'txt', 'test' ]
            }
            src_content = """Hello world
Hello world 2"""
            with io.BytesIO(src_content.encode()) as src_strm:
                tgstore.TgStore.save_stream(header, src_strm, tgst_path, 5) 
            
            with io.BytesIO() as dst_strm:
                saved_header = tgstore.TgStore.read(tgst_path, dst_strm, 3)
                content = dst_strm.getvalue().decode()
                self.assertEqual(src_content, content)
                self.assertEqual(
                    saved_header['content-type'], header['content-type'])
                self.assertEqual(saved_header.tags, header['tags'])
        finally:
            os.remove(tgst_path)

# vi: se ts=4 sw=4 et:
