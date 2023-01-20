import timeit
from xml_parser import XmlParser
from xml_parser_with_regex import XmlParser as XmlParserWithRegex
from yaml_constructor import YamlConstructor
from main_with_libs import xml_to_yaml as xml_to_yaml_with_libs
import example


def run_xml_parser():
    YamlConstructor(XmlParser(example.xml).get_root()).construct()


def run_xml_parser_with_regex():
    YamlConstructor(XmlParserWithRegex(example.xml).get_root()).construct()


def run_xml_to_yaml_with_libs():
    xml_to_yaml_with_libs(example.xml)


def main():
    runs = 1000
    print(f'Runs: {runs}')
    print(f'xml_parser: {timeit.timeit(run_xml_parser, number=runs)} seconds')
    print(f'xml_parser_with_regex: {timeit.timeit(run_xml_parser_with_regex, number=runs)} seconds')
    print(f'xml_to_yaml_with_libs: {timeit.timeit(run_xml_to_yaml_with_libs, number=runs)} seconds')


if __name__ == '__main__':
    main()
