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

    def test_update_header(self):
        tgst_h, tgst_path = tempfile.mkstemp()
        try:
            os.close(tgst_h)
            header = {
                'content-type': 'plain/text',
                'tags': [ 'txt', 'test' ],
                'private': 'Private data'
            }
            src_content = """Hello world
Hello world 2
Hello world 3"""
            with io.BytesIO(src_content.encode()) as src_strm:
                tgstore.TgStore.save_stream(header, src_strm, tgst_path, 5) 

            header['tags'] += 'internal-tags'
            header['note'] = 'A note for test'           

            tgstore.TgStore.save_header(header, tgst_path, 7) 

            with io.BytesIO() as dst_strm:
                saved_header = tgstore.TgStore.read(tgst_path, dst_strm, 3)
                content = dst_strm.getvalue().decode()
                self.assertEqual(src_content, content)
                self.assertEqual(
                    saved_header['content-type'], header['content-type'])
                self.assertEqual(saved_header.tags, header['tags'])
                self.assertEqual(saved_header.note, header['note']) 
        finally:
            os.remove(tgst_path)

    def test_save_callable(self):
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
                saved_header = None
                def get_strm(header):
                    nonlocal saved_header
                    saved_header = header
                    return dst_strm
                tgstore.TgStore.read(tgst_path, get_strm, 3)

                content = dst_strm.getvalue().decode()
                self.assertEqual(src_content, content)
                self.assertEqual(
                    saved_header['content-type'], header['content-type'])
                self.assertEqual(saved_header.tags, header['tags'])
        finally:
            os.remove(tgst_path)



# vi: se ts=4 sw=4 et:
