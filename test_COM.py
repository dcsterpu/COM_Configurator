import unittest
import os
import os.path
import ntpath
from lxml import etree
#import HtmlTestRunner


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

    def isPresent(path, callout):
        tree = etree.parse(path)
        root = tree.getroot()
        callouts = root.findall(".//{http://autosar.org/schema/r4.0}VALUE-REF")
        for elem in callouts:
            if elem.text.split("/")[-1] == callout:
                return True
        return False

    def CheckNameRoutingPath(path, param):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(
            ".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            name = elem.getchildren()[0].text
            if name == param:
                return True
        return False

    def CheckRoutingPath(path, param1, param2, param3, param4, param5):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            short_name_src = elem.getchildren()[2].getchildren()[0].getchildren()[0].text
            if short_name_src == param1:
                value_src = elem.getchildren()[2].getchildren()[0].getchildren()[2].getchildren()[0].getchildren()[1].text
                if value_src.isdigit():
                    value_ref_src = elem.getchildren()[2].getchildren()[0].getchildren()[3].getchildren()[0].getchildren()[1].text
                    if value_ref_src == param2:
                        short_name_dest = elem.getchildren()[2].getchildren()[1].getchildren()[0].text
                        if short_name_dest == param3:
                            value_dest = elem.getchildren()[2].getchildren()[1].getchildren()[2].getchildren()[0].getchildren()[1].text
                            if value_dest == param4:
                                value_ref_dest = elem.getchildren()[2].getchildren()[1].getchildren()[3].getchildren()[0].getchildren()[1].text
                                if value_ref_dest == param5:
                                    return True
        return False

    def CheckId(path):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}PARAMETER-VALUES/{http://autosar.org/schema/r4.0}ECUC-NUMERICAL-PARAM-VALUE/{http://autosar.org/schema/r4.0}VALUE")
        index = 0
        for elem in elements:
            value = elem.text
            if int(value) == index:
                index = index + 1
        if len(elements) == index:
            return True
        else:
            return False

    def CheckEcuC(path, param):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            short_name = elem.getchildren()[0].text
            if short_name == param:
                value = elem.getchildren()[2].getchildren()[0].getchildren()[1].text
                if int(value) == 8:
                    return True
        return False

    def CheckLinTp1(path, param):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            short_name = elem.getchildren()[0].text
            if short_name == param:
                return True
        return False

    def CheckLinTp2(path, param1, param2, param3):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            elem1 = elem.getchildren()[2].getchildren()[0].getchildren()[1].text
            if param1 == elem1:
                elem2 = elem.getchildren()[2].getchildren()[1].getchildren()[1].text
                if param2 == elem2:
                    elem3 = elem.getchildren()[2].getchildren()[2].getchildren()[1].text
                    if param3 == elem3:
                        return True
        return False

    def CheckLinTp3(path, param1, param2, param3):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            elem1 = elem.getchildren()[3].getchildren()[0].getchildren()[1].text
            if param1 == elem1:
                elem2 = elem.getchildren()[3].getchildren()[1].getchildren()[1].text
                if param2 == elem2:
                    elem3 = elem.getchildren()[3].getchildren()[2].getchildren()[1].text
                    if param3 == elem3:
                        return True
        return False

    def CheckLinTp4(path, param1, param2):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            elem1 = elem.getchildren()[2].getchildren()[0].getchildren()[1].text
            if param1 == elem1:
                elem2 = elem.getchildren()[2].getchildren()[1].getchildren()[1].text
                if param2 == elem2:
                    return True
        return False

    def CheckLinIf1(path, param):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            short_name = elem.getchildren()[0].text
            if short_name == param:
                return True
        return False

    def CheckLinIf2(path, param):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            short_name = elem.getchildren()[0].text
            if short_name == param:
                return True
        return False

    def CheckLinIf3(path, param1, param2, param3, param4):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            elem1 = elem.getchildren()[2].getchildren()[0].getchildren()[1].text
            if elem1 == param1:
                elem2 = elem.getchildren()[2].getchildren()[1].getchildren()[1].text
                if elem2 == param2:
                    elem3 = elem.getchildren()[2].getchildren()[2].getchildren()[1].text
                    if elem3 == param3:
                        elem4 = elem.getchildren()[2].getchildren()[3].getchildren()[1].text
                        if elem4 == param4:
                            return True
        return False

    def CheckLinIf4(path, param):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            short_name = elem.getchildren()[3].getchildren()[0].getchildren()[0].text
            if short_name == param:
                return True
        return False

    def CheckLinIf5(path, param1, param2):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            elem1 = elem.getchildren()[3].getchildren()[0].getchildren()[2].getchildren()[0].getchildren()[0].text
            if elem1 == param1:
                elem2 = elem.getchildren()[3].getchildren()[0].getchildren()[2].getchildren()[0].getchildren()[2].getchildren()[0].getchildren()[1].text
                if elem2 == param2:
                    return True
        return False

    def CheckLinIf6(path, param1, param2, param3):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            elem1 = elem.getchildren()[3].getchildren()[0].getchildren()[2].getchildren()[0].getchildren()[1].text
            if elem1 == param1:
                elem2 = elem.getchildren()[3].getchildren()[0].getchildren()[2].getchildren()[1].getchildren()[1].text
                if elem2 == param2:
                    elem3 = elem.getchildren()[3].getchildren()[0].getchildren()[3].getchildren()[0].getchildren()[1].text
                    if elem3 == param3:
                        return True
        return False

    def CheckLinIf7(path, param):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            short_name = elem.getchildren()[0].text
            if short_name == param:
                return True
        return False

    def CheckLinIf8(path, param1, param2, param3):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            elem1 = elem.getchildren()[2].getchildren()[0].getchildren()[1].text
            if elem1 == param1:
                elem2 = elem.getchildren()[2].getchildren()[1].getchildren()[1].text
                if elem2 == param2:
                    elem3 = elem.getchildren()[3].getchildren()[0].getchildren()[1].text
                    if elem3 == param3:
                        return True
        return False

    def CheckCanTp1(path, param1, param2, param3, param4, param5):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            elem1 = elem.getchildren()[0].text
            if elem1 == param1:
                elem2 = elem.getchildren()[2].getchildren()[0].getchildren()[1].text
                if elem2 == param2:
                    elem3 = elem.getchildren()[2].getchildren()[1].getchildren()[1].text
                    if elem3 == param3:
                        elem4 = elem.getchildren()[2].getchildren()[2].getchildren()[1].text
                        if elem4 == param4:
                            elem5 = elem.getchildren()[2].getchildren()[3].getchildren()[1].text
                            if elem5 == param5:
                                return True
        return False

    def CheckCanTp2(path, param):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            short_name = elem.getchildren()[0].text
            if param == short_name:
                return True
        return False

    def CheckCanTp3(path, param):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            elem1 = elem.getchildren()[2].getchildren()[0].getchildren()[1].text
            if param == elem1:
                return True
        return False

    def CheckCanTp4(path, param):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            short_name = elem.getchildren()[0].text
            if short_name == param:
                return True
        return False

    def CheckCanTp51(path, param2, param3, param4, param5, param6, param7, param8, param9, param10, param11):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            elem1 = elem.getchildren()[2].getchildren()[0].getchildren()[1].text
            if elem1.isdigit():
                elem2 = elem.getchildren()[2].getchildren()[1].getchildren()[1].text
                if elem2 == param2:
                    elem3 = elem.getchildren()[2].getchildren()[2].getchildren()[1].text
                    if elem3 == param3:
                        elem4 = elem.getchildren()[2].getchildren()[3].getchildren()[1].text
                        if elem4 == param4:
                            elem5 = elem.getchildren()[2].getchildren()[4].getchildren()[1].text
                            if elem5 == param5:
                                elem6 = elem.getchildren()[2].getchildren()[5].getchildren()[1].text
                                if elem6 == param6:
                                    elem7 = elem.getchildren()[2].getchildren()[6].getchildren()[1].text
                                    if elem7 == param7:
                                        elem8 = elem.getchildren()[2].getchildren()[7].getchildren()[1].text
                                        if elem8 == param8:
                                            elem9 = elem.getchildren()[2].getchildren()[8].getchildren()[1].text
                                            if elem9 == param9:
                                                elem10 = elem.getchildren()[2].getchildren()[9].getchildren()[1].text
                                                if elem10 == param10:
                                                    elem11 = elem.getchildren()[2].getchildren()[10].getchildren()[1].text
                                                    if elem11 == param11:
                                                        return True
        return False

    def CheckCanTp52(path, param2, param3, param4, param5, param6, param7, param8, param9):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            elem1 = elem.getchildren()[2].getchildren()[0].getchildren()[1].text
            if elem1.isdigit():
                elem2 = elem.getchildren()[2].getchildren()[1].getchildren()[1].text
                if elem2 == param2:
                    elem3 = elem.getchildren()[2].getchildren()[2].getchildren()[1].text
                    if elem3 == param3:
                        elem4 = elem.getchildren()[2].getchildren()[3].getchildren()[1].text
                        if elem4 == param4:
                            elem5 = elem.getchildren()[2].getchildren()[4].getchildren()[1].text
                            if elem5 == param5:
                                elem6 = elem.getchildren()[2].getchildren()[5].getchildren()[1].text
                                if elem6 == param6:
                                    elem7 = elem.getchildren()[2].getchildren()[6].getchildren()[1].text
                                    if elem7 == param7:
                                        elem8 = elem.getchildren()[2].getchildren()[7].getchildren()[1].text
                                        if elem8 == param8:
                                            elem9 = elem.getchildren()[2].getchildren()[8].getchildren()[1].text
                                            if elem9 == param9:
                                                return True
        return False

    def CheckCanTp6(path, param):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            elem1 = elem.getchildren()[3].getchildren()[0].getchildren()[1].text
            if elem1 == param:
                return True
        return False

    def CheckCanTp7(path, param1, param2):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        for elem in elements:
            elem1 = elem.getchildren()[0].text
            if elem1 == param1:
                elem2 = elem.getchildren()[2].getchildren()[0].getchildren()[1].text
                if elem2 == param2:
                    return True
        return False

    def CheckCanTp8(path):
        tree = etree.parse(path)
        root = tree.getroot()
        elements = root.findall(".//{http://autosar.org/schema/r4.0}ELEMENTS/{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES/{http://autosar.org/schema/r4.0}CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE/{http://autosar.org/schema/r4.0}SUB-CONTAINERS/{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE")
        cnt = 0
        for x in range(0, len(elements),2):
            short_name_rx = elements[x].getchildren()[0].text.split("_")[0]
            short_name_tx = elements[x+1].getchildren()[0].text.split("_")[0]
            value0 = elements[x].getchildren()[2].getchildren()[0].getchildren()[1].text
            value1 = elements[x+1].getchildren()[2].getchildren()[0].getchildren()[1].text
            if short_name_rx == "CanTpRxNSdu" and short_name_tx == "CanTpTxNSdu" and value0 == value1 and int(value0) == cnt:
                cnt = cnt + 1
        if cnt == len(elements)/2:
            return True
        else:
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

    ###################################################################################################################
    def test_TRS_COMCONF_GEN_004_TEST01(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.004\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.004\\TEST01\\out -NeMo')
        self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.004\\TEST01\\out\\ComCallout.xml','Pdu_CounterIn_ETH','ComIPduCallout'))

    #def test_TRS_COMCONF_GEN_004_TEST02(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.004\\TEST02\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.004\\TEST02\\out -NeMo')
    #    self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.004\\TEST02\\out\\ComCallout.xml','Pdu_CounterIn_ETH', 'ComIPduCallout'))

    #def test_TRS_COMCONF_GEN_005_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.005\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.005\\TEST01\\out -NeMo')
    #    self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.005\\TEST01\\out\\ComCallout.xml', 'HS4_CDE_CMB_SIGNALISATION_DMD_COULEUR_CMB_HS4_128', 'ComTimeoutNotification'))
    #    self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.005\\TEST01\\out\\ComCallout.xml', 'HS4_CDE_CMB_SIGNALISATION_DMD_COULEUR_CMB_HS4_128', 'ComNotification'))

    #def test_TRS_COMCONF_GEN_005_TEST02(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.005\\TEST02\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.005\\TEST02\\out -NeMo')
    #    self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.005\\TEST02\\out\\ComCallout.xml', 'HS4_CDE_CMB_SIGNALISATION_DMD_COULEUR_CMB_HS4_128', 'ComTimeoutNotification'))
    #    self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.005\\TEST02\\out\\ComCallout.xml', 'HS4_CDE_CMB_SIGNALISATION_DMD_COULEUR_CMB_HS4_128', 'ComNotification'))

    #def test_TRS_COMCONF_GEN_005_TEST03(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.005\\TEST03\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.005\\TEST03\\out -NeMo')
    #    self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.005\\TEST03\\out\\ComCallout.xml', 'HS4_CDE_CMB_SIGNALISATION_DMD_COULEUR_CMB_HS4_128', 'ComTimeoutNotification'))
    #    self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.005\\TEST03\\out\\ComCallout.xml', 'HS4_CDE_CMB_SIGNALISATION_DMD_COULEUR_CMB_HS4_128', 'ComNotification'))

    #def test_TRS_COMCONF_GEN_010_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.010\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.010\\TEST01\\out -EnGw')
    #    self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.010\\TEST01\\out\\EnGw_PduR_Update.xml','isip_HS4_VSM_INF_CFG_T','PduRDestPdu'))

    #def test_TRS_COMCONF_GEN_010_TEST02(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.010\\TEST02\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.010\\TEST02\\out -EnGw')
    #    self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.010\\TEST02\\out\\EnGw_PduR_Update.xml','isip_HS4_VSM_INF_CFG_865','PduRDestPdu'))

    #def test_TRS_COMCONF_GEN_010_TEST03(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.010\\TEST03\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.010\\TEST03\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.010\\TEST03\\out\\EnGw_PduR_Update.xml','isip_HS4_VSM_INF_CFG_865T','PduRDestPdu'))

    #def test_TRS_COMCONF_GEN_011_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.011\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.011\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.011\\TEST01\\out\\EnGw_PduR_Update.xml','isip_HS4_VSM_INF_CFG_865T', 'PduRDestPdu'))

    #def test_TRS_COMCONF_GEN_011_TEST02(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.011\\TEST02\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.011\\TEST02\\out -EnGw')
    #    self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.011\\TEST02\\out\\EnGw_PduR_Update.xml','isip_HS4_VSM_INF_CFG_865T', 'PduRDestPdu'))

    #def test_TRS_COMCONF_GEN_012_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.012\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.012\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.012\\TEST01\\out\\EnGw_PduR_Update.xml','isip_HS4_VSM_INF_CFG_865T','PduRDestPdu'))
    #    self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.012\\TEST01\\out\\EnGw_PduR_Update.xml','ARVSW_TBXDETReport_Frame','PduRDestPdu'))
    #    self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.012\\TEST01\\out\\EnGw_PduR_Update.xml','isip_HS4_VSM_CDE_PTR_MESSAGE_417T', 'PduRDestPdu'))
    #    self.assertTrue(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.012\\TEST01\\out\\EnGw_PduR_Update.xml','isip_HS1_REQ_EOBD_ON_CAN_7E7_2023T','PduRDestPdu'))

    #def test_TRS_COMCONF_GEN_012_TEST02(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.012\\TEST02\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.012\\TEST02\\out -EnGw')
    #    self.assertFalse(FileCheck.CheckParameter(head + '\\Tests\\TRS.COMCONF.GEN.012\\TEST02\\out\\EnGw_PduR_Update.xml','HS1_REQ_EOBD_ON_CAN_7E9','PduRDestPdu'))

    #def test_TRS_COMCONF_GEN_015_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST01\\out -EnGw')
    #    self.assertFalse(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST01\\out\\PduR.epc','PduRRoutingPath_isip_HS4_VSM_INF_CFG'))

    #def test_TRS_COMCONF_GEN_015_TEST02(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST02\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST02\\out -EnGw')
    #    self.assertFalse(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST02\\out\\PduR.epc','PduRRoutingPath_isip_HS4_VSM_INF_CFG'))

    #def test_TRS_COMCONF_GEN_015_TEST03(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST03\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST03\\out -EnGw')
    #    self.assertFalse(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST03\\out\\PduR.epc','PduRRoutingPath_isip_HS4_VSM_INF_CFG_isip_HS4_VSM_INF_PRG_RTAB_FROM_CDD'))

    #def test_TRS_COMCONF_GEN_015_TEST04(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST04\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST04\\out -EnGw')
    #    self.assertFalse(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST04\\out\\PduR.epc','PduRRoutingPath_isip_HS4_VSM_INF_CFG_isip_HS4_VSM_INF_PRG_RTAB_FROM_CDD'))

    #def test_TRS_COMCONF_GEN_015_TEST05(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST05\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST05\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST05\\out\\PduR.epc','PduRRoutingPath_isip_HS4_VSM_INF_CFG_isip_HS4_VSM_INF_PRG_RTAB_FROM_CDD'))
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.015\\TEST05\out\\PduR.epc','PduRRoutingPath_isip_HS4_VSM_INF_CFG'))

    #def test_TRS_COMCONF_GEN_016_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.016\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.016\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.016\\TEST01\\out\\PduR.epc','PduRRoutingPath_isip_HS4_VSM_INF_CFG'))
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.016\\TEST01\\out\\PduR.epc','PduRRoutingPath_isip_HS4_VSM_INF_CFG_isip_HS4_VSM_INF_PRG_RTAB_FROM_CDD'))
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.016\\TEST01\\out\\PduR.epc','PduRRoutingPath_isip_HS2_VIN_VDS_BSI_492'))
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.016\\TEST01\\out\\PduR.epc','PduRRoutingPath_isip_HS2_VIN_VDS_BSI_492_isip_HS2_VERS_BSI_112_FROM_CDD'))
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.016\\TEST01\\out\\PduR.epc','PduRRoutingPath_isip_HS4_VSM_CDE_PTR_MESSAGE'))
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.016\\TEST01\\out\\PduR.epc','PduRRoutingPath_isip_HS4_VSM_CDE_PTR_MESSAGE_isip_HS4_VMF_DSGN_FROM_CDD'))
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.016\\TEST01\\out\\PduR.epc','PduRRoutingPath_isip_HS1_REQ_EOBD_ON_CAN_7E7'))
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.016\\TEST01\\out\\PduR.epc','PduRRoutingPath_isip_HS1_REQ_EOBD_ON_CAN_7E7_isip_HS1_REQ_EOBD_ON_CAN_7E6_FROM_CDD'))

    #def test_TRS_COMCONF_GEN_016_TEST02(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.016\\TEST02\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.016\\TEST02\\out -EnGw')
    #    self.assertFalse(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.016\\TEST02\\out\\PduR.epc','PduRRoutingPath_isip_HS1_REQ_EOBD_ON_CAN_7E9'))
    #    self.assertFalse(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.016\\TEST02\\out\\PduR.epc','PduRRoutingPath_isip_HS1_REQ_EOBD_ON_CAN_7E9_isip_HS1_REQ_EOBD_ON_CAN_7E8_FROM_CDD'))

    #def test_TRS_COMCONF_GEN_017_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.017\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.017\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.017\\TEST01\\out\\PduR.epc','PduRRoutingPath_isip_HS4_VSM_INF_CFG'))

    #def test_TRS_COMCONF_GEN_018_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.018\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.018\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.018\\TEST01\\out\\PduR.epc','PduRSrcPdu_isip_HS4_VSM_INF_CFG','/EcuC/EcuC/EcucPduCollection/isip_HS4_VSM_INF_CFG_865T','PduRDestPdu_isip_HS4_VSM_INF_CFG_isip_HS4_VSM_INF_PRG_RTAB_TO_CDD','PDUR_DIRECT','/EcuC/EcuC/EcucPduCollection/isip_HS4_VSM_INF_PRG_RTAB_TO_CDD'))

    #def test_TRS_COMCONF_GEN_019_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.019\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.019\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.019\\TEST01\\out\\PduR.epc','PduRRoutingPath_isip_HS4_VSM_INF_CFG_isip_HS4_VSM_INF_PRG_RTAB_FROM_CDD'))

    #def test_TRS_COMCONF_GEN_020_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.020\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.020\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.020\\TEST01\\out\\PduR.epc','PduRSrcPdu_isip_HS4_VSM_INF_CFG_isip_HS4_VSM_INF_PRG_RTAB_FROM_CDD','/EcuC/EcuC/EcucPduCollection/isip_HS4_VSM_INF_PRG_RTAB_FROM_CDD','PduRDestPdu_isip_HS4_VSM_INF_CFG_isip_HS4_VSM_INF_PRG_RTAB','PDUR_DIRECT','/EcuC/EcuC/EcucPduCollection/isip_HS4_VSM_INF_PRG_RTAB_352T'))

    #def test_TRS_COMCONF_GEN_021_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.021\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.021\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.021\\TEST01\\out\\PduR.epc','PduRRoutingPath_EnGw_LinIf_REQ_LIN_VSM_1_1P3'))

    #def test_TRS_COMCONF_GEN_022_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.022\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.022\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.022\\TEST01\\out\\PduR.epc','PduRSrcPdu_EnGw_LinIf_REQ_LIN_VSM_1_1P3','/EcuC/EcuC/EcucPduCollection/EnGwCLD_REQ_LIN_VSM_1_1P3_LinIf','PduRDestPdu_EnGw_LinIf_REQ_LIN_VSM_1_1P3','PDUR_DIRECT','/EcuC/EcuC/EcucPduCollection/LinIf_REQ_LIN_VSM_1_1P3_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_023_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.023\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.023\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.023\\TEST01\\out\\PduR.epc','PduRRoutingPath_EnGw_LinIf_REP_LIN_VSM_1_1P3'))

    #def test_TRS_COMCONF_GEN_024_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.024\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.024\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.024\\TEST01\\out\\PduR.epc','PduRSrcPdu_EnGw_LinIf_REP_LIN_VSM_1_1P3','/EcuC/EcuC/EcucPduCollection/LinIf_REP_LIN_VSM_1_1P3_EnGwCLD','PduRDestPdu_EnGw_LinIf_REP_LIN_VSM_1_1P3','PDUR_DIRECT','/EcuC/EcuC/EcucPduCollection/EnGwCLD_REP_LIN_VSM_1_1P3_LinIf'))

    #def test_TRS_COMCONF_GEN_025_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.025\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.025\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.025\\TEST01\\out\\PduR.epc','PduRRoutingPath_EnGw_LinTp_REQ_FRONT_WIPING_LIN_VSM_1'))

    #def test_TRS_COMCONF_GEN_026_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.026\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.026\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.026\\TEST01\\out\\PduR.epc','PduRSrcPdu_EnGw_LinTp_REQ_FRONT_WIPING_LIN_VSM_1','/EcuC/EcuC/EcucPduCollection/EnGwCLD_REQ_FRONT_WIPING_LIN_VSM_1_LinTp','PduRDestPdu_EnGw_LinTp_REQ_FRONT_WIPING_LIN_VSM_1','PDUR_DIRECT','/EcuC/EcuC/EcucPduCollection/LinTp_REQ_FRONT_WIPING_LIN_VSM_1_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_027_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.027\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.027\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.027\\TEST01\\out\\PduR.epc','PduRRoutingPath_EnGw_LinTp_REP_FRONT_WIPING_LIN_VSM_1'))

    #def test_TRS_COMCONF_GEN_028_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.028\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.028\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.028\\TEST01\\out\\PduR.epc','PduRSrcPdu_EnGw_LinTp_REP_FRONT_WIPING_LIN_VSM_1','/EcuC/EcuC/EcucPduCollection/LinTp_REP_FRONT_WIPING_LIN_VSM_1_EnGwCLD','PduRDestPdu_EnGw_LinTp_REP_FRONT_WIPING_LIN_VSM_1','PDUR_DIRECT','/EcuC/EcuC/EcucPduCollection/EnGwCLD_REP_FRONT_WIPING_LIN_VSM_1_LinTp'))

    #def test_TRS_COMCONF_GEN_029_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.029\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.029\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.029\\TEST01\\out\\PduR.epc','PduRRoutingPath_EnGw_CanIf_REQ_DIAG_SIR_LIN_VSM_1'))

    #def test_TRS_COMCONF_GEN_030_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.030\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.030\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.030\\TEST01\\out\\PduR.epc','PduRSrcPdu_EnGw_CanIf_REQ_DIAG_SIR_LIN_VSM_1','/EcuC/EcuC/EcucPduCollection/CanIf_REQ_DIAG_SIR_LIN_VSM_1_EnGwCLD','PduRDestPdu_EnGw_CanIf_REQ_DIAG_SIR_LIN_VSM_1','PDUR_DIRECT','/EcuC/EcuC/EcucPduCollection/EnGwCLD_REQ_DIAG_SIR_LIN_VSM_1_CanIf'))

    #def test_TRS_COMCONF_GEN_031_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.031\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.031\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.031\\TEST01\\out\\PduR.epc','PduRRoutingPath_EnGw_CanIf_REP_DIAG_SIR_LIN_VSM_1'))

    #def test_TRS_COMCONF_GEN_032_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.032\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.032\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.032\\TEST01\\out\\PduR.epc','PduRSrcPdu_EnGw_CanIf_REP_DIAG_SIR_LIN_VSM_1','/EcuC/EcuC/EcucPduCollection/EnGwCLD_REP_DIAG_SIR_LIN_VSM_1_CanIf','PduRDestPdu_EnGw_CanIf_REP_DIAG_SIR_LIN_VSM_1','PDUR_DIRECT','/EcuC/EcuC/EcucPduCollection/CanIf_REP_DIAG_SIR_LIN_VSM_1_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_033_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.033\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.033\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.033\\TEST01\\out\\PduR.epc','PduRRoutingPath_EnGw_CanTp_REQ_DIAG_FRONT_WIPING_LIN_VSM_1'))

    #def test_TRS_COMCONF_GEN_034_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.034\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.034\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.034\\TEST01\\out\\PduR.epc','PduRSrcPdu_EnGw_CanTp_REQ_DIAG_FRONT_WIPING_LIN_VSM_1','/EcuC/EcuC/EcucPduCollection/CanTp_REQ_DIAG_FRONT_WIPING_LIN_VSM_1_EnGwCLD','PduRDestPdu_EnGw_CanTp_REQ_DIAG_FRONT_WIPING_LIN_VSM_1','PDUR_DIRECT','/EcuC/EcuC/EcucPduCollection/EnGwCLD_REQ_DIAG_FRONT_WIPING_LIN_VSM_1_CanTp'))

    #def test_TRS_COMCONF_GEN_035_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.035\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.035\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckNameRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.035\\TEST01\\out\\PduR.epc','PduRRoutingPath_EnGw_CanTp_REP_DIAG_FRONT_WIPING_LIN_VSM_1'))

    #def test_TRS_COMCONF_GEN_036_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.036\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.036\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckRoutingPath(head + '\\Tests\\TRS.COMCONF.GEN.036\\TEST01\\out\\PduR.epc','PduRSrcPdu_EnGw_CanTp_REP_DIAG_FRONT_WIPING_LIN_VSM_1','/EcuC/EcuC/EcucPduCollection/EnGwCLD_REP_DIAG_FRONT_WIPING_LIN_VSM_1_CanTp','PduRDestPdu_EnGw_CanTp_REP_DIAG_FRONT_WIPING_LIN_VSM_1','PDUR_DIRECT','/EcuC/EcuC/EcucPduCollection/CanTp_REP_DIAG_FRONT_WIPING_LIN_VSM_1_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_037_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.037\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.037\\TEST01\\out -EnGw')
    #   self.assertTrue(FileCheck.CheckId(head + '\\Tests\\TRS.COMCONF.GEN.037\\TEST01\\out\\PduR.epc'))

    #def test_TRS_COMCONF_GEN_040_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST01\\out -EnGw')
    #    self.assertFalse(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST01\\out\\EcuC.epc','isip_HS4_VSM_INF_PRG_RTAB_TO_CDD'))
    #    self.assertFalse(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST01\\out\\EcuC.epc','isip_HS4_VSM_INF_PRG_RTAB_FROM_CDD'))

    #def test_TRS_COMCONF_GEN_040_TEST02(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST02\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST02\\out -EnGw')
    #    self.assertFalse(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST02\\out\\EcuC.epc','isip_HS4_VSM_INF_PRG_RTAB1_TO_CDD'))
    #    self.assertFalse(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST02\\out\\EcuC.epc','isip_HS4_VSM_INF_PRG_RTAB1_FROM_CDD'))

    #def test_TRS_COMCONF_GEN_040_TEST03(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST03\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST03\\out -EnGw')
    #    self.assertFalse(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST03\\out\\EcuC.epc','isip_HS4_VSM_INF_PRG_RTAB1_TO_CDD'))
    #    self.assertFalse(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST03\\out\\EcuC.epc','isip_HS4_VSM_INF_PRG_RTAB1_FROM_CDD'))

    #def test_TRS_COMCONF_GEN_040_TEST04(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST04\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST04\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST04\\out\\EcuC.epc','isip_HS4_VSM_INF_PRG_RTAB_TO_CDD'))
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.040\\TEST04\\out\\EcuC.epc','isip_HS4_VSM_INF_PRG_RTAB_FROM_CDD'))

    #def test_TRS_COMCONF_GEN_041_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.041\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.041\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.041\\TEST01\\out\\EcuC.epc','EnGwCLD_REQ_DIAG_FRONT_WIPING_LIN_VSM_1_CanTp'))

    #def test_TRS_COMCONF_GEN_042_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.042\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.042\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.042\\TEST01\\out\\EcuC.epc','CanTp_REQ_DIAG_FRONT_WIPING_LIN_VSM_1_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_043_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.043\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.043\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.043\\TEST01\\out\\EcuC.epc','EnGwCLD_REP_DIAG_FRONT_WIPING_LIN_VSM_1_CanTp'))

    #def test_TRS_COMCONF_GEN_044_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.044\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.044\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.044\\TEST01\\out\\EcuC.epc','CanTp_REP_DIAG_FRONT_WIPING_LIN_VSM_1_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_045_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.045\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.045\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.045\\TEST01\\out\\EcuC.epc','EnGwCLD_REQ_FRONT_WIPING_LIN_VSM_1_LinTp'))

    #def test_TRS_COMCONF_GEN_046_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.046\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.046\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.046\\TEST01\\out\\EcuC.epc','LinTp_REQ_FRONT_WIPING_LIN_VSM_1_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_047_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.047\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.047\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.047\\TEST01\\out\\EcuC.epc','EnGwCLD_REP_FRONT_WIPING_LIN_VSM_1_LinTp'))

    #def test_TRS_COMCONF_GEN_048_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.048\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.048\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.048\\TEST01\\out\\EcuC.epc','LinTp_REP_FRONT_WIPING_LIN_VSM_1_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_049_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.049\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.049\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.049\\TEST01\\out\\EcuC.epc','EnGwCLD_REQ_DIAG_SIR_LIN_VSM_1_CanIf'))

    #def test_TRS_COMCONF_GEN_050_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.050\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.050\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.050\\TEST01\\out\\EcuC.epc','CanIf_REQ_DIAG_SIR_LIN_VSM_1_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_051_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.051\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.051\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.051\\TEST01\\out\\EcuC.epc','EnGwCLD_REP_DIAG_SIR_LIN_VSM_1_CanIf'))

    #def test_TRS_COMCONF_GEN_052_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.052\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.052\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.052\\TEST01\\out\\EcuC.epc','CanIf_REP_DIAG_SIR_LIN_VSM_1_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_053_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.053\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.053\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.053\\TEST01\\out\\EcuC.epc','EnGwCLD_REQ_LIN_VSM_1_1P3_LinIf'))

    #def test_TRS_COMCONF_GEN_054_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.054\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.054\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.054\\TEST01\\out\\EcuC.epc','LinIf_REQ_LIN_VSM_1_1P3_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_055_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.055\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.055\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.055\\TEST01\\out\\EcuC.epc','EnGwCLD_REP_LIN_VSM_1_1P3_LinIf'))

    #def test_TRS_COMCONF_GEN_056_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.056\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.056\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.056\\TEST01\\out\\EcuC.epc','LinIf_REP_LIN_VSM_1_1P3_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_057_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.057\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.057\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.057\\TEST01\\out\\EcuC.epc','CanIf_REQ_DIAG_LIN_VSM_1_CanTp'))

    #def test_TRS_COMCONF_GEN_058_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.058\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.058\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.058\\TEST01\\out\\EcuC.epc','CanTp_REP_DIAG_LIN_VSM_1_CanIf'))

    #def test_TRS_COMCONF_GEN_059_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.059\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.059\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.059\\TEST01\\out\\EcuC.epc','CanTp_REP_DIAG_LIN_VSM_1_FRONT_WIPING_CanIf'))

    #def test_TRS_COMCONF_GEN_060_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.060\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.060\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.060\\TEST01\\out\\EcuC.epc','CanTp_FC_REP_DIAG_LIN_VSM_1_FRONT_WIPING_CanIf'))

    #def test_TRS_COMCONF_GEN_061_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.061\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.061\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.061\\TEST01\\out\\EcuC.epc','isip_HS4_VSM_INF_PRG_RTAB_TO_CDD'))

    #def test_TRS_COMCONF_GEN_062_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.062\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.062\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckEcuC(head + '\\Tests\\TRS.COMCONF.GEN.062\\TEST01\\out\\EcuC.epc','isip_HS4_VSM_INF_PRG_RTAB_FROM_CDD'))

    #def test_TRS_COMCONF_GEN_065_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.065\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.065\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinTp1(head + '\\Tests\\TRS.COMCONF.GEN.065\\TEST01\\out\\LinTp.epc','LinTpRxNSdu_REP_FRONT_WIPING_LIN_VSM_1'))

    #def test_TRS_COMCONF_GEN_066_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.066\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.066\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinTp2(head + '\\Tests\\TRS.COMCONF.GEN.066\\TEST01\\out\\LinTp.epc','1','41','1.0'))

    #def test_TRS_COMCONF_GEN_067_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.067\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.067\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinTp3(head + '\\Tests\\TRS.COMCONF.GEN.067\\TEST01\\out\\LinTp.epc','/EcuC/EcuC/EcucPduCollection/LinTp_REP_FRONT_WIPING_LIN_VSM_1_EnGwCLD','/LinIf/LinIf/LinIfGlobalConfig/LIN_VSM_1_Channel','/LinTp/LinTp/LinTpGlobalConfig/LinTpChannel_LIN_VSM_1'))

    #def test_TRS_COMCONF_GEN_068_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.068\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.068\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinTp1(head + '\\Tests\\TRS.COMCONF.GEN.068\\TEST01\\out\\LinTp.epc','LinTpTxNSdu_REQ_FRONT_WIPING_LIN_VSM_1'))

    #def test_TRS_COMCONF_GEN_069_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.069\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.069\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinTp2(head + '\\Tests\\TRS.COMCONF.GEN.069\\TEST01\\out\\LinTp.epc','0.1','41','0.1'))

    #def test_TRS_COMCONF_GEN_070_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.070\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.070\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinTp3(head + '\\Tests\\TRS.COMCONF.GEN.070\\TEST01\\out\\LinTp.epc','/EcuC/EcuC/EcucPduCollection/LinTp_REQ_FRONT_WIPING_LIN_VSM_1_EnGwCLD','/LinIf/LinIf/LinIfGlobalConfig/LIN_VSM_1_Channel','/LinTp/LinTp/LinTpGlobalConfig/LinTpChannel_LIN_VSM_1'))

    #def test_TRS_COMCONF_GEN_071_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.071\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.071\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinTp1(head + '\\Tests\\TRS.COMCONF.GEN.071\\TEST01\\out\\LinTp.epc','LinTpChannel_LIN_VSM_1'))

    #def test_TRS_COMCONF_GEN_072_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.072\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.072\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinTp4(head + '\\Tests\\TRS.COMCONF.GEN.072\\TEST01\\out\\LinTp.epc','0','1'))

    #def test_TRS_COMCONF_GEN_075_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.075\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.075\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf1(head + '\\Tests\\TRS.COMCONF.GEN.075\\TEST01\\out\\LinIf.epc','LIN_VSM_1_Channel'))

    #def test_TRS_COMCONF_GEN_076_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.076\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.076\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf2(head + '\\Tests\\TRS.COMCONF.GEN.076\\TEST01\\out\\LinIf.epc','LinIfFrame_REP_LIN_VSM_1_1P3'))

    #def test_TRS_COMCONF_GEN_077_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.077\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.077\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf3(head + '\\Tests\\TRS.COMCONF.GEN.077\\TEST01\\out\\LinIf.epc','8','61','CLASSIC','UNCONDITIONAL'))

    #def test_TRS_COMCONF_GEN_078_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.078\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.078\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf4(head + '\\Tests\\TRS.COMCONF.GEN.078\\TEST01\\out\\LinIf.epc','LinIfPduDirection_REP_LIN_VSM_1_1P3'))

    #def test_TRS_COMCONF_GEN_079_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.079\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.079\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf5(head + '\\Tests\\TRS.COMCONF.GEN.079\\TEST01\\out\\LinIf.epc','LinIfRxPdu_REP_LIN_VSM_1_1P3','/EcuC/EcuC/EcucPduCollection/LinIf_REP_LIN_VSM_1_1P3_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_080_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.080\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.080\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf2(head + '\\Tests\\TRS.COMCONF.GEN.080\\TEST01\\out\\LinIf.epc','LinIfFrame_REQ_LIN_VSM_1_1P3'))

    #def test_TRS_COMCONF_GEN_081_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.081\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.081\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf3(head + '\\Tests\\TRS.COMCONF.GEN.081\\TEST01\\out\\LinIf.epc','8','60','CLASSIC','UNCONDITIONAL'))

    #def test_TRS_COMCONF_GEN_082_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.082\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.082\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf4(head + '\\Tests\\TRS.COMCONF.GEN.082\\TEST01\\out\\LinIf.epc','LinIfPduDirection_REQ_LIN_VSM_1_1P3'))

    #def test_TRS_COMCONF_GEN_083_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.083\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.083\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf5(head + '\\Tests\\TRS.COMCONF.GEN.083\\TEST01\\out\\LinIf.epc','LinIfTxPdu_REQ_LIN_VSM_1_1P3','/EcuC/EcuC/EcucPduCollection/LinIf_REQ_LIN_VSM_1_1P3_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_084_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.084\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.084\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf2(head + '\\Tests\\TRS.COMCONF.GEN.084\\TEST01\\out\\LinIf.epc','LinIfScheduleTable_REP_LIN_VSM_1_1P3'))

    #def test_TRS_COMCONF_GEN_085_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.085\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.085\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf3(head + '\\Tests\\TRS.COMCONF.GEN.085\\TEST01\\out\\LinIf.epc','SCH_REP_LIN_VSM_1_1P3','START_FROM_BEGINNING','RUN_ONCE','LINTP_DIAG_RESPONSE'))

    #def test_TRS_COMCONF_GEN_086_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.086\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.086\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf4(head + '\\Tests\\TRS.COMCONF.GEN.086\\TEST01\\out\\LinIf.epc','LinIfEntry_0'))

    #def test_TRS_COMCONF_GEN_087_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.087\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.087\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf6(head + '\\Tests\\TRS.COMCONF.GEN.087\\TEST01\\out\\LinIf.epc','0','0.080','/LinIf/LinIf/LinIfGlobalConfig/LIN_VSM_1_Channel/LinIfFrame_REP_LIN_VSM_1_1P3'))

    #def test_TRS_COMCONF_GEN_088_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.088\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.088\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf7(head + '\\Tests\\TRS.COMCONF.GEN.088\\TEST01\\out\\LinIf.epc','LinIfEntry_1'))

    #def test_TRS_COMCONF_GEN_089_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.089\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.089\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf8(head + '\\Tests\\TRS.COMCONF.GEN.089\\TEST01\\out\\LinIf.epc','1','0.010','/LinIf/LinIf/LinIfGlobalConfig/LIN_VSM_1_Channel/LinIfFrame_REP_LIN_VSM_1_1P3'))

    #def test_TRS_COMCONF_GEN_090_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.090\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.090\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf2(head + '\\Tests\\TRS.COMCONF.GEN.090\\TEST01\\out\\LinIf.epc','LinIfScheduleTable_REQ_LIN_VSM_1_1P3'))

    #def test_TRS_COMCONF_GEN_091_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.091\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.091\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf3(head + '\\Tests\\TRS.COMCONF.GEN.091\\TEST01\\out\\LinIf.epc','SCH_REQ_LIN_VSM_1_1P3','START_FROM_BEGINNING','RUN_ONCE','LINTP_DIAG_REQUEST'))

    #def test_TRS_COMCONF_GEN_092_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.092\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.092\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf4(head + '\\Tests\\TRS.COMCONF.GEN.092\\TEST01\\out\\LinIf.epc','LinIfEntry_0'))

    #def test_TRS_COMCONF_GEN_093_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.093\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.093\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckLinIf6(head + '\\Tests\\TRS.COMCONF.GEN.093\\TEST01\\out\\LinIf.epc','0','0.010','/LinIf/LinIf/LinIfGlobalConfig/LIN_VSM_1_Channel/LinIfFrame_REQ_LIN_VSM_1_1P3'))

    #def test_TRS_COMCONF_GEN_096_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.096\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.096\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp1(head + '\\Tests\\TRS.COMCONF.GEN.096\\TEST01\\out\\CanTp.epc','CanTpGeneral','255','32767','32767','32767'))

    #def test_TRS_COMCONF_GEN_097_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.097\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.097\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp2(head + '\\Tests\\TRS.COMCONF.GEN.097\\TEST01\\out\\CanTp.epc','CanTpChannel_Gw_DIAG_LIN_VSM_1'))

    #def test_TRS_COMCONF_GEN_098_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.098\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.098\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp3(head + '\\Tests\\TRS.COMCONF.GEN.098\\TEST01\\out\\CanTp.epc','CANTP_MODE_HALF_DUPLEX'))

    #def test_TRS_COMCONF_GEN_099_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.099\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.099\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp4(head + '\\Tests\\TRS.COMCONF.GEN.099\\TEST01\\out\\CanTp.epc','CanTpRxNSdu_REQ_DIAG_LIN_VSM_1_FRONT_WIPING'))

    #def test_TRS_COMCONF_GEN_0100_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.0100\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.0100\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp51(head + '\\Tests\\TRS.COMCONF.GEN.0100\\TEST01\\out\\CanTp.epc','0','1','0','0.1','0.03','0.25','0.01','CANTP_EXTENDED','CANTP_OFF','CANTP_PHYSICAL'))

    #def test_TRS_COMCONF_GEN_0101_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.0101\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.0101\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp6(head + '\\Tests\\TRS.COMCONF.GEN.0101\\TEST01\\out\\CanTp.epc','/EcuC/EcuC/EcucPduCollection/CanTp_REQ_DIAG_FRONT_WIPING_LIN_VSM_1_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_0102_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.0102\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.0102\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp7(head + '\\Tests\\TRS.COMCONF.GEN.0102\\TEST01\\out\\CanTp.epc','CanTpNSa_REQ_DIAG_LIN_VSM_1_FRONT_WIPING','41'))

    #def test_TRS_COMCONF_GEN_0103_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.0103\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.0103\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp7(head + '\\Tests\\TRS.COMCONF.GEN.0103\\TEST01\\out\\CanTp.epc','CanTpNTa_REQ_DIAG_LIN_VSM_1_FRONT_WIPING','41'))

    #def test_TRS_COMCONF_GEN_0104_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.0104\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.0104\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp7(head + '\\Tests\\TRS.COMCONF.GEN.0104\\TEST01\\out\\CanTp.epc','CanTpRxNPdu_REQ_DIAG_LIN_VSM_1_FRONT_WIPING','/EcuC/EcuC/EcucPduCollection/CanIf_REQ_DIAG_LIN_VSM_1_CanTp'))

    #def test_TRS_COMCONF_GEN_0105_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.0105\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.0105\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp7(head + '\\Tests\\TRS.COMCONF.GEN.0105\\TEST01\\out\\CanTp.epc','CanTpTxFcNPdu_REQ_DIAG_LIN_VSM_1_FRONT_WIPING','/EcuC/EcuC/EcucPduCollection/CanTp_FC_REP_DIAG_LIN_VSM_1_FRONT_WIPING_CanIf'))

    #def test_TRS_COMCONF_GEN_0106_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.0106\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.0106\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp4(head + '\\Tests\\TRS.COMCONF.GEN.0106\\TEST01\\out\\CanTp.epc','CanTpTxNSdu_REP_DIAG_LIN_VSM_1_FRONT_WIPING'))

    #def test_TRS_COMCONF_GEN_0107_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.0107\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.0107\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp52(head + '\\Tests\\TRS.COMCONF.GEN.0107\\TEST01\\out\\CanTp.epc','1','0','0.1','0.03','0.25','CANTP_EXTENDED','CANTP_OFF','CANTP_PHYSICAL'))

    #def test_TRS_COMCONF_GEN_0108_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.0108\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.0108\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp6(head + '\\Tests\\TRS.COMCONF.GEN.0108\\TEST01\\out\\CanTp.epc','/EcuC/EcuC/EcucPduCollection/CanTp_REP_DIAG_FRONT_WIPING_LIN_VSM_1_EnGwCLD'))

    #def test_TRS_COMCONF_GEN_0109_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.0109\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.0109\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp7(head + '\\Tests\\TRS.COMCONF.GEN.0109\\TEST01\\out\\CanTp.epc','CanTpNSa_REP_DIAG_LIN_VSM_1_FRONT_WIPING','41'))

    #def test_TRS_COMCONF_GEN_0110_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.0110\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.0110\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp7(head + '\\Tests\\TRS.COMCONF.GEN.0110\\TEST01\\out\\CanTp.epc','CanTpNTa_REP_DIAG_LIN_VSM_1_FRONT_WIPING','41'))

    #def test_TRS_COMCONF_GEN_0110_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.0110\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.0110\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp7(head + '\\Tests\\TRS.COMCONF.GEN.0110\\TEST01\\out\\CanTp.epc','CanTpNTa_REP_DIAG_LIN_VSM_1_FRONT_WIPING','41'))

    #def test_TRS_COMCONF_GEN_0111_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.0111\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.0111\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp7(head + '\\Tests\\TRS.COMCONF.GEN.0111\\TEST01\\out\\CanTp.epc','CanTpTxNPdu_REP_DIAG_LIN_VSM_1_FRONT_WIPING','/EcuC/EcuC/EcucPduCollection/CanTp_REP_DIAG_LIN_VSM_1_FRONT_WIPING_CanIf'))

    #def test_TRS_COMCONF_GEN_0112_TEST01(self):
    #    current_path = os.path.realpath(__file__)
    #    head, tail = ntpath.split(current_path)
    #    os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.0112\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.0112\\TEST01\\out -EnGw')
    #    self.assertTrue(FileCheck.CheckCanTp7(head + '\\Tests\\TRS.COMCONF.GEN.0112\\TEST01\\out\\CanTp.epc','CanTpRxFcNPdu_REP_DIAG_LIN_VSM_1_FRONT_WIPING','/EcuC/EcuC/EcucPduCollection/CanIf_REQ_DIAG_LIN_VSM_1_CanTp'))

    def test_TRS_COMCONF_GEN_0113_TEST01(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('C:\\Users\\msnecula\\AppData\\Local\\Programs\\Python\\Python37\\python COM_Configurator.py -in @' + head + '\\Tests\\TRS.COMCONF.GEN.0113\\TEST01\\inputs.txt -out ' + head + '\\Tests\\TRS.COMCONF.GEN.0113\\TEST01\\out -EnGw')
        self.assertTrue(FileCheck.CheckCanTp8(head + '\\Tests\\TRS.COMCONF.GEN.0113\\TEST01\\out\\CanTp.epc'))




























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

    # def test_TRS_COMCONF_GEN_005(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('coverage run COM_Configurator.py -in ' + head + '\\Tests\\TRS.COMCONF.GEN.005\\in -out ' + head + '\\Tests\\TRS.COMCONF.GEN.005\\out -EnGw')
    #     self.assertFalse(FileCheck.ecuc(head + '\\Tests\\TRS.COMCONF.GEN.005\\in\EPC_GwDiagCanLinConfig.epc', head + '\\Tests\\TRS.COMCONF.GEN.005\\out\EcuC.epc'))

suite = unittest.TestLoader().loadTestsFromTestCase(COMConfigurator)
unittest.TextTestRunner(verbosity=2).run(suite)

# current_path = os.path.realpath(__file__)
# head, tail = ntpath.split(current_path)
# if __name__ == "__main__":
#     unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=head + "\\tests"))