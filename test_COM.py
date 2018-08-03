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


    def isOutput(path):
        """
        path = used for defining the file folder to be checked
        """
        if os.path.isfile(path):
            return True
        else:
            return False

    def checkFile(path, files):
        """
        path = used for defining the folder to be checked for files with extension
        files = used for defining the files to be checked
        """
        bool_message = []
        for fname in os.listdir(path):
            bool_message.append(False)
        i = 0
        for file in files:
            if file in os.listdir(path):
                bool_message[i] = True
                i = i + 1
            else:
                return False
        for elem in bool_message:
            if elem == False:
                return False
        return True

    def checkPduR(path, inPath):
        """
        path = used for defining the file to be checked
        inPath = used for defining the file from where to obtain source/target frame names
        """
        found_routingtable = found_routingpath = found_srcPdu = found_DestPdu = False
        mapping_list = []
        tree = etree.parse(inPath)
        root = tree.getroot()
        source = root.findall(".//GATEWAY-MAPPING")
        for elem in source:
            temp = []
            for c in elem:
                if c.tag == "SOURCE-FRAME-REF":
                    temp.append(c.text.split("ft_", 1)[1])
                    #source_name.append(c.text.split("ft_", 1)[1])
                if c.tag == "TARGET-FRAME-REF":
                    temp.append(c.text.split("ft_", 1)[1])
                    #target_name.append(c.text.split("ft_", 1)[1])
            mapping_list.append(temp)
        tree1 = etree.parse(path)
        root1 = tree1.getroot()
        sub_containers = root1.findall(".//{http://autosar.org/schema/r4.0}SUB-CONTAINERS")
        for container in sub_containers:
            for mapping in mapping_list:
                for elem in container:
                    for elem2 in elem.iter(tag="{http://autosar.org/schema/r4.0}SHORT-NAME"):
                        if elem2.text == "PduRRoutingTable_" + mapping[0]:
                            found_routingtable = True
                        if elem2.text == "PduRRoutingPath_" + mapping[0]:
                            found_routingpath = True
                        if elem2.text == "PduRSrcPdu_" + mapping[0]:
                            found_srcPdu = True
                        if elem2.text == "PduRDestPdu_" + mapping[0] + "_" + mapping[1] + "_TO_CDD":
                            found_DestPdu = True
                    if not found_routingtable and not found_DestPdu and not found_routingpath and not found_srcPdu:
                        return False
        if found_routingtable and found_routingpath and found_srcPdu and found_DestPdu:
            return True
        else:
            return False

    # def ecuc(path1, path2):
    #     """
    #         path1 = used for defining the file to be checked for values(from input)
    #         path2 = used for defining the file to be checked (from output)
    #     """
    #     a = 7
    #     tree = etree.parse(path1)
    #     root = tree.getroot()
    #     source = root.findall(".//{http://autosar.org/2.1.2}CONTAINERS")
    #     for container in source:
    #     #     if container.getchildren[0].text == "DiagTool":
    #     #     if container.getchildren[0].text == "BTA":
    #         for elem in container:
    #             for elem2 in elem:





