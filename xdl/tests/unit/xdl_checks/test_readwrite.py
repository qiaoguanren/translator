from xdl import XDL
import os
import shutil
import pytest

HERE = os.path.abspath(os.path.dirname(__file__))
INTEGRATION_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(HERE)), 'integration', 'files')

@pytest.mark.unit
def test_readwrite():
    for f in os.listdir(INTEGRATION_FOLDER):
        if f.endswith('.xdl'):
            f_path = os.path.join(INTEGRATION_FOLDER, f)
            if not f.startswith('AlkylFluor'):
                # AlkylFluor weird as writes internal props
                x = XDL(f_path)
                os.makedirs('test_output', exist_ok=True)
                save_xml_path = os.path.join('test_output', f)
                save_json_path = os.path.join('test_output', f[:-3] + 'json')
                x.save(save_xml_path)
                x.save(save_json_path, file_format='json')
                x_xml = XDL(save_xml_path)
                x_json = XDL(save_json_path)
                shutil.rmtree('test_output')
                assert x_xml == x_json == x
