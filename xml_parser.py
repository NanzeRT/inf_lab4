import pprint

class XmlObject:
    def __init__(self, tag):
        self.tag = tag
        self.children: list[XmlObject] = []
        self.attributes: dict[str, str] = {}
        self.text = ''
    
    def to_dict(self) -> dict:
        result = {}

        if self.text:
            if len(self.attributes) == 0 and len(self.children) == 0:
                return self.text.strip()
            result['__text'] = self.text.strip()
            
        for child in self.children:
            if child.tag not in result:
                result[child.tag] = child.to_dict()
            elif isinstance(result[child.tag], list):
                result[child.tag].append(child.to_dict())
            else:
                result[child.tag] = [result[child.tag], child.to_dict()]
        for key, value in self.attributes.items():
            result[f'_{key}'] = value
        return result


class XmlParser:
    def __init__(self, xml: str):
        self.xml = xml.strip()
        self.current_idx = 0
        self.stack = []
        self.root = XmlObject('root')
        self.stack.append(self.root)
        self._parse()
    
    def _skip_xml_declaration(self):
        if self.xml[1] == '?':
            self.current_idx = self.xml.find('>') + 1
    
    def _parse(self):
        self._skip_xml_declaration()
        while self.current_idx < len(self.xml):
            self._parse_step()

    def _parse_step(self):
        self._lstrip()
        self._skip_comments()
        if self.xml[self.current_idx] == '<':
            self._parse_element()
        else:
            self._parse_text()

    def _lstrip(self):
        while self.xml[self.current_idx] == ' ':
            self.current_idx += 1
    
    def _skip_comments(self):
        while self._skip_comment():
            self._lstrip()

    def _skip_comment(self) -> bool:
        if self.xml[self.current_idx:self.current_idx + 4] == '<!--':
            self.current_idx = self.xml.find('-->', self.current_idx) + 3
            return True

    def _parse_element(self):
        tag_body_close = self.xml.find('>', self.current_idx)
        if tag_body_close == -1:
            raise ValueError('Invalid XML')
        tag_body = self.xml[self.current_idx + 1:tag_body_close]
        if tag_body[0] == '/':
            self._parse_close_tag(tag_body)
            return
        if tag_body[-1] == '/':
            self._parse_self_closing_tag(tag_body)
            return
        self._parse_open_tag(tag_body)

    def _parse_close_tag(self, tag_body):
        tag = tag_body[1:]
        if tag != self.stack[-1].tag:
            raise ValueError('Invalid XML')
        self.stack.pop()
        self.current_idx = self.xml.find('>', self.current_idx) + 1

    def _parse_self_closing_tag(self, tag_body):
        tag, attributes = self._get_tag_and_attributes(tag_body[:-1])
        child = XmlObject(tag)
        child.attributes = attributes
        self.stack[-1].children.append(child)
        self.current_idx = self.xml.find('>', self.current_idx) + 1

    def _parse_open_tag(self, tag_body):
        tag, attributes = self._get_tag_and_attributes(tag_body)
        child = XmlObject(tag)
        child.attributes = attributes
        self.stack[-1].children.append(child)
        self.stack.append(child)
        self.current_idx = self.xml.find('>', self.current_idx) + 1

    def _get_tag_and_attributes(self, tag_body):
        tag, *attributes_raw = tag_body.split(' ')
        attributes = self._parse_attributes(' '.join(attributes_raw))
        return tag, attributes

    def _parse_attributes(self, attributes_raw):
        attributes = {}
        while attributes_raw:
            key, attributes_raw = attributes_raw.split('=', 1)
            if attributes_raw[0] == '"':
                value = attributes_raw[1:attributes_raw.find('"', 1)]
                attributes_raw = attributes_raw[attributes_raw.find('"', 1) + 1:].strip()
            else:
                value = attributes_raw[:attributes_raw.find(' ', 1)]
                attributes_raw = attributes_raw[attributes_raw.find(' ', 1) + 1:].strip()
            attributes[key] = value
        return attributes

    def _parse_text(self):
        text_close = self.xml.find('<', self.current_idx)
        if text_close == -1:
            raise ValueError('Invalid XML')
        text = self.xml[self.current_idx:text_close]
        if text.strip():
            self.stack[-1].text = self.stack[-1].text + text
        self.current_idx = text_close

    def get_root(self):
        return self.root.to_dict()


if __name__ == '__main__':
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <data>
        <country name="Liechtenstein">
            <rank updated="yes">2</rank>
            <year>2008</year>
            <gdppc>141100</gdppc>
            <neighbor name="Austria" direction="E"/>
            <neighbor name="Switzerland" direction="W"/>
        </country>
        <country name="Singapore">
            <rank updated="yes">5</rank>
            <year>2011</year>
            <gdppc>59900</gdppc>
            <neighbor name="Malaysia" direction="N"/>
        </country>
        <country name="Panama">
            <rank updated="yes">69</rank>
            <year>2011</year>
            <gdppc>13600</gdppc>
            <neighbor name="Costa Rica" direction="W"/>
            <neighbor name="Colombia" direction="E"/>
        </country>
    </data>
    """
    
    pprint.pprint(XmlParser(xml).get_root())

    # pprint.pprint(xml2dict(xml))
    # print(xml2dict(xml)['data']['country'][0]['_name'])
    # print(xml2dict(xml)['data']['country'][0]['neighbor'][1]['_name'])
