# file format

I describe about tgstore file format.

|No.|offset|size|endian|Name|description|
|--|--|--|--|--|
|1.|0|4||marker|represent marker about this file format. ['T','S','T','R']|
|2.|4|4|LE|header size|meta data size about contents|
|3.|8||header + size|utf-8 json formated header|max size is less than 32bit bytes|
|4.|8 + header size||content||

## standard json header

This table is standard json header

|key|value desription|type|example|
|--|--|--|--|
|content-length|content data length|number|13459112|
|title|The title of data contents|string|"Hello world data blog"|
|tags|list of strings which data creater assigned.|["text", "blog"]|
|content-type|system assigned data type. value must be mime type|"text/html"|
|note|additional information about the contents|"my first blog"|
