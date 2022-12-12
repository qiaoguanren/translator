from chemputerxdl.platform import ChemputerPlatform
from lxml import etree
import os
import pytest

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')
INTEGRATION_FOLDER = os.path.join(HERE, '..', '..', 'integration', 'files')

@pytest.mark.unit
def test_schema():
    platform = ChemputerPlatform()
    schema = platform.schema
    xsd_path = 'xdl_chemputer_schema.xsd'
    with open(xsd_path, 'w') as fd:
        fd.write(schema)

    xmlschema_doc = etree.parse(xsd_path)
    os.remove(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    parser = etree.XMLParser(schema=xmlschema)

    for f in os.listdir(FOLDER):
        print(f)
        if f.endswith('.xdl'):
            with open(os.path.join(FOLDER, f)) as fd:
                etree.fromstring(fd.read(), parser)
            # assert xmlschema.validate(etree.parse(os.path.join(FOLDER, f)))

    for f in os.listdir(INTEGRATION_FOLDER):
        if f.endswith('.xdl'):
            with open(os.path.join(INTEGRATION_FOLDER, f)) as fd:
                etree.fromstring(fd.read(), parser)
            # assert xmlschema.validate(
            #     etree.parse(os.path.join(INTEGRATION_FOLDER, f)))