class COMConfigurator(unittest.TestCase):
    # def test_TRS_COMCONF_INOUT_001_1(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('coverage run COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.INOUT.001_1\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.INOUT.001_1\\out -NeMo')
    #     self.assertTrue(FileCheck.checkFile(head + '\\Tests\\TRS.COMCONF.INOUT.001_1\\out\\', ['ComCallout.xml','result_COM.log']))

    # def test_TRS_COMCONF_INOUT_001_2(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('coverage run COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.INOUT.001_2\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.INOUT.001_2\\out -EnGw')
    #     self.assertTrue(FileCheck.checkFile(head + '\\Tests\\TRS.COMCONF.INOUT.001_2\\out\\', ['EcuC.epc', 'PduR.epc', 'EnGwCCB.epc', 'EnGwCCD.epc', 'EnGwCCLD.epc', 'EnGwCLD.epc', 'EnGwFonc.epc', 'result_COM.log']))

    # def test_TRS_COMCONF_INOUT_001_3(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('coverage run COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.INOUT.001_3\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.INOUT.001_3\\out -EnGw -NeMo')
    #     self.assertTrue(FileCheck.checkFile(head + '\\Tests\\TRS.COMCONF.INOUT.001_3\\out\\', ['ComCallout.xml','EcuC.epc', 'PduR.epc', 'EnGwCCB.epc', 'EnGwCCD.epc', 'EnGwCCLD.epc', 'EnGwCLD.epc', 'EnGwFonc.epc', 'result_COM.log']))

    # def test_TRS_COMCONF_INOUT_001_4(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('coverage run COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.INOUT.001_4\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.INOUT.001_4\\out')
    #     self.assertFalse(FileCheck.checkFile(head + '\\Tests\\TRS.COMCONF.INOUT.001_4\\out\\', ['ComCallout.xml','EcuC.epc', 'PduR.epc', 'EnGwCCB.epc', 'EnGwCCD.epc', 'EnGwCCLD.epc', 'EnGwCLD.epc', 'EnGwFonc.epc']))

    # def test_TRS_COMCONF_GEN_001_1(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('coverage run COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.001_1\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.001_1\\out -NeMo')
    #     self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_1\\out\\ComCallout.xml', 'CounterIn_ETH', 'ComTimeoutNotification'))
    #     self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_1\\out\\ComCallout.xml', 'CounterIn_ETH', 'ComNotification'))


    # def test_TRS_COMCONF_GEN_001_2(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('coverage run COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.001_2\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.001_2\\out -NeMo')
    #     self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_2\\out\\ComCallout.xml', 'Pdu_CounterIn_ETH', 'ComIPduCallout'))


    # def test_TRS_COMCONF_GEN_001_3(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('coverage run COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.001_3\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.001_3\\out -NeMo')
    #     self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_3\\out\\ComCallout.xml', 'CounterIn_ETH', 'ComTimeoutNotification'))
    #     self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_3\\out\\ComCallout.xml', 'CounterIn_ETH', 'ComNotification'))
    #     self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_3\\out\\ComCallout.xml', 'Pdu_CounterIn_ETH', 'ComIPduCallout'))

    #
    # def test_TRS_COMCONF_GEN_001_4(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('coverage run COM_Configurator.py -in ' + head + '\\Tests\\TRS.COMCONF.GEN.001_4 -out_script ' + head + '\\Tests\\TRS.COMCONF.GEN.001_4\\out -NeMo')
    #     self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_4\\out\\ComCallout.xml', 'CounterIn_ETH', 'ComTimeoutNotification'))
    #     self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_4\\out\\ComCallout.xml', 'CounterIn_ETH', 'ComNotification'))
    #     self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.001_4\\out\\ComCallout.xml', 'Pdu_CounterIn_ETH', 'ComIPduCallout'))

    # def test_TRS_COMCONF_GEN_003_1(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('coverage run COM_Configurator.py -in ' + head + '\\Tests\\TRS.COMCONF.GEN.003_1\\in -out ' + head + '\\Tests\\TRS.COMCONF.GEN.003_1\\out -EnGw')
    #     self.assertTrue(FileCheck.checkPduR(head + '\\Tests\\TRS.COMCONF.GEN.003_1\\out\PduR.epc', head + '\\Tests\\TRS.COMCONF.GEN.003_1\\in\MAPPING.xml'))

    # def test_TRS_COMCONF_GEN_003_2(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('coverage run COM_Configurator.py -in ' + head + '\\Tests\\TRS.COMCONF.GEN.003_2\\in -out ' + head + '\\Tests\\TRS.COMCONF.GEN.003_2\\out -EnGw')
    #     self.assertTrue(FileCheck.checkPduR(head + '\\Tests\\TRS.COMCONF.GEN.003_2\\out\PduR.epc', head + '\\Tests\\TRS.COMCONF.GEN.003_2\\in\MAPPING.xml'))

    # def test_TRS_COMCONF_GEN_003_3(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('coverage run COM_Configurator.py -in ' + head + '\\Tests\\TRS.COMCONF.GEN.003_3\\in -out ' + head + '\\Tests\\TRS.COMCONF.GEN.003_3\\out -EnGw')
    #     self.assertTrue(FileCheck.checkPduR(head + '\\Tests\\TRS.COMCONF.GEN.003_3\\out\PduR.epc', head + '\\Tests\\TRS.COMCONF.GEN.003_3\\in\MAPPING.xml'))

    # def test_TRS_COMCONF_GEN_003_4(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('coverage run COM_Configurator.py -in ' + head + '\\Tests\\TRS.COMCONF.GEN.003_4\\in -out ' + head + '\\Tests\\TRS.COMCONF.GEN.003_4\\out -EnGw')
    #     self.assertTrue(FileCheck.checkPduR(head + '\\Tests\\TRS.COMCONF.GEN.003_4\\out\PduR.epc', head + '\\Tests\\TRS.COMCONF.GEN.003_4\\in\MAPPING.xml'))

    # def test_TRS_COMCONF_GEN_003_5(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('coverage run COM_Configurator.py -in ' + head + '\\Tests\\TRS.COMCONF.GEN.003_5\\in -out ' + head + '\\Tests\\TRS.COMCONF.GEN.003_5\\out -EnGw')
    #     self.assertTrue(FileCheck.checkPduR(head + '\\Tests\\TRS.COMCONF.GEN.003_5\\out\PduR.epc', head + '\\Tests\\TRS.COMCONF.GEN.003_5\\in\MAPPING.xml'))

    # def test_TRS_COMCONF_GEN_003_6(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('coverage run COM_Configurator.py -in ' + head + '\\Tests\\TRS.COMCONF.GEN.003_6\\in -out ' + head + '\\Tests\\TRS.COMCONF.GEN.003_6\\out -EnGw')
    #     self.assertFalse(FileCheck.checkPduR(head + '\\Tests\\TRS.COMCONF.GEN.003_6\\out\PduR.epc', head + '\\Tests\\TRS.COMCONF.GEN.003_6\\in\MAPPING.xml'))

    def test_TRS_COMCONF_GEN_005(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('coverage run COM_Configurator.py -in ' + head + '\\Tests\\TRS.COMCONF.GEN.005\\in -out ' + head + '\\Tests\\TRS.COMCONF.GEN.005\\out -EnGw')
        self.assertFalse(FileCheck.ecuc(head + '\\Tests\\TRS.COMCONF.GEN.005\\in\EPC_GwDiagCanLinConfig.epc', head + '\\Tests\\TRS.COMCONF.GEN.005\\out\EcuC.epc'))

suite = unittest.TestLoader().loadTestsFromTestCase(COMConfigurator)
unittest.TextTestRunner(verbosity=2).run(suite)

# current_path = os.path.realpath(__file__)
# head, tail = ntpath.split(current_path)
# if __name__ == "__main__":
#     unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=head + "\\tests"))