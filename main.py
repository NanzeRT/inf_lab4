from xml_parser import XmlParser
from yaml_constructor import YamlConstructor
import sys
import example


def main(runs=1) -> None:
    for _ in range(runs):
        data = XmlParser(example.xml).get_root()
        yaml = YamlConstructor(data).construct()
    print(yaml)


if __name__ == '__main__':
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    main(runs)
