from unittest import case

import requests


class DocGenerator:
    """
    test doc
    """
    doc_fields = ['name', 'desc', 'method', 'url', 'header', 'params', 'response_status', 'response_body', 'note']

    def __init__(self, *args, **kwargs):
        self._data = {}
        self._header = []
        for k, v in kwargs.items():
            setattr(self, k, v)
            self._data[k] = v
        self.fix_blank_field()

    def fix_blank_field(self):
        for name in self.doc_fields:
            try:
                self.__getattribute__(name)
            except AttributeError:
                self.__setattr__(name, '')

    def parse_header(self):
        header_line_list = []
        t = '| {}| {} | {}|\n'
        for each_header in self._header:
            key, val, required = each_header
            header_line_list.append(t.format(key, required, val))
        self.header = ''.join(header_line_list)

    def gen_doc(self, name=None):
        with open('doc_tmp.md', 'r+') as f:
            tmp = f.read()
            out = tmp.format(**self._data)
            output_filename = '{}.md'.format(name or self.name)
            with open(output_filename, 'w+') as of:
                of.write(out)


if __name__ == '__main__':
    a = DocGenerator(name='测试名称', desc='测试一下描述')
    a.gen_doc()


class TestCase(case.TestCase):
    """
    测试doc名称
    """

    client = requests.session()
    doc_gen = DocGenerator()

    def set_header(self, header_line):
        if isinstance(header_line, list):
            for line in header_line:
                key, value, required = line
                self.client.headers.update({key: value})
            self.doc_gen._header = header_line
        else:
            key, value, required = header_line
            self.client.headers.update({key: value})
            self.doc_gen._header.extend([header_line])

        self.doc_gen.parse_header()

    def setUp(self):
        self.set_header([
            ('jwt', 'xxxxxxxxx', 1)
        ])

    def tearDown(self):
        self.doc_gen.gen_doc(self.__doc__)

    def test_a(self):
        self.assertEqual(1, 2)
