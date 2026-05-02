import json
import struct
import sys

class Header:
    """ dtrack header """

    def __init__(self, header = None):
        """ constructor """
        if not header:
            self._header = {
                'content-length': sys.maxsize * 2 + 1
            }
        else:
            self._header = header
        pass

    def read_from_stream(self, stream):
        """ load data from stream """
        header_size_bytes = stream.read(4)
        header_size, = struct.unpack('<i', header_size_bytes)
        header_data = stream.read(header_size)
        header_data = header_data.rstrip(b'\0')
        self._header = json.loads(header_data.decode())
        return header_size

    def write_to_stream(self, stream, header_size = None):
        """ wrte stream """
        header_data_str = json.dumps(self._header)
        header_data = header_data_str.encode()
        if len(header_data) > sys.maxsize * 2 + 1:
            raise OverflowError()     
        if header_size is None:
            header_size = len(header_data)
        elif header_size < len(header_data):
            raise RuntimeError()
        header_size = len(header_data) if not header_size else header_size
        stream.write(struct.pack('<i', header_size))
        stream.write(header_data)
        padding_size = header_size - len(header_data)
        stream.write(bytearray(padding_size)) 

    @property
    def header_size(self):
        """ header size """
        header_data_str = json.dumps(self._header)
        header_data = header_data_str.encode()
        return len(header_data) 
        
 
    @property
    def header(self):
        return self._header

    def __getitem__(self, key: str):
        """ get value by key string"""
        return self.header[key]

    def __setitem__(self, key: str, value):
        """ set value by key """
        self.header[key] = value


    @property
    def title(self):
        return self['title']
    
    @title.setter
    def title(self, value):
        self['title'] = value


    @property
    def tags(self):
        return self['tags']
    
    @tags.setter
    def tags(self, value: list):
        self['tags'] = value

        
    @property
    def content_type(self):
        return self['content-type']

    @content_type.setter
    def content_type(self, content_type: str):
        self['content-type'] = content_type

    @property
    def note(self):
        return self['note']

    @note.setter
    def note(self, note: str):
        self['note'] = note


    @property
    def content_length(self):
        return self['content-length']

    @content_length.setter
    def content_length(self, length: int):
        self['content-length'] = length
        
# vi: se ts=4 sw=4 et:
