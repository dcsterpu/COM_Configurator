import unittest
import os
import os.path
import ntpath
from lxml import etree
import HtmlTestRunner


class FileCheck():
    def CheckParameter(path, callout, param):
        """
        function that checks in a Scriptor script if a specific CALLOUT has a given parameter set
        """
        tree = etree.parse(path)
        root = tree.getroot()
        callouts = root.findall(".//Expression")
        for elem in callouts:
            if callout in elem.text and param in elem.text:
                for item in elem.getparent().iterdescendants():
                    if item.tag == "Expression":
                        if callout in item.text:
                            return True
        return False


class COMConfigurator(unittest.TestCase):
    def test_TRS_COMCONF_GEN_001_1(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('coverage run COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.001_1\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.001_1\\out -NeMo')
        self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_1\\out\\ComCallout.xml', 'CounterIn_ETH', 'ComTimeoutNotification'))
        self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_1\\out\\ComCallout.xml', 'CounterIn_ETH', 'ComNotification'))


    def test_TRS_COMCONF_GEN_001_2(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('coverage run COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.001_2\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.001_2\\out -NeMo')
        self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_2\\out\\ComCallout.xml', 'Pdu_CounterIn_ETH', 'ComIPduCallout'))


    def test_TRS_COMCONF_GEN_001_3(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('coverage run COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.001_3\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.001_3\\out -NeMo')
        self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_3\\out\\ComCallout.xml', 'CounterIn_ETH', 'ComTimeoutNotification'))
        self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_3\\out\\ComCallout.xml', 'CounterIn_ETH', 'ComNotification'))
        self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_3\\out\\ComCallout.xml', 'Pdu_CounterIn_ETH', 'ComIPduCallout'))


    def test_TRS_COMCONF_GEN_001_4(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('coverage run COM_Configurator.py -in ' + head + '\\Tests\\TRS.COMCONF.GEN.001_4 -out_script ' + head + '\\Tests\\TRS.COMCONF.GEN.001_4\\out -NeMo')
        self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_4\\out\\ComCallout.xml', 'CounterIn_ETH', 'ComTimeoutNotification'))
        self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_4\\out\\ComCallout.xml', 'CounterIn_ETH', 'ComNotification'))
        self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_4\\out\\ComCallout.xml', 'Pdu_CounterIn_ETH', 'ComIPduCallout'))


suite = unittest.TestLoader().loadTestsFromTestCase(COMConfigurator)
unittest.TextTestRunner(verbosity=2).run(suite)

# current_path = os.path.realpath(__file__)
# head, tail = ntpath.split(current_path)
# if __name__ == "__main__":
#     unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=head + "\\tests"))