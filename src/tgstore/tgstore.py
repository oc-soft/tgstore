import math
import os
import sys
import tempfile

from .header import Header

class TgStore:
    """ taged store file """

    @classmethod
    def save_stream(cls, 
        header_data,
        content_strm,
        store_path,
        chunk_size: int=1024 ** 2):
        """ save data with header """
        with open(store_path, "wb") as dst_strm:
            tgstore = TgStore(chunk_size)
            if isinstance(header_data, Header):
                header = Header(dict(header_data.header))
            else:
                header = Header(dict(header_data))
            header.content_length = sys.maxsize * 2 + 1
            tgstore.write_marker(dst_strm)
            header_start = dst_strm.tell()
            header_size_len = 4
            header_size_with_padding = header.header_size
            dst_strm.seek(header_size_with_padding + header_size_len,
                          os.SEEK_CUR) 
            data_size = tgstore.write_content(content_strm, dst_strm)   
            # header will be shrink with actual data size
            header.content_length = data_size
            dst_strm.seek(header_start, os.SEEK_SET)
            tgstore.write_header(dst_strm, header, header_size_with_padding)


    @classmethod
    def save(cls, 
        header_data,
        content_path,
        store_path,
        chunk_size: int=1024 ** 2):
        """ save data with header """
        with open(content_path, "rb") as src_strm:
            cls.save_stream(header_data, src_strm, store_path, chunk_size)


    @classmethod
    def read_header(cls, 
        store_path):
        """ save data with header """

        result = None
        with open(store_path, "rb") as strm:
            tgstore = TgStore()
            tgstore.read_marker(strm)
            result, _ = tgstore.read_header_with_strm(strm)
        return result

    @classmethod
    def save_header(cls,
            header_data,
            store_path,
            chunk_size: int=1024 ** 2):
        """ save header """
        with tempfile.TemporaryFile() as tmp_content_strm:
            old_header = cls.read(store_path, tmp_content_strm, chunk_size)
            if isinstance(header_data, Header): 
                header_data = header_data.header
            new_header = dict(header_data) 
            new_header['content-length'] = old_header.content_length 
            tmp_content_strm.seek(0, os.SEEK_SET)
            cls.save_stream(new_header, tmp_content_strm, store_path)
        
        
    @classmethod
    def read(cls, store_path, dst_strm, chunk_size: int=1024 ** 2):
        """ read content """
        result = None
        with open(store_path, "rb") as strm:
            tgstore = TgStore(chunk_size)
            tgstore.read_marker(strm)
            result, _ = tgstore.read_header_with_strm(strm)
            if callable(dst_strm):
                dst_strm = dst_strm(result) 
            tgstore.read_content(result, strm, dst_strm) 
        return result 

    def __init__(self,
        chunk_size: int=1024 ** 2):
        """ constructor """
        self._chunk_size = chunk_size

    @property
    def path(self):
        return self._path


    @property
    def chunk_size(self):
        return self._chunk_size

    def read_marker(self, strm):
        """ read marker """
        mark_bytes = strm.read(4)
        return mark_bytes.decode() if mark_bytes else None 
    def write_marker(self, strm):
        """ write maker """
        strm.write(b'TSTR')

    def read_header_with_strm(self, strm):
        """ read header from file"""
        result = Header()
        header_size = result.read_from_stream(strm)
        return result, header_size

    def write_header(self, strm, header, header_size = None):
        """ write header """
        header.write_to_stream(strm, header_size)

    def read_content(self, header :Header, src_strm, dst_strm):
        """ read content """
        
        chunk = bytearray(self.chunk_size)
        read_count = math.ceil(header.content_length / self.chunk_size)

        for idx in range(read_count):
            read_size = src_strm.readinto(chunk)
            if read_size == 0:
                break
            if read_size < len(chunk):
                chunk = chunk[:read_size]
            dst_strm.write(chunk)

    def write_content(self, src_strm, dst_strm):
        """ write content """
        chunk = bytearray(self.chunk_size)
        total_size = 0
        while True:
            read_size = src_strm.readinto(chunk)
            if read_size == 0:
                break
            if read_size < len(chunk):
                chunk = chunk[:read_size]
            dst_strm.write(chunk)
            total_size += read_size
        return total_size
        
# vi: se ts=4 sw=4 et:
