import xmltodict
import yaml
import sys
import example
import pprint


def xml_to_yaml(xml):
    d = xmltodict.parse(xml)
    return yaml.dump(d, allow_unicode=True, indent=2)


def main(runs=1):
    for _ in range(runs):
        yaml = xml_to_yaml(example.xml)
    print(yaml)


if __name__ == '__main__':
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    main(runs)
