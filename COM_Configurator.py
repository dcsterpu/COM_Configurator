import argparse
import logging
import os
import sys
import re
from lxml import etree, objectify
from xml.dom.minidom import parseString
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
#from coverage import Coverage


def arg_parse(parser):
    parser.add_argument('-in', '--inp', nargs='*', help="input path or file", required=True, default="")
    parser.add_argument('-out', '--out', help="output path", required=False, default="")
    parser.add_argument('-out_epc', '--out_epc', help="output path for configuration file(s)", required=False, default="")
    parser.add_argument('-out_script', '--out_script', help="output path for Scriptor file(s)", required=False, default="")
    parser.add_argument('-out_log', '--out_log', help="output path for log file", required=False, default="")
    parser.add_argument('-NeMo', action="store_const", const="-NeMo", required=False, default="")
    parser.add_argument('-EnGw', action="store_const", const="-EnGw", required=False, default="")
    parser.add_argument('-CFHM', action="store_const", const="-CFHM", required=False, default="")
    parser.add_argument('-LPhM', action="store_const", const="-LPhM", required=False, default="")


def prettify_xml(elem):
    rough_string = etree.tostring(elem, pretty_print=True)
    reparsed = parseString(rough_string)
    return '\n'.join([line for line in reparsed.toprettyxml(indent=' '*4).split('\n') if line.strip()])


def check_if_xml_is_wellformed(file):
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(file)


def set_logger(path):
    # logger creation and setting
    logger = logging.getLogger('result')
    hdlr = logging.FileHandler(path + '/result_COM.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    open(path + '/result_COM.log', 'w').close()
    return logger


def main():
    # parsing the command line arguments
    parser = argparse.ArgumentParser()
    arg_parse(parser)
    args = parser.parse_args()
    input_path = args.inp
    error = False
    paths_list = []
    files_list = []
    entry_list = []
    NeMo = False
    if args.NeMo:
        NeMo = True
    EnGw = False
    if args.EnGw:
        EnGw = True
    CFHM = False
    if args.CFHM:
        CFHM = True
    LPhM = False
    if args.LPhM:
        LPhM = True
    for path in input_path:
        if path.startswith('@'):
            file = open(path[1:])
            line_file = file.readline()
            while line_file != "":
                line_file = line_file.rstrip()
                line_file = line_file.lstrip()
                if "#" not in line_file:
                    if os.path.isdir(line_file):
                        paths_list.append(line_file)
                    elif os.path.isfile(line_file):
                        files_list.append(line_file)
                    else:
                        print("\nError defining the input path: " + line_file + "\n")
                        error = True
                    line_file = file.readline()
                else:
                    line_file = file.readline()
            file.close()
        else:
            if os.path.isdir(path):
                paths_list.append(path)
            elif os.path.isfile(path):
                files_list.append(path)
            else:
                print("\nError defining the input path: " + path + "\n")
                error = True
    for path in paths_list:
        for (dirpath, dirnames, filenames) in os.walk(path):
            for file in filenames:
                fullname = dirpath + '\\' + file
                files_list.append(fullname)
    [entry_list.append(elem) for elem in files_list if elem not in entry_list]
    if error:
        sys.exit(1)
    output_path = args.out
    output_epc = args.out_epc
    output_script = args.out_script
    output_log = args.out_log
    if output_path:
        if not os.path.isdir(output_path):
            print("\nError defining the output path!\n")
            sys.exit(1)
        if output_log:
            if not os.path.isdir(output_log):
                print("\nError defining the output log path!\n")
                sys.exit(1)
            logger = set_logger(output_log)
            if NeMo:
                NeMo_script(entry_list, output_path, logger)
            if EnGw:
                PduR_script(entry_list, output_path, logger)
                EnGw_config(entry_list, output_path, logger)
                EcuC_config(entry_list, output_path, logger)
                PduR_config(entry_list, output_path, logger)
                CanTp_config(entry_list, output_path, logger)
                CanIf_config(entry_list, output_path, logger)
                LinTp_config(entry_list, output_path, logger)
                LinIf_config(entry_list, output_path, logger)
                BswM_config(entry_list, output_path, logger)
            if CFHM:
                CFHM_script(entry_list, output_path, logger)
            if LPhM:
                LPhM_config(entry_list, output_path, logger)
        else:
            logger = set_logger(output_path)
            if NeMo:
                NeMo_script(entry_list, output_path, logger)
            if EnGw:
                PduR_script(entry_list, output_path, logger)
                EnGw_config(entry_list, output_path, logger)
                EcuC_config(entry_list, output_path, logger)
                PduR_config(entry_list, output_path, logger)
                CanTp_config(entry_list, output_path, logger)
                CanIf_config(entry_list, output_path, logger)
                LinTp_config(entry_list, output_path, logger)
                LinIf_config(entry_list, output_path, logger)
                BswM_config(entry_list, output_path, logger)
            if CFHM:
                CFHM_script(entry_list, output_path, logger)
            if LPhM:
                LPhM_config(entry_list, output_path, logger)
    elif not output_path:
        if output_epc:
            if not os.path.isdir(output_epc):
                print("\nError defining the output epc path!\n")
                sys.exit(1)
            if output_log:
                if not os.path.isdir(output_log):
                    print("\nError defining the output log path!\n")
                    sys.exit(1)
                logger = set_logger(output_log)
                if EnGw:
                    EnGw_config(entry_list, output_epc, logger)
                    EcuC_config(entry_list, output_epc, logger)
                    PduR_config(entry_list, output_epc, logger)
                    CanTp_config(entry_list, output_epc, logger)
                    CanIf_config(entry_list, output_epc, logger)
                    LinTp_config(entry_list, output_epc, logger)
                    LinIf_config(entry_list, output_epc, logger)
                    BswM_config(entry_list, output_epc, logger)
                if LPhM:
                    LPhM_config(entry_list, output_epc, logger)
            else:
                logger = set_logger(output_epc)
                if EnGw:
                    EnGw_config(entry_list, output_epc, logger)
                    EcuC_config(entry_list, output_epc, logger)
                    PduR_config(entry_list, output_epc, logger)
                    CanTp_config(entry_list, output_epc, logger)
                    CanIf_config(entry_list, output_epc, logger)
                    LinTp_config(entry_list, output_epc, logger)
                    LinIf_config(entry_list, output_epc, logger)
                    BswM_config(entry_list, output_epc, logger)
                if LPhM:
                    LPhM_config(entry_list, output_epc, logger)
        if output_script:
            if not os.path.isdir(output_script):
                print("\nError defining the output script path!\n")
                sys.exit(1)
            if output_log:
                if not os.path.isdir(output_log):
                    print("\nError defining the output log path!\n")
                    sys.exit(1)
                logger = set_logger(output_log)
                if NeMo:
                    NeMo_script(entry_list, output_script, logger)
                if EnGw:
                    PduR_script(entry_list, output_script, logger)
                if CFHM:
                    CFHM_script(entry_list, output_script, logger)
            else:
                logger = set_logger(output_script)
                if NeMo:
                    NeMo_script(entry_list, output_script, logger)
                if EnGw:
                    PduR_script(entry_list, output_script, logger)
                if CFHM:
                    CFHM_script(entry_list, output_script, logger)
    else:
        print("\nNo output path defined!\n")
        sys.exit(1)


def PduR_script(file_list, output_path, logger):
    mappings = []
    can_frames = []
    frames_port = []
    items = []
    triggerings = []
    can_frames_triggering = []
    routes = []
    for file in file_list:
        if file.endswith('.arxml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            frames = root.findall(".//{http://autosar.org/schema/r4.0}PDU-TRIGGERING")
            for elem in frames:
                obj_elem = {}
                obj_elem['PDU'] = elem.find("{http://autosar.org/schema/r4.0}I-PDU-REF").text.split("/")[-1]
                obj_elem['NAME'] = elem.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                obj_elem['CHANNEL'] = elem.getparent().getparent().getchildren()[0].text
                obj_elem['CLUSTER'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                obj_elem['PACKAGE'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                obj_elem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                triggerings.append(obj_elem)
            frames = root.findall(".//{http://autosar.org/schema/r4.0}CAN-FRAME")
            for elem in frames:
                obj_elem = {}
                obj_elem['NAME'] = elem.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                obj_elem['PDU'] = elem.find(".//{http://autosar.org/schema/r4.0}PDU-REF").text.split("/")[-1]
                can_frames.append(obj_elem)
            frames = root.findall(".//{http://autosar.org/schema/r4.0}CAN-FRAME-TRIGGERING")
            for elem in frames:
                obj_elem = {}
                obj_elem['CAN-FRAME'] = elem.find(".//{http://autosar.org/schema/r4.0}FRAME-REF").text.split("/")[-1]
                obj_elem['ID'] = elem.find(".//{http://autosar.org/schema/r4.0}IDENTIFIER").text
                obj_elem['PORT'] = None
                ports = elem.findall(".//{http://autosar.org/schema/r4.0}FRAME-PORT-REF")
                for port in ports:
                    if "/VSM/" in port.text:
                        obj_elem['PORT'] = port.text.split("/")[-1]
                obj_elem['WAY'] = None
                can_frames_triggering.append(obj_elem)
            frames = root.findall(".//{http://autosar.org/schema/r4.0}FRAME-PORT")
            for elem in frames:
                obj_elem = {}
                obj_elem['NAME'] = elem.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                direction = elem.find("{http://autosar.org/schema/r4.0}COMMUNICATION-DIRECTION").text
                obj_elem['WAY'] = None
                if direction == "OUT":
                    obj_elem['WAY'] = "T"
                elif direction == "IN":
                    obj_elem['WAY'] = "R"
                else:
                    logger.error("The communication direction of frame-port " + obj_elem['NAME'] + " is not valid")
                frames_port.append(obj_elem)
        elif file.endswith('.xml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            mapping = root.findall(".//GATEWAY-MAPPING")
            for elem in mapping:
                obj_elem = {}
                obj_elem['SOURCE'] = elem.find(".//SOURCE-I-PDU-REF").text
                obj_elem['SOURCE-PDU'] = None
                obj_elem['SOURCE-CLUSTER'] = None
                obj_elem['TARGET'] = elem.find(".//TARGET-I-PDU-REF").text
                obj_elem['TARGET-PDU'] = None
                obj_elem['TARGET-CLUSTER'] = None
                obj_elem['TYPE'] = elem.find(".//CDD-TYPE").text
                mappings.append(obj_elem)
    for mapping in mappings:
        for frame in triggerings:
            if mapping['SOURCE'].split("/")[-1] == frame['NAME']:
                mapping['SOURCE-CLUSTER'] = frame['CLUSTER']
                mapping['SOURCE-PDU'] = frame['PDU']
            if mapping['TARGET'].split("/")[-1] == frame['NAME']:
                mapping['TARGET-CLUSTER'] = frame['CLUSTER']
                mapping['TARGET-PDU'] = frame['PDU']
    for elem in can_frames_triggering:
        for port in frames_port:
            if elem['PORT'] and elem['PORT'] == port['NAME']:
                elem['WAY'] = port['WAY']
                break
    # TRS.COMCONF.GEN.009(0)
    for mapping in mappings[:]:
        obj_map = {}
        dest_list = []
        obj_map['SOURCE'] = mapping['SOURCE-PDU']
        obj_map['CLUSTER'] = mapping['SOURCE-CLUSTER']
        obj_map['ID'] = None
        obj_map['WAY'] = None
        for frame in can_frames:
            if mapping['SOURCE-PDU'] == frame['PDU']:
                for assoc in can_frames_triggering:
                    if frame['NAME'] == assoc['CAN-FRAME']:
                        obj_map['ID'] = assoc['ID']
                        obj_map['WAY'] = assoc['WAY']
        for dest in mappings[:]:
            if dest['SOURCE'] == mapping['SOURCE']:
                obj_dest = {}
                obj_dest['TARGET'] = dest['TARGET-PDU']
                obj_dest['CLUSTER'] = dest['TARGET-CLUSTER']
                obj_dest['TYPE'] = dest['TYPE']
                obj_dest['ID'] = None
                obj_dest['WAY'] = None
                for frame in can_frames:
                    if dest['TARGET-PDU'] == frame['PDU']:
                        for assoc in can_frames_triggering:
                            if frame['NAME'] == assoc['CAN-FRAME']:
                                obj_dest['ID'] = assoc['ID']
                                obj_dest['WAY'] = assoc['WAY']
                dest_list.append(obj_dest)
                mappings.remove(dest)
        if dest_list:
            obj_map['TARGET'] = dest_list
            items.append(obj_map)

    # TRS.COMCONF.GEN.012(0)
    for item in items:
        for dest in item['TARGET']:
            if dest['TYPE'] == "GW-REMOTE-DIAG":
                routes.append(item)
                break
            elif dest['TYPE'] == "GW-FILTERED":
                routes.append(item)
                break
            elif dest['TYPE'] == "GW-LIN-UNCONNECTED":
                routes.append(item)
                break
            elif dest['TYPE'] == "GW-CAN-DIAG":
                routes.append(item)
                break
    # TRS.COMCONF.GEN.010(0)
    for route in routes[:]:
        if route['SOURCE'] is None:
            routes.remove(route)
            '''logger.warning('The mapping with source ' + route['SOURCE'] + " has been deleted because the source reference cannot be found")'''
            continue
        if route['ID'] is None:
            routes.remove(route)
            logger.warning('The mapping with source ' + route['SOURCE'] + " has been deleted because the source ID cannot be established")
            continue
        # TRS.COMCONF.GEN.0011(0)
        if route['WAY'] is None:
            routes.remove(route)
            logger.warning('The mapping with source ' + route['SOURCE'] + " has been deleted because the communication direction cannot be established")
        else:
            for dest in route['TARGET']:
                if dest['TARGET'] is None:
                    routes.remove(route)
                    '''logger.warning('The mapping with source ' + route['SOURCE'] + " has been deleted because the target reference cannot be found")'''
    rootScript = etree.Element('Script')
    name = etree.SubElement(rootScript, 'Name').text = "EnGw_PduR_Update"
    description = etree.SubElement(rootScript, 'Decription').text = "Updated PduR configuration for EnGw"
    expression = etree.SubElement(rootScript, 'Expression').text = "as:modconf('PduR')[1]"
    operations = etree.SubElement(rootScript, 'Operations')
    for route in routes:
        operation = etree.SubElement(operations, 'Operation')
        operation.attrib['Type'] = "ForEach"
        expression = etree.SubElement(operation, 'Expression')
        expression.text = "as:modconf('PduR')[1]/PduRRoutingTables/*/PduRRoutingTable/*/PduRRoutingPath/*[@name=" + '"' + route['SOURCE'] + "_" + route['ID'] + route['WAY'] + '"]' + "/PduRSrcPdu/PduRSrcPduRef[.=" + '"ASPath:/EcuC/EcuC/EcucPduCollection/' + route['SOURCE'] + "_" + route['ID'] + route['WAY'] + '"]/../../PduRDestPdu/*/PduRDestPduRef[.="ASPath:/EcuC/EcuC/EcucPduCollection/' + route['SOURCE'] + "_" + route['ID'] + route['WAY'] + '"]/../../../../*[@name="PduRRoutingPath_' + route['SOURCE'] + '"]/PduRDestPdu'
        operations_add = etree.SubElement(operation, 'Operations')
        operation = etree.SubElement(operations_add, 'Operation')
        operation.attrib['Type'] = "Add"
        expression = etree.SubElement(operation, 'Expression').text = '"PduRDestPdu_' + route['SOURCE'] + '"'
        operation = etree.SubElement(operations_add, 'Operation')
        operation.attrib['Type'] = "ForEach"
        expression = etree.SubElement(operation, 'Expression').text = "PduRDestPdu_" + route['SOURCE'] + "/PduRDestPduDataProvision"
        operations_local = etree.SubElement(operation, 'Operations')
        operation = etree.SubElement(operations_local, 'Operation')
        operation.attrib['Type'] = "SetEnabled"
        expression = etree.SubElement(operation, 'Expression').text = "boolean(1)"
        operation = etree.SubElement(operations_local, 'Operation')
        operation.attrib['Type'] = "SetValue"
        expression = etree.SubElement(operation, 'Expression').text = '"PDUR_DIRECT"'
        operation = etree.SubElement(operations_add, 'Operation')
        operation.attrib['Type'] = "ForEach"
        expression = etree.SubElement(operation, "Expression").text = "PduRDestPdu_" + route['SOURCE'] + "/PduRDestPduRef"
        operations_local2 = etree.SubElement(operation, 'Operations')
        operation = etree.SubElement(operations_local2, 'Operation')
        operation.attrib['Type'] = "SetValue"
        expression = etree.SubElement(operation, 'Expression').text = '"ASPath:/EcuC/EcuC/EcucPduCollection/' + route['SOURCE'] + "_" + route['ID'] + route['WAY'] + '"'
        operation = etree.SubElement(operations, "Operation")
        operation.attrib['Type'] = "ForEach"
        expression = etree.SubElement(operation, 'Expression')
        expression.text = "as:modconf('PduR')[1]/PduRRoutingTables/*/PduRRoutingTable/*/PduRRoutingPath/*[@name=" + '"' + route['SOURCE'] + "_" + route['ID'] + route['WAY'] + '"]'
        operations_last = etree.SubElement(operation, 'Operations')
        operation = etree.SubElement(operations_last, 'Operation')
        operation.attrib['Type'] = "Remove"
        expression = etree.SubElement(operation, 'Expression').text = "boolean(1)"
    pretty_xml = prettify_xml(rootScript)
    tree = etree.ElementTree(etree.fromstring(pretty_xml))
    tree.write(output_path + "/EnGw_PduR_Update.xml", encoding="UTF-8", xml_declaration=True, method="xml", doctype = "<!-- XML file generated by COM_Configurator-18 -->")


def PduR_config(file_list, output_path, logger):
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    mappings = []
    can_frames = []
    frames_port = []
    items = []
    nads = []
    diag_tools = []
    triggerings = []
    rpg_triggerings = []
    can_frames_triggering = []
    routes = []
    for file in file_list:
        if file.endswith('.arxml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            frames = root.findall(".//{http://autosar.org/schema/r4.0}PDU-TRIGGERING")
            for elem in frames:
                obj_elem = {}
                obj_elem['PDU'] = elem.find("{http://autosar.org/schema/r4.0}I-PDU-REF").text.split("/")[-1]
                obj_elem['NAME'] = elem.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                obj_elem['CHANNEL'] = elem.getparent().getparent().getchildren()[0].text
                obj_elem['CLUSTER'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                obj_elem['PACKAGE'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                obj_elem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                triggerings.append(obj_elem)
                # #RPG path
                # port_refs = elem.findall(".//{http://autosar.org/schema/r4.0}I-PDU-PORT-REF")
                # obj_temp = {}
                # cont_test = False
                # ecu_list = []
                # for port_ref in port_refs:
                #     if port_ref.attrib['DEST'] == "I-PDU-PORT" and port_ref.text == "/RootP_NetworkDesc/ECUINSTANCES/OUTIL_DIAG/cc_OUTIL_DIAG_HS1/ippIn_OUTIL_DIAG_HS1":
                #         obj_temp['PDU'] = obj_elem['PDU']
                #         cont_test = True
                #     if cont_test and "ippOut_" in port_ref.text:
                #         ecu_list.append(port_ref.text.split("/")[3])
                # if cont_test:
                #     obj_temp['ECU'] = ecu_list
                #     rpg_triggerings.append(obj_temp)
            frames = root.findall(".//{http://autosar.org/schema/r4.0}CAN-FRAME")
            for elem in frames:
                obj_elem = {}
                obj_elem['NAME'] = elem.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                obj_elem['PDU'] = elem.find(".//{http://autosar.org/schema/r4.0}PDU-REF").text.split("/")[-1]
                can_frames.append(obj_elem)
            frames = root.findall(".//{http://autosar.org/schema/r4.0}CAN-FRAME-TRIGGERING")
            for elem in frames:
                obj_elem = {}
                obj_elem['CAN-FRAME'] = elem.find(".//{http://autosar.org/schema/r4.0}FRAME-REF").text.split("/")[-1]
                obj_elem['ID'] = elem.find(".//{http://autosar.org/schema/r4.0}IDENTIFIER").text
                obj_elem['PORT'] = None
                ports = elem.findall(".//{http://autosar.org/schema/r4.0}FRAME-PORT-REF")
                for port in ports:
                    if "/VSM/" in port.text:
                        obj_elem['PORT'] = port.text.split("/")[-1]
                obj_elem['WAY'] = None
                can_frames_triggering.append(obj_elem)
            frames = root.findall(".//{http://autosar.org/schema/r4.0}FRAME-PORT")
            for elem in frames:
                obj_elem = {}
                obj_elem['WAY'] = None
                obj_elem['NAME'] = elem.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                direction = elem.find("{http://autosar.org/schema/r4.0}COMMUNICATION-DIRECTION").text
                if direction == "OUT":
                    obj_elem['WAY'] = "T"
                elif direction == "IN":
                    obj_elem['WAY'] = "R"
                else:
                    logger.error("The communication direction of frame-port " + obj_elem['NAME'] + " is not valid")
                frames_port.append(obj_elem)
            elements = root.findall(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-CONFIG")
            for elem in elements:
                obj_nad = {}
                obj_nad['NAME'] = elem.find(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-ECU-REF").text.split("/")[-2]
                obj_nad['NETWORK'] = elem.find(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-ECU-REF").text.split("/")[-1]
                obj_nad['ID'] = elem.find(".//{http://autosar.org/schema/r4.0}CONFIGURED-NAD").text
                obj_nad['LIN'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                obj_nad['CONFIG'] = elem.find(".//{http://autosar.org/schema/r4.0}PROTOCOL-VERSION").text
                nads.append(obj_nad)
        elif file.endswith('.xml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            mapping = root.findall(".//GATEWAY-MAPPING")
            for elem in mapping:
                obj_elem = {}
                obj_elem['SOURCE'] = elem.find(".//SOURCE-I-PDU-REF").text
                obj_elem['SOURCE-PDU'] = None
                obj_elem['SOURCE-CLUSTER'] = None
                obj_elem['TARGET'] = elem.find(".//TARGET-I-PDU-REF").text
                obj_elem['TARGET-PDU'] = None
                obj_elem['TARGET-CLUSTER'] = None
                obj_elem['TYPE'] = elem.find(".//CDD-TYPE").text
                mappings.append(obj_elem)
            diags = root.findall(".//CAN-DIAG-TOOL")
            for elem in diags:
                diag_tools.append(elem.find(".//CAN-CLUSTER-REF").text.split("/")[-1])
        elif file.endswith('.txt'):
            with open(file) as text_file:
                for cnt, line in enumerate(text_file):
                    temp_line = line.strip().split()
                    temp_dict = {}
                    temp_dict['ROUTING-PATH-NAME'] = temp_line[0]
                    temp_dict['ROUTING-PATH-DEST-DIAG'] = temp_line[1]
                    temp_dict['ROUTING-PATH-DEST-DOIP'] = temp_line[2]
                    rpg_triggerings.append(temp_dict)

    for mapping in mappings:
        for frame in triggerings:
            if mapping['SOURCE'].split("/")[-1] == frame['NAME']:
                mapping['SOURCE-CLUSTER'] = frame['CLUSTER']
                mapping['SOURCE-PDU'] = frame['PDU']
            if mapping['TARGET'].split("/")[-1] == frame['NAME']:
                mapping['TARGET-CLUSTER'] = frame['CLUSTER']
                mapping['TARGET-PDU'] = frame['PDU']
    # delete mappings without complete data
    for mapping in mappings[:]:
        if mapping['SOURCE-CLUSTER'] is None or mapping['TARGET-CLUSTER'] is None:
            mappings.remove(mapping)
    for elem in can_frames_triggering:
        for port in frames_port:
            if elem['PORT'] and elem['PORT'] == port['NAME']:
                elem['WAY'] = port['WAY']
                break
    # TRS.COMCONF.GEN.014(0)
    for mapping in mappings[:]:
        obj_map = {}
        dest_list = []
        obj_map['SOURCE'] = mapping['SOURCE-PDU']
        obj_map['CLUSTER'] = mapping['SOURCE-CLUSTER']
        obj_map['ID'] = None
        obj_map['WAY'] = None
        for frame in can_frames:
            if mapping['SOURCE-PDU'] == frame['PDU']:
                for assoc in can_frames_triggering:
                    if frame['NAME'] == assoc['CAN-FRAME']:
                        obj_map['ID'] = assoc['ID']
                        obj_map['WAY'] = assoc['WAY']
        for dest in mappings[:]:
            if dest['SOURCE'] == mapping['SOURCE']:
                obj_dest = {}
                obj_dest['TARGET'] = dest['TARGET-PDU']
                obj_dest['CLUSTER'] = dest['TARGET-CLUSTER']
                obj_dest['TYPE'] = dest['TYPE']
                obj_dest['ID'] = None
                obj_dest['WAY'] = None
                for frame in can_frames:
                    if dest['TARGET-PDU'] == frame['PDU']:
                        for assoc in can_frames_triggering:
                            if frame['NAME'] == assoc['CAN-FRAME']:
                                obj_dest['ID'] = assoc['ID']
                                obj_dest['WAY'] = assoc['WAY']
                dest_list.append(obj_dest)
                mappings.remove(dest)
        if dest_list:
            obj_map['TARGET'] = dest_list
            items.append(obj_map)

    # TRS.COMCONF.GEN.016(0)
    for item in items:
        for dest in item['TARGET']:
            if dest['TYPE'] == "GW-REMOTE-DIAG":
                routes.append(item)
                break
            elif dest['TYPE'] == "GW-FILTERED":
                routes.append(item)
                break
            elif dest['TYPE'] == "GW-LIN-UNCONNECTED":
                routes.append(item)
                break
            elif dest['TYPE'] == "GW-CAN-DIAG":
                routes.append(item)
                break

    # TRS.COMCONF.GEN.015(0)
    for route in routes[:]:
        if route['SOURCE'] is None:
            routes.remove(route)
            '''logger.warning('The mapping with source ' + route['SOURCE'] + " has been deleted because the source reference cannot be found")'''
            continue
        if route['ID'] is None:
            routes.remove(route)
            logger.warning('The mapping with source ' + route['SOURCE'] + " has been deleted because the source ID cannot be established")
            continue
        if route['WAY'] is None:
            routes.remove(route)
            logger.warning('The mapping with source ' + route['SOURCE'] + " has been deleted because the communication direction cannot be established")
        else:
            for dest in route['TARGET']:
                if dest['TARGET'] is None:
                    routes.remove(route)
                    '''logger.warning('The mapping with source ' + route['SOURCE'] + " has been deleted because the target reference cannot be found")'''
                    continue
                if dest['ID'] is None:
                    routes.remove(route)
                    logger.warning('The mapping with source ' + route['SOURCE'] + " has been deleted because the target ID cannot be established")
                    continue
                if dest['WAY'] is None:
                    routes.remove(route)
                    logger.warning('The mapping with source ' + route['SOURCE'] + " has been deleted because the communication direction cannot be established")
    # create ouput file: PduR.epc
    rootPduR = etree.Element('AUTOSAR', {attr_qname: 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd'}, nsmap=NSMAP)
    packages = etree.SubElement(rootPduR, 'AR-PACKAGES')
    package = etree.SubElement(packages, 'AR-PACKAGE')
    short_name = etree.SubElement(package, 'SHORT-NAME').text = "PduR"
    elements = etree.SubElement(package, 'ELEMENTS')
    ecuc_module = etree.SubElement(elements, 'ECUC-MODULE-CONFIGURATION-VALUES')
    short_name = etree.SubElement(ecuc_module, 'SHORT-NAME').text = "PduR"
    definition = etree.SubElement(ecuc_module, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-MODULE-DEF"
    definition.text = "/AUTOSAR/EcuDefs/PduR"
    description = etree.SubElement(ecuc_module, 'IMPLEMENTATION-CONFIG-VARIANT').text = "VARIANT-POST-BUILD"
    containers = etree.SubElement(ecuc_module, 'CONTAINERS')
    ecuc_container = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "PduRRoutingTables"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables"
    parameter_values = etree.SubElement(ecuc_container, 'PARAMETER-VALUES')
    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRConfigurationId"
    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "0"
    subcontainer_init = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    # routing path groups creation
    if rpg_triggerings:
        # diag RPG
        ecuc_container_value = etree.SubElement(subcontainer_init, 'ECUC-CONTAINER-VALUE')
        short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = 'RPG_CAN_DIAG'
        definition = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingPathGroup"
        param_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
        ecuc_numerical_param_value = etree.SubElement(param_values, 'ECUC-NUMERICAL-PARAM-VALUE')
        definition_routing = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
        definition_routing.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
        definition_routing.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingPathGroup/PduRIsEnabledAtInit"
        value_routing = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "0"
        ecuc_numerical_param_value = etree.SubElement(param_values, 'ECUC-NUMERICAL-PARAM-VALUE')
        definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
        definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingPathGroup/PduRRoutingPathGroupId"
        value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(0)
        refer_values_diag = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
        # ethernet RPG
        ecuc_container_value = etree.SubElement(subcontainer_init, 'ECUC-CONTAINER-VALUE')
        short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = 'RPG_ETH_DOIP'
        definition = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingPathGroup"
        param_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
        ecuc_numerical_param_value = etree.SubElement(param_values, 'ECUC-NUMERICAL-PARAM-VALUE')
        definition_routing = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
        definition_routing.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
        definition_routing.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingPathGroup/PduRIsEnabledAtInit"
        value_routing = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "0"
        ecuc_numerical_param_value = etree.SubElement(param_values, 'ECUC-NUMERICAL-PARAM-VALUE')
        definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
        definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingPathGroup/PduRRoutingPathGroupId"
        value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(1)
        refer_values_doip = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
        # add RPG references:
        for data in rpg_triggerings:
            ecuc_reference_value = etree.SubElement(refer_values_diag, 'ECUC-REFERENCE-VALUE')
            definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingPathGroup/PduRDestPduRef"
            value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
            value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value_ref.text = '/PduR/PduR/PduRRoutingTables/PduRRoutingTable/' + data['ROUTING-PATH-NAME'] + "/" + data['ROUTING-PATH-DEST-DIAG']
            ecuc_reference_value = etree.SubElement(refer_values_doip, 'ECUC-REFERENCE-VALUE')
            definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingPathGroup/PduRDestPduRef"
            value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
            value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value_ref.text = '/PduR/PduR/PduRRoutingTables/PduRRoutingTable/' + data['ROUTING-PATH-NAME'] + "/" + data['ROUTING-PATH-DEST-DOIP']
    # routing paths creation
    ecuc_container_value = etree.SubElement(subcontainer_init, 'ECUC-CONTAINER-VALUE')
    short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRRoutingTable"
    definition = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable"
    param_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    ecuc_numerical_param_value = etree.SubElement(param_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    definition_routing = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    definition_routing.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
    definition_routing.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRIsMinimumRouting"
    value_routing = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "0"
    subcontainer_route = etree.SubElement(ecuc_container_value, 'SUB-CONTAINERS')
    index_id = 0
    for route in routes:
        ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
        # TRS.COMCONF.GEN.017(0)
        short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_' + route['SOURCE']
        definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
        subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
        # TRS.COMCONF.GEN.018(0)
        # src
        ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
        short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_" + route['SOURCE']
        definition = etree.SubElement(ecuc_container_value_src, 'DEFINITION-REF')
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu"
        parameter_values = etree.SubElement(ecuc_container_value_src, 'PARAMETER-VALUES')
        ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
        definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
        definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSourcePduHandleId"
        value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index_id)
        index_id = index_id + 1
        reference_values = etree.SubElement(ecuc_container_value_src, 'REFERENCE-VALUES')
        ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
        definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
        definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSrcPduRef"
        value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/" + route['SOURCE'] + "_" + str(route['ID']) + str(route['WAY'])
        #dest
        for destination in route['TARGET']:
            ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_" + route['SOURCE'] + "_" + destination['TARGET'] + "_TO_CDD"
            definition = etree.SubElement(ecuc_container_value_dest, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu"
            parameter_values = etree.SubElement(ecuc_container_value_dest, 'PARAMETER-VALUES')
            ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
            definition = etree.SubElement(ecuc_textual_param_value, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduDataProvision"
            value = etree.SubElement(ecuc_textual_param_value, 'VALUE').text = "PDUR_DIRECT"
            reference_values = etree.SubElement(ecuc_container_value_dest, 'REFERENCE-VALUES')
            ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduRef"
            value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/" + destination['TARGET'] + "_TO_CDD"
        #backward route
        for dest in route['TARGET']:
            ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
            # TRS.COMCONF.GEN.019(0)
            short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_' + route['SOURCE'] + "_" + dest['TARGET'] + "_FROM_CDD"
            definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
            subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
            # TRS.COMCONF.GEN.020(0)
            #src
            ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_" + route['SOURCE'] + "_" + dest['TARGET'] + "_FROM_CDD"
            definition = etree.SubElement(ecuc_container_value_src, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu"
            parameter_values = etree.SubElement(ecuc_container_value_src, 'PARAMETER-VALUES')
            ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
            definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSourcePduHandleId"
            value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index_id)
            index_id = index_id + 1
            reference_values = etree.SubElement(ecuc_container_value_src, 'REFERENCE-VALUES')
            ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSrcPduRef"
            value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/" + dest['TARGET'] + "_FROM_CDD"
            #dest
            ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_" + route['SOURCE'] + "_" + dest['TARGET']
            definition = etree.SubElement(ecuc_container_value_dest, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu"
            parameter_values = etree.SubElement(ecuc_container_value_dest, 'PARAMETER-VALUES')
            ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
            definition = etree.SubElement(ecuc_textual_param_value, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduDataProvision"
            value = etree.SubElement(ecuc_textual_param_value, 'VALUE').text = "PDUR_DIRECT"
            reference_values = etree.SubElement(ecuc_container_value_dest, 'REFERENCE-VALUES')
            ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduRef"
            value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/" + dest['TARGET'] + "_" + str(dest['ID']) + str(dest['WAY'])

    network_list = []
    comment = etree.Comment("LinIf")
    subcontainer_route.append(comment)
    for nad in nads:
        if nad['CONFIG'] == "1.3":
            nad_network = re.search("LIN_VSM_\d", nad["NETWORK"])
            if nad_network.group(0) not in network_list:
                network_list.append(nad_network.group(0))
                ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.021(0)
                short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_LinIf_REQ_' + nad_network.group(0) + "_1P3"
                definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
                subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
                # TRS.COMCONF.GEN.022(0)
                # src
                ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_LinIf_REQ_" + nad_network.group(0) + "_1P3"
                definition = etree.SubElement(ecuc_container_value_src, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu"
                parameter_values = etree.SubElement(ecuc_container_value_src, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSourcePduHandleId"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index_id)
                index_id = index_id + 1
                reference_values = etree.SubElement(ecuc_container_value_src, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSrcPduRef"
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REQ_" + nad_network.group(0) + "_1P3_LinIf"
                # dest
                ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_LinIf_REQ_" + nad_network.group(0) + "_1P3"
                definition = etree.SubElement(ecuc_container_value_dest, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu"
                parameter_values = etree.SubElement(ecuc_container_value_dest, 'PARAMETER-VALUES')
                ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_textual_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduDataProvision"
                value = etree.SubElement(ecuc_textual_param_value, 'VALUE').text = "PDUR_DIRECT"
                reference_values = etree.SubElement(ecuc_container_value_dest, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduRef"
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/LinIf_REQ_" + nad_network.group(0) + "_1P3_EnGwCLD"
                # backwards route
                ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.023(0)
                short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_LinIf_REP_' + nad_network.group(0) + "_1P3"
                definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
                subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
                # TRS.COMCONF.GEN.024(0)
                # src
                ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_LinIf_REP_" + nad_network.group(0) + "_1P3"
                definition = etree.SubElement(ecuc_container_value_src, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu"
                parameter_values = etree.SubElement(ecuc_container_value_src, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSourcePduHandleId"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index_id)
                index_id = index_id + 1
                reference_values = etree.SubElement(ecuc_container_value_src, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSrcPduRef"
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/LinIf_REP_" + nad_network.group(0) + "_1P3_EnGwCLD"
                # dest
                ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_LinIf_REP_" + nad_network.group(0) + "_1P3"
                definition = etree.SubElement(ecuc_container_value_dest, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu"
                parameter_values = etree.SubElement(ecuc_container_value_dest, 'PARAMETER-VALUES')
                ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_textual_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduDataProvision"
                value = etree.SubElement(ecuc_textual_param_value, 'VALUE').text = "PDUR_DIRECT"
                reference_values = etree.SubElement(ecuc_container_value_dest, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduRef"
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REP_" + nad_network.group(0) + "_1P3_LinIf"

    for diag_tool in diag_tools:
        for nad in nads:
            # if nad['CONFIG'] == "2.1":
            #     comment = etree.Comment("CanTp")
            #     subcontainer_route.append(comment)
            #     ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
            #     # TRS.COMCONF.GEN.033(0)
            #     short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_CanTp_REQ_' + diag_tool + "_" + nad['NETWORK']
            #     definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
            #     definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
            #     subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
            #     # TRS.COMCONF.GEN.034(0)
            #     # src
            #     ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
            #     short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_CanTp_REQ_" + diag_tool + "_" + nad['NETWORK']
            #     definition = etree.SubElement(ecuc_container_value_src, 'DEFINITION-REF')
            #     definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu"
            #     parameter_values = etree.SubElement(ecuc_container_value_src, 'PARAMETER-VALUES')
            #     ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
            #     definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
            #     definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSourcePduHandleId"
            #     value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index_id)
            #     index_id = index_id + 1
            #     reference_values = etree.SubElement(ecuc_container_value_src, 'REFERENCE-VALUES')
            #     ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            #     definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
            #     definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSrcPduRef"
            #     value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/CanTp_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_EnGwCLD"
            #     # dest
            #     ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
            #     short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_CanTp_REQ_" + diag_tool + "_" + nad['NETWORK']
            #     definition = etree.SubElement(ecuc_container_value_dest, 'DEFINITION-REF')
            #     definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu"
            #     parameter_values = etree.SubElement(ecuc_container_value_dest, 'PARAMETER-VALUES')
            #     ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
            #     definition = etree.SubElement(ecuc_textual_param_value, 'DEFINITION-REF')
            #     definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduDataProvision"
            #     value = etree.SubElement(ecuc_textual_param_value, 'VALUE').text = "PDUR_DIRECT"
            #     reference_values = etree.SubElement(ecuc_container_value_dest, 'REFERENCE-VALUES')
            #     ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            #     definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
            #     definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduRef"
            #     value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_CanTp"
            #     # backwards route
            #     ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
            #     # TRS.COMCONF.GEN.035(0)
            #     short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_CanTp_REP_' + diag_tool + "_" + nad['NETWORK']
            #     definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
            #     definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
            #     subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
            #     # TRS.COMCONF.GEN.036(0)
            #     # src
            #     ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
            #     short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_CanTp_REP_" + diag_tool + "_" + nad['NETWORK']
            #     definition = etree.SubElement(ecuc_container_value_src, 'DEFINITION-REF')
            #     definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu"
            #     parameter_values = etree.SubElement(ecuc_container_value_src, 'PARAMETER-VALUES')
            #     ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
            #     definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
            #     definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSourcePduHandleId"
            #     value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index_id)
            #     index_id = index_id + 1
            #     reference_values = etree.SubElement(ecuc_container_value_src, 'REFERENCE-VALUES')
            #     ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            #     definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
            #     definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSrcPduRef"
            #     value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REP_" + diag_tool + "_" + nad['NETWORK'] + "_CanTp"
            #     # dest
            #     ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
            #     short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_CanTp_REP_" + diag_tool + "_" + nad['NETWORK']
            #     definition = etree.SubElement(ecuc_container_value_dest, 'DEFINITION-REF')
            #     definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu"
            #     parameter_values = etree.SubElement(ecuc_container_value_dest, 'PARAMETER-VALUES')
            #     ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
            #     definition = etree.SubElement(ecuc_textual_param_value, 'DEFINITION-REF')
            #     definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduDataProvision"
            #     value = etree.SubElement(ecuc_textual_param_value, 'VALUE').text = "PDUR_DIRECT"
            #     reference_values = etree.SubElement(ecuc_container_value_dest, 'REFERENCE-VALUES')
            #     ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            #     definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
            #     definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduRef"
            #     value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/CanTp_REP_" + diag_tool + "_" + nad['NETWORK'] + "_EnGwCLD"
            if nad['CONFIG'] == "1.3":
                comment = etree.Comment("CanIf")
                subcontainer_route.append(comment)
                ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.029(0)
                short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_CanIf_REQ_' + diag_tool + "_" + nad['NETWORK']
                definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
                subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
                # TRS.COMCONF.GEN.030(0)
                # src
                ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_CanIf_REQ_" + diag_tool + "_" + nad['NETWORK']
                definition = etree.SubElement(ecuc_container_value_src, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu"
                parameter_values = etree.SubElement(ecuc_container_value_src, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSourcePduHandleId"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index_id)
                index_id = index_id + 1
                reference_values = etree.SubElement(ecuc_container_value_src, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSrcPduRef"
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/CanIf_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_EnGwCLD"
                # dest
                ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_CanIf_REQ_" + diag_tool + "_" + nad['NETWORK']
                definition = etree.SubElement(ecuc_container_value_dest, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu"
                parameter_values = etree.SubElement(ecuc_container_value_dest, 'PARAMETER-VALUES')
                ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_textual_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduDataProvision"
                value = etree.SubElement(ecuc_textual_param_value, 'VALUE').text = "PDUR_DIRECT"
                reference_values = etree.SubElement(ecuc_container_value_dest, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduRef"
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_CanIf"
                # backwards route
                ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.031(0)
                short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_CanIf_REP_' + diag_tool + "_" + nad['NETWORK']
                definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
                subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
                # TRS.COMCONF.GEN.032(0)
                # src
                ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_CanIf_REP_" + diag_tool + "_" + nad['NETWORK']
                definition = etree.SubElement(ecuc_container_value_src, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu"
                parameter_values = etree.SubElement(ecuc_container_value_src, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSourcePduHandleId"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index_id)
                index_id = index_id + 1
                reference_values = etree.SubElement(ecuc_container_value_src, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSrcPduRef"
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REP_" + diag_tool + "_" + nad['NETWORK'] + "_CanIf"
                # dest
                ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_CanIf_REP_" + diag_tool + "_" + nad['NETWORK']
                definition = etree.SubElement(ecuc_container_value_dest, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu"
                parameter_values = etree.SubElement(ecuc_container_value_dest, 'PARAMETER-VALUES')
                ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_textual_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduDataProvision"
                value = etree.SubElement(ecuc_textual_param_value, 'VALUE').text = "PDUR_DIRECT"
                reference_values = etree.SubElement(ecuc_container_value_dest, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduRef"
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/CanIf_REP_" + diag_tool + "_" + nad['NETWORK'] + "_EnGwCLD"
    comment = etree.Comment("LinTp")
    subcontainer_route.append(comment)
    # for nad in nads:
    #     if nad['CONFIG'] == "2.1":
    #         ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
    #         # TRS.COMCONF.GEN.025(0)
    #         short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_LinTp_REQ_' + nad['NETWORK']
    #         definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
    #         subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
    #         # TRS.COMCONF.GEN.026(0)
    #         # src
    #         ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
    #         short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_LinTp_REQ_" + nad['NETWORK']
    #         definition = etree.SubElement(ecuc_container_value_src, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu"
    #         parameter_values = etree.SubElement(ecuc_container_value_src, 'PARAMETER-VALUES')
    #         ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #         definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSourcePduHandleId"
    #         value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index_id)
    #         index_id = index_id + 1
    #         reference_values = etree.SubElement(ecuc_container_value_src, 'REFERENCE-VALUES')
    #         ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
    #         definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSrcPduRef"
    #         value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REQ_" + nad['NETWORK'] + "_LinTp"
    #         # dest
    #         ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
    #         short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_LinTp_REQ_" + nad['NETWORK']
    #         definition = etree.SubElement(ecuc_container_value_dest, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu"
    #         parameter_values = etree.SubElement(ecuc_container_value_dest, 'PARAMETER-VALUES')
    #         ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
    #         definition = etree.SubElement(ecuc_textual_param_value, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduDataProvision"
    #         value = etree.SubElement(ecuc_textual_param_value, 'VALUE').text = "PDUR_DIRECT"
    #         reference_values = etree.SubElement(ecuc_container_value_dest, 'REFERENCE-VALUES')
    #         ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
    #         definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduRef"
    #         value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/LinTp_REQ_" + nad['NETWORK'] + "_EnGwCLD"
    #         # backwards route
    #         ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
    #         # TRS.COMCONF.GEN.027(0)
    #         short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_LinTp_REP_' + nad['NETWORK']
    #         definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
    #         subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
    #         # TRS.COMCONF.GEN.028(0)
    #         # src
    #         ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
    #         short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_LinTp_REP_" + nad['NETWORK']
    #         definition = etree.SubElement(ecuc_container_value_src, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu"
    #         parameter_values = etree.SubElement(ecuc_container_value_src, 'PARAMETER-VALUES')
    #         ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #         definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSourcePduHandleId"
    #         value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index_id)
    #         index_id = index_id + 1
    #         reference_values = etree.SubElement(ecuc_container_value_src, 'REFERENCE-VALUES')
    #         ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
    #         definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRSrcPdu/PduRSrcPduRef"
    #         value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/LinTp_REP_" + nad['NETWORK'] + "_EnGwCLD"
    #         # dest
    #         ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
    #         short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_LinTp_REP_" + nad['NETWORK']
    #         definition = etree.SubElement(ecuc_container_value_dest, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu"
    #         parameter_values = etree.SubElement(ecuc_container_value_dest, 'PARAMETER-VALUES')
    #         ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
    #         definition = etree.SubElement(ecuc_textual_param_value, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduDataProvision"
    #         value = etree.SubElement(ecuc_textual_param_value, 'VALUE').text = "PDUR_DIRECT"
    #         reference_values = etree.SubElement(ecuc_container_value_dest, 'REFERENCE-VALUES')
    #         ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
    #         definition = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath/PduRDestPdu/PduRDestPduRef"
    #         value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REP_" + nad['NETWORK'] + "_LinTp"
    # generate data
    pretty_xml = prettify_xml(rootPduR)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/PduR.epc', encoding='UTF-8', xml_declaration=True, method="xml", doctype = "<!-- XML file generated by COM_Configurator-18 -->")
    return


def EnGw_config(file_list, output_path, logger):
    # create config
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    mappings = []
    can_frames = []
    diag_tools = []
    nads = []
    diag_pdu_types = []
    pdu_mappings = []
    can_connectors = []
    for file in file_list:
        if file.endswith('.arxml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            frames = root.findall(".//{http://autosar.org/schema/r4.0}PDU-TRIGGERING")
            for elem in frames:
                obj_elem = {}
                obj_elem['DEST'] = elem.find("{http://autosar.org/schema/r4.0}I-PDU-REF").attrib['DEST']
                obj_elem['PDU'] = elem.find("{http://autosar.org/schema/r4.0}I-PDU-REF").text.split("/")[-1]
                obj_elem['PDU-REF'] = elem.find("{http://autosar.org/schema/r4.0}I-PDU-REF").text
                obj_elem['NAME'] = elem.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                ports = elem.findall(".//{http://autosar.org/schema/r4.0}I-PDU-PORT-REF")
                port_list = []
                for port in ports:
                    port_list.append(port.text)
                obj_elem['PORTS'] = port_list
                obj_elem['CHANNEL'] = elem.getparent().getparent().getchildren()[0].text
                obj_elem['CLUSTER'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                obj_elem['PACKAGE'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                obj_elem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                can_frames.append(obj_elem)
            elements = root.findall(".//{http://autosar.org/schema/r4.0}DCM-I-PDU")
            for elem in elements:
                obj_elem = {}
                obj_elem['NAME'] = elem.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                obj_elem['SIZE'] = elem.find("{http://autosar.org/schema/r4.0}LENGTH").text
                obj_elem['TYPE'] = elem.find("{http://autosar.org/schema/r4.0}DIAG-PDU-TYPE").text
                diag_pdu_types.append(obj_elem)
            elements = root.findall(".//{http://autosar.org/schema/r4.0}I-PDU-MAPPING")
            for elem in elements:
                obj_elem = {}
                obj_elem['SOURCE'] = elem.find("{http://autosar.org/schema/r4.0}SOURCE-I-PDU-REF").text
                targets = elem.findall(".//{http://autosar.org/schema/r4.0}TARGET-I-PDU-REF")
                temp_list = []
                for target in targets:
                    temp_list.append(target.text)
                obj_elem['TARGET'] = temp_list
                pdu_mappings.append(obj_elem)
            elements = root.findall(".//{http://autosar.org/schema/r4.0}CAN-COMMUNICATION-CONNECTOR")
            for elem in elements:
                obj_elem = {}
                obj_elem['NAME'] = elem.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                obj_elem['INSTANCE'] = elem.getparent().getparent().getchildren()[0].text
                ports = elem.findall(".//{http://autosar.org/schema/r4.0}I-PDU-PORT")
                for port in ports:
                    if port.find("{http://autosar.org/schema/r4.0}COMMUNICATION-DIRECTION").text == "IN":
                        obj_elem['IN-PORT'] = port.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                    elif port.find("{http://autosar.org/schema/r4.0}COMMUNICATION-DIRECTION").text == "OUT":
                        obj_elem['OUT-PORT'] = port.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                can_connectors.append(obj_elem)
            elements = root.findall(".//{http://autosar.org/schema/r4.0}ETHERNET-COMMUNICATION-CONNECTOR")
            for elem in elements:
                obj_elem = {}
                obj_elem['NAME'] = elem.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                obj_elem['INSTANCE'] = elem.getparent().getparent().getchildren()[0].text
                ports = elem.findall(".//{http://autosar.org/schema/r4.0}I-PDU-PORT")
                for port in ports:
                    if port.find("{http://autosar.org/schema/r4.0}COMMUNICATION-DIRECTION").text == "IN":
                        obj_elem['IN-PORT'] = port.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                    elif port.find("{http://autosar.org/schema/r4.0}COMMUNICATION-DIRECTION").text == "OUT":
                        obj_elem['OUT-PORT'] = port.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                can_connectors.append(obj_elem)
            elements = root.findall(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-CONFIG")
            for elem in elements:
                obj_nad = {}
                obj_nad['NAME'] = elem.find(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-ECU-REF").text.split("/")[-2]
                obj_nad['NETWORK'] = elem.find(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-ECU-REF").text.split("/")[-1]
                obj_nad['ID'] = elem.find(".//{http://autosar.org/schema/r4.0}CONFIGURED-NAD").text
                obj_nad['LIN'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                obj_nad['CONFIG'] = elem.find(".//{http://autosar.org/schema/r4.0}PROTOCOL-VERSION").text
                nads.append(obj_nad)
        elif file.endswith('.xml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            mapping = root.findall(".//GATEWAY-MAPPING")
            for elem in mapping:
                obj_elem = {}
                obj_elem['SOURCE'] = elem.find(".//SOURCE-I-PDU-REF").text
                obj_elem['SOURCE-PDU'] = None
                obj_elem['SOURCE-CLUSTER'] = None
                obj_elem['TARGET'] = elem.find(".//TARGET-I-PDU-REF").text
                obj_elem['TARGET-PDU'] = None
                obj_elem['TARGET-CLUSTER'] = None
                obj_elem['TYPE'] = elem.find(".//CDD-TYPE").text
                mappings.append(obj_elem)
            diags = root.findall(".//CAN-DIAG-TOOL")
            for elem in diags:
                diag_tools.append(elem.find(".//CAN-CLUSTER-REF").text.split("/")[-1])

    for mapping in mappings:
        for frame in can_frames:
            if mapping['SOURCE'].split("/")[-1] == frame['NAME']:
                mapping['SOURCE-CLUSTER'] = frame['CLUSTER']
                mapping['SOURCE-PDU'] = frame['PDU']
            if mapping['TARGET'].split("/")[-1] == frame['NAME']:
                mapping['TARGET-CLUSTER'] = frame['CLUSTER']
                mapping['TARGET-PDU'] = frame['PDU']

    # create ouput file: EnGwCLD.epc
    rootCLD = etree.Element('AUTOSAR', {attr_qname: 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd'}, nsmap=NSMAP)
    packages = etree.SubElement(rootCLD, 'AR-PACKAGES')
    package = etree.SubElement(packages, 'AR-PACKAGE')
    short_name = etree.SubElement(package, 'SHORT-NAME').text = "EnGwCLD"
    elements = etree.SubElement(package, 'ELEMENTS')
    ecuc_module = etree.SubElement(elements, 'ECUC-MODULE-CONFIGURATION-VALUES')
    short_name = etree.SubElement(ecuc_module, 'SHORT-NAME').text = "EnGwCLD"
    definition = etree.SubElement(ecuc_module, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-MODULE-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCLD"
    description = etree.SubElement(ecuc_module, 'IMPLEMENTATION-CONFIG-VARIANT').text = "VARIANT-PRE-COMPILE"
    containers = etree.SubElement(ecuc_module, 'CONTAINERS')
    # Create CddComStackContribution section
    ecuc_container_master = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
    short_name = etree.SubElement(ecuc_container_master, 'SHORT-NAME').text = "CddComStackContribution"
    definition = etree.SubElement(ecuc_container_master, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution"
    subcontainer = etree.SubElement(ecuc_container_master, 'SUB-CONTAINERS')
    ecuc_container = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    # TRS.COMCONF.GEN.0166(0)
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddPduRUpperLayerContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution"
    subcontainers_CDD = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    index = 0
    network_list = []
    for nad in nads:
        if nad['CONFIG'] == "1.3":
            nad_network = re.search("LIN_VSM_\d", nad["NETWORK"])
            if nad_network.group(0) not in network_list:
                network_list.append(nad_network.group(0))
                # REQ part
                comment = etree.Comment("LinIf")
                subcontainers_CDD.append(comment)
                ecuc_container_value = etree.SubElement(subcontainers_CDD, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0167(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerRxPdu_REP_" + nad_network.group(0) + "_1P3"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerHandleId"
                # TRS.COMCONF.GEN.0168(0)
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                #index = index + 1
                textual_2 = etree.SubElement(parameter_values, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_2 = etree.SubElement(textual_2, "DEFINITION-REF")
                definition_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_2.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRApiType"
                value_2 = etree.SubElement(textual_2, "VALUE").text = "IF"
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REP_" + nad_network.group(0) + "_1P3_LinIf"
                # REP part
                ecuc_container_value = etree.SubElement(subcontainers_CDD, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0169(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerTxPdu_REQ_" + nad_network.group(0) + "_1P3"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerHandleId"
                # TRS.COMCONF.GEN.0170(0)
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                index = index + 1
                textual_2 = etree.SubElement(parameter_values, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_2 = etree.SubElement(textual_2, "DEFINITION-REF")
                definition_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_2.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRApiType"
                value_2 = etree.SubElement(textual_2, "VALUE").text = "IF"
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REQ_" + nad_network.group(0) + "_1P3_LinIf"
    # for nad in nads:
    #     if nad['CONFIG'] == "2.1":
    #         # REQ part
    #         comment = etree.Comment("LinTp")
    #         subcontainers_CDD.append(comment)
    #         ecuc_container_value = etree.SubElement(subcontainers_CDD, 'ECUC-CONTAINER-VALUE')
    #         # TRS.COMCONF.GEN.0171(0)
    #         short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerRxPdu_REP_" + nad['NETWORK'] + "_2P1"
    #         definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #         definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu"
    #         parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #         ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #         definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #         definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerHandleId"
    #         # TRS.COMCONF.GEN.0172(0)
    #         value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
    #         #index = index + 1
    #         textual_2 = etree.SubElement(parameter_values, "ECUC-TEXTUAL-PARAM-VALUE")
    #         definition_2 = etree.SubElement(textual_2, "DEFINITION-REF")
    #         definition_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
    #         definition_2.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRApiType"
    #         value_2 = etree.SubElement(textual_2, "VALUE").text = "TP"
    #         reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
    #         ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
    #         definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
    #         definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerPduRef"
    #         value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
    #         value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
    #         value_ref.text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REP_" + nad['NETWORK'] + "_LinTp"
    #         # REP part
    #         ecuc_container_value = etree.SubElement(subcontainers_CDD, 'ECUC-CONTAINER-VALUE')
    #         # TRS.COMCONF.GEN.0173(0)
    #         short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerTxPdu_REQ_" + nad['NETWORK'] + "_2P1"
    #         definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #         definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu"
    #         parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #         ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #         definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #         definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerHandleId"
    #         # TRS.COMCONF.GEN.0174(0)
    #         value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
    #         index = index + 1
    #         textual_2 = etree.SubElement(parameter_values, "ECUC-TEXTUAL-PARAM-VALUE")
    #         definition_2 = etree.SubElement(textual_2, "DEFINITION-REF")
    #         definition_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
    #         definition_2.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRApiType"
    #         value_2 = etree.SubElement(textual_2, "VALUE").text = "TP"
    #         reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
    #         ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
    #         definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
    #         definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerPduRef"
    #         value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
    #         value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
    #         value_ref.text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REQ_" + nad['NETWORK'] + "_LinTp"
    for diag_tool in diag_tools:
        for nad in nads:
            nad_network = re.search("LIN_VSM_\d", nad["NETWORK"])
            # if nad['CONFIG'] == "2.1":
            #     # REQ part
            #     comment = etree.Comment("CanTp")
            #     subcontainers_CDD.append(comment)
            #     ecuc_container_value = etree.SubElement(subcontainers_CDD, 'ECUC-CONTAINER-VALUE')
            #     # TRS.COMCONF.GEN.0175(0)
            #     short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerRxPdu_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_2P1"
            #     definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu"
            #     parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
            #     ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
            #     definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerHandleId"
            #     # TRS.COMCONF.GEN.0176(0)
            #     value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
            #     #index = index + 1
            #     textual_2 = etree.SubElement(parameter_values, "ECUC-TEXTUAL-PARAM-VALUE")
            #     definition_2 = etree.SubElement(textual_2, "DEFINITION-REF")
            #     definition_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            #     definition_2.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRApiType"
            #     value_2 = etree.SubElement(textual_2, "VALUE").text = "TP"
            #     reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
            #     ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            #     definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerPduRef"
            #     value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
            #     value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            #     value_ref.text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_CanTp"
            #     # REP part
            #     ecuc_container_value = etree.SubElement(subcontainers_CDD, 'ECUC-CONTAINER-VALUE')
            #     # TRS.COMCONF.GEN.0177(0)
            #     short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerTxPdu_REP_" + diag_tool + "_" + nad['NETWORK'] + "_2P1"
            #     definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu"
            #     parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
            #     ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
            #     definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerHandleId"
            #     # TRS.COMCONF.GEN.0178(0)
            #     value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
            #     index = index + 1
            #     textual_2 = etree.SubElement(parameter_values, "ECUC-TEXTUAL-PARAM-VALUE")
            #     definition_2 = etree.SubElement(textual_2, "DEFINITION-REF")
            #     definition_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            #     definition_2.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRApiType"
            #     value_2 = etree.SubElement(textual_2, "VALUE").text = "TP"
            #     reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
            #     ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            #     definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerPduRef"
            #     value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
            #     value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            #     value_ref.text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REP_" + diag_tool + "_" + nad['NETWORK'] + "_CanTp"
            #     # RoutingPath backward
            #     ecuc_container_value = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
            #     # TRS.COMCONF.GEN.0179(0)
            #     short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "EnGwCLDRoutingPath_REP_" + diag_tool + "_" + nad['NETWORK'] + "_2P1"
            #     definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDRoutingPath"
            #     reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
            #     ecuc_reference_src = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            #     definition_ref = etree.SubElement(ecuc_reference_src, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDRoutingPath/EnGwCLDSrcRef"
            #     value_ref = etree.SubElement(ecuc_reference_src, 'VALUE-REF')
            #     value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            #     # TRS.COMCONF.GEN.0180(0)
            #     value_ref.text = "/EnGwCLD/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/PduRUpperLayerRxPdu_REP_" + nad['NETWORK'] + "_2P1"
            #     ecuc_reference_dest = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            #     definition_ref = etree.SubElement(ecuc_reference_dest, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDRoutingPath/EnGwCLDDestRef"
            #     value_ref = etree.SubElement(ecuc_reference_dest, 'VALUE-REF')
            #     value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            #     value_ref.text = "/EnGwCLD/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/PduRUpperLayerTxPdu_REP_" + diag_tool + "_" + nad['NETWORK'] + "_2P1"
            #     # RoutingPath forward
            #     ecuc_container_value = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
            #     # TRS.COMCONF.GEN.0181(0)
            #     short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "EnGwCLDRoutingPath_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_2P1"
            #     definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDRoutingPath"
            #     reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
            #     ecuc_reference_src = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            #     definition_ref = etree.SubElement(ecuc_reference_src, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDRoutingPath/EnGwCLDSrcRef"
            #     value_ref = etree.SubElement(ecuc_reference_src, 'VALUE-REF')
            #     value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            #     # TRS.COMCONF.GEN.0182(0)
            #     value_ref.text = "/EnGwCLD/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/PduRUpperLayerRxPdu_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_2P1"
            #     ecuc_reference_dest = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            #     definition_ref = etree.SubElement(ecuc_reference_dest, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDRoutingPath/EnGwCLDDestRef"
            #     value_ref = etree.SubElement(ecuc_reference_dest, 'VALUE-REF')
            #     value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            #     value_ref.text = "/EnGwCLD/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/PduRUpperLayerTxPdu_REQ_" + nad['NETWORK'] + "_2P1"
            #     # ReqRep
            #     ecuc_container_value = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
            #     # TRS.COMCONF.GEN.0183(0)
            #     short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "EnGwCLDReqRepConfiguration_" + diag_tool + "_" + nad['NETWORK'] + "_2P1"
            #     definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDReqRepConfiguration"
            #     reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
            #     ecuc_reference_src = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            #     definition_ref = etree.SubElement(ecuc_reference_src, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDReqRepConfiguration/EnGwCLDReqRef"
            #     value_ref = etree.SubElement(ecuc_reference_src, 'VALUE-REF')
            #     value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            #     # TRS.COMCONF.GEN.0184(0)
            #     value_ref.text = "/EnGwCLD/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/PduRUpperLayerRxPdu_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_2P1"
            #     ecuc_reference_dest = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            #     definition_ref = etree.SubElement(ecuc_reference_dest, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDReqRepConfiguration/EnGwCLDRepRef"
            #     value_ref = etree.SubElement(ecuc_reference_dest, 'VALUE-REF')
            #     value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            #     value_ref.text = "/EnGwCLD/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/PduRUpperLayerTxPdu_REP_" + diag_tool + "_" + nad['NETWORK'] + "_2P1"
            #     ecuc_reference_dest = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            #     definition_ref = etree.SubElement(ecuc_reference_dest, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDReqRepConfiguration/EnGwCLDCanBufferRef"
            #     value_ref = etree.SubElement(ecuc_reference_dest, 'VALUE-REF')
            #     value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            #     value_ref.text = "/EnGwCLD/EnGwCLD/EnGwCLDBuffer/cEnGw_GW_CAN_" + diag_tool + "_INDEX"
            #     ecuc_reference_dest = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            #     definition_ref = etree.SubElement(ecuc_reference_dest, 'DEFINITION-REF')
            #     definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDReqRepConfiguration/EnGwCLDLinBufferRef"
            #     value_ref = etree.SubElement(ecuc_reference_dest, 'VALUE-REF')
            #     value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            #     value_ref.text = "/EnGwCLD/EnGwCLD/EnGwCLDBuffer/cEnGw_" + nad_network.group(0) + "_INDEX"
            if nad['CONFIG'] == "1.3":
                # REQ part
                comment = etree.Comment("CanIf")
                subcontainers_CDD.append(comment)
                ecuc_container_value = etree.SubElement(subcontainers_CDD, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0185(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerRxPdu_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_1P3"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerHandleId"
                # TRS.COMCONF.GEN.0186(0)
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                #index = index + 1
                textual_2 = etree.SubElement(parameter_values, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_2 = etree.SubElement(textual_2, "DEFINITION-REF")
                definition_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_2.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRApiType"
                value_2 = etree.SubElement(textual_2, "VALUE").text = "IF"
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_CanIf"
                # REP part
                ecuc_container_value = etree.SubElement(subcontainers_CDD, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0187(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerTxPdu_REP_" + diag_tool + "_" + nad['NETWORK'] + "_1P3"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerHandleId"
                # TRS.COMCONF.GEN.0188(0)
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                index = index + 1
                textual_2 = etree.SubElement(parameter_values, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_2 = etree.SubElement(textual_2, "DEFINITION-REF")
                definition_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_2.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRApiType"
                value_2 = etree.SubElement(textual_2, "VALUE").text = "IF"
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/EnGwCLD_REP_" + diag_tool + "_" + nad['NETWORK'] + "_CanIf"
                # RoutingPath backward
                ecuc_container_value = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0189(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "EnGwCLDRoutingPath_REP_" + diag_tool + "_" + nad['NETWORK'] + "_1P3"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDRoutingPath"
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_src = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_src, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDRoutingPath/EnGwCLDSrcRef"
                value_ref = etree.SubElement(ecuc_reference_src, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                # TRS.COMCONF.GEN.0190(0)
                value_ref.text = "/EnGwCLD/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/PduRUpperLayerRxPdu_REP_" + nad_network.group(0) + "_1P3"
                ecuc_reference_dest = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_dest, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDRoutingPath/EnGwCLDDestRef"
                value_ref = etree.SubElement(ecuc_reference_dest, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EnGwCLD/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/PduRUpperLayerTxPdu_REP_" + diag_tool + "_" + nad['NETWORK'] + "_1P3"
                # RoutingPath forward
                ecuc_container_value = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0191(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "EnGwCLDRoutingPath_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_1P3"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDRoutingPath"
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_src = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_src, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDRoutingPath/EnGwCLDSrcRef"
                value_ref = etree.SubElement(ecuc_reference_src, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                # TRS.COMCONF.GEN.0192(0)
                value_ref.text = "/EnGwCLD/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/PduRUpperLayerRxPdu_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_1P3"
                ecuc_reference_dest = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_dest, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDRoutingPath/EnGwCLDDestRef"
                value_ref = etree.SubElement(ecuc_reference_dest, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EnGwCLD/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/PduRUpperLayerTxPdu_REQ_" + nad_network.group(0) + "_1P3"
                # ReqRep
                ecuc_container_value = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0193(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "EnGwCLDReqRepConfiguration_" + diag_tool + "_" + nad['NETWORK'] + "_1P3"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDReqRepConfiguration"
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_src = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_src, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDReqRepConfiguration/EnGwCLDReqRef"
                value_ref = etree.SubElement(ecuc_reference_src, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                # TRS.COMCONF.GEN.0194(0)
                value_ref.text = "/EnGwCLD/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/PduRUpperLayerRxPdu_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_1P3"
                ecuc_reference_dest = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_dest, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDReqRepConfiguration/EnGwCLDRepRef"
                value_ref = etree.SubElement(ecuc_reference_dest, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EnGwCLD/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/PduRUpperLayerTxPdu_REP_" + diag_tool + "_" + nad['NETWORK'] + "_1P3"
                ecuc_reference_dest = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_dest, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDReqRepConfiguration/EnGwCLDCanBufferRef"
                value_ref = etree.SubElement(ecuc_reference_dest, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EnGwCLD/EnGwCLD/EnGwCLDBuffer/cEnGw_GW_CAN_" + diag_tool + "_INDEX"
                ecuc_reference_dest = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_dest, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDReqRepConfiguration/EnGwCLDLinBufferRef"
                value_ref = etree.SubElement(ecuc_reference_dest, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EnGwCLD/EnGwCLD/EnGwCLDBuffer/cEnGw_" + nad_network.group(0) + "_INDEX"

    # fill buffer section
    network_list = []
    ecuc_container_master = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
    short_name = etree.SubElement(ecuc_container_master, 'SHORT-NAME').text = "EnGwCLDBuffer"
    definition = etree.SubElement(ecuc_container_master, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDBuffer"
    subcontainer = etree.SubElement(ecuc_container_master, 'SUB-CONTAINERS')
    for diag_tool in diag_tools:
        ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
        # TRS.COMCONF.GEN.0196(0)
        short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "cEnGw_GW_CAN_" + diag_tool + "_INDEX"
        definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
        definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDBuffer/EnGwCLDCanBuffer"
    for nad in nads:
        nad_network = re.search("LIN_VSM_\d", nad["NETWORK"])
        if nad['CONFIG'] == "1.3":
            if nad_network.group(0) not in network_list:
                network_list.append(nad_network.group(0))
        # else:
        #     if nad_network.group(0) not in network_list:
        #         network_list.append(nad_network.group(0))
    for network in network_list:
        ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
        # TRS.COMCONF.GEN.0197(0)
        short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "cEnGw_" + network + "_INDEX"
        definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
        definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/EnGwCLDBuffer/EnGwCLDLinBuffer"


    pretty_xml = prettify_xml(rootCLD)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/EnGwCLD.epc', encoding='UTF-8', xml_declaration=True, method="xml", doctype = "<!-- XML file generated by COM_Configurator-18 -->")

    # create output file: EnGwCCLD.epc
    rootCCLD = etree.Element('AUTOSAR', {attr_qname: 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd'}, nsmap=NSMAP)
    packages = etree.SubElement(rootCCLD, 'AR-PACKAGES')
    package = etree.SubElement(packages, 'AR-PACKAGE')
    short_name = etree.SubElement(package, 'SHORT-NAME').text = "EnGwCCLD"
    elements = etree.SubElement(package, 'ELEMENTS')
    ecuc_module = etree.SubElement(elements, 'ECUC-MODULE-CONFIGURATION-VALUES')
    short_name = etree.SubElement(ecuc_module, 'SHORT-NAME').text = "EnGwCCLD"
    definition = etree.SubElement(ecuc_module, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-MODULE-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCCLD"
    description = etree.SubElement(ecuc_module, 'IMPLEMENTATION-CONFIG-VARIANT').text = "VARIANT-PRE-COMPILE"
    # implement TRS.COMCONF.GEN.006(1)
    containers = etree.SubElement(ecuc_module, 'CONTAINERS')
    ecuc_container = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddComStackContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution"
    subcontainer = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    ecuc_container = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    # TRS.COMCONF.GEN.0199(0)
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddPduRLowerLayerContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution"
    subcontainers = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    index = 0
    # TRS.COMCONF.GEN.0198(0)
    for mapping in mappings:
        found_source = False
        found_target = False
        for frame in can_frames:
            if mapping['SOURCE'] == "/" + frame['ROOT'] + "/" + frame['PACKAGE'] + "/" + frame['CLUSTER'] + "/" + frame['CHANNEL'] + "/" + frame['NAME']:
                found_source = True
            if mapping['TARGET'] == "/" + frame['ROOT'] + "/" + frame['PACKAGE'] + "/" + frame['CLUSTER'] + "/" + frame['CHANNEL'] + "/" + frame['NAME']:
                found_target = True
            if found_source and found_target and mapping['TYPE'] == "GW-LIN-UNCONNECTED":
                # REQ part
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0200(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRLowerLayerRxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu/CddPduRLowerLayerHandleId"
                # TRS.COMCONF.GEN.0201(0)
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu/CddPduRLowerLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                # REP part
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0202(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRLowerLayerTxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu/CddPduRLowerLayerHandleId"
                # TRS.COMCONF.GEN.0203(0)
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                index = index + 1
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu/CddPduRLowerLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
                # Routing path
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0205(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "RoutingPathCCLD_" + mapping['SOURCE-PDU'] + "_TO_" + mapping['TARGET-PDU']
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCLDRoutingPath"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_textual_param_value, "DEFINITION-REF")
                definition_ref.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCLDRoutingPath/EnGwAuthorizationCallout"
                # TRS.COMCONF.GEN.0206(0)
                value = etree.SubElement(ecuc_textual_param_value, 'VALUE').text = mapping['SOURCE-PDU'] + "_to_" + mapping['TARGET-PDU']
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCLDRoutingPath/EnGwCCLDSrcRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EnGwCCLD/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/PduRLowerLayerTxPdu_" + mapping['TARGET-PDU'] + "_TO_CDD"
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCLDRoutingPath/EnGwCCLDDestRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EnGwCCLD/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/PduRLowerLayerRxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                break
    # generate data
    pretty_xml = prettify_xml(rootCCLD)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/EnGwCCLD.epc', encoding='UTF-8', xml_declaration=True, method="xml", doctype = "<!-- XML file generated by COM_Configurator-18 -->")

    # create output file: EnGwCCB.epc
    rootCCB = etree.Element('AUTOSAR', {attr_qname: 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd'}, nsmap=NSMAP)
    packages = etree.SubElement(rootCCB, 'AR-PACKAGES')
    package = etree.SubElement(packages, 'AR-PACKAGE')
    short_name = etree.SubElement(package, 'SHORT-NAME').text = "EnGwCCB"
    elements = etree.SubElement(package, 'ELEMENTS')
    ecuc_module = etree.SubElement(elements, 'ECUC-MODULE-CONFIGURATION-VALUES')
    short_name = etree.SubElement(ecuc_module, 'SHORT-NAME').text = "EnGwCCB"
    definition = etree.SubElement(ecuc_module, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-MODULE-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCCB"
    description = etree.SubElement(ecuc_module, 'IMPLEMENTATION-CONFIG-VARIANT').text = "VARIANT-PRE-COMPILE"
    # implement TRS.COMCONF.GEN.00B(1)
    containers = etree.SubElement(ecuc_module, 'CONTAINERS')
    ecuc_container = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddComStackContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution"
    subcontainer = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    ecuc_container = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    # TRS.COMCONF.GEN.0208(0)
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddPduRLowerLayerContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution"
    subcontainers = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    index = 0
    # TRS.COMCONF.GEN.0207(0)
    for mapping in mappings:
        found_source = False
        found_target = False
        for frame in can_frames:
            if mapping['SOURCE'] == "/" + frame['ROOT'] + "/" + frame['PACKAGE'] + "/" + frame['CLUSTER'] + "/" + frame['CHANNEL'] + "/" + frame['NAME']:
                found_source = True
            if mapping['TARGET'] == "/" + frame['ROOT'] + "/" + frame['PACKAGE'] + "/" + frame['CLUSTER'] + "/" + frame['CHANNEL'] + "/" + frame['NAME']:
                found_target = True
            if found_source and found_target and mapping['TYPE'] == "GW-REMOTE-DIAG":
                # REQ part
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0209(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRLowerLayerRxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu/CddPduRLowerLayerHandleId"
                # TRS.COMCONF.GEN.0210(0)
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu/CddPduRLowerLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                # REP part
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0211(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRLowerLayerTxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu/CddPduRLowerLayerHandleId"
                # TRS.COMCONF.GEN.0212(0)
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                index = index + 1
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu/CddPduRLowerLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
                # Routing path
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0214(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "RoutingPathCCB_" + mapping['SOURCE-PDU'] + "_TO_" + mapping['TARGET-PDU']
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCBRoutingPath"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_textual_param_value, "DEFINITION-REF")
                definition_ref.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCBRoutingPath/EnGwAuthorizationCallout"
                # TRS.COMCONF.GEN.0215(0)
                value = etree.SubElement(ecuc_textual_param_value, 'VALUE').text = mapping['SOURCE-PDU'] + "_to_" + mapping['TARGET-PDU']
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCBRoutingPath/EnGwCCBSrcRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EnGwCCB/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/PduRLowerLayerTxPdu_" + mapping['TARGET-PDU'] + "_TO_CDD"
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCBRoutingPath/EnGwCCBDestRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EnGwCCB/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/PduRLowerLayerRxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                break
    # generate data
    pretty_xml = prettify_xml(rootCCB)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/EnGwCCB.epc', encoding='UTF-8', xml_declaration=True, method="xml", doctype = "<!-- XML file generated by COM_Configurator-18 -->")

    # create output file: EnGwCCD.epc
    rootCCD = etree.Element('AUTOSAR', {attr_qname: 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd'}, nsmap=NSMAP)
    packages = etree.SubElement(rootCCD, 'AR-PACKAGES')
    package = etree.SubElement(packages, 'AR-PACKAGE')
    short_name = etree.SubElement(package, 'SHORT-NAME').text = "EnGwCCD"
    elements = etree.SubElement(package, 'ELEMENTS')
    ecuc_module = etree.SubElement(elements, 'ECUC-MODULE-CONFIGURATION-VALUES')
    short_name = etree.SubElement(ecuc_module, 'SHORT-NAME').text = "EnGwCCD"
    definition = etree.SubElement(ecuc_module, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-MODULE-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCCD"
    description = etree.SubElement(ecuc_module, 'IMPLEMENTATION-CONFIG-VARIANT').text = "VARIANT-PRE-COMPILE"
    containers = etree.SubElement(ecuc_module, 'CONTAINERS')
    ecuc_container = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddComStackContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution"
    subcontainer = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    ecuc_container = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    # TRS.COMCONF.GEN.0217(0)
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddPduRLowerLayerContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution"
    subcontainers = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    index = 0
    data_elements_to = []
    # TRS.COMCONF.GEN.0216(0)
    for mapping in mappings:
        found_source = False
        found_target = False
        target_cluster = ""
        source_cluster = ""
        for frame in can_frames:
            if mapping['SOURCE'] == "/" + frame['ROOT'] + "/" + frame['PACKAGE'] + "/" + frame['CLUSTER'] + "/" + frame['CHANNEL'] + "/" + frame['NAME']:
                found_source = True
                source_cluster = frame['CLUSTER']
            if mapping['TARGET'] == "/" + frame['ROOT'] + "/" + frame['PACKAGE'] + "/" + frame['CLUSTER'] + "/" + frame['CHANNEL'] + "/" + frame['NAME']:
                found_target = True
                target_cluster = frame['CLUSTER']
            if found_source and found_target and mapping['TYPE'] == "GW-CAN-DIAG":
                obj_sort = {}
                # TRS.COMCONF.GEN.0220(0)
                obj_sort['SHORT-NAME'] = "PduRLowerLayerTxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
                # TRS.COMCONF.GEN.0221(0)
                obj_sort['ID'] = 0
                obj_sort['REF'] = "/EcuC/EcuC/EcucPduCollection/" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
                obj_sort['CLUSTER'] = target_cluster
                data_elements_to.append(obj_sort)
                # Routing path
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0223(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "RoutingPathCCD_" + mapping['SOURCE-PDU'] + "_TO_" + mapping['TARGET-PDU']
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCDRoutingPath"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_textual_param_value, "DEFINITION-REF")
                definition_ref.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCDRoutingPath/EnGwAuthorizationCallout"
                # TRS.COMCONF.GEN.0224(0)
                value = etree.SubElement(ecuc_textual_param_value, 'VALUE').text = mapping['SOURCE-PDU'] + "_to_" + mapping['TARGET-PDU']
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCDRoutingPath/EnGwCCDSrcRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EnGwCCD/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/PduRLowerLayerTxPdu_" + mapping['TARGET-PDU'] + "_TO_CDD"
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCDRoutingPath/EnGwCCDDestRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EnGwCCLD/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/PduRLowerLayerRxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                break
    data_elements_to = sorted(data_elements_to, key=lambda x: x['CLUSTER'], reverse=True)
    index = 0
    for elem in data_elements_to:
        elem['ID'] = index
        index = index + 1
    data_elements_from = []
    for mapping in mappings:
        found_source = False
        found_target = False
        target_cluster = ""
        for frame in can_frames:
            if mapping['SOURCE'] == "/" + frame['ROOT'] + "/" + frame['PACKAGE'] + "/" + frame['CLUSTER'] + "/" + frame['CHANNEL'] + "/" + frame['NAME']:
                found_source = True
            if mapping['TARGET'] == "/" + frame['ROOT'] + "/" + frame['PACKAGE'] + "/" + frame['CLUSTER'] + "/" + frame['CHANNEL'] + "/" + frame['NAME']:
                found_target = True
                target_cluster = frame['CLUSTER']
            if found_source and found_target and mapping['TYPE'] == "GW-CAN-DIAG":
                obj_sort = {}
                # TRS.COMCONF.GEN.0218(0)
                obj_sort['SHORT-NAME'] = "PduRLowerLayerRxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                # TRS.COMCONF.GEN.0219(0)
                obj_sort['ID'] = 0
                obj_sort['REF'] = "/EcuC/EcuC/EcucPduCollection/" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                obj_sort['CLUSTER'] = target_cluster
                data_elements_from.append(obj_sort)
                break

    data_elements_from = sorted(data_elements_from, key=lambda x: x['CLUSTER'], reverse=True)
    index = 0
    for elem in data_elements_from:
        elem['ID'] = index
        index = index + 1
    data_elements = data_elements_to + data_elements_from
    for elem in data_elements:
        if "_TO_" in elem['SHORT-NAME']:
            ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = elem['SHORT-NAME']
            definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu"
            parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
            ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
            definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu/CddPduRLowerLayerHandleId"
            value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(elem['ID'])
            reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
            ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu/CddPduRLowerLayerPduRef"
            value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
            value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value_ref.text = elem['REF']
        else:
            ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = elem['SHORT-NAME']
            definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu"
            parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
            ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
            definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu/CddPduRLowerLayerHandleId"
            value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(elem['ID'])
            reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
            ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu/CddPduRLowerLayerPduRef"
            value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
            value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value_ref.text = elem['REF']
    ToDiagBegin = 0
    ToDiagEnd = 0
    ToHSBegin = 0
    ToHSEnd = 0
    ToFDBegin = 0
    ToFDEnd = int(len(data_elements)/2-1)
    FromDiagBegin = int(len(data_elements)/2)
    FromDiagEnd = 0
    FromHSBegin = int(len(data_elements)/2)
    FromHSEnd = 0
    FromFDBegin = 0
    FromFDEnd = len(data_elements)-1
    countHS = 0
    countFD = 0
    for elem in data_elements_to:
        if "HS" in elem['CLUSTER']:
            countHS = countHS + 1
        else:
            countFD = countFD + 1
    if countHS + countFD > 0:
        ToDiagEnd = int(len(data_elements) / 2 - 1)
        FromDiagEnd = len(data_elements) - 1
    if countHS > 0:
        ToHSEnd = ToHSBegin + countHS - 1
        FromHSEnd = FromHSBegin + countHS - 1
    else:
        ToHSEnd = ToHSBegin
        FromHSEnd = FromHSBegin
    if countFD >0:
        FromFDBegin = FromHSEnd + 1
        ToFDBegin = ToHSEnd + 1
        ToFDEnd = ToFDBegin + countFD - 1
        FromFDEnd = FromFDBegin + countFD - 1
    else:
        FromFDBegin = FromHSEnd
        ToFDBegin = ToHSEnd
        ToFDEnd = ToFDBegin
        FromFDEnd = FromFDBegin

    ecuc_container = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
    # TRS.COMCONF.GEN.0225(0)
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddDiagIndexing"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddDiagIndexing"
    parameter_values = etree.SubElement(ecuc_container, 'PARAMETER-VALUES')
    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddDiagIndexing/IndexToDiagBegin"
    # TRS.COMCONF.GEN.0226(0)
    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(ToDiagBegin)
    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddDiagIndexing/IndexToDiagEnd"
    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(ToDiagEnd)
    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddDiagIndexing/IndexToHSDiagBegin"
    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(ToHSBegin)
    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddDiagIndexing/IndexToHSDiagEnd"
    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(ToHSEnd)
    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddDiagIndexing/IndexToFDDiagBegin"
    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(ToFDBegin)
    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddDiagIndexing/IndexToFDDiagEnd"
    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(ToFDEnd)
    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddDiagIndexing/IndexFromDiagBegin"
    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(FromDiagBegin)
    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddDiagIndexing/IndexFromDiagEnd"
    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(FromDiagEnd)
    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddDiagIndexing/IndexFromHSDiagBegin"
    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(FromHSBegin)
    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddDiagIndexing/IndexFromHSDiagEnd"
    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(FromHSEnd)
    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddDiagIndexing/IndexFromFDDiagBegin"
    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(FromFDBegin)
    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddDiagIndexing/IndexFromFDDiagEnd"
    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(FromFDEnd)
    # generate data
    pretty_xml = prettify_xml(rootCCD)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/EnGwCCD.epc', encoding='UTF-8', xml_declaration=True, method="xml", doctype = "<!-- XML file generated by COM_Configurator-18 -->")

    # #EnGwCD
    # replist = []
    # reqlist = []
    # reqreplist = []
    # for triggering in can_frames:
    #     if triggering['DEST'] == "DCM-I-PDU":
    #         for pdu in diag_pdu_types:
    #             if triggering['PDU-REF'].split("/")[-1] == pdu['NAME'] and pdu['TYPE'] == 'DIAG-REQUEST':
    #                 reqlist.append(triggering)
    #             elif triggering['PDU-REF'].split("/")[-1] == pdu['NAME'] and pdu['TYPE'] == 'DIAG-RESPONSE':
    #                 replist.append(triggering)
    # for frame in reqlist:
    #     for port in frame['PORTS']:
    #         for connector in can_connectors:
    #             try:
    #                 if ((connector['INSTANCE'] + "/" + connector['NAME'] + "/" + connector['IN-PORT']) in port) and (connector['INSTANCE'] == 'VSM'):
    #                     for mapping in pdu_mappings:
    #                         if (frame['CLUSTER'] + "/" + frame['CHANNEL'] + "/" + frame['NAME']) in mapping['SOURCE']:
    #                             for pdu in mapping['TARGET']:
    #                                 obj_out = {}
    #                                 obj_out['REQUEST-IN-VSM'] = mapping['SOURCE']
    #                                 obj_out['REQPDU-IN-VSM'] = frame['PDU']
    #                                 obj_out['REQUEST-OUT-VSM'] = pdu
    #                                 for frame2 in reqlist:
    #                                     if pdu.split("/")[-1] == frame2['NAME']:
    #                                         for port2 in frame2['PORTS']:
    #                                             for connector2 in can_connectors:
    #                                                 if (connector2['INSTANCE'] + "/" + connector2['NAME'] + "/" + connector2['IN-PORT']) in port2:
    #                                                     obj_out['ECU-INSTANCE'] = connector2['INSTANCE']
    #                                                     for frame3 in replist:
    #                                                         for port2 in frame3['PORTS']:
    #                                                             if (connector2['INSTANCE'] + "/" + connector2['NAME'] + "/" + connector2['OUT-PORT']) in port2:
    #                                                                 obj_out['RESPONSE-IN-VSM'] = "/" + frame3['ROOT'] + "/" + frame3['PACKAGE'] + "/" + frame3['CLUSTER'] + "/" + frame3['CHANNEL'] + "/" + frame3['NAME']
    #                                                                 obj_out['REPPDU-IN-VSM'] = frame3['PDU']
    #                                                                 for mapping2 in pdu_mappings:
    #                                                                     if obj_out['RESPONSE-IN-VSM'] == mapping2['SOURCE']:
    #                                                                         for pdu2 in mapping2['TARGET']:
    #                                                                             for frame4 in replist:
    #                                                                                 if (frame4['CLUSTER'] + "/" + frame4['CHANNEL'] + "/" + frame4['NAME']) in pdu2:
    #                                                                                     for port3 in frame4['PORTS']:
    #                                                                                         if connector['OUT-PORT'] in port3:
    #                                                                                             obj_out['RESPONSE-OUT-VSM'] = "/" + frame4['ROOT'] + "/" + frame4['PACKAGE'] + "/" + frame4['CLUSTER'] + "/" + frame4['CHANNEL'] + "/" + frame4['NAME']
    #                                                                                             obj_out['CLUSTER-DIAG'] = frame4['CLUSTER']
    #                                                                                             reqreplist.append(obj_out)
    #             except KeyError as e:
    #                 logger.warning(str(e) + ": " + connector['NAME'])
    #                 #print(str(e) + ": " + connector['NAME'])
    #
    #
    # # create output file: EnGwCD.epc
    # rootCD = etree.Element('AUTOSAR', {attr_qname: 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd'}, nsmap=NSMAP)
    # packages = etree.SubElement(rootCD, 'AR-PACKAGES')
    # package = etree.SubElement(packages, 'AR-PACKAGE')
    # short_name = etree.SubElement(package, 'SHORT-NAME').text = "EnGwCanDiag"
    # elements = etree.SubElement(package, 'ELEMENTS')
    # ecuc_module = etree.SubElement(elements, 'ECUC-MODULE-CONFIGURATION-VALUES')
    # short_name = etree.SubElement(ecuc_module, 'SHORT-NAME').text = "EnGwCanDiag"
    # definition = etree.SubElement(ecuc_module, 'DEFINITION-REF')
    # definition.attrib['DEST'] = "ECUC-MODULE-DEF"
    # definition.text = "/TS_2018/EnGwCanDiag"
    # description = etree.SubElement(ecuc_module, 'IMPLEMENTATION-CONFIG-VARIANT').text = "VARIANT-PRE-COMPILE"
    # containers_general = etree.SubElement(ecuc_module, 'CONTAINERS')
    # container_cdd = etree.SubElement(containers_general, 'ECUC-CONTAINER-VALUE')
    # short_name = etree.SubElement(container_cdd, 'SHORT-NAME').text = "CddComStackContribution_0"
    # definition = etree.SubElement(container_cdd, 'DEFINITION-REF')
    # definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    # definition.text = "/TS_2018/EnGwCanDiag/CddComStackContribution"
    # subcontainers = etree.SubElement(container_cdd, 'SUB-CONTAINERS')
    # container = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
    # short_name = etree.SubElement(container, 'SHORT-NAME').text = "CddPduRUpperLayerContribution"
    # definition = etree.SubElement(container, 'DEFINITION-REF')
    # definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    # definition.text = "/TS_2018/EnGwCanDiag/CddComStackContribution/CddPduRUpperLayerContribution"
    # subcontainers_cdd = etree.SubElement(container, 'SUB-CONTAINERS')
    # container_diag = etree.SubElement(containers_general, 'ECUC-CONTAINER-VALUE')
    # short_name = etree.SubElement(container_diag, 'SHORT-NAME').text = "EnGwCanDiagReqRep"
    # definition = etree.SubElement(container_diag, 'DEFINITION-REF')
    # definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    # definition.text = "/TS_2018/EnGwCanDiag/EnGwCanDiagReqRepConfiguration"
    # subcontainers_diag = etree.SubElement(container_diag, 'SUB-CONTAINERS')
    # response_list = []
    # for group in reqreplist:
    #     # CddPduRUpperLayerRxPdu
    #     ecuc_container = etree.SubElement(subcontainers_cdd, 'ECUC-CONTAINER-VALUE')
    #     short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddPduRUpperLayerRxPdu_" + group['REQPDU-IN-VSM']
    #     definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    #     definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #     definition.text = "/TS_2018/EnGwCanDiag/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu"
    #     parameter_values = etree.SubElement(ecuc_container, 'PARAMETER-VALUES')
    #     textual_param = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
    #     definition = etree.SubElement(textual_param, 'DEFINITION-REF')
    #     definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
    #     definition.text = "/TS_2018/EnGwCanDiag/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRApiType"
    #     value = etree.SubElement(textual_param, 'VALUE').text = "TP"
    #     numerical_param = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #     definition = etree.SubElement(numerical_param, 'DEFINITION-REF')
    #     definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #     definition.text = "/TS_2018/EnGwCanDiag/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerHandleId"
    #     value = etree.SubElement(numerical_param, 'VALUE').text = "0"
    #     reference_values = etree.SubElement(ecuc_container, 'REFERENCE-VALUES')
    #     reference_param = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
    #     definition = etree.SubElement(reference_param, 'DEFINITION-REF')
    #     definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #     definition.text = "/TS_2018/EnGwCanDiag/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerPduRef"
    #     value = etree.SubElement(reference_param, 'VALUE-REF')
    #     value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
    #     value.text = "/EcuC/EcuC/EcucPduCollection/" + group['REQPDU-IN-VSM']
    #     #EnGwCanDiagReq
    #     ecuc_container = etree.SubElement(subcontainers_diag, 'ECUC-CONTAINER-VALUE')
    #     short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "EnGwCanDiagRep_" + group['CLUSTER-DIAG']
    #     definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    #     definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #     definition.text = "/TS_2018/EnGwCanDiag/EnGwCanDiagReqRepConfiguration/EnGwCanDiagReq"
    #     reference_values = etree.SubElement(ecuc_container, 'REFERENCE-VALUES')
    #     reference_param = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
    #     definition = etree.SubElement(reference_param, 'DEFINITION-REF')
    #     definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #     definition.text = "/TS_2018/EnGwCanDiag/EnGwCanDiagReqRepConfiguration/EnGwCanDiagReq/EnGwCanDiagReqRef"
    #     value = etree.SubElement(reference_param, 'VALUE-REF')
    #     value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
    #     value.text = "/EnGwCanDiag/EnGwCanDiag/CddComStackContribution_0/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu_" + group['REQPDU-IN-VSM']
    #     reference_param = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
    #     definition = etree.SubElement(reference_param, 'DEFINITION-REF')
    #     definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #     definition.text = "/TS_2018/EnGwCanDiag/EnGwCanDiagReqRepConfiguration/EnGwCanDiagReq/RoutingPathGroupRef"
    #     value = etree.SubElement(reference_param, 'VALUE-REF')
    #     value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
    #     value.text = "/PduR/PduR/PduRRoutingTables/RPG_DIAG_REP_" + group['CLUSTER-DIAG']
    #     if group['RESPONSE-IN-VSM'] not in response_list:
    #         response_list.append(group['RESPONSE-IN-VSM'])
    #         # CddPduRUpperLayerRxPdu
    #         ecuc_container = etree.SubElement(subcontainers_cdd, 'ECUC-CONTAINER-VALUE')
    #         short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddPduRUpperLayerRxPdu_" + group['REPPDU-IN-VSM']
    #         definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition.text = "/TS_2018/EnGwCanDiag/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu"
    #         parameter_values = etree.SubElement(ecuc_container, 'PARAMETER-VALUES')
    #         textual_param = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
    #         definition = etree.SubElement(textual_param, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
    #         definition.text = "/TS_2018/EnGwCanDiag/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRApiType"
    #         value = etree.SubElement(textual_param, 'VALUE').text = "TP"
    #         numerical_param = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #         definition = etree.SubElement(numerical_param, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition.text = "/TS_2018/EnGwCanDiag/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerHandleId"
    #         value = etree.SubElement(numerical_param, 'VALUE').text = "2"
    #         reference_values = etree.SubElement(ecuc_container, 'REFERENCE-VALUES')
    #         reference_param = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
    #         definition = etree.SubElement(reference_param, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #         definition.text = "/TS_2018/EnGwCanDiag/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerPduRef"
    #         value = etree.SubElement(reference_param, 'VALUE-REF')
    #         value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
    #         value.text = "/EcuC/EcuC/EcucPduCollection/" + group['REPPDU-IN-VSM']
    #         # CddPduRUpperLayerTxPdu
    #         ecuc_container = etree.SubElement(subcontainers_cdd, 'ECUC-CONTAINER-VALUE')
    #         short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddPduRUpperLayerTxPdu_" + group['REPPDU-IN-VSM'] + "_CDD_NAK78"
    #         definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition.text = "/TS_2018/EnGwCanDiag/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu"
    #         parameter_values = etree.SubElement(ecuc_container, 'PARAMETER-VALUES')
    #         textual_param = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
    #         definition = etree.SubElement(textual_param, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
    #         definition.text = "/TS_2018/EnGwCanDiag/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRApiType"
    #         value = etree.SubElement(textual_param, 'VALUE').text = "IF"
    #         numerical_param = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #         definition = etree.SubElement(numerical_param, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition.text = "/TS_2018/EnGwCanDiag/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerHandleId"
    #         value = etree.SubElement(numerical_param, 'VALUE').text = "0"
    #         reference_values = etree.SubElement(ecuc_container, 'REFERENCE-VALUES')
    #         reference_param = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
    #         definition = etree.SubElement(reference_param, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #         definition.text = "/TS_2018/EnGwCanDiag/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerPduRef"
    #         value = etree.SubElement(reference_param, 'VALUE-REF')
    #         value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
    #         value.text = "/EcuC/EcuC/EcucPduCollection/" + group['REPPDU-IN-VSM'] + "_CDD_NAK78"
    #         # EnGwCanDiagRep
    #         ecuc_container = etree.SubElement(subcontainers_diag, 'ECUC-CONTAINER-VALUE')
    #         short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "EnGwCanDiagRep"
    #         definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition.text = "/TS_2018/EnGwCanDiag/EnGwCanDiagReqRepConfiguration/EnGwCanDiagRep"
    #         reference_values = etree.SubElement(ecuc_container, 'REFERENCE-VALUES')
    #         reference_param = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
    #         definition = etree.SubElement(reference_param, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #         definition.text = "/TS_2018/EnGwCanDiag/EnGwCanDiagReqRepConfiguration/EnGwCanDiagRep/EnGwCanDiagRepRef"
    #         value = etree.SubElement(reference_param, 'VALUE-REF')
    #         value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
    #         value.text = "/EnGwCanDiag/EnGwCanDiag/CddComStackContribution_0/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu_" + group['REPPDU-IN-VSM']
    #         reference_param = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
    #         definition = etree.SubElement(reference_param, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #         definition.text = "/TS_2018/EnGwCanDiag/EnGwCanDiagReqRepConfiguration/EnGwCanDiagRep/PduRRoutingPathNak78Ref"
    #         value = etree.SubElement(reference_param, 'VALUE-REF')
    #         value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
    #         value.text = "/PduR/PduR/PduRRoutingTables/PduRRoutingTable/RPath_" + group['REPPDU-IN-VSM'] + "_NAK78"
    #
    # # generate data
    # pretty_xml = prettify_xml(rootCD)
    # output = etree.ElementTree(etree.fromstring(pretty_xml))
    # output.write(output_path + '/EnGwCD.epc', encoding='UTF-8', xml_declaration=True, method="xml", doctype = "<!-- XML file generated by COM_Configurator-18 -->")

    # create output file: EnGwFonc.epc
    rootFonc = etree.Element('AUTOSAR', {attr_qname: 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd'}, nsmap=NSMAP)
    packages = etree.SubElement(rootFonc, 'AR-PACKAGES')
    package = etree.SubElement(packages, 'AR-PACKAGE')
    short_name = etree.SubElement(package, 'SHORT-NAME').text = "EnGwFonc"
    elements = etree.SubElement(package, 'ELEMENTS')
    ecuc_module = etree.SubElement(elements, 'ECUC-MODULE-CONFIGURATION-VALUES')
    short_name = etree.SubElement(ecuc_module, 'SHORT-NAME').text = "EnGwFonc"
    definition = etree.SubElement(ecuc_module, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-MODULE-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwFonc"
    description = etree.SubElement(ecuc_module, 'IMPLEMENTATION-CONFIG-VARIANT').text = "VARIANT-PRE-COMPILE"
    # implement TRS.COMCONF.GEN.002(1)
    containers = etree.SubElement(ecuc_module, 'CONTAINERS')
    ecuc_container = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddComStackContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution"
    subcontainer = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    ecuc_container = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    # TRS.COMCONF.GEN.0228(0)
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddPduRLowerLayerContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution"
    subcontainers = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    index = 0
    # TRS.COMCONF.GEN.0227(0)
    for mapping in mappings:
        found_source = False
        found_target = False
        for frame in can_frames:
            if mapping['SOURCE'] == "/" + frame['ROOT'] + "/" + frame['PACKAGE'] + "/" + frame['CLUSTER'] + "/" + frame['CHANNEL'] + "/" + frame['NAME']:
                found_source = True
            if mapping['TARGET'] == "/" + frame['ROOT'] + "/" + frame['PACKAGE'] + "/" + frame['CLUSTER'] + "/" + frame['CHANNEL'] + "/" + frame['NAME']:
                found_target = True
            if found_source and found_target and mapping['TYPE'] == "GW-FILTERED":
                # REQ part
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0229(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRLowerLayerRxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu/CddPduRLowerLayerHandleId"
                # TRS.COMCONF.GEN.0230(0)
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu/CddPduRLowerLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                # REP part
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0231(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRLowerLayerTxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu/CddPduRLowerLayerHandleId"
                # TRS.COMCONF.GEN.0232(0)
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                index = index + 1
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu/CddPduRLowerLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
                # Routing path
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.0234(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "RoutingPathFonc_" + mapping['SOURCE-PDU'] + "_TO_" + mapping['TARGET-PDU']
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/EnGwFoncRoutingPath"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_textual_param_value, "DEFINITION-REF")
                definition_ref.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/EnGwFoncRoutingPath/EnGwAuthorizationCallout"
                # TRS.COMCONF.GEN.0235(0)
                value = etree.SubElement(ecuc_textual_param_value, 'VALUE').text = mapping['SOURCE-PDU'] + "_to_" + mapping['TARGET-PDU']
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/EnGwFoncRoutingPath/EnGwFoncSrcRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EnGwFonc/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/PduRLowerLayerTxPdu_" + mapping['TARGET-PDU'] + "_TO_CDD"
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/EnGwFoncRoutingPath/EnGwFoncDestRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EnGwFonc/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/PduRLowerLayerRxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                break
    # generate data
    pretty_xml = prettify_xml(rootFonc)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/EnGwFonc.epc', encoding='UTF-8', xml_declaration=True, method="xml", doctype = "<!-- XML file generated by COM_Configurator-18 -->")


def NeMo_script(file_list, output_path, logger):
    logger.info('======================================NeMo===========================================')
    error_no = 0
    warning_no = 0
    info_no = 0
    mappings = []
    callouts = []
    clusters = []
    triggerings = []
    directions = []
    try:
        for file in file_list:
            if file.endswith(".xml"):
                try:
                    check_if_xml_is_wellformed(file)
                    logger.info('The file: ' + file + ' is well-formed')
                    info_no = info_no + 1
                except Exception as e:
                    logger.error('The file: ' + file + ' is not well-formed: ' + str(e))
                    print('ERROR: The file: ' + file + ' is not well-formed: ' + str(e))
                    error_no = error_no + 1
                parser = etree.XMLParser(remove_comments=True)
                tree = objectify.parse(file, parser=parser)
                root = tree.getroot()
                callout = root.findall(".//SPECIFIC-CALLOUT")
                for elem in callout:
                    obj_elem = {}
                    obj_elem['NAME'] = elem.find("SHORT-NAME").text
                    obj_elem['CLUSTER'] = ""
                    obj_elem['GATEWAY'] = False
                    if elem.find("PDU-REF") is not None:
                        obj_elem['PDU'] = elem.find("PDU-REF").text
                    else:
                        obj_elem['PDU'] = ""
                    if elem.find("SYSTEM-SIGNAL-REF") is not None:
                        obj_elem['SIGNAL'] = elem.find("SYSTEM-SIGNAL-REF").text
                    else:
                        obj_elem['SIGNAL'] = ""
                    callouts.append(obj_elem)
                cluster_mapping = root.findall(".//CLUSTER-MAPPING")
                for mapping in cluster_mapping:
                    obj_elem = {}
                    obj_elem['SOURCE'] = mapping.find("SOURCE-CLUSTER").text.split("/")[-1]
                    obj_elem['TARGET'] = mapping.find("TARGET-CLUSTER").text.split("/")[-1]
                    clusters.append(obj_elem)
            elif file.endswith(".arxml"):
                try:
                    check_if_xml_is_wellformed(file)
                    logger.info('The file: ' + file + ' is well-formed')
                    info_no = info_no + 1
                except Exception as e:
                    logger.error('The file: ' + file + ' is not well-formed: ' + str(e))
                    print('ERROR: The file: ' + file + ' is not well-formed: ' + str(e))
                parser = etree.XMLParser(remove_comments=True)
                tree = objectify.parse(file, parser=parser)
                root = tree.getroot()
                mapping = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-TO-SIGNAL-MAPPING")
                for elem in mapping:
                    obj_elem = {}
                    obj_elem['DATA'] = elem
                    obj_elem['SIGNAL'] = elem.find(".//{http://autosar.org/schema/r4.0}SYSTEM-SIGNAL-REF").text
                    mappings.append(obj_elem)
                pdu_triggerings = root.findall(".//{http://autosar.org/schema/r4.0}PDU-TRIGGERING")
                for triggering in pdu_triggerings:
                    obj_elem = {}
                    obj_elem['NAME'] = triggering.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text
                    obj_elem['PDU'] = triggering.find(".//{http://autosar.org/schema/r4.0}I-PDU-REF").text
                    obj_elem['CLUSTER'] = triggering.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    # obj_elem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    triggerings.append(obj_elem)
                pdu_directions = root.findall(".//{http://autosar.org/schema/r4.0}I-SIGNAL-I-PDU-REF-CONDITIONAL")
                for pdu in pdu_directions:
                    obj_elem = {}
                    obj_elem['PDU'] = pdu.find(".//{http://autosar.org/schema/r4.0}I-SIGNAL-I-PDU-REF").text
                    obj_elem['DIRECTION'] = pdu.getparent().getparent().getchildren()[1].text
                    directions.append(obj_elem)
        if error_no != 0:
            print("There is at least one blocking error! Check the generated log.")
            print("\n stopped with: " + str(info_no) + " infos, " + str(warning_no) + " warnings, " + str(error_no) + " errors\n")
            try:
                os.remove(output_path + '/ComCallout.xml')
            except OSError:
                pass
            sys.exit(1)
        # check that the callouts are mapped (there is a system mapping with the referenced signal from callout)
        for callout in callouts[:]:
            if callout['SIGNAL'] != "":
                found = False
                for mapping in mappings:
                    if mapping['SIGNAL'] == callout['SIGNAL']:
                        found = True
                    if found:
                        break
                if not found:
                    callout['SIGNAL'] = ""
        # check if the PDU is referenced in a gateway cluster
        for callout in callouts:
            for triggering in triggerings:
                if callout['PDU'] == triggering['PDU']:
                    callout['CLUSTER'] = triggering['CLUSTER']
                    break
        for callout in callouts:
            for cluster in clusters:
                if callout['CLUSTER'] in [cluster['SOURCE'], cluster['TARGET']]:
                    for pdu in directions:
                        if callout['PDU'] == pdu['PDU'] and pdu['DIRECTION'] == "OUT":
                            callout['GATEWAY'] = True
        # create Scriptor script
        rootScript = etree.Element('Script')
        name = etree.SubElement(rootScript, 'Name').text = "ComCallout"
        description = etree.SubElement(rootScript, 'Decription').text = "Fix the parameters"
        expression = etree.SubElement(rootScript, 'Expression').text = "as:modconf('Com')[1]"
        operations = etree.SubElement(rootScript, 'Operations')
        for elem in callouts:
            if elem['SIGNAL'] != "":
                # TRS.COMCONF.GEN.005(0)
                # set ComTimeoutNotification
                operation = etree.SubElement(operations, 'Operation')
                operation.attrib['Type'] = "ForEach"
                expression = etree.SubElement(operation, 'Expression')
                expression.text = "as:modconf('Com')[1]/ComConfig/*/ComSignal/*[contains(@name,'" + elem['SIGNAL'].split("/")[-1] + "')]/ComTimeoutNotification"
                operations2 = etree.SubElement(operation, 'Operations')
                operation_enable = etree.SubElement(operations2, 'Operation')
                operation_enable.attrib['Type'] = "SetEnabled"
                expression_enable = etree.SubElement(operation_enable, 'Expression').text = "boolean(1)"
                operation2 = etree.SubElement(operations2, 'Operation')
                operation2.attrib['Type'] = "SetValue"
                expression2 = etree.SubElement(operation2, 'Expression').text = '"NmLib_COMCbkRxTOut_' + elem['SIGNAL'].split("/")[-1] + '"'
                # set ComNotification
                # operation = etree.SubElement(operations, 'Operation')
                # operation.attrib['Type'] = "ForEach"
                # expression = etree.SubElement(operation, 'Expression')
                # expression.text = "as:modconf('Com')[1]/ComConfig/*/ComSignal/*[contains(@name,'" + elem['SIGNAL'].split("/")[-1] + "')]/ComNotification"
                # operations2 = etree.SubElement(operation, 'Operations')
                # operation_enable = etree.SubElement(operations2, 'Operation')
                # operation_enable.attrib['Type'] = "SetEnabled"
                # expression_enable = etree.SubElement(operation_enable, 'Expression').text = "boolean(1)"
                # operation2 = etree.SubElement(operations2, 'Operation')
                # operation2.attrib['Type'] = "SetValue"
                # expression2 = etree.SubElement(operation2, 'Expression').text = '"NmLib_COMCbk_' + elem['SIGNAL'].split("/")[-1] + '"'
            if elem['PDU'] != "":
                # TRS.COMCONF.GEN.004(0)
                # set ComIPduCallout
                operation = etree.SubElement(operations, 'Operation')
                operation.attrib['Type'] = "ForEach"
                expression = etree.SubElement(operation, 'Expression')
                if not elem['GATEWAY']:
                    expression.text = "as:modconf('Com')[1]/ComConfig/*/ComIPdu/*[text:match(@name,'^PD" + elem['PDU'].split("/")[-1] + "_\d*+[RT]$')]/ComIPduCallout"
                else:
                    expression.text = "as:modconf('Com')[1]/ComConfig/*/ComIPdu/*[text:match(@name,'^PD" + elem['PDU'].split("/")[-1] + "_[RT]$')]/ComIPduCallout"
                operations2 = etree.SubElement(operation, 'Operations')
                operation_enable = etree.SubElement(operations2, 'Operation')
                operation_enable.attrib['Type'] = "SetEnabled"
                expression_enable = etree.SubElement(operation_enable, 'Expression').text = "boolean(1)"
                operation2 = etree.SubElement(operations2, 'Operation')
                operation2.attrib['Type'] = "SetValue"
                expression2 = etree.SubElement(operation2, 'Expression').text = '"NmLib_COMCallout_' + elem['PDU'].split("/")[-1] + '"'
        pretty_xml = prettify_xml(rootScript)
        tree = etree.ElementTree(etree.fromstring(pretty_xml))
        tree.write(output_path + "/ComCallout.xml", encoding="UTF-8", xml_declaration=True, method="xml", doctype = "<!-- XML file generated by COM_Configurator-18 -->")
        print("\nNeMo execution finished with: " + str(info_no) + " infos, " + str(warning_no) + " warnings, " + str(error_no) + " errors\n")
    except Exception as e:
        print("Unexpected error: " + str(e))
        print("\nExecution stopped with: " + str(info_no) + " infos, " + str(warning_no) + " warnings, " + str(error_no) + " errors\n")
        try:
            os.remove(output_path + '/ComCallout.xml')
        except OSError:
            pass
        sys.exit(1)


def EcuC_config(file_list, output_path, logger):
    # create config
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    mappings = []
    can_frames = []
    items = []
    diag_tools = []
    nads = []
    for file in file_list:
        if file.endswith('.arxml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            frames = root.findall(".//{http://autosar.org/schema/r4.0}PDU-TRIGGERING")
            for elem in frames:
                obj_elem = {}
                obj_elem['PDU'] = elem.find("{http://autosar.org/schema/r4.0}I-PDU-REF").text.split("/")[-1]
                obj_elem['NAME'] = elem.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                obj_elem['CHANNEL'] = elem.getparent().getparent().getchildren()[0].text
                obj_elem['CLUSTER'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                obj_elem['PACKAGE'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                obj_elem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                can_frames.append(obj_elem)
            elements = root.findall(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-CONFIG")
            for elem in elements:
                obj_nad = {}
                obj_nad['NAME'] = elem.find(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-ECU-REF").text.split("/")[-2]
                obj_nad['NETWORK'] = elem.find(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-ECU-REF").text.split("/")[-1]
                obj_nad['ID'] = elem.find(".//{http://autosar.org/schema/r4.0}CONFIGURED-NAD").text
                obj_nad['LIN'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                obj_nad['CONFIG'] = elem.find(".//{http://autosar.org/schema/r4.0}PROTOCOL-VERSION").text
                nads.append(obj_nad)
        elif file.endswith('.xml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            mapping = root.findall(".//GATEWAY-MAPPING")
            for elem in mapping:
                obj_elem = {}
                obj_elem['SOURCE'] = elem.find(".//SOURCE-I-PDU-REF").text
                obj_elem['SOURCE-PDU'] = None
                obj_elem['SOURCE-CLUSTER'] = None
                obj_elem['TARGET'] = elem.find(".//TARGET-I-PDU-REF").text
                obj_elem['TARGET-PDU'] = None
                obj_elem['TARGET-CLUSTER'] = None
                obj_elem['TYPE'] = elem.find(".//CDD-TYPE").text
                mappings.append(obj_elem)
            diags = root.findall(".//CAN-DIAG-TOOL")
            for elem in diags:
                diag_tools.append(elem.find(".//CAN-CLUSTER-REF").text.split("/")[-1])
    for mapping in mappings:
        for frame in can_frames:
            if mapping['SOURCE'].split("/")[-1] == frame['NAME']:
                mapping['SOURCE-CLUSTER'] = frame['CLUSTER']
                mapping['SOURCE-PDU'] = frame['PDU']
            if mapping['TARGET'].split("/")[-1] == frame['NAME']:
                mapping['TARGET-CLUSTER'] = frame['CLUSTER']
                mapping['TARGET-PDU'] = frame['PDU']
    for mapping in mappings[:]:
        obj_map = {}
        dest_list = []
        obj_map['SOURCE'] = mapping['SOURCE-PDU']
        obj_map['CLUSTER'] = mapping['SOURCE-CLUSTER']
        for dest in mappings[:]:
            if dest['SOURCE'] == mapping['SOURCE']:
                obj_dest = {}
                obj_dest['TARGET'] = dest['TARGET-PDU']
                obj_dest['CLUSTER'] = dest['TARGET-CLUSTER']
                obj_dest['TYPE'] = dest['TYPE']
                dest_list.append(obj_dest)
                mappings.remove(dest)
        if dest_list:
            obj_map['TARGET'] = dest_list
            items.append(obj_map)
    # TRS.COMCONF.GEN.040(0)
    for item in items[:]:
        if item['SOURCE'] is None:
            items.remove(item)
        else:
            for dest in item['TARGET']:
                if dest['TARGET'] is None:
                    items.remove(item)
    # create ouput file: EcuC.epc
    rootEcuC = etree.Element('AUTOSAR', {attr_qname: 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd'}, nsmap=NSMAP)
    packages = etree.SubElement(rootEcuC, 'AR-PACKAGES')
    package = etree.SubElement(packages, 'AR-PACKAGE')
    short_name = etree.SubElement(package, 'SHORT-NAME').text = "EcuC"
    elements = etree.SubElement(package, 'ELEMENTS')
    ecuc_module = etree.SubElement(elements, 'ECUC-MODULE-CONFIGURATION-VALUES')
    short_name = etree.SubElement(ecuc_module, 'SHORT-NAME').text = "EcuC"
    definition = etree.SubElement(ecuc_module, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-MODULE-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EcuC"
    description = etree.SubElement(ecuc_module, 'IMPLEMENTATION-CONFIG-VARIANT').text = "VARIANT-POST-BUILD"
    # implement TRS.COMCONF.GEN.001(1)
    containers = etree.SubElement(ecuc_module, 'CONTAINERS')
    ecuc_container = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "EcucPduCollection"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection"
    subcontainer = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    # CanTp<=>CanTp
    comment = etree.Comment("CanTp<=>CanTp")
    subcontainer.append(comment)
    # for diag_tool in diag_tools:
    #     for nad in nads:
    #         if nad['CONFIG'] == "2.1":
    #             # REQ part
    #             ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    #             # TRS.COMCONF.GEN.041(0)
    #             short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "EnGwCLD_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_CanTp"
    #             definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #             definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #             definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
    #             parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #             ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #             definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #             definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #             definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
    #             value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    #             ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    #             # TRS.COMCONF.GEN.042(0)
    #             short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanTp_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_EnGwCLD"
    #             definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #             definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #             definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
    #             parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #             ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #             definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #             definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #             definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
    #             value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    #             # REP part
    #             ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    #             # TRS.COMCONF.GEN.043(0)
    #             short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "EnGwCLD_REP_" + diag_tool + "_" + nad['NETWORK'] + "_CanTp"
    #             definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #             definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #             definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
    #             parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #             ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #             definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #             definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #             definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
    #             value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    #             ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    #             # TRS.COMCONF.GEN.044(0)
    #             short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanTp_REP_" + diag_tool + "_" + nad['NETWORK']  + "_EnGwCLD"
    #             definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #             definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #             definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
    #             parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #             ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #             definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #             definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #             definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
    #             value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    # LinTp<=>LinTp
    comment = etree.Comment("LinTp<=>LinTp")
    subcontainer.append(comment)
    # for nad in nads:
    #     if nad['CONFIG'] == "2.1":
    #         # REQ part
    #         ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    #         # TRS.COMCONF.GEN.045(0)
    #         short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "EnGwCLD_REQ_" + nad['NETWORK'] + "_LinTp"
    #         definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #         definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
    #         parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #         ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #         definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
    #         value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    #         ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    #         # TRS.COMCONF.GEN.046(0)
    #         short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "LinTp_REQ_" + nad['NETWORK'] + "_EnGwCLD"
    #         definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #         definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
    #         parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #         ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #         definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
    #         value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    #         # REP part
    #         ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    #         # TRS.COMCONF.GEN.047(0)
    #         short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "EnGwCLD_REP_" + nad['NETWORK'] + "_LinTp"
    #         definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #         definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
    #         parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #         ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #         definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
    #         value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    #         ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    #         # TRS.COMCONF.GEN.048(0)
    #         short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "LinTp_REP_" + nad['NETWORK'] + "_EnGwCLD"
    #         definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #         definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
    #         parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #         ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #         definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
    #         value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    # CanIf<=>CanTp
    comment = etree.Comment("CanIf<=>CanTp")
    subcontainer.append(comment)
    # for diag_tool in diag_tools:
    #     network_list = []
    #     for nad in nads:
    #         nad_network = re.search("LIN_VSM_\d", nad["LIN"])
    #         if nad['CONFIG'] == "2.1":
    #             if nad_network.group(0) not in network_list:
    #                 network_list.append(nad_network.group(0))
    #                 ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    #                 # TRS.COMCONF.GEN.057(0)
    #                 short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanIf_REQ_" + diag_tool + "_" + nad_network.group(0) + "_CanTp"
    #                 definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #                 definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #                 definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
    #                 parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #                 ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #                 definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #                 definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #                 definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
    #                 value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    #                 ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    #                 # TRS.COMCONF.GEN.058(0)
    #                 short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanTp_REP_" + diag_tool + "_" + nad_network.group(0) + "_CanIf"
    #                 definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #                 definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #                 definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
    #                 parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #                 ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #                 definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #                 definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #                 definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
    #                 value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    # for diag_tool in diag_tools:
    #     for nad in nads:
    #         nad_network = re.search("LIN_VSM_\d", nad["LIN"])
    #         if nad['CONFIG'] == "2.1":
    #             ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    #             # TRS.COMCONF.GEN.059(0)
    #             short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanTp_REP_" + diag_tool + "_" + nad_network.group(0) + "_" + nad['NAME'] + "_CanIf"
    #             definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #             definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #             definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
    #             parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #             ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #             definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #             definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #             definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
    #             value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    #             ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    #             # TRS.COMCONF.GEN.060(0)
    #             short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanTp_FC_REP_" + diag_tool + "_" + nad_network.group(0) + "_" + nad['NAME'] + "_CanIf"
    #             definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #             definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #             definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
    #             parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #             ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #             definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #             definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #             definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
    #             value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    # CanIf<=>CanIf
    comment = etree.Comment("CanIf<=>CanIf")
    subcontainer.append(comment)
    for diag_tool in diag_tools:
        for nad in nads:
            if nad['CONFIG'] == "1.3":
                # REQ part
                ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.049(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "EnGwCLD_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_CanIf"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
                ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.050(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanIf_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_EnGwCLD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
                # REP part
                ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.051(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "EnGwCLD_REP_" + diag_tool + "_" + nad['NETWORK'] + "_CanIf"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
                ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.052(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanIf_REP_" + diag_tool + "_" + nad['NETWORK'] + "_EnGwCLD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    # LinIf<=>LinIf
    comment = etree.Comment("LinIf<=>LinIf")
    subcontainer.append(comment)
    network_list = []
    for nad in nads:
        if nad['CONFIG'] == "1.3":
            nad_network = re.search("LIN_VSM_\d", nad['NETWORK'])
            if nad_network.group(0) not in network_list:
                network_list.append(nad_network.group(0))
                # REQ part
                ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.053(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "EnGwCLD_REQ_" + nad_network.group(0) + "_1P3_LinIf"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
                ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.054(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "LinIf_REQ_" + nad_network.group(0) + "_1P3_EnGwCLD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
                # REP part
                ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.055(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "EnGwCLD_REP_" + nad_network.group(0) + "_1P3_LinIf"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
                ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                # TRS.COMCONF.GEN.056(0)
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "LinIf_REP_" + nad_network.group(0) + "_1P3_EnGwCLD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    # PduR dependencies
    comment = etree.Comment("PduR dependencies")
    subcontainer.append(comment)
    for item in items:
        for destination in item['TARGET']:
            ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
            # TRS.COMCONF.GEN.061(0)
            short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = destination['TARGET'] + "_TO_CDD"
            definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
            parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
            ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
            definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
            value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
            ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
            # TRS.COMCONF.GEN.062(0)
            short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = destination['TARGET'] + "_FROM_CDD"
            definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
            parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
            ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
            definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
            value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    #only for testing
    # comment = etree.Comment("PduR dependencies")
    # subcontainer.append(comment)
    # for item in items:
    #     # to be deleted because the frame will be automatically imported
    #     ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    #     short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = item['SOURCE']
    #     definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #     definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #     definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
    #     parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #     ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #     definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #     definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #     definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
    #     value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
    #     for destination in item['TARGET']:
    #         # to be deleted because the frame will be automatically imported
    #         ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    #         short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = destination['TARGET']
    #         definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
    #         definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
    #         parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
    #         ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    #         definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    #         definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
    #         value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"

    # generate data
    pretty_xml = prettify_xml(rootEcuC)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/EcuC.epc', encoding='UTF-8', xml_declaration=True, method="xml", doctype = "<!-- XML file generated by COM_Configurator-18 -->")
    return


def CanIf_config(file_list, output_path, logger):
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    diag_tools = []
    nads = []
    lins = []
    lins21 = []
    for file in file_list:
        if file.endswith('.arxml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            elements = root.findall(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-CONFIG")
            for elem in elements:
                obj_nad = {}
                obj_nad['NAME'] = elem.find(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-ECU-REF").text.split("/")[-2]
                obj_nad['NETWORK'] = elem.find(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-ECU-REF").text.split("/")[-1]
                obj_nad['ID'] = elem.find(".//{http://autosar.org/schema/r4.0}CONFIGURED-NAD").text
                obj_nad['LIN'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                obj_nad['CONFIG'] = elem.find(".//{http://autosar.org/schema/r4.0}PROTOCOL-VERSION").text
                nads.append(obj_nad)
        elif file.endswith('.xml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            diags = root.findall(".//CAN-DIAG-TOOL")
            for elem in diags:
                diag_tools.append(elem.find(".//CAN-CLUSTER-REF").text.split("/")[-1])
            lins13 = root.findall(".//CAN-ID-LIN13")
            for elem in lins13:
                obj_lin = {}
                obj_lin['NAME'] = elem.find(".//LIN-SLAVE-REF").text.split("/")[-1]
                obj_lin['REQ-ID'] = elem.find(".//REQUEST-ID").text
                obj_lin['REP-ID'] = elem.find(".//RESPONSE-ID").text
                lins.append(obj_lin)
            # lins13 = root.findall(".//CAN-ID-LIN21")
            # for elem in lins13:
            #     obj_lin = {}
            #     obj_lin['NAME'] = elem.find(".//LIN-CLUSTER-REF").text.split("/")[-1]
            #     obj_lin['REQ-ID'] = elem.find(".//REQUEST-ID").text
            #     obj_lin['REP-ID'] = elem.find(".//RESPONSE-ID").text
            #     lins21.append(obj_lin)

    # create ouput file: CanIf.epc
    rootCanIf = etree.Element('AUTOSAR', {attr_qname: 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd'}, nsmap=NSMAP)
    packages = etree.SubElement(rootCanIf, 'AR-PACKAGES')
    package = etree.SubElement(packages, 'AR-PACKAGE')
    short_name = etree.SubElement(package, 'SHORT-NAME').text = "CanIf"
    elements = etree.SubElement(package, 'ELEMENTS')
    ecuc_module = etree.SubElement(elements, 'ECUC-MODULE-CONFIGURATION-VALUES')
    short_name = etree.SubElement(ecuc_module, 'SHORT-NAME').text = "CanIf"
    definition = etree.SubElement(ecuc_module, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-MODULE-DEF"
    definition.text = "/AUTOSAR/EcuDefs/CanIf"
    description = etree.SubElement(ecuc_module, 'IMPLEMENTATION-CONFIG-VARIANT').text = "VARIANT-POST-BUILD"
    containers = etree.SubElement(ecuc_module, "CONTAINERS")
    ecuc_container_value = etree.SubElement(containers, "ECUC-CONTAINER-VALUE")
    short_name = etree.SubElement(ecuc_container_value, "SHORT-NAME").text = "CanIfInitCfg"
    definition_config = etree.SubElement(ecuc_container_value, "DEFINITION-REF")
    definition_config.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition_config.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg"
    subcontainer_init = etree.SubElement(ecuc_container_value, "SUB-CONTAINERS")
    for diag_tool in diag_tools:
        for lin in lins21:
            # Rx part
            ecuc_container_value = etree.SubElement(subcontainer_init, "ECUC-CONTAINER-VALUE")
            # TRS.COMCONF.GEN.0116(0)
            short_name = etree.SubElement(ecuc_container_value, "SHORT-NAME").text = "CanIfRxPduCfg_REQ_" + diag_tool + "_" + lin['NAME']
            definition = etree.SubElement(ecuc_container_value, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg"
            parameters = etree.SubElement(ecuc_container_value, "PARAMETER-VALUES")
            numerical_0 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
            definition_0 = etree.SubElement(numerical_0, "DEFINITION-REF")
            definition_0.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_0.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg/CanIfRxPduCanId"
            # TRS.COMCONF.GEN.0117(0)
            value_0 = etree.SubElement(numerical_0, "VALUE").text = lin['REQ-ID']
            numerical_1 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
            definition_1 = etree.SubElement(numerical_1, "DEFINITION-REF")
            definition_1.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_1.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg/CanIfRxPduDlc"
            value_1 = etree.SubElement(numerical_1, "VALUE").text = "8"
            textual_1 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
            def_textual_1 = etree.SubElement(textual_1, "DEFINITION-REF")
            def_textual_1.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            def_textual_1.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg/CanIfRxPduCanIdType"
            val_textual_1 = etree.SubElement(textual_1, "VALUE").text = "STANDARD_NO_FD_CAN"
            textual_2 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
            def_textual_2 = etree.SubElement(textual_2, "DEFINITION-REF")
            def_textual_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            def_textual_2.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg/CanIfRxPduUserRxIndicationUL"
            val_textual_2 = etree.SubElement(textual_2, "VALUE").text = "CAN_TP"
            references = etree.SubElement(ecuc_container_value, "REFERENCE-VALUES")
            ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg/CanIfRxPduRef"
            value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            # TRS.COMCONF.GEN.0118(0)
            value.text = "/EcuC/EcuC/EcucPduCollection/CanIf_REQ_" + diag_tool + "_" + lin['NAME'] + "_CanTp"
            ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg/CanIfRxPduHrhIdRef"
            value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/CanIf/CanIf/CanIfInitCfg/CanIfInitHohCfg/HOH_0_VSM_" + diag_tool
            # Tx part
            ecuc_container_value = etree.SubElement(subcontainer_init, "ECUC-CONTAINER-VALUE")
            # TRS.COMCONF.GEN.0119(0)
            short_name = etree.SubElement(ecuc_container_value, "SHORT-NAME").text = "CanIfTxPduCfg_REP_" + diag_tool + "_" + lin['NAME']
            definition = etree.SubElement(ecuc_container_value, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg"
            parameters = etree.SubElement(ecuc_container_value, "PARAMETER-VALUES")
            numerical_0 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
            definition_0 = etree.SubElement(numerical_0, "DEFINITION-REF")
            definition_0.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_0.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduCanId"
            # TRS.COMCONF.GEN.0120(0)
            value_0 = etree.SubElement(numerical_0, "VALUE").text = lin['REP-ID']
            numerical_1 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
            definition_1 = etree.SubElement(numerical_1, "DEFINITION-REF")
            definition_1.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_1.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduDlc"
            value_1 = etree.SubElement(numerical_1, "VALUE").text = "8"
            textual_1 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
            def_textual_1 = etree.SubElement(textual_1, "DEFINITION-REF")
            def_textual_1.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            def_textual_1.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduCanIdType"
            val_textual_1 = etree.SubElement(textual_1, "VALUE").text = "STANDARD_CAN"
            references = etree.SubElement(ecuc_container_value, "REFERENCE-VALUES")
            ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduRef"
            value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            # TRS.COMCONF.GEN.0121(0)
            value.text = "/EcuC/EcuC/EcucPduCollection/CanTp_REP_" + diag_tool + "_" + lin['NAME'] + "_CanIf"
            ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduBufferRef"
            value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/CanIf/CanIf/CanIfInitCfg/HOH_2_VSM_" + diag_tool
    for diag_tool in diag_tools:
        for nad in nads:
            nad_network = re.search("LIN_VSM_\d", nad["LIN"])
            if nad['CONFIG'] == "1.3":
                # Rx N PDU
                ecuc_container_value = etree.SubElement(subcontainer_init, "ECUC-CONTAINER-VALUE")
                # TRS.COMCONF.GEN.0122(0)
                short_name = etree.SubElement(ecuc_container_value, "SHORT-NAME").text = "CanIfRxPduCfg_REQ_" + diag_tool + "_" + nad['NETWORK']
                definition = etree.SubElement(ecuc_container_value, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg"
                parameters = etree.SubElement(ecuc_container_value, "PARAMETER-VALUES")
                for lin in lins:
                    lin_network = re.search("LIN_VSM_\d", lin["NAME"])
                    # if lin_network.group(0) == nad_network.group(0) and nad['NAME'] in lin['NAME']:
                    if lin_network.group(0) == nad_network.group(0) and nad['NAME'] == lin['NAME'].replace("_" + lin_network.group(0), ''):
                        numerical_0 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_0 = etree.SubElement(numerical_0, "DEFINITION-REF")
                        definition_0.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                        definition_0.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg/CanIfRxPduCanId"
                        # TRS.COMCONF.GEN.0123(0)
                        value_0 = etree.SubElement(numerical_0, "VALUE").text = lin['REQ-ID']
                numerical_1 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                definition_1 = etree.SubElement(numerical_1, "DEFINITION-REF")
                definition_1.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_1.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg/CanIfRxPduDlc"
                value_1 = etree.SubElement(numerical_1, "VALUE").text = "8"
                textual_1 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                def_textual_1 = etree.SubElement(textual_1, "DEFINITION-REF")
                def_textual_1.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                def_textual_1.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg/CanIfRxPduCanIdType"
                val_textual_1 = etree.SubElement(textual_1, "VALUE").text = "STANDARD_NO_FD_CAN"
                textual_3 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                def_textual_3 = etree.SubElement(textual_3, "DEFINITION-REF")
                def_textual_3.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                def_textual_3.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg/CanIfRxPduUserRxIndicationUL"
                val_textual_3 = etree.SubElement(textual_3, "VALUE").text = "PDUR"
                references = etree.SubElement(ecuc_container_value, "REFERENCE-VALUES")
                ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
                definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg/CanIfRxPduRef"
                value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
                value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                # TRS.COMCONF.GEN.0124(0)
                value.text = "/EcuC/EcuC/EcucPduCollection/CanIf_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_EnGwCLD"
                ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
                definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg/CanIfRxPduHrhIdRef"
                value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
                value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value.text = "/CanIf/CanIf/CanIfInitCfg/CanIfInitHohCfg/HOH_0_VSM_" + diag_tool
                # Tx N FC PDU
                ecuc_container_value = etree.SubElement(subcontainer_init, "ECUC-CONTAINER-VALUE")
                # TRS.COMCONF.GEN.0125(0)
                short_name = etree.SubElement(ecuc_container_value, "SHORT-NAME").text = "CanIfTxPduCfg_REP_" + diag_tool + "_" + nad['NETWORK']
                definition = etree.SubElement(ecuc_container_value, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg"
                parameters = etree.SubElement(ecuc_container_value, "PARAMETER-VALUES")
                for lin in lins:
                    lin_network = re.search("LIN_VSM_\d", lin["NAME"])
                    nad_network = re.search("LIN_VSM_\d", nad["LIN"])
                    #if lin_network.group(0) == nad_network.group(0) and nad['NAME'] in lin['NAME']:
                    if lin_network.group(0) == nad_network.group(0) and nad['NAME'] == lin['NAME'].replace('_' + lin_network.group(0), ""):
                        numerical_0 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_0 = etree.SubElement(numerical_0, "DEFINITION-REF")
                        definition_0.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                        definition_0.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduCanId"
                        # TRS.COMCONF.GEN.0126(0)
                        value_0 = etree.SubElement(numerical_0, "VALUE").text = lin['REP-ID']
                numerical_1 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                definition_1 = etree.SubElement(numerical_1, "DEFINITION-REF")
                definition_1.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_1.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduDlc"
                value_1 = etree.SubElement(numerical_1, "VALUE").text = "8"
                textual_1 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                def_textual_1 = etree.SubElement(textual_1, "DEFINITION-REF")
                def_textual_1.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                def_textual_1.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduCanIdType"
                val_textual_1 = etree.SubElement(textual_1, "VALUE").text = "STANDARD_CAN"
                textual_2 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                def_textual_2 = etree.SubElement(textual_2, "DEFINITION-REF")
                def_textual_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                def_textual_2.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduType"
                val_textual_2 = etree.SubElement(textual_2, "VALUE").text = "STATIC"
                textual_3 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                def_textual_3 = etree.SubElement(textual_3, "DEFINITION-REF")
                def_textual_3.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                def_textual_3.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduUserTxConfirmationUL"
                val_textual_3 = etree.SubElement(textual_3, "VALUE").text = "PDUR"
                references = etree.SubElement(ecuc_container_value, "REFERENCE-VALUES")
                ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
                definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduRef"
                value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
                value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                # TRS.COMCONF.GEN.0127(0)
                value.text = "/EcuC/EcuC/EcucPduCollection/CanIf_REP_" + diag_tool + "_" + nad['NETWORK'] + "_EnGwCLD"
                ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
                definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduBufferRef"
                value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
                value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value.text = "/CanIf/CanIf/CanIfInitCfg/HOH_2_VSM_" + diag_tool
            # else:
            #     # Tx N PDU
            #     ecuc_container_value = etree.SubElement(subcontainer_init, "ECUC-CONTAINER-VALUE")
            #     # TRS.COMCONF.GEN.0128(0)
            #     short_name = etree.SubElement(ecuc_container_value, "SHORT-NAME").text = "CanIfTxPduCfg_REP_" + diag_tool + "_" + nad_network.group(0) + "_" + nad['NAME']
            #     definition = etree.SubElement(ecuc_container_value, "DEFINITION-REF")
            #     definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg"
            #     parameters = etree.SubElement(ecuc_container_value, "PARAMETER-VALUES")
            #     for lin in lins21:
            #         lin_network = re.search("LIN_VSM_\d", lin["NAME"])
            #         nad_network = re.search("LIN_VSM_\d", nad["LIN"])
            #         if lin_network.group(0) == nad_network.group(0):
            #             numerical_0 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
            #             definition_0 = etree.SubElement(numerical_0, "DEFINITION-REF")
            #             definition_0.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #             definition_0.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduCanId"
            #             # TRS.COMCONF.GEN.0129(0)
            #             value_0 = etree.SubElement(numerical_0, "VALUE").text = lin['REP-ID']
            #     numerical_1 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
            #     definition_1 = etree.SubElement(numerical_1, "DEFINITION-REF")
            #     definition_1.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition_1.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduDlc"
            #     value_1 = etree.SubElement(numerical_1, "VALUE").text = "8"
            #     textual_1 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
            #     def_textual_1 = etree.SubElement(textual_1, "DEFINITION-REF")
            #     def_textual_1.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            #     def_textual_1.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduCanIdType"
            #     val_textual_1 = etree.SubElement(textual_1, "VALUE").text = "STANDARD_CAN"
            #     textual_2 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
            #     def_textual_2 = etree.SubElement(textual_2, "DEFINITION-REF")
            #     def_textual_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            #     def_textual_2.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduType"
            #     val_textual_2 = etree.SubElement(textual_2, "VALUE").text = "STATIC"
            #     textual_3 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
            #     def_textual_3 = etree.SubElement(textual_3, "DEFINITION-REF")
            #     def_textual_3.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            #     def_textual_3.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduUserTxConfirmationUL"
            #     val_textual_3 = etree.SubElement(textual_3, "VALUE").text = "CAN_TP"
            #     references = etree.SubElement(ecuc_container_value, "REFERENCE-VALUES")
            #     ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            #     definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
            #     definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduRef"
            #     value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
            #     value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            #     # TRS.COMCONF.GEN.0130(0)
            #     value.text = "/EcuC/EcuC/EcucPduCollection/CanTp_REP_" + diag_tool + "_" + nad_network.group(0) + "_" + nad['NAME'] + "_CanIf"
            #     ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            #     definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
            #     definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduBufferRef"
            #     value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
            #     value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            #     value.text = "/CanIf/CanIf/CanIfInitCfg/HOH_2_VSM_" + diag_tool
            #     # Tx N FC PDU
            #     ecuc_container_value = etree.SubElement(subcontainer_init, "ECUC-CONTAINER-VALUE")
            #     # TRS.COMCONF.GEN.0131(0)
            #     short_name = etree.SubElement(ecuc_container_value, "SHORT-NAME").text = "CanIfTxPduCfg_FC_REP_" + diag_tool + "_" + nad_network.group(0) + "_" + nad['NAME']
            #     definition = etree.SubElement(ecuc_container_value, "DEFINITION-REF")
            #     definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg"
            #     parameters = etree.SubElement(ecuc_container_value, "PARAMETER-VALUES")
            #     for lin in lins21:
            #         lin_network = re.search("LIN_VSM_\d", lin["NAME"])
            #         nad_network = re.search("LIN_VSM_\d", nad["LIN"])
            #         if lin_network.group(0) == nad_network.group(0):
            #             numerical_0 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
            #             definition_0 = etree.SubElement(numerical_0, "DEFINITION-REF")
            #             definition_0.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #             definition_0.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduCanId"
            #             # TRS.COMCONF.GEN.0132(0)
            #             value_0 = etree.SubElement(numerical_0, "VALUE").text = lin['REP-ID']
            #     numerical_1 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
            #     definition_1 = etree.SubElement(numerical_1, "DEFINITION-REF")
            #     definition_1.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            #     definition_1.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduDlc"
            #     value_1 = etree.SubElement(numerical_1, "VALUE").text = "8"
            #     textual_1 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
            #     def_textual_1 = etree.SubElement(textual_1, "DEFINITION-REF")
            #     def_textual_1.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            #     def_textual_1.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduCanIdType"
            #     val_textual_1 = etree.SubElement(textual_1, "VALUE").text = "STANDARD_CAN"
            #     textual_2 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
            #     def_textual_2 = etree.SubElement(textual_2, "DEFINITION-REF")
            #     def_textual_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            #     def_textual_2.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduType"
            #     val_textual_2 = etree.SubElement(textual_2, "VALUE").text = "STATIC"
            #     textual_3 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
            #     def_textual_3 = etree.SubElement(textual_3, "DEFINITION-REF")
            #     def_textual_3.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            #     def_textual_3.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduUserTxConfirmationUL"
            #     val_textual_3 = etree.SubElement(textual_3, "VALUE").text = "CAN_TP"
            #     references = etree.SubElement(ecuc_container_value, "REFERENCE-VALUES")
            #     ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            #     definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
            #     definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduRef"
            #     value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
            #     value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            #     # TRS.COMCONF.GEN.013(0)
            #     value.text = "/EcuC/EcuC/EcucPduCollection/CanTp_FC_REP_" + diag_tool + "_" + nad_network.group(0) + "_" + nad['NAME'] + "_CanIf"
            #     ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            #     definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
            #     definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            #     definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduBufferRef"
            #     value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
            #     value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            #     value.text = "/CanIf/CanIf/CanIfInitCfg/HOH_2_VSM_" + diag_tool
    # generate data
    pretty_xml = prettify_xml(rootCanIf)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/CanIf.epc', encoding='UTF-8', xml_declaration=True, method="xml", doctype="<!-- XML file generated by COM_Configurator-18 -->")
    return


def CanTp_config(file_list, output_path, logger):
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    diag_tools = []
    nads = []
    lins = []
    for file in file_list:
        if file.endswith('.arxml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            elements = root.findall(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-CONFIG")
            for elem in elements:
                obj_nad = {}
                obj_nad['NAME'] = elem.find(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-ECU-REF").text.split("/")[-2]
                obj_nad['NETWORK'] = elem.find(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-ECU-REF").text.split("/")[-1]
                obj_nad['ID'] = elem.find(".//{http://autosar.org/schema/r4.0}CONFIGURED-NAD").text
                obj_nad['LIN'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                obj_nad['CONFIG'] = elem.find(".//{http://autosar.org/schema/r4.0}PROTOCOL-VERSION").text
                nads.append(obj_nad)
        elif file.endswith('.xml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            diags = root.findall(".//CAN-DIAG-TOOL")
            for elem in diags:
                diag_tools.append(elem.find(".//CAN-CLUSTER-REF").text.split("/")[-1])
            # lins21 = root.findall(".//CAN-ID-LIN21")
            # for elem in lins21:
            #     obj_lin = {}
            #     obj_lin['NAME'] = elem.find(".//LIN-CLUSTER-REF").text.split("/")[-1]
            #     obj_lin['REQ-ID'] = elem.find(".//REQUEST-ID").text
            #     obj_lin['REP-ID'] = elem.find(".//RESPONSE-ID").text
            #     lins.append(obj_lin)

    # create ouput file: CanTp.epc
    rootCanTp = etree.Element('AUTOSAR', {attr_qname: 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd'}, nsmap=NSMAP)
    packages = etree.SubElement(rootCanTp, 'AR-PACKAGES')
    package = etree.SubElement(packages, 'AR-PACKAGE')
    short_name = etree.SubElement(package, 'SHORT-NAME').text = "CanTp"
    elements = etree.SubElement(package, 'ELEMENTS')
    ecuc_module = etree.SubElement(elements, 'ECUC-MODULE-CONFIGURATION-VALUES')
    short_name = etree.SubElement(ecuc_module, 'SHORT-NAME').text = "CanTp"
    definition = etree.SubElement(ecuc_module, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-MODULE-DEF"
    definition.text = "/AUTOSAR/EcuDefs/CanTp"
    description = etree.SubElement(ecuc_module, 'IMPLEMENTATION-CONFIG-VARIANT').text = "VARIANT-POST-BUILD"
    containers = etree.SubElement(ecuc_module, "CONTAINERS")
    ecuc_container_general = etree.SubElement(containers, "ECUC-CONTAINER-VALUE")
    short_name = etree.SubElement(ecuc_container_general, "SHORT-NAME").text = "CanTpGeneral"
    definition_config = etree.SubElement(ecuc_container_general, "DEFINITION-REF")
    definition_config.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition_config.text = "/AUTOSAR/EcuDefs/CanTp/CanTpGeneral"
    parameter_values = etree.SubElement(ecuc_container_general, "PARAMETER-VALUES")
    ecuc_num_1 = etree.SubElement(parameter_values, "ECUC-NUMERICAL-PARAM-VALUE")
    definition_ref = etree.SubElement(ecuc_num_1, "DEFINITION-REF")
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/CanTp/CanTpGeneral/CanTpPaddingByte"
    # TRS.COMCONF.GEN.097(0)
    value = etree.SubElement(ecuc_num_1, "VALUE").text = "255"
    ecuc_num_2 = etree.SubElement(parameter_values, "ECUC-NUMERICAL-PARAM-VALUE")
    definition_ref = etree.SubElement(ecuc_num_2, "DEFINITION-REF")
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/CanTp/CanTpGeneral/CanTpMaxTxNSdus"
    value = etree.SubElement(ecuc_num_2, "VALUE").text = "32767"
    ecuc_num_3 = etree.SubElement(parameter_values, "ECUC-NUMERICAL-PARAM-VALUE")
    definition_ref = etree.SubElement(ecuc_num_3, "DEFINITION-REF")
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/CanTp/CanTpGeneral/CanTpMaxRxNSdus"
    value = etree.SubElement(ecuc_num_3, "VALUE").text = "32767"
    ecuc_num_4 = etree.SubElement(parameter_values, "ECUC-NUMERICAL-PARAM-VALUE")
    definition_ref = etree.SubElement(ecuc_num_4, "DEFINITION-REF")
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/CanTp/CanTpGeneral/CanTpMaxFcPdus"
    value = etree.SubElement(ecuc_num_4, "VALUE").text = "32767"

    ecuc_container_value = etree.SubElement(containers, "ECUC-CONTAINER-VALUE")
    short_name = etree.SubElement(ecuc_container_value, "SHORT-NAME").text = "CanTpConfig"
    definition_config = etree.SubElement(ecuc_container_value, "DEFINITION-REF")
    definition_config.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition_config.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig"
    subcontainer_init = etree.SubElement(ecuc_container_value, "SUB-CONTAINERS")
    id = 0
    for diag_tool in diag_tools:
        for lin in lins:
            lin_network = re.search("LIN_VSM_\d", lin["NAME"])
            ecuc_container_value = etree.SubElement(subcontainer_init, "ECUC-CONTAINER-VALUE")
            # TRS.COMCONF.GEN.097(0)
            short_name = etree.SubElement(ecuc_container_value, "SHORT-NAME").text = "CanTpChannel_Gw_" + diag_tool + "_" + lin['NAME']
            definition = etree.SubElement(ecuc_container_value, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel"
            parameter = etree.SubElement(ecuc_container_value, "PARAMETER-VALUES")
            ecuc_textual_param_value = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
            definition_ref = etree.SubElement(ecuc_textual_param_value, "DEFINITION-REF")
            definition_ref.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpChannelMode"
            # TRS.COMCONF.GEN.098(0)
            value = etree.SubElement(ecuc_textual_param_value, "VALUE").text = "CANTP_MODE_HALF_DUPLEX"
            subcontainer_nad = etree.SubElement(ecuc_container_value, "SUB-CONTAINERS")
            for nad in nads:
                if nad['CONFIG'] == "2.1":
                    nad_network = re.search("LIN_VSM_\d", nad["LIN"])
                    if lin_network.group(0) == nad_network.group(0):
                        # REQ part
                        ecuc_container_nad = etree.SubElement(subcontainer_nad, "ECUC-CONTAINER-VALUE")
                        # TRS.COMCONF.GEN.099(0)
                        short_name = etree.SubElement(ecuc_container_nad, "SHORT-NAME").text = "CanTpRxNSdu_REQ_" + diag_tool + "_" + lin['NAME'] + "_" + nad['NAME']
                        definition = etree.SubElement(ecuc_container_nad, "DEFINITION-REF")
                        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                        definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu"
                        parameters = etree.SubElement(ecuc_container_nad, "PARAMETER-VALUES")
                        numerical_0 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_0 = etree.SubElement(numerical_0, "DEFINITION-REF")
                        definition_0.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                        definition_0.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpRxNSduId"
                        # TRS.COMCONF.GEN.0100(0)
                        value_0 = etree.SubElement(numerical_0, "VALUE").text = str(id)
                        #id = id + 1
                        numerical_1 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_1 = etree.SubElement(numerical_1, "DEFINITION-REF")
                        definition_1.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                        definition_1.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpBs"
                        value_1 = etree.SubElement(numerical_1, "VALUE").text = "0"
                        numerical_2 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_2 = etree.SubElement(numerical_2, "DEFINITION-REF")
                        definition_2.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                        definition_2.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpRxDl"
                        value_2 = etree.SubElement(numerical_2, "VALUE").text = "1"
                        numerical_3 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_3 = etree.SubElement(numerical_3, "DEFINITION-REF")
                        definition_3.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                        definition_3.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpRxWftMax"
                        value_3 = etree.SubElement(numerical_3, "VALUE").text = "0"
                        numerical_4 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_4 = etree.SubElement(numerical_4, "DEFINITION-REF")
                        definition_4.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
                        definition_4.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpNar"
                        value_4 = etree.SubElement(numerical_4, "VALUE").text = "0.1"
                        numerical_5 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_5 = etree.SubElement(numerical_5, "DEFINITION-REF")
                        definition_5.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
                        definition_5.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpNbr"
                        value_5 = etree.SubElement(numerical_5, "VALUE").text = "0.03"
                        numerical_6 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_6 = etree.SubElement(numerical_6, "DEFINITION-REF")
                        definition_6.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
                        definition_6.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpNcr"
                        value_6 = etree.SubElement(numerical_6, "VALUE").text = "0.25"
                        numerical_7 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_7 = etree.SubElement(numerical_7, "DEFINITION-REF")
                        definition_7.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
                        definition_7.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpSTmin"
                        value_7 = etree.SubElement(numerical_7, "VALUE").text = "0.01"
                        textual_1 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                        def_textual_1 = etree.SubElement(textual_1, "DEFINITION-REF")
                        def_textual_1.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                        def_textual_1.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpRxAddressingFormat"
                        val_textual_1 = etree.SubElement(textual_1, "VALUE").text = "CANTP_EXTENDED"
                        textual_2 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                        def_textual_2 = etree.SubElement(textual_2, "DEFINITION-REF")
                        def_textual_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                        def_textual_2.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpRxPaddingActivation"
                        val_textual_2 = etree.SubElement(textual_2, "VALUE").text = "CANTP_OFF"
                        textual_3 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                        def_textual_3 = etree.SubElement(textual_3, "DEFINITION-REF")
                        def_textual_3.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                        def_textual_3.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpRxTaType"
                        val_textual_3 = etree.SubElement(textual_3, "VALUE").text = "CANTP_PHYSICAL"
                        references = etree.SubElement(ecuc_container_nad, "REFERENCE-VALUES")
                        ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
                        definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
                        definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                        definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpRxNSduRef"
                        value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
                        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                        # TRS.COMCONF.GEN.0101(0)
                        value.text = "/EcuC/EcuC/EcucPduCollection/CanTp_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_EnGwCLD"
                        subcontainers = etree.SubElement(ecuc_container_nad, "SUB-CONTAINERS")
                        ecuc_container_1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
                        # TRS.COMCONF.GEN.0102(0)
                        short_name = etree.SubElement(ecuc_container_1, "SHORT-NAME").text = "CanTpNSa_REQ_" + diag_tool + "_" + lin['NAME'] + "_" + nad['NAME']
                        definition = etree.SubElement(ecuc_container_1, "DEFINITION-REF")
                        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                        definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpNSa"
                        param_values = etree.SubElement(ecuc_container_1, "PARAMETER-VALUES")
                        ecuc_numerical = etree.SubElement(param_values, "ECUC-NUMERICAL-PARAM-VALUE")
                        def_param = etree.SubElement(ecuc_numerical, "DEFINITION-REF")
                        def_param.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                        def_param.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpNSa/CanTpNSa"
                        value = etree.SubElement(ecuc_numerical, "VALUE").text = nad["ID"]
                        ecuc_container_2 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
                        # TRS.COMCONF.GEN.0103(0)
                        short_name = etree.SubElement(ecuc_container_2, "SHORT-NAME").text = "CanTpNTa_REQ_" + diag_tool + "_" + lin['NAME'] + "_" + nad['NAME']
                        definition = etree.SubElement(ecuc_container_2, "DEFINITION-REF")
                        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                        definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpNTa"
                        param_values = etree.SubElement(ecuc_container_2, "PARAMETER-VALUES")
                        ecuc_numerical = etree.SubElement(param_values, "ECUC-NUMERICAL-PARAM-VALUE")
                        def_param = etree.SubElement(ecuc_numerical, "DEFINITION-REF")
                        def_param.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                        def_param.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpNTa/CanTpNTa"
                        value = etree.SubElement(ecuc_numerical, "VALUE").text = nad["ID"]
                        ecuc_container_3 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
                        # TRS.COMCONF.GEN.0104(0)
                        short_name = etree.SubElement(ecuc_container_3, "SHORT-NAME").text = "CanTpRxNPdu_REQ_" + diag_tool + "_" + lin['NAME'] + "_" + nad['NAME']
                        definition = etree.SubElement(ecuc_container_3, "DEFINITION-REF")
                        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                        definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpRxNPdu"
                        ref_values = etree.SubElement(ecuc_container_3, "REFERENCE-VALUES")
                        ecuc_reference = etree.SubElement(ref_values, "ECUC-REFERENCE-VALUE")
                        def_param = etree.SubElement(ecuc_reference, "DEFINITION-REF")
                        def_param.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                        def_param.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpRxNPdu/CanTpRxNPduRef"
                        value = etree.SubElement(ecuc_reference, "VALUE-REF")
                        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                        value.text = "/EcuC/EcuC/EcucPduCollection/CanIf_REQ_" + diag_tool + "_" + nad_network.group(0) + "_CanTp"
                        ecuc_container_4 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
                        # TRS.COMCONF.GEN.0105(0)
                        short_name = etree.SubElement(ecuc_container_4, "SHORT-NAME").text = "CanTpTxFcNPdu_REQ_" + diag_tool + "_" + lin['NAME'] + "_" + nad['NAME']
                        definition = etree.SubElement(ecuc_container_4, "DEFINITION-REF")
                        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                        definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpTxFcNPdu"
                        ref_values = etree.SubElement(ecuc_container_4, "REFERENCE-VALUES")
                        ecuc_reference = etree.SubElement(ref_values, "ECUC-REFERENCE-VALUE")
                        def_param = etree.SubElement(ecuc_reference, "DEFINITION-REF")
                        def_param.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                        def_param.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpTxFcNPdu/CanTpTxFcNPduRef"
                        value = etree.SubElement(ecuc_reference, "VALUE-REF")
                        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                        value.text = "/EcuC/EcuC/EcucPduCollection/CanTp_FC_REP_" + diag_tool + "_" + nad_network.group(0) + "_" + nad['NAME'] + "_CanIf"
                        # REP part
                        ecuc_container_nad = etree.SubElement(subcontainer_nad, "ECUC-CONTAINER-VALUE")
                        # TRS.COMCONF.GEN.0106(0)
                        short_name = etree.SubElement(ecuc_container_nad, "SHORT-NAME").text = "CanTpTxNSdu_REP_" + diag_tool + "_" + lin['NAME'] + "_" + nad['NAME']
                        definition = etree.SubElement(ecuc_container_nad, "DEFINITION-REF")
                        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                        definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu"
                        parameters = etree.SubElement(ecuc_container_nad, "PARAMETER-VALUES")
                        numerical_0 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_0 = etree.SubElement(numerical_0, "DEFINITION-REF")
                        definition_0.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                        definition_0.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpTxNSduId"
                        # TRS.COMCONF.GEN.0107(0)
                        value_0 = etree.SubElement(numerical_0, "VALUE").text = str(id)
                        id = id + 1
                        numerical_1 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_1 = etree.SubElement(numerical_1, "DEFINITION-REF")
                        definition_1.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                        definition_1.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpTxDl"
                        value_1 = etree.SubElement(numerical_1, "VALUE").text = "1"
                        numerical_2 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_2 = etree.SubElement(numerical_2, "DEFINITION-REF")
                        definition_2.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
                        definition_2.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpTc"
                        value_2 = etree.SubElement(numerical_2, "VALUE").text = "0"
                        numerical_3 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_3 = etree.SubElement(numerical_3, "DEFINITION-REF")
                        definition_3.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
                        definition_3.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpNas"
                        value_3 = etree.SubElement(numerical_3, "VALUE").text = "0.1"
                        numerical_4 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_4 = etree.SubElement(numerical_4, "DEFINITION-REF")
                        definition_4.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
                        definition_4.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpNbs"
                        value_4 = etree.SubElement(numerical_4, "VALUE").text = "0.03"
                        numerical_5 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_5 = etree.SubElement(numerical_5, "DEFINITION-REF")
                        definition_5.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
                        definition_5.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpNcs"
                        value_5 = etree.SubElement(numerical_5, "VALUE").text = "0.25"
                        textual_1 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                        def_textual_1 = etree.SubElement(textual_1, "DEFINITION-REF")
                        def_textual_1.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                        def_textual_1.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpTxAddressingFormat"
                        val_textual_1 = etree.SubElement(textual_1, "VALUE").text = "CANTP_EXTENDED"
                        textual_2 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                        def_textual_2 = etree.SubElement(textual_2, "DEFINITION-REF")
                        def_textual_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                        def_textual_2.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpTxPaddingActivation"
                        val_textual_2 = etree.SubElement(textual_2, "VALUE").text = "CANTP_OFF"
                        textual_3 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                        def_textual_3 = etree.SubElement(textual_3, "DEFINITION-REF")
                        def_textual_3.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                        def_textual_3.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpTxTaType"
                        val_textual_3 = etree.SubElement(textual_3, "VALUE").text = "CANTP_PHYSICAL"
                        references = etree.SubElement(ecuc_container_nad, "REFERENCE-VALUES")
                        ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
                        definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
                        definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                        definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpTxNSduRef"
                        value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
                        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                        # TRS.COMCONF.GEN.0108(0)
                        value.text = "/EcuC/EcuC/EcucPduCollection/CanTp_REP_" + diag_tool + "_" + nad['NETWORK'] + "_EnGwCLD"
                        subcontainers = etree.SubElement(ecuc_container_nad, "SUB-CONTAINERS")
                        ecuc_container_1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
                        # TRS.COMCONF.GEN.0109(0)
                        short_name = etree.SubElement(ecuc_container_1, "SHORT-NAME").text = "CanTpNSa_REP_" + diag_tool + "_" + lin['NAME'] + "_" + nad['NAME']
                        definition = etree.SubElement(ecuc_container_1, "DEFINITION-REF")
                        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                        definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpNSa"
                        param_values = etree.SubElement(ecuc_container_1, "PARAMETER-VALUES")
                        ecuc_numerical = etree.SubElement(param_values, "ECUC-NUMERICAL-PARAM-VALUE")
                        def_param = etree.SubElement(ecuc_numerical, "DEFINITION-REF")
                        def_param.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                        def_param.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpNSa/CanTpNSa"
                        value = etree.SubElement(ecuc_numerical, "VALUE").text = nad["ID"]
                        ecuc_container_2 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
                        # TRS.COMCONF.GEN.0110(0)
                        short_name = etree.SubElement(ecuc_container_2, "SHORT-NAME").text = "CanTpNTa_REP_" + diag_tool + "_" + lin['NAME'] + "_" + nad['NAME']
                        definition = etree.SubElement(ecuc_container_2, "DEFINITION-REF")
                        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                        definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpNTa"
                        param_values = etree.SubElement(ecuc_container_2, "PARAMETER-VALUES")
                        ecuc_numerical = etree.SubElement(param_values, "ECUC-NUMERICAL-PARAM-VALUE")
                        def_param = etree.SubElement(ecuc_numerical, "DEFINITION-REF")
                        def_param.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                        def_param.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpNTa/CanTpNTa"
                        value = etree.SubElement(ecuc_numerical, "VALUE").text = nad["ID"]
                        ecuc_container_3 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
                        # TRS.COMCONF.GEN.0111(0)
                        short_name = etree.SubElement(ecuc_container_3, "SHORT-NAME").text = "CanTpTxNPdu_REP_" + diag_tool + "_" + lin['NAME'] + "_" + nad['NAME']
                        definition = etree.SubElement(ecuc_container_3, "DEFINITION-REF")
                        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                        definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpTxNPdu"
                        ref_values = etree.SubElement(ecuc_container_3, "REFERENCE-VALUES")
                        ecuc_reference = etree.SubElement(ref_values, "ECUC-REFERENCE-VALUE")
                        def_param = etree.SubElement(ecuc_reference, "DEFINITION-REF")
                        def_param.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                        def_param.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpTxNPdu/CanTpTxNPduRef"
                        value = etree.SubElement(ecuc_reference, "VALUE-REF")
                        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                        value.text = "/EcuC/EcuC/EcucPduCollection/CanTp_REP_" + diag_tool + "_" + nad_network.group(0) + "_" + nad['NAME'] + "_CanIf"
                        ecuc_container_4 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
                        # TRS.COMCONF.GEN.0112(0)
                        short_name = etree.SubElement(ecuc_container_4, "SHORT-NAME").text = "CanTpRxFcNPdu_REP_" + diag_tool + "_" + lin['NAME'] + "_" + nad['NAME']
                        definition = etree.SubElement(ecuc_container_4, "DEFINITION-REF")
                        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                        definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpRxFcNPdu"
                        ref_values = etree.SubElement(ecuc_container_4, "REFERENCE-VALUES")
                        ecuc_reference = etree.SubElement(ref_values, "ECUC-REFERENCE-VALUE")
                        def_param = etree.SubElement(ecuc_reference, "DEFINITION-REF")
                        def_param.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                        def_param.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpRxFcNPdu/CanTpRxFcNPduRef"
                        value = etree.SubElement(ecuc_reference, "VALUE-REF")
                        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                        value.text = "/EcuC/EcuC/EcucPduCollection/CanIf_REQ_" + diag_tool + "_" + nad_network.group(0) + "_CanTp"
    # generate data
    pretty_xml = prettify_xml(rootCanTp)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/CanTp.epc', encoding='UTF-8', xml_declaration=True, method="xml", doctype = "<!-- XML file generated by COM_Configurator-18 -->")
    return


def LinTp_config(file_list, output_path, logger):
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    nads = []
    lins = []
    for file in file_list:
        if file.endswith('.arxml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            elements = root.findall(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-CONFIG")
            for elem in elements:
                obj_nad = {}
                obj_nad['NAME'] = elem.find(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-ECU-REF").text.split("/")[-2]
                obj_nad['NETWORK'] = elem.find(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-ECU-REF").text.split("/")[-1]
                obj_nad['ID'] = elem.find(".//{http://autosar.org/schema/r4.0}CONFIGURED-NAD").text
                obj_nad['LIN'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                obj_nad['CONFIG'] = elem.find(".//{http://autosar.org/schema/r4.0}PROTOCOL-VERSION").text
                nads.append(obj_nad)
        # elif file.endswith('.xml'):
        #     parser = etree.XMLParser(remove_comments=True)
        #     tree = objectify.parse(file, parser=parser)
        #     root = tree.getroot()
        #     lins21 = root.findall(".//CAN-ID-LIN21")
        #     for elem in lins21:
        #         obj_lin = {}
        #         obj_lin['NAME'] = elem.find(".//LIN-CLUSTER-REF").text.split("/")[-1]
        #         obj_lin['REQ-ID'] = elem.find(".//REQUEST-ID").text
        #         obj_lin['REP-ID'] = elem.find(".//RESPONSE-ID").text
        #         lins.append(obj_lin)

    # create ouput file: LinTp.epc
    rootLinTp = etree.Element('AUTOSAR', {attr_qname: 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd'}, nsmap=NSMAP)
    packages = etree.SubElement(rootLinTp, 'AR-PACKAGES')
    package = etree.SubElement(packages, 'AR-PACKAGE')
    short_name = etree.SubElement(package, 'SHORT-NAME').text = "LinTp"
    elements = etree.SubElement(package, 'ELEMENTS')
    ecuc_module = etree.SubElement(elements, 'ECUC-MODULE-CONFIGURATION-VALUES')
    short_name = etree.SubElement(ecuc_module, 'SHORT-NAME').text = "LinTp"
    definition = etree.SubElement(ecuc_module, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-MODULE-DEF"
    definition.text = "/AUTOSAR/EcuDefs/LinTp"
    description = etree.SubElement(ecuc_module, 'IMPLEMENTATION-CONFIG-VARIANT').text = "VARIANT-POST-BUILD"
    containers = etree.SubElement(ecuc_module, 'CONTAINERS')
    ecuc_general = etree.SubElement(containers, "ECUC-CONTAINER-VALUE")
    short_name = etree.SubElement(ecuc_general, "SHORT-NAME").text = "LinTpGlobalConfig"
    definition_general = etree.SubElement(ecuc_general, "DEFINITION-REF")
    definition_general.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition_general.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig"
    parameter_values = etree.SubElement(ecuc_general, "PARAMETER-VALUES")
    subcontainer_general = etree.SubElement(ecuc_general, "SUB-CONTAINERS")
    # for nad in nads:
    #     nad_network = re.search("LIN_VSM_\d", nad["NETWORK"])
    #     if nad['CONFIG'] == "2.1":
    #         lin = ""
    #         if nad['LIN'] == "VSM_LIN_VSM_1":
    #             lin = "LIN_VSM_1_Channel"
    #         elif nad['LIN'] == "VSM_LIN_VSM_2":
    #             lin = "LIN_VSM_2_Channel"
    #         elif nad['LIN'] == "VSM_LIN_VSM_3":
    #             lin = "LIN_VSM_3_Channel"
    #         elif nad['LIN'] == "VSM_LIN_VSM_4":
    #             lin = "LIN_VSM_4_Channel"
    #         elif nad['LIN'] == "VSM_LIN_VSM_5":
    #             lin = "LIN_VSM_5_Channel"
    #         elif nad['LIN'] == "VSM_LIN_VSM_6":
    #             lin = "LIN_VSM_6_Channel"
    #         elif nad['LIN'] == "VSM_LIN_VSM_7":
    #             lin = "LIN_VSM_7_Channel"
    #         elif nad['LIN'] == "VSM_LIN_VSM_8":
    #             lin = "LIN_VSM_8_Channel"
    #         # REP part
    #         ecuc_nad = etree.SubElement(subcontainer_general, "ECUC-CONTAINER-VALUE")
    #         # TRS.COMCONF.GEN.065(0)
    #         short_name = etree.SubElement(ecuc_nad, "SHORT-NAME").text = "LinTpRxNSdu_REP_" + nad['NETWORK']
    #         definition_nad = etree.SubElement(ecuc_nad, "DEFINITION-REF")
    #         definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition_nad.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpRxNSdu"
    #         parameters = etree.SubElement(ecuc_nad, "PARAMETER-VALUES")
    #         numerical_1 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
    #         definition_1 = etree.SubElement(numerical_1, "DEFINITION-REF")
    #         definition_1.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition_1.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpRxNSdu/LinTpDl"
    #         # TRS.COMCONF.GEN.066(0)
    #         value_1 = etree.SubElement(numerical_1, "VALUE").text = "1"
    #         numerical_2 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
    #         definition_2 = etree.SubElement(numerical_2, "DEFINITION-REF")
    #         definition_2.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition_2.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpRxNSdu/LinTpRxNSduNad"
    #         value_2 = etree.SubElement(numerical_2, "VALUE").text = str(nad['ID'])
    #         numerical_3 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
    #         definition_3 = etree.SubElement(numerical_3, "DEFINITION-REF")
    #         definition_3.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
    #         definition_3.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpRxNSdu/LinTpNcr"
    #         value_3 = etree.SubElement(numerical_3, "VALUE").text = "1.0"
    #         references = etree.SubElement(ecuc_nad, "REFERENCE-VALUES")
    #         ecuc_ref_value_1 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
    #         definition = etree.SubElement(ecuc_ref_value_1, "DEFINITION-REF")
    #         definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpRxNSdu/LinTpRxNSduPduRef"
    #         value = etree.SubElement(ecuc_ref_value_1, "VALUE-REF")
    #         value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
    #         # TRS.COMCONF.GEN.067(0)
    #         value.text = "/EcuC/EcuC/EcucPduCollection/LinTp_REP_" + nad['NETWORK'] + "_EnGwCLD"
    #         ecuc_ref_value_2 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
    #         definition = etree.SubElement(ecuc_ref_value_2, "DEFINITION-REF")
    #         definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpRxNSdu/LinTpRxNSduChannelRef"
    #         value = etree.SubElement(ecuc_ref_value_2, "VALUE-REF")
    #         value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
    #         value.text = "/LinIf/LinIf/LinIfGlobalConfig/" + lin
    #         ecuc_ref_value_2 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
    #         definition = etree.SubElement(ecuc_ref_value_2, "DEFINITION-REF")
    #         definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpRxNSdu/LinTpRxNSduTpChannelRef"
    #         value = etree.SubElement(ecuc_ref_value_2, "VALUE-REF")
    #         value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
    #         value.text = "/LinTp/LinTp/LinTpGlobalConfig/LinTpChannel_" + nad_network.group(0)
    #         # REQ part
    #         ecuc_nad = etree.SubElement(subcontainer_general, "ECUC-CONTAINER-VALUE")
    #         # TRS.COMCONF.GEN.068(0)
    #         short_name = etree.SubElement(ecuc_nad, "SHORT-NAME").text = "LinTpTxNSdu_REQ_" + nad['NETWORK']
    #         definition_nad = etree.SubElement(ecuc_nad, "DEFINITION-REF")
    #         definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #         definition_nad.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpTxNSdu"
    #         parameters = etree.SubElement(ecuc_nad, "PARAMETER-VALUES")
    #         numerical_1 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
    #         definition_1 = etree.SubElement(numerical_1, "DEFINITION-REF")
    #         definition_1.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
    #         definition_1.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpTxNSdu/LinTpNas"
    #         # TRS.COMCONF.GEN.069(0)
    #         value_1 = etree.SubElement(numerical_1, "VALUE").text = "0.1"
    #         numerical_2 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
    #         definition_2 = etree.SubElement(numerical_2, "DEFINITION-REF")
    #         definition_2.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    #         definition_2.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpTxNSdu/LinTpTxNSduNad"
    #         value_2 = etree.SubElement(numerical_2, "VALUE").text = str(nad['ID'])
    #         numerical_3 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
    #         definition_3 = etree.SubElement(numerical_3, "DEFINITION-REF")
    #         definition_3.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
    #         definition_3.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpTxNSdu/LinTpNcs"
    #         value_3 = etree.SubElement(numerical_3, "VALUE").text = "0.1"
    #         references = etree.SubElement(ecuc_nad, "REFERENCE-VALUES")
    #         ecuc_ref_value_1 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
    #         definition = etree.SubElement(ecuc_ref_value_1, "DEFINITION-REF")
    #         definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpTxNSdu/LinTpTxNSduPduRef"
    #         value = etree.SubElement(ecuc_ref_value_1, "VALUE-REF")
    #         value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
    #         # TRS.COMCONF.GEN.070(0)
    #         value.text = "/EcuC/EcuC/EcucPduCollection/LinTp_REQ_" + nad['NETWORK'] + "_EnGwCLD"
    #         ecuc_ref_value_2 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
    #         definition = etree.SubElement(ecuc_ref_value_2, "DEFINITION-REF")
    #         definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpTxNSdu/LinTpTxNSduChannelRef"
    #         value = etree.SubElement(ecuc_ref_value_2, "VALUE-REF")
    #         value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
    #         value.text = "/LinIf/LinIf/LinIfGlobalConfig/" + lin
    #         ecuc_ref_value_2 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
    #         definition = etree.SubElement(ecuc_ref_value_2, "DEFINITION-REF")
    #         definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
    #         definition.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpTxNSdu/LinTpTxNSduTpChannelRef"
    #         value = etree.SubElement(ecuc_ref_value_2, "VALUE-REF")
    #         value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
    #         value.text = "/LinTp/LinTp/LinTpGlobalConfig/LinTpChannel_" + nad_network.group(0)
    # network_list = []
    # for nad in nads:
    #     if nad['CONFIG'] == "2.1":
    #         nad_network = re.search("LIN_VSM_\d", nad["NETWORK"])
    #         if nad_network.group(0) not in network_list:
    #             network_list.append(nad_network.group(0))
    #             ecuc_nad = etree.SubElement(subcontainer_general, "ECUC-CONTAINER-VALUE")
    #             # TRS.COMCONF.GEN.071(0)
    #             short_name = etree.SubElement(ecuc_nad, "SHORT-NAME").text = "LinTpChannel_" + nad_network.group(0)
    #             definition_nad = etree.SubElement(ecuc_nad, "DEFINITION-REF")
    #             definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    #             definition_nad.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpChannelConfig"
    #             parameter_values = etree.SubElement(ecuc_nad, "PARAMETER-VALUES")
    #             boolean_1 = etree.SubElement(parameter_values, "ECUC-NUMERICAL-PARAM-VALUE")
    #             definition_1 = etree.SubElement(boolean_1, "DEFINITION-REF")
    #             definition_1.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
    #             definition_1.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpChannelConfig/LinTpDropNotRequestedNad"
    #             # TRS.COMCONF.GEN.072(0)
    #             value_1 = etree.SubElement(boolean_1, "VALUE").text = "0"
    #             boolean_2 = etree.SubElement(parameter_values, "ECUC-NUMERICAL-PARAM-VALUE")
    #             definition_2 = etree.SubElement(boolean_2, "DEFINITION-REF")
    #             definition_2.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
    #             definition_2.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpChannelConfig/LinTpScheduleChangeDiag"
    #             value_2 = etree.SubElement(boolean_2, "VALUE").text = "1"

    # generate data
    pretty_xml = prettify_xml(rootLinTp)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/LinTp.epc', encoding='UTF-8', xml_declaration=True, method="xml", doctype = "<!-- XML file generated by COM_Configurator-18 -->")
    return


def LinIf_config(file_list, output_path, logger):
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    nads = []
    lins = []
    for file in file_list:
        if file.endswith('.arxml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            elements = root.findall(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-CONFIG")
            for elem in elements:
                obj_nad = {}
                obj_nad['NAME'] = elem.find(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-ECU-REF").text.split("/")[-2]
                obj_nad['NETWORK'] = elem.find(".//{http://autosar.org/schema/r4.0}LIN-SLAVE-ECU-REF").text.split("/")[-1]
                obj_nad['ID'] = elem.find(".//{http://autosar.org/schema/r4.0}CONFIGURED-NAD").text
                obj_nad['LIN'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                obj_nad['CONFIG'] = elem.find(".//{http://autosar.org/schema/r4.0}PROTOCOL-VERSION").text
                nads.append(obj_nad)
        elif file.endswith('.xml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            lins13 = root.findall(".//CAN-ID-LIN13")
            for elem in lins13:
                obj_lin = {}
                obj_lin['NAME'] = elem.find(".//LIN-SLAVE-REF").text.split("/")[-1]
                obj_lin['REQ-ID'] = elem.find(".//REQUEST-ID").text
                obj_lin['REP-ID'] = elem.find(".//RESPONSE-ID").text
                lins.append(obj_lin)

    # create ouput file: LinIf.epc
    rootLinIf = etree.Element('AUTOSAR', {attr_qname: 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd'}, nsmap=NSMAP)
    packages = etree.SubElement(rootLinIf, 'AR-PACKAGES')
    package = etree.SubElement(packages, 'AR-PACKAGE')
    short_name = etree.SubElement(package, 'SHORT-NAME').text = "LinIf"
    elements = etree.SubElement(package, 'ELEMENTS')
    ecuc_module = etree.SubElement(elements, 'ECUC-MODULE-CONFIGURATION-VALUES')
    short_name = etree.SubElement(ecuc_module, 'SHORT-NAME').text = "LinIf"
    definition = etree.SubElement(ecuc_module, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-MODULE-DEF"
    definition.text = "/AUTOSAR/EcuDefs/LinIf"
    description = etree.SubElement(ecuc_module, 'IMPLEMENTATION-CONFIG-VARIANT').text = "VARIANT-POST-BUILD"
    containers = etree.SubElement(ecuc_module, 'CONTAINERS')
    ecuc_general = etree.SubElement(containers, "ECUC-CONTAINER-VALUE")
    short_name = etree.SubElement(ecuc_general, "SHORT-NAME").text = "LinIfGlobalConfig"
    definition_general = etree.SubElement(ecuc_general, "DEFINITION-REF")
    definition_general.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition_general.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig"
    parameter_values = etree.SubElement(ecuc_general, "PARAMETER-VALUES")
    subcontainer_master = etree.SubElement(ecuc_general, "SUB-CONTAINERS")
    network_list = []
    for nad in nads:
        if nad['CONFIG'] == "1.3":
            nad_network = re.search("LIN_VSM_\d", nad["NETWORK"])
            if nad_network.group(0) not in network_list:
                network_list.append(nad_network.group(0))
                ecuc_general = etree.SubElement(subcontainer_master, "ECUC-CONTAINER-VALUE")
                # TRS.COMCONF.GEN.075(0)
                short_name = etree.SubElement(ecuc_general, "SHORT-NAME").text = nad_network.group(0) + "_Channel"
                definition_general = etree.SubElement(ecuc_general, "DEFINITION-REF")
                definition_general.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_general.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel"
                parameter_values = etree.SubElement(ecuc_general, "PARAMETER-VALUES")
                subcontainer_general = etree.SubElement(ecuc_general, "SUB-CONTAINERS")
                # REQ part lin network
                ecuc_nad = etree.SubElement(subcontainer_general, "ECUC-CONTAINER-VALUE")
                # TRS.COMCONF.GEN.076(0)
                short_name = etree.SubElement(ecuc_nad, "SHORT-NAME").text = "LinIfFrame_REP_" + nad_network.group(0) + "_1P3"
                definition_nad = etree.SubElement(ecuc_nad, "DEFINITION-REF")
                definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_nad.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame"
                parameters = etree.SubElement(ecuc_nad, "PARAMETER-VALUES")
                numerical_1 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                definition_1 = etree.SubElement(numerical_1, "DEFINITION-REF")
                definition_1.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_1.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame/LinIfLength"
                # TRS.COMCONF.GEN.077(0)
                value_1 = etree.SubElement(numerical_1, "VALUE").text = "8"
                numerical_2 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                definition_2 = etree.SubElement(numerical_2, "DEFINITION-REF")
                definition_2.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_2.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame/LinIfPid"
                value_2 = etree.SubElement(numerical_2, "VALUE").text = "61"
                numerical_3 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_3 = etree.SubElement(numerical_3, "DEFINITION-REF")
                definition_3.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_3.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame/LinIfChecksumType"
                value_3 = etree.SubElement(numerical_3, "VALUE").text = "CLASSIC"
                numerical_4 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_4 = etree.SubElement(numerical_4, "DEFINITION-REF")
                definition_4.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_4.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame/LinIfFrameType"
                value_4 = etree.SubElement(numerical_4, "VALUE").text = "UNCONDITIONAL"
                subcontainer_local = etree.SubElement(ecuc_nad, "SUB-CONTAINERS")
                lin_direction = etree.SubElement(subcontainer_local, "ECUC-CONTAINER-VALUE")
                # TRS.COMCONF.GEN.078(0)
                short_name = etree.SubElement(lin_direction, "SHORT-NAME").text = "LinIfPduDirection_REP_" + nad_network.group(0) + "_1P3"
                definition_nad = etree.SubElement(lin_direction, "DEFINITION-REF")
                definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_nad.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame/LinIfPduDirection"
                subcontainer_local2 = etree.SubElement(lin_direction, "SUB-CONTAINERS")
                lin_direction2 = etree.SubElement(subcontainer_local2, "ECUC-CONTAINER-VALUE")
                # TRS.COMCONF.GEN.079(0)
                short_name = etree.SubElement(lin_direction2, "SHORT-NAME").text = "LinIfRxPdu_REP_" + nad_network.group(0) + "_1P3"
                definition_nad = etree.SubElement(lin_direction2, "DEFINITION-REF")
                definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_nad.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame/LinIfPduDirection/LinIfRxPdu"
                references = etree.SubElement(lin_direction2, "REFERENCE-VALUES")
                ecuc_ref_value_1 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
                definition = etree.SubElement(ecuc_ref_value_1, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame/LinIfPduDirection/LinIfRxPdu/LinIfRxPduRef"
                value = etree.SubElement(ecuc_ref_value_1, "VALUE-REF")
                value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value.text = "/EcuC/EcuC/EcucPduCollection/LinIf_REP_" + nad_network.group(0) + "_1P3_EnGwCLD"
                # REP part schedule table
                ecuc_nad = etree.SubElement(subcontainer_general, "ECUC-CONTAINER-VALUE")
                # TRS.COMCONF.GEN.084(0)
                short_name = etree.SubElement(ecuc_nad, "SHORT-NAME").text = "LinIfScheduleTable_REP_" + nad_network.group(0) + "_1P3"
                definition_nad = etree.SubElement(ecuc_nad, "DEFINITION-REF")
                definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_nad.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable"
                parameters = etree.SubElement(ecuc_nad, "PARAMETER-VALUES")
                textual_1 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_1 = etree.SubElement(textual_1, "DEFINITION-REF")
                definition_1.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_1.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfScheduleTableName"
                # TRS.COMCONF.GEN.085(0)
                value_1 = etree.SubElement(textual_1, "VALUE").text = "SCH_REP_" + nad_network.group(0) + "_1P3"
                textual_2 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_2 = etree.SubElement(textual_2, "DEFINITION-REF")
                definition_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_2.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfResumePosition"
                value_2 = etree.SubElement(textual_2, "VALUE").text = "START_FROM_BEGINNING"
                textual_3 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_3 = etree.SubElement(textual_3, "DEFINITION-REF")
                definition_3.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_3.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfRunMode"
                value_3 = etree.SubElement(textual_3, "VALUE").text = "RUN_ONCE"
                textual_4 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_4 = etree.SubElement(textual_4, "DEFINITION-REF")
                definition_4.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_4.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfScheduleMode"
                value_4 = etree.SubElement(textual_4, "VALUE").text = "LINTP_DIAG_RESPONSE"
                subcontainer_local = etree.SubElement(ecuc_nad, "SUB-CONTAINERS")
                lin_entry0 = etree.SubElement(subcontainer_local, "ECUC-CONTAINER-VALUE")
                # TRS.COMCONF.GEN.086(0)
                short_name = etree.SubElement(lin_entry0, "SHORT-NAME").text = "LinIfEntry_0"
                definition_nad = etree.SubElement(lin_entry0, "DEFINITION-REF")
                definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_nad.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfEntry"
                parameters_local = etree.SubElement(lin_entry0, "PARAMETER-VALUES")
                textual_1 = etree.SubElement(parameters_local, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_1 = etree.SubElement(textual_1, "DEFINITION-REF")
                definition_1.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_1.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfEntry/LinIfEntryIndex"
                # TRS.COMCONF.GEN.087(0)
                value_1 = etree.SubElement(textual_1, "VALUE").text = "0"
                numerical_2 = etree.SubElement(parameters_local, "ECUC-NUMERICAL-PARAM-VALUE")
                definition_2 = etree.SubElement(numerical_2, "DEFINITION-REF")
                definition_2.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
                definition_2.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfEntry/LinIfDelay"
                value_2 = etree.SubElement(numerical_2, "VALUE").text = "0.080"
                references = etree.SubElement(lin_entry0, "REFERENCE-VALUES")
                ecuc_ref_value_1 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
                definition = etree.SubElement(ecuc_ref_value_1, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfEntry/LinIfFrameRef"
                value = etree.SubElement(ecuc_ref_value_1, "VALUE-REF")
                value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value.text = "/LinIf/LinIf/LinIfGlobalConfig/" + nad_network.group(0) + "_Channel/LinIfFrame_REP_" + nad_network.group(0) + "_1P3"
                lin_entry1 = etree.SubElement(subcontainer_local, "ECUC-CONTAINER-VALUE")
                # TRS.COMCONF.GEN.088(0)
                short_name = etree.SubElement(lin_entry1, "SHORT-NAME").text = "LinIfEntry_1"
                definition_nad = etree.SubElement(lin_entry1, "DEFINITION-REF")
                definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_nad.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfEntry"
                parameters_local = etree.SubElement(lin_entry1, "PARAMETER-VALUES")
                textual_1 = etree.SubElement(parameters_local, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_1 = etree.SubElement(textual_1, "DEFINITION-REF")
                definition_1.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_1.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfEntry/LinIfEntryIndex"
                # TRS.COMCONF.GEN.089(0)
                value_1 = etree.SubElement(textual_1, "VALUE").text = "1"
                numerical_2 = etree.SubElement(parameters_local, "ECUC-NUMERICAL-PARAM-VALUE")
                definition_2 = etree.SubElement(numerical_2, "DEFINITION-REF")
                definition_2.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
                definition_2.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfEntry/LinIfDelay"
                value_2 = etree.SubElement(numerical_2, "VALUE").text = "0.010"
                references = etree.SubElement(lin_entry1, "REFERENCE-VALUES")
                ecuc_ref_value_1 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
                definition = etree.SubElement(ecuc_ref_value_1, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfEntry/LinIfFrameRef"
                value = etree.SubElement(ecuc_ref_value_1, "VALUE-REF")
                value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value.text = "/LinIf/LinIf/LinIfGlobalConfig/" + nad_network.group(0) + "_Channel/LinIfFrame_REP_" + nad_network.group(0) + "_1P3"
                # REQ part lin network
                ecuc_nad = etree.SubElement(subcontainer_general, "ECUC-CONTAINER-VALUE")
                # TRS.COMCONF.GEN.080(0)
                short_name = etree.SubElement(ecuc_nad, "SHORT-NAME").text = "LinIfFrame_REQ_" + nad_network.group(0) + "_1P3"
                definition_nad = etree.SubElement(ecuc_nad, "DEFINITION-REF")
                definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_nad.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame"
                parameters = etree.SubElement(ecuc_nad, "PARAMETER-VALUES")
                numerical_1 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                definition_1 = etree.SubElement(numerical_1, "DEFINITION-REF")
                definition_1.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_1.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame/LinIfLength"
                # TRS.COMCONF.GEN.081(0)
                value_1 = etree.SubElement(numerical_1, "VALUE").text = "8"
                numerical_2 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                definition_2 = etree.SubElement(numerical_2, "DEFINITION-REF")
                definition_2.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_2.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame/LinIfPid"
                value_2 = etree.SubElement(numerical_2, "VALUE").text = "60"
                numerical_3 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_3 = etree.SubElement(numerical_3, "DEFINITION-REF")
                definition_3.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_3.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame/LinIfChecksumType"
                value_3 = etree.SubElement(numerical_3, "VALUE").text = "CLASSIC"
                numerical_4 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_4 = etree.SubElement(numerical_4, "DEFINITION-REF")
                definition_4.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_4.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame/LinIfFrameType"
                value_4 = etree.SubElement(numerical_4, "VALUE").text = "UNCONDITIONAL"
                subcontainer_local = etree.SubElement(ecuc_nad, "SUB-CONTAINERS")
                lin_direction = etree.SubElement(subcontainer_local, "ECUC-CONTAINER-VALUE")
                # TRS.COMCONF.GEN.082(0)
                short_name = etree.SubElement(lin_direction, "SHORT-NAME").text = "LinIfPduDirection_REQ_" + nad_network.group(0) + "_1P3"
                definition_nad = etree.SubElement(lin_direction, "DEFINITION-REF")
                definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_nad.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame/LinIfPduDirection"
                subcontainer_local2 = etree.SubElement(lin_direction, "SUB-CONTAINERS")
                lin_direction2 = etree.SubElement(subcontainer_local2, "ECUC-CONTAINER-VALUE")
                # TRS.COMCONF.GEN.083(0)
                short_name = etree.SubElement(lin_direction2, "SHORT-NAME").text = "LinIfTxPdu_REQ_" + nad_network.group(0) + "_1P3"
                definition_nad = etree.SubElement(lin_direction2, "DEFINITION-REF")
                definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_nad.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame/LinIfPduDirection/LinIfTxPdu"
                references = etree.SubElement(lin_direction2, "REFERENCE-VALUES")
                ecuc_ref_value_1 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
                definition = etree.SubElement(ecuc_ref_value_1, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfFrame/LinIfPduDirection/LinIfTxPdu/LinIfTxPduRef"
                value = etree.SubElement(ecuc_ref_value_1, "VALUE-REF")
                value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value.text = "/EcuC/EcuC/EcucPduCollection/LinIf_REQ_" + nad_network.group(0) + "_1P3_EnGwCLD"
                # REQ part schedule table
                ecuc_nad = etree.SubElement(subcontainer_general, "ECUC-CONTAINER-VALUE")
                # TRS.COMCONF.GEN.090(0)
                short_name = etree.SubElement(ecuc_nad, "SHORT-NAME").text = "LinIfScheduleTable_REQ_" + nad_network.group(0) + "_1P3"
                definition_nad = etree.SubElement(ecuc_nad, "DEFINITION-REF")
                definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_nad.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable"
                parameters = etree.SubElement(ecuc_nad, "PARAMETER-VALUES")
                textual_1 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_1 = etree.SubElement(textual_1, "DEFINITION-REF")
                definition_1.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_1.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfScheduleTableName"
                # TRS.COMCONF.GEN.091(0)
                value_1 = etree.SubElement(textual_1, "VALUE").text = "SCH_REQ_" + nad_network.group(0) + "_1P3"
                textual_2 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_2 = etree.SubElement(textual_2, "DEFINITION-REF")
                definition_2.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_2.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfResumePosition"
                value_2 = etree.SubElement(textual_2, "VALUE").text = "START_FROM_BEGINNING"
                textual_3 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_3 = etree.SubElement(textual_3, "DEFINITION-REF")
                definition_3.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_3.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfRunMode"
                value_3 = etree.SubElement(textual_3, "VALUE").text = "RUN_ONCE"
                textual_4 = etree.SubElement(parameters, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_4 = etree.SubElement(textual_4, "DEFINITION-REF")
                definition_4.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_4.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfScheduleMode"
                value_4 = etree.SubElement(textual_4, "VALUE").text = "LINTP_DIAG_REQUEST"
                subcontainer_local = etree.SubElement(ecuc_nad, "SUB-CONTAINERS")
                lin_entry0 = etree.SubElement(subcontainer_local, "ECUC-CONTAINER-VALUE")
                # TRS.COMCONF.GEN.092(0)
                short_name = etree.SubElement(lin_entry0, "SHORT-NAME").text = "LinIfEntry_0"
                definition_nad = etree.SubElement(lin_entry0, "DEFINITION-REF")
                definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_nad.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfEntry"
                parameters_local = etree.SubElement(lin_entry0, "PARAMETER-VALUES")
                textual_1 = etree.SubElement(parameters_local, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_1 = etree.SubElement(textual_1, "DEFINITION-REF")
                definition_1.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_1.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfEntry/LinIfEntryIndex"
                # TRS.COMCONF.GEN.093(0)
                value_1 = etree.SubElement(textual_1, "VALUE").text = "0"
                numerical_2 = etree.SubElement(parameters_local, "ECUC-NUMERICAL-PARAM-VALUE")
                definition_2 = etree.SubElement(numerical_2, "DEFINITION-REF")
                definition_2.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
                definition_2.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfEntry/LinIfDelay"
                value_2 = etree.SubElement(numerical_2, "VALUE").text = "0.010"
                references = etree.SubElement(lin_entry0, "REFERENCE-VALUES")
                ecuc_ref_value_1 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
                definition = etree.SubElement(ecuc_ref_value_1, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/LinIf/LinIfGlobalConfig/LinIfChannel/LinIfScheduleTable/LinIfEntry/LinIfFrameRef"
                value = etree.SubElement(ecuc_ref_value_1, "VALUE-REF")
                value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value.text = "/LinIf/LinIf/LinIfGlobalConfig/" + nad_network.group(0) + "_Channel/LinIfFrame_REQ_" + nad_network.group(0) + "_1P3"

    # generate data
    pretty_xml = prettify_xml(rootLinIf)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/LinIf.epc', encoding='UTF-8', xml_declaration=True, method="xml", doctype = "<!-- XML file generated by COM_Configurator-18 -->")
    return


def BswM_config(file_list, output_path, logger):
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    tables = []
    networks = []
    for file in file_list:
        if file.endswith('.arxml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            elements = root.findall(".//{http://autosar.org/schema/r4.0}LIN-SCHEDULE-TABLE")
            for elem in elements:
                obj_table = {}
                obj_table['NAME'] = elem.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text
                obj_table['CATEGORY'] = elem.find(".//{http://autosar.org/schema/r4.0}CATEGORY").text
                obj_table['LIN'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                tables.append(obj_table)

    # check that for each LIN-CLUSTER there is at least one schedule-table of category REQUEST_DIAG and one of category RESPONSE_DIAG
    network_list = []
    for table in tables:
        if table['LIN'] not in network_list:
            network_list.append(table['LIN'])

    for network in network_list:
        obj_network = {}
        obj_network['NAME'] = network
        obj_network['RESPONSE'] = False
        obj_network['REQUEST'] = False
        networks.append(obj_network)

    for table in tables:
        for network in networks:
            if table['LIN'] == network['NAME']:
                if table['CATEGORY'] == "RESPONSE_DIAG":
                    network['RESPONSE'] = True
                if table['CATEGORY'] == "REQUEST_DIAG":
                    network['REQUEST'] = True

    # TRS.COMCONF.GEN.0137(0)
    for network in networks[:]:
        if not network['RESPONSE']:
            logger.error("LIN-CLUSTER " + network['NAME'] + " does not have a SCHEDULE-TABLE of type RESPONSE_DIAG")
            networks.remove(network)
            for table in tables[:]:
                if table['LIN'] == network['NAME']:
                    tables.remove(table)
    for network in networks[:]:
        if not network['REQUEST']:
            logger.error("LIN-CLUSTER " + network['NAME'] + " does not have a SCHEDULE-TABLE of type REQUEST_DIAG")
            networks.remove(network)
            for table in tables[:]:
                if table['LIN'] == network['NAME']:
                    tables.remove(table)

    # create ouput file: BswM.epc
    rootBswM = etree.Element('AUTOSAR', {attr_qname: 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd'}, nsmap=NSMAP)
    packages = etree.SubElement(rootBswM, 'AR-PACKAGES')
    package = etree.SubElement(packages, 'AR-PACKAGE')
    short_name = etree.SubElement(package, 'SHORT-NAME').text = "BswM"
    elements = etree.SubElement(package, 'ELEMENTS')
    ecuc_module = etree.SubElement(elements, 'ECUC-MODULE-CONFIGURATION-VALUES')
    short_name = etree.SubElement(ecuc_module, 'SHORT-NAME').text = "BswM"
    definition = etree.SubElement(ecuc_module, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-MODULE-DEF"
    definition.text = "/AUTOSAR/EcuDefs/BswM"
    description = etree.SubElement(ecuc_module, 'IMPLEMENTATION-CONFIG-VARIANT').text = "VARIANT-PRE-COMPILE"
    containers = etree.SubElement(ecuc_module, 'CONTAINERS')
    ecuc_general = etree.SubElement(containers, "ECUC-CONTAINER-VALUE")
    # TRS.COMCONF.GEN.0136(0)
    short_name = etree.SubElement(ecuc_general, "SHORT-NAME").text = "BswMConfig_0"
    definition_general = etree.SubElement(ecuc_general, "DEFINITION-REF")
    definition_general.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition_general.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig"
    subcontainer_master = etree.SubElement(ecuc_general, "SUB-CONTAINERS")
    ecuc_arbitration = etree.SubElement(subcontainer_master, "ECUC-CONTAINER-VALUE")
    short_name = etree.SubElement(ecuc_arbitration, "SHORT-NAME").text = "BswMArbitration"
    definition = etree.SubElement(ecuc_arbitration, "DEFINITION-REF")
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration"
    subcontainer_arbitration = etree.SubElement(ecuc_arbitration, "SUB-CONTAINERS")
    ecuc_control = etree.SubElement(subcontainer_master, "ECUC-CONTAINER-VALUE")
    short_name = etree.SubElement(ecuc_control, "SHORT-NAME").text = "BswMModeControl"
    definition = etree.SubElement(ecuc_control, "DEFINITION-REF")
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl"
    subcontainer_control = etree.SubElement(ecuc_control, "SUB-CONTAINERS")
    for table in tables:
        if table['CATEGORY'] in ["RESPONSE_DIAG", "REQUEST_DIAG", "FUNCTIONAL"]:
            container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
            # TRS.COMCONF.GEN.0138(0)
            short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMLogicalExpression_BswMRule_CurrentSchedule_" + table["LIN"] + "_" + table["NAME"]
            definition = etree.SubElement(container, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMLogicalExpression"
            reference_values = etree.SubElement(container, "REFERENCE-VALUES")
            reference = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(reference, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-CHOICE-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMLogicalExpression/BswMArgumentRef"
            value = etree.SubElement(reference, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/BswM/BswM/BswMConfig_0/BswMArbitration/BswMModeCondition_LinScheduleTable_" + table["LIN"] + "_" + table["NAME"]

            # TRS.COMCONF.GEN.0139(0)
            container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMModeCondition_LinScheduleTable_" + table["LIN"] + "_" + table["NAME"]
            definition = etree.SubElement(container, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition"
            parameter = etree.SubElement(container, "PARAMETER-VALUES")
            textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
            definition = etree.SubElement(textual_param, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionType"
            value = etree.SubElement(textual_param, "VALUE").text = "BSWM_EQUALS"
            reference_values = etree.SubElement(container, "REFERENCE-VALUES")
            reference = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(reference, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionMode"
            value = etree.SubElement(reference, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/BswM/BswM/BswMConfig_0/BswMArbitration/BswMScheduleIndication_" + table["LIN"] + "_" + table["NAME"]
            subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
            container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMConditionValue"
            definition1 = etree.SubElement(container1, "DEFINITION-REF")
            definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
            definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionValue"
            subcontainers1 = etree.SubElement(container1, "SUB-CONTAINERS")
            container2 = etree.SubElement(subcontainers1, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container2, "SHORT-NAME").text = "BswMConditionValue"
            definition2 = etree.SubElement(container2, "DEFINITION-REF")
            definition2.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition2.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionValue/BswMBswMode"
            parameters2 = etree.SubElement(container2, "PARAMETER-VALUES")
            textual_param2 = etree.SubElement(parameters2, "ECUC-TEXTUAL-PARAM-VALUE")
            definition = etree.SubElement(textual_param2, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionValue/BswMBswMode/BswMBswRequestedMode"
            value = etree.SubElement(textual_param2, "VALUE").text = "LinSMConf_LinSMSchedule_" + table["LIN"] + "_" + table["NAME"]

            # TRS.COMCONF.GEN.0140(0)
            container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMScheduleIndication_" + table["LIN"] + "_" + table["NAME"]
            definition = etree.SubElement(container, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort"
            parameter = etree.SubElement(container, "PARAMETER-VALUES")
            textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
            definition = etree.SubElement(textual_param, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMRequestProcessing"
            value = etree.SubElement(textual_param, "VALUE").text = "BSWM_IMMEDIATE"
            subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
            container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMModeRequestSource"
            definition1 = etree.SubElement(container1, "DEFINITION-REF")
            definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
            definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeRequestSource"
            subcontainers1 = etree.SubElement(container1, "SUB-CONTAINERS")
            container2 = etree.SubElement(subcontainers1, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container2, "SHORT-NAME").text = "BswMModeRequestSource"
            definition2 = etree.SubElement(container2, "DEFINITION-REF")
            definition2.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition2.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeRequestSource/BswMLinScheduleIndication"
            references2 = etree.SubElement(container2, "REFERENCE-VALUES")
            reference = etree.SubElement(references2, 'ECUC-REFERENCE-VALUE')
            definition = etree.SubElement(reference, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-SYMBOLIC-NAME-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeRequestSource/BswMLinScheduleIndication/BswMLinScheduleRef"
            value = etree.SubElement(reference, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/LinSM/LinSM/LinSMConfigSet/" + table["LIN"] + "/" + table["NAME"]

            # TRS.COMCONF.GEN.0141(0)
            container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMRule_CurrentSchedule_" + table["LIN"] + "_" + table["NAME"]
            definition = etree.SubElement(container, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule"
            parameter = etree.SubElement(container, "PARAMETER-VALUES")
            numerical_param = etree.SubElement(parameter, "ECUC-NUMERICAL-PARAM-VALUE")
            definition = etree.SubElement(numerical_param, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMNestedExecutionOnly"
            value = etree.SubElement(numerical_param, "VALUE").text = "0"
            textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
            definition = etree.SubElement(textual_param, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMRuleInitState"
            value = etree.SubElement(textual_param, "VALUE").text = "BSWM_FALSE"
            reference_values = etree.SubElement(container, "REFERENCE-VALUES")
            reference1 = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(reference1, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMRuleExpressionRef"
            value = etree.SubElement(reference1, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/BswM/BswM/BswMConfig_0/BswMArbitration/BswMLogicalExpression_BswMRule_CurrentSchedule_" + table["LIN"] + "_" + table["NAME"]
            reference2 = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(reference2, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMRuleTrueActionList"
            value = etree.SubElement(reference2, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/BswM/BswM/BswMConfig_0/BswMModeControl/BswMActionList_BswMRule_CurrentSchedule_" + table["LIN"] + "_" + table["NAME"] + "_TrueActionList"

            # TRS.COMCONF.GEN.0142(0)
            container = etree.SubElement(subcontainer_control, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMActionList_BswMRule_CurrentSchedule_" + table["LIN"] + "_" + table["NAME"] + "_TrueActionList"
            definition = etree.SubElement(container, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList"
            parameter = etree.SubElement(container, "PARAMETER-VALUES")
            textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
            definition = etree.SubElement(textual_param, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListExecution"
            value = etree.SubElement(textual_param, "VALUE").text = "BSWM_CONDITION"
            subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
            container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMActionList_" + table["LIN"] + "_" + table["NAME"]
            definition1 = etree.SubElement(container1, "DEFINITION-REF")
            definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
            definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem"
            parameter = etree.SubElement(container1, "PARAMETER-VALUES")
            numerical_param1 = etree.SubElement(parameter, "ECUC-NUMERICAL-PARAM-VALUE")
            definition = etree.SubElement(numerical_param1, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem/BswMAbortOnFail"
            value = etree.SubElement(numerical_param1, "VALUE").text = "0"
            textual_param = etree.SubElement(parameter, "ECUC-NUMERICAL-PARAM-VALUE")
            definition = etree.SubElement(textual_param, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem/BswMActionListItemIndex"
            value = etree.SubElement(textual_param, "VALUE").text = "0"
            references = etree.SubElement(container1, "REFERENCE-VALUES")
            reference = etree.SubElement(references, 'ECUC-REFERENCE-VALUE')
            definition = etree.SubElement(reference, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-CHOICE-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem/BswMActionListItemRef"
            value = etree.SubElement(reference, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/BswM/BswM/BswMConfig_0/BswMModeControl/BswMAction_BswMUserCallout_Confirmation_" + table["LIN"] + "_" + table["NAME"]

        # TRS.COMCONF.GEN.0143(0)
        if table['CATEGORY'] == "RESPONSE_DIAG":
            container = etree.SubElement(subcontainer_control, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMAction_BswMUserCallout_Confirmation_" + table["LIN"] + "_" + table["NAME"]
            definition = etree.SubElement(container, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction"
            subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
            container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMAvailableActions"
            definition1 = etree.SubElement(container1, "DEFINITION-REF")
            definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
            definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions"
            subcontainers1 = etree.SubElement(container1, "SUB-CONTAINERS")
            container2 = etree.SubElement(subcontainers1, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container2, "SHORT-NAME").text = "BswMAvailableActions"
            definition2 = etree.SubElement(container2, "DEFINITION-REF")
            definition2.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition2.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions/BswMUserCallout"
            parameters2 = etree.SubElement(container2, "PARAMETER-VALUES")
            textual_param2 = etree.SubElement(parameters2, "ECUC-TEXTUAL-PARAM-VALUE")
            definition = etree.SubElement(textual_param2, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions/BswMUserCallout/BswMUserCalloutFunction"
            value = etree.SubElement(textual_param2, "VALUE").text = "SSR_ScheduleRequestConfirmation(ComMConf_ComMChannel_" + table["LIN"] + ",LinSMConf_LinSMSchedule_" + table["LIN"] + "_" + table["NAME"] + ",LINTP_DIAG_RESPONSE)"

            # TRS.COMCONF.GEN.0144(0)
            container = etree.SubElement(subcontainer_control, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMAction_BswMUserCallout_" + table["LIN"] + "_DiagResp"
            definition = etree.SubElement(container, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction"
            subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
            container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMAvailableActions"
            definition1 = etree.SubElement(container1, "DEFINITION-REF")
            definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
            definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions"
            subcontainers1 = etree.SubElement(container1, "SUB-CONTAINERS")
            container2 = etree.SubElement(subcontainers1, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container2, "SHORT-NAME").text = "BswMAvailableActions"
            definition2 = etree.SubElement(container2, "DEFINITION-REF")
            definition2.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition2.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions/BswMUserCallout"
            parameters2 = etree.SubElement(container2, "PARAMETER-VALUES")
            textual_param2 = etree.SubElement(parameters2, "ECUC-TEXTUAL-PARAM-VALUE")
            definition = etree.SubElement(textual_param2, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions/BswMUserCallout/BswMUserCalloutFunction"
            value = etree.SubElement(textual_param2, "VALUE").text = "SSR_DiagScheduleResponse(ComMConf_ComMChannel_" + table["LIN"] + ",LinSMConf_LinSMSchedule_" + table["LIN"] + "_" + table["NAME"] + ")"

        # TRS.COMCONF.GEN.0145(0)
        if table['CATEGORY'] == "FUNCTIONAL":
            container = etree.SubElement(subcontainer_control, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMAction_BswMUserCallout_Confirmation_" + table["LIN"] + "_" + table["NAME"]
            definition = etree.SubElement(container, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction"
            subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
            container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMAvailableActions"
            definition1 = etree.SubElement(container1, "DEFINITION-REF")
            definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
            definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions"
            subcontainers1 = etree.SubElement(container1, "SUB-CONTAINERS")
            container2 = etree.SubElement(subcontainers1, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container2, "SHORT-NAME").text = "BswMAvailableActions"
            definition2 = etree.SubElement(container2, "DEFINITION-REF")
            definition2.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition2.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions/BswMUserCallout"
            parameters2 = etree.SubElement(container2, "PARAMETER-VALUES")
            textual_param2 = etree.SubElement(parameters2, "ECUC-TEXTUAL-PARAM-VALUE")
            definition = etree.SubElement(textual_param2, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions/BswMUserCallout/BswMUserCalloutFunction"
            value = etree.SubElement(textual_param2, "VALUE").text = "SSR_ScheduleRequestConfirmation(ComMConf_ComMChannel_" + table["LIN"] + ",LinSMConf_LinSMSchedule_" + table["LIN"] + "_" + table["NAME"] + ",LINTP_APPLICATIVE_SCHEDULE)"

        # TRS.COMCONF.GEN.0146(0)
        if table['CATEGORY'] == "REQUEST_DIAG":
            container = etree.SubElement(subcontainer_control, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMAction_BswMUserCallout_Confirmation_" + table["LIN"] + "_" + table["NAME"]
            definition = etree.SubElement(container, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction"
            subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
            container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMAvailableActions"
            definition1 = etree.SubElement(container1, "DEFINITION-REF")
            definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
            definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions"
            subcontainers1 = etree.SubElement(container1, "SUB-CONTAINERS")
            container2 = etree.SubElement(subcontainers1, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container2, "SHORT-NAME").text = "BswMAvailableActions"
            definition2 = etree.SubElement(container2, "DEFINITION-REF")
            definition2.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition2.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions/BswMUserCallout"
            parameters2 = etree.SubElement(container2, "PARAMETER-VALUES")
            textual_param2 = etree.SubElement(parameters2, "ECUC-TEXTUAL-PARAM-VALUE")
            definition = etree.SubElement(textual_param2, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions/BswMUserCallout/BswMUserCalloutFunction"
            value = etree.SubElement(textual_param2, "VALUE").text = "SSR_ScheduleRequestConfirmation(ComMConf_ComMChannel_" + table["LIN"] + ",LinSMConf_LinSMSchedule_" + table["LIN"] + "_" + table["NAME"] + ",LINTP_DIAG_REQUEST)"

            # TRS.COMCONF.GEN.0147(0)
            container = etree.SubElement(subcontainer_control, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMAction_BswMUserCallout_" + table["LIN"] + "_DiagReq"
            definition = etree.SubElement(container, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction"
            subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
            container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMAvailableActions"
            definition1 = etree.SubElement(container1, "DEFINITION-REF")
            definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
            definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions"
            subcontainers1 = etree.SubElement(container1, "SUB-CONTAINERS")
            container2 = etree.SubElement(subcontainers1, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container2, "SHORT-NAME").text = "BswMAvailableActions"
            definition2 = etree.SubElement(container2, "DEFINITION-REF")
            definition2.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition2.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions/BswMUserCallout"
            parameters2 = etree.SubElement(container2, "PARAMETER-VALUES")
            textual_param2 = etree.SubElement(parameters2, "ECUC-TEXTUAL-PARAM-VALUE")
            definition = etree.SubElement(textual_param2, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions/BswMUserCallout/BswMUserCalloutFunction"
            value = etree.SubElement(textual_param2, "VALUE").text = "SSR_DiagScheduleRequest(ComMConf_ComMChannel_" + table["LIN"] + ",LinSMConf_LinSMSchedule_" + table["LIN"] + "_" + table["NAME"] + ")"

    # TRS.COMCONF.GEN.0148(0)
    for network in networks:
        container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMLogicalExpression_BswMRule_LinTp_" + network["NAME"] + "_Applicative"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMLogicalExpression"
        reference_values = etree.SubElement(container, "REFERENCE-VALUES")
        reference = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
        definition = etree.SubElement(reference, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-CHOICE-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMLogicalExpression/BswMArgumentRef"
        value = etree.SubElement(reference, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/BswM/BswM/BswMConfig_0/BswMArbitration/BswMModeCondition_BswMModeRequestPort_" + network["NAME"] + "_LINTP_APPLICATIVE_SCHEDULE"

        # TRS.COMCONF.GEN.0149(0)
        container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMLogicalExpression_BswMRule_LinTp_" + network["NAME"] + "_DiagReq"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMLogicalExpression"
        reference_values = etree.SubElement(container, "REFERENCE-VALUES")
        reference = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
        definition = etree.SubElement(reference, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-CHOICE-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMLogicalExpression/BswMArgumentRef"
        value = etree.SubElement(reference, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/BswM/BswM/BswMConfig_0/BswMArbitration/BswMModeCondition_BswMModeRequestPort_" + network["NAME"] + "_LINTP_DIAG_REQUEST"

        # TRS.COMCONF.GEN.0150(0)
        container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMLogicalExpression_BswMRule_LinTp_" + network["NAME"] + "_DiagResp"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMLogicalExpression"
        reference_values = etree.SubElement(container, "REFERENCE-VALUES")
        reference = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
        definition = etree.SubElement(reference, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-CHOICE-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMLogicalExpression/BswMArgumentRef"
        value = etree.SubElement(reference, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/BswM/BswM/BswMConfig_0/BswMArbitration/BswMModeCondition_BswMModeRequestPort_" + network["NAME"] + "_LINTP_DIAG_RESPONSE"

        # TRS.COMCONF.GEN.0151(0)
        container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMModeCondition_BswMModeRequestPort_" + network["NAME"] + "_LINTP_APPLICATIVE_SCHEDULE"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition"
        parameter = etree.SubElement(container, "PARAMETER-VALUES")
        textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionType"
        value = etree.SubElement(textual_param, "VALUE").text = "BSWM_EQUALS"
        reference_values = etree.SubElement(container, "REFERENCE-VALUES")
        reference = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
        definition = etree.SubElement(reference, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-CHOICE-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionMode"
        value = etree.SubElement(reference, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/BswM/BswM/BswMConfig_0/BswMArbitration/BswMModeRequestPort_" + network["NAME"] + "_Applicative"
        subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
        container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMConditionValue"
        definition1 = etree.SubElement(container1, "DEFINITION-REF")
        definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
        definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionValue"
        subcontainers1 = etree.SubElement(container1, "SUB-CONTAINERS")
        container2 = etree.SubElement(subcontainers1, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container2, "SHORT-NAME").text = "BswMConditionValue"
        definition2 = etree.SubElement(container2, "DEFINITION-REF")
        definition2.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition2.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionValue/BswMBswMode"
        parameters2 = etree.SubElement(container2, "PARAMETER-VALUES")
        textual_param2 = etree.SubElement(parameters2, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param2, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionValue/BswMBswMode/BswMBswRequestedMode"
        value = etree.SubElement(textual_param2, "VALUE").text = "LINTP_APPLICATIVE_SCHEDULE"

        # TRS.COMCONF.GEN.0152(0)
        container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMModeCondition_BswMModeRequestPort_" + network["NAME"] + "_LINTP_DIAG_REQUEST"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition"
        parameter = etree.SubElement(container, "PARAMETER-VALUES")
        textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionType"
        value = etree.SubElement(textual_param, "VALUE").text = "BSWM_EQUALS"
        reference_values = etree.SubElement(container, "REFERENCE-VALUES")
        reference = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
        definition = etree.SubElement(reference, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionMode"
        value = etree.SubElement(reference, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/BswM/BswM/BswMConfig_0/BswMArbitration/BswMModeRequestPort_" + network["NAME"] + "_DiagReq"
        subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
        container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMConditionValue"
        definition1 = etree.SubElement(container1, "DEFINITION-REF")
        definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
        definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionValue"
        subcontainers1 = etree.SubElement(container1, "SUB-CONTAINERS")
        container2 = etree.SubElement(subcontainers1, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container2, "SHORT-NAME").text = "BswMConditionValue"
        definition2 = etree.SubElement(container2, "DEFINITION-REF")
        definition2.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition2.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionValue/BswMBswMode"
        parameters2 = etree.SubElement(container2, "PARAMETER-VALUES")
        textual_param2 = etree.SubElement(parameters2, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param2, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionValue/BswMBswMode/BswMBswRequestedMode"
        value = etree.SubElement(textual_param2, "VALUE").text = "LINTP_DIAG_REQUEST"

        # TRS.COMCONF.GEN.0153(0)
        container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMModeCondition_BswMModeRequestPort_" + network["NAME"] + "_LINTP_DIAG_RESPONSE"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition"
        parameter = etree.SubElement(container, "PARAMETER-VALUES")
        textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionType"
        value = etree.SubElement(textual_param, "VALUE").text = "BSWM_EQUALS"
        reference_values = etree.SubElement(container, "REFERENCE-VALUES")
        reference = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
        definition = etree.SubElement(reference, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionMode"
        value = etree.SubElement(reference, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/BswM/BswM/BswMConfig_0/BswMArbitration/BswMModeRequestPort_" + network["NAME"] + "_DiagResp"
        subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
        container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMConditionValue"
        definition1 = etree.SubElement(container1, "DEFINITION-REF")
        definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
        definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionValue"
        subcontainers1 = etree.SubElement(container1, "SUB-CONTAINERS")
        container2 = etree.SubElement(subcontainers1, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container2, "SHORT-NAME").text = "BswMConditionValue"
        definition2 = etree.SubElement(container2, "DEFINITION-REF")
        definition2.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition2.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionValue/BswMBswMode"
        parameters2 = etree.SubElement(container2, "PARAMETER-VALUES")
        textual_param2 = etree.SubElement(parameters2, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param2, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeCondition/BswMConditionValue/BswMBswMode/BswMBswRequestedMode"
        value = etree.SubElement(textual_param2, "VALUE").text = "LINTP_DIAG_RESPONSE"

        # TRS.COMCONF.GEN.0154(0)
        container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMModeRequestPort_" + network["NAME"] + "_Applicative"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort"
        parameter = etree.SubElement(container, "PARAMETER-VALUES")
        textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMRequestProcessing"
        value = etree.SubElement(textual_param, "VALUE").text = "BSWM_IMMEDIATE"
        subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
        container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMModeInitValue"
        definition1 = etree.SubElement(container1, "DEFINITION-REF")
        definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
        definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeInitValue/BswMBswModeInitValue"
        parameter = etree.SubElement(container1, "PARAMETER-VALUES")
        textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeInitValue/BswMBswModeInitValue/BswMBswModeInitValueMode"
        value = etree.SubElement(textual_param, "VALUE").text = "LINTP_APPLICATIVE_SCHEDULE"
        container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMModeRequestSource"
        definition1 = etree.SubElement(container1, "DEFINITION-REF")
        definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
        definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeRequestSource"
        subcontainers1 = etree.SubElement(container1, "SUB-CONTAINERS")
        container2 = etree.SubElement(subcontainers1, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container2, "SHORT-NAME").text = "BswMModeRequestSource"
        definition2 = etree.SubElement(container2, "DEFINITION-REF")
        definition2.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition2.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeRequestSource/BswMLinTpModeRequest"
        references2 = etree.SubElement(container2, "REFERENCE-VALUES")
        reference = etree.SubElement(references2, 'ECUC-REFERENCE-VALUE')
        definition = etree.SubElement(reference, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-SYMBOLIC-NAME-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeRequestSource/BswMLinTpModeRequest/BswMLinTpChannelRef"
        value = etree.SubElement(reference, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/LinIf/LinIf/LinIfGlobalConfig/" + network["NAME"] + "_Channel"

        # TRS.COMCONF.GEN.0155(0)
        container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMModeRequestPort_" + network["NAME"] + "_DiagReq"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort"
        parameter = etree.SubElement(container, "PARAMETER-VALUES")
        textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMRequestProcessing"
        value = etree.SubElement(textual_param, "VALUE").text = "BSWM_IMMEDIATE"
        subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
        container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMModeInitValue"
        definition1 = etree.SubElement(container1, "DEFINITION-REF")
        definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
        definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeInitValue/BswMBswModeInitValue"
        parameter = etree.SubElement(container1, "PARAMETER-VALUES")
        textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeInitValue/BswMBswModeInitValue/BswMBswModeInitValueMode"
        value = etree.SubElement(textual_param, "VALUE").text = "LINTP_APPLICATIVE_SCHEDULE"
        container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMModeRequestSource"
        definition1 = etree.SubElement(container1, "DEFINITION-REF")
        definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
        definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeRequestSource"
        subcontainers1 = etree.SubElement(container1, "SUB-CONTAINERS")
        container2 = etree.SubElement(subcontainers1, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container2, "SHORT-NAME").text = "BswMModeRequestSource"
        definition2 = etree.SubElement(container2, "DEFINITION-REF")
        definition2.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition2.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeRequestSource/BswMLinTpModeRequest"
        references2 = etree.SubElement(container2, "REFERENCE-VALUES")
        reference = etree.SubElement(references2, 'ECUC-REFERENCE-VALUE')
        definition = etree.SubElement(reference, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-SYMBOLIC-NAME-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeRequestSource/BswMLinTpModeRequest/BswMLinTpChannelRef"
        value = etree.SubElement(reference, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/LinIf/LinIf/LinIfGlobalConfig/" + network["NAME"] + "_Channel"

        # TRS.COMCONF.GEN.0156(0)
        container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMModeRequestPort_" + network["NAME"] + "_DiagResp"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort"
        parameter = etree.SubElement(container, "PARAMETER-VALUES")
        textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMRequestProcessing"
        value = etree.SubElement(textual_param, "VALUE").text = "BSWM_IMMEDIATE"
        subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
        container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMModeInitValue"
        definition1 = etree.SubElement(container1, "DEFINITION-REF")
        definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
        definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeInitValue/BswMBswModeInitValue"
        parameter = etree.SubElement(container1, "PARAMETER-VALUES")
        textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeInitValue/BswMBswModeInitValue/BswMBswModeInitValueMode"
        value = etree.SubElement(textual_param, "VALUE").text = "LINTP_DIAG_REQUEST"
        container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMModeRequestSource"
        definition1 = etree.SubElement(container1, "DEFINITION-REF")
        definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
        definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeRequestSource"
        subcontainers1 = etree.SubElement(container1, "SUB-CONTAINERS")
        container2 = etree.SubElement(subcontainers1, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container2, "SHORT-NAME").text = "BswMModeRequestSource"
        definition2 = etree.SubElement(container2, "DEFINITION-REF")
        definition2.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition2.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeRequestSource/BswMLinTpModeRequest"
        references2 = etree.SubElement(container2, "REFERENCE-VALUES")
        reference = etree.SubElement(references2, 'ECUC-REFERENCE-VALUE')
        definition = etree.SubElement(reference, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-SYMBOLIC-NAME-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMModeRequestPort/BswMModeRequestSource/BswMLinTpModeRequest/BswMLinTpChannelRef"
        value = etree.SubElement(reference, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/LinIf/LinIf/LinIfGlobalConfig/" + network["NAME"] + "_Channel"

        # TRS.COMCONF.GEN.0157(0)
        container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMRule_LinTp_" + network["NAME"] + "_Applicative"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule"
        parameter = etree.SubElement(container, "PARAMETER-VALUES")
        numerical_param = etree.SubElement(parameter, "ECUC-NUMERICAL-PARAM-VALUE")
        definition = etree.SubElement(numerical_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMNestedExecutionOnly"
        value = etree.SubElement(numerical_param, "VALUE").text = "0"
        textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMRuleInitState"
        value = etree.SubElement(textual_param, "VALUE").text = "BSWM_FALSE"
        reference_values = etree.SubElement(container, "REFERENCE-VALUES")
        reference1 = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
        definition = etree.SubElement(reference1, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMRuleExpressionRef"
        value = etree.SubElement(reference1, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/BswM/BswM/BswMConfig_0/BswMArbitration/BswMLogicalExpression_BswMRule_LinTp_" + network["NAME"] + "_Applicative"
        reference2 = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
        definition = etree.SubElement(reference2, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMRuleTrueActionList"
        value = etree.SubElement(reference2, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/BswM/BswM/BswMConfig_0/BswMModeControl/BswMActionList_BswMRule_LinTp_" + network["NAME"] + "_Applicative_TrueActionList"

        # TRS.COMCONF.GEN.0158(0)
        container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMRule_LinTp_" + network["NAME"] + "_DiagReq"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule"
        parameter = etree.SubElement(container, "PARAMETER-VALUES")
        numerical_param = etree.SubElement(parameter, "ECUC-NUMERICAL-PARAM-VALUE")
        definition = etree.SubElement(numerical_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMNestedExecutionOnly"
        value = etree.SubElement(numerical_param, "VALUE").text = "0"
        textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMRuleInitState"
        value = etree.SubElement(textual_param, "VALUE").text = "BSWM_FALSE"
        reference_values = etree.SubElement(container, "REFERENCE-VALUES")
        reference1 = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
        definition = etree.SubElement(reference1, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMRuleExpressionRef"
        value = etree.SubElement(reference1, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/BswM/BswM/BswMConfig_0/BswMArbitration/BswMLogicalExpression_BswMRule_LinTp_" + network["NAME"] + "_DiagReq"
        reference2 = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
        definition = etree.SubElement(reference2, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMRuleTrueActionList"
        value = etree.SubElement(reference2, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/BswM/BswM/BswMConfig_0/BswMModeControl/BswMActionList_BswMRule_LinTp_" + network["NAME"] + "_DiagReq_TrueActionList"

        # TRS.COMCONF.GEN.0159(0)
        container = etree.SubElement(subcontainer_arbitration, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMRule_LinTp_" + network["NAME"] + "_DiagResp"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule"
        parameter = etree.SubElement(container, "PARAMETER-VALUES")
        numerical_param = etree.SubElement(parameter, "ECUC-NUMERICAL-PARAM-VALUE")
        definition = etree.SubElement(numerical_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMNestedExecutionOnly"
        value = etree.SubElement(numerical_param, "VALUE").text = "0"
        textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMRuleInitState"
        value = etree.SubElement(textual_param, "VALUE").text = "BSWM_FALSE"
        reference_values = etree.SubElement(container, "REFERENCE-VALUES")
        reference1 = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
        definition = etree.SubElement(reference1, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMRuleExpressionRef"
        value = etree.SubElement(reference1, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/BswM/BswM/BswMConfig_0/BswMArbitration/BswMLogicalExpression_BswMRule_LinTp_" + network["NAME"] + "_DiagResp"
        reference2 = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
        definition = etree.SubElement(reference2, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMArbitration/BswMRule/BswMRuleTrueActionList"
        value = etree.SubElement(reference2, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/BswM/BswM/BswMConfig_0/BswMModeControl/BswMActionList_BswMRule_LinTp_" + network["NAME"] + "_DiagResp_TrueActionList"

        # TRS.COMCONF.GEN.0160(0)
        container = etree.SubElement(subcontainer_control, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMActionList_BswMRule_LinTp_" + network["NAME"] + "_Applicative_TrueActionList"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList"
        parameter = etree.SubElement(container, "PARAMETER-VALUES")
        textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListExecution"
        value = etree.SubElement(textual_param, "VALUE").text = "BSWM_CONDITION"
        subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
        container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMActionList_" + network["NAME"] + "_Applicative"
        definition1 = etree.SubElement(container1, "DEFINITION-REF")
        definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
        definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem"
        parameter = etree.SubElement(container1, "PARAMETER-VALUES")
        numerical_param1 = etree.SubElement(parameter, "ECUC-NUMERICAL-PARAM-VALUE")
        definition = etree.SubElement(numerical_param1, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem/BswMAbortOnFail"
        value = etree.SubElement(numerical_param1, "VALUE").text = "0"
        textual_param = etree.SubElement(parameter, "ECUC-NUMERICAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem/BswMActionListItemIndex"
        value = etree.SubElement(textual_param, "VALUE").text = "0"
        references = etree.SubElement(container1, "REFERENCE-VALUES")
        reference = etree.SubElement(references, 'ECUC-REFERENCE-VALUE')
        definition = etree.SubElement(reference, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-CHOICE-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem/BswMActionListItemRef"
        value = etree.SubElement(reference, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/BswM/BswM/BswMConfig_0/BswMModeControl/BswMAction_BswMUserCallout_" + network["NAME"] + "_Applicative"

        # TRS.COMCONF.GEN.0161(0)
        container = etree.SubElement(subcontainer_control, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMActionList_BswMRule_LinTp_" + network["NAME"] + "_DiagReq_TrueActionList"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList"
        parameter = etree.SubElement(container, "PARAMETER-VALUES")
        textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListExecution"
        value = etree.SubElement(textual_param, "VALUE").text = "BSWM_CONDITION"
        subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
        container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMActionList_" + network["NAME"] + "_DiagReq"
        definition1 = etree.SubElement(container1, "DEFINITION-REF")
        definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
        definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem"
        parameter = etree.SubElement(container1, "PARAMETER-VALUES")
        numerical_param1 = etree.SubElement(parameter, "ECUC-NUMERICAL-PARAM-VALUE")
        definition = etree.SubElement(numerical_param1, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem/BswMAbortOnFail"
        value = etree.SubElement(numerical_param1, "VALUE").text = "0"
        textual_param = etree.SubElement(parameter, "ECUC-NUMERICAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem/BswMActionListItemIndex"
        value = etree.SubElement(textual_param, "VALUE").text = "0"
        references = etree.SubElement(container1, "REFERENCE-VALUES")
        reference = etree.SubElement(references, 'ECUC-REFERENCE-VALUE')
        definition = etree.SubElement(reference, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-CHOICE-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem/BswMActionListItemRef"
        value = etree.SubElement(reference, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/BswM/BswM/BswMConfig_0/BswMModeControl/BswMAction_BswMUserCallout_" + network["NAME"] + "_DiagReq"

        # TRS.COMCONF.GEN.0162(0)
        container = etree.SubElement(subcontainer_control, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMActionList_BswMRule_LinTp_" + network["NAME"] + "_DiagResp_TrueActionList"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList"
        parameter = etree.SubElement(container, "PARAMETER-VALUES")
        textual_param = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListExecution"
        value = etree.SubElement(textual_param, "VALUE").text = "BSWM_CONDITION"
        subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
        container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMActionList_" + network["NAME"] + "_DiagResp"
        definition1 = etree.SubElement(container1, "DEFINITION-REF")
        definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
        definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem"
        parameter = etree.SubElement(container1, "PARAMETER-VALUES")
        numerical_param1 = etree.SubElement(parameter, "ECUC-NUMERICAL-PARAM-VALUE")
        definition = etree.SubElement(numerical_param1, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem/BswMAbortOnFail"
        value = etree.SubElement(numerical_param1, "VALUE").text = "0"
        textual_param = etree.SubElement(parameter, "ECUC-NUMERICAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem/BswMActionListItemIndex"
        value = etree.SubElement(textual_param, "VALUE").text = "0"
        references = etree.SubElement(container1, "REFERENCE-VALUES")
        reference = etree.SubElement(references, 'ECUC-REFERENCE-VALUE')
        definition = etree.SubElement(reference, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-CHOICE-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMActionList/BswMActionListItem/BswMActionListItemRef"
        value = etree.SubElement(reference, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/BswM/BswM/BswMConfig_0/BswMModeControl/BswMAction_BswMUserCallout_" + network["NAME"] + "_DiagResp"

        # TRS.COMCONF.GEN.0163(0)
        container = etree.SubElement(subcontainer_control, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container, "SHORT-NAME").text = "BswMAction_BswMUserCallout_" + network["NAME"] + "_Applicative"
        definition = etree.SubElement(container, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction"
        subcontainers = etree.SubElement(container, "SUB-CONTAINERS")
        container1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container1, "SHORT-NAME").text = "BswMAvailableActions"
        definition1 = etree.SubElement(container1, "DEFINITION-REF")
        definition1.attrib['DEST'] = "ECUC-CHOICE-CONTAINER-DEF"
        definition1.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions"
        subcontainers1 = etree.SubElement(container1, "SUB-CONTAINERS")
        container2 = etree.SubElement(subcontainers1, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container2, "SHORT-NAME").text = "BswMAvailableActions"
        definition2 = etree.SubElement(container2, "DEFINITION-REF")
        definition2.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition2.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions/BswMUserCallout"
        parameters2 = etree.SubElement(container2, "PARAMETER-VALUES")
        textual_param2 = etree.SubElement(parameters2, "ECUC-TEXTUAL-PARAM-VALUE")
        definition = etree.SubElement(textual_param2, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/BswM/BswMConfig/BswMModeControl/BswMAction/BswMAvailableActions/BswMUserCallout/BswMUserCalloutFunction"
        value = etree.SubElement(textual_param2, "VALUE").text = "SSR_AppLicativeScheduleRequest(ComMConf_ComMChannel_" + network["NAME"] + ")"

    # generate data
    pretty_xml = prettify_xml(rootBswM)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/BswM.epc', encoding='UTF-8', xml_declaration=True, method="xml", doctype = "<!-- XML file generated by COM_Configurator-18 -->")
    return


def CFHM_script(file_list, output_path, logger):
    fault_frames = []
    can_frames = []
    can_frames_triggering = []
    existing_ipdus = []
    for file in file_list:
        if file.endswith('.xml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            frames = root.findall(".//FAULT-EVENT-FRAME")
            for elem in frames:
                if elem.find(".//PDU-REF") is not None:
                    obj_elem = {}
                    obj_elem['PDU'] = elem.find(".//PDU-REF").text
                    obj_elem['ECU'] = elem.find(".//ECU-CODE").text
                    obj_elem['FRAME'] = None
                    obj_elem['ID'] = None
                    fault_frames.append(obj_elem)
        if file.endswith('.arxml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            frames = root.findall(".//{http://autosar.org/schema/r4.0}CAN-FRAME")
            for elem in frames:
                obj_elem = {}
                obj_elem['NAME'] = elem.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                obj_elem['PDU'] = elem.find(".//{http://autosar.org/schema/r4.0}PDU-REF").text.split("/")[-1]
                can_frames.append(obj_elem)
            frames = root.findall(".//{http://autosar.org/schema/r4.0}LIN-UNCONDITIONAL-FRAME")
            for elem in frames:
                obj_elem = {}
                obj_elem['NAME'] = elem.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text
                obj_elem['PDU'] = elem.find(".//{http://autosar.org/schema/r4.0}PDU-REF").text.split("/")[-1]
                can_frames.append(obj_elem)
            frames = root.findall(".//{http://autosar.org/schema/r4.0}USER-DEFINED-I-PDU")
            for elem in frames :
                existing_ipdus.append(elem.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text)
            frames = root.findall(".//{http://autosar.org/schema/r4.0}CAN-FRAME-TRIGGERING")
            for elem in frames:
                obj_elem = {}
                obj_elem['CAN-FRAME'] = elem.find(".//{http://autosar.org/schema/r4.0}FRAME-REF").text.split("/")[-1]
                obj_elem['ID'] = elem.find(".//{http://autosar.org/schema/r4.0}IDENTIFIER").text
                can_frames_triggering.append(obj_elem)
            frames = root.findall(".//{http://autosar.org/schema/r4.0}LIN-FRAME-TRIGGERING")
            for elem in frames:
                obj_elem = {}
                obj_elem['CAN-FRAME'] = elem.find(".//{http://autosar.org/schema/r4.0}FRAME-REF").text.split("/")[-1]
                obj_elem['ID'] = elem.find(".//{http://autosar.org/schema/r4.0}IDENTIFIER").text
                can_frames_triggering.append(obj_elem)

    for frame in fault_frames[:]:
        if frame['PDU'].split("/")[-1] not in existing_ipdus:
            fault_frames.remove(frame)
            logger.warning("The PDU: " + frame['PDU'].split("/")[-1] + " is not present in the network messaging file.")

    for frame in fault_frames:
        name = frame['PDU'].split("/")[-1]
        for can_frame in can_frames:
            if can_frame['PDU'] == name:
                frame['FRAME'] = can_frame['NAME']
                for triggering in can_frames_triggering:
                    if can_frame['NAME'] == triggering['CAN-FRAME']:
                        frame['ID'] = triggering['ID']

    rootScript = etree.Element('Script')
    name = etree.SubElement(rootScript, 'Name').text = "CfhmTedPdu"
    description = etree.SubElement(rootScript, 'Decription').text = "Fixe the CfhmEcuNbr and the CfhmTedPduRef with the information find in Fault Event frame configuration"
    expression = etree.SubElement(rootScript, 'Expression').text = "as:modconf('Dem')[1]"
    operations = etree.SubElement(rootScript, 'Operations')
    for frame in fault_frames:
        condition = etree.SubElement(operations, 'Operation')
        condition.attrib['Type'] = "Condition"
        expression = etree.SubElement(condition, 'Expression')
        expression.text = "not(node:exists(as:modconf('Dem')[1]/DemCfhm/CfhmRemoteFaultDecoder/CfhmTedPdu/*/CfhmTedPduRef" + '[.="ASPath:/EcuC/EcuC/EcucPduCollection/' + frame['PDU'].split("/")[-1] + "_" + frame['ID'] + 'R"]))'
        operations2 = etree.SubElement(condition, 'Operations')
        operation = etree.SubElement(operations2, 'Operation')
        operation.attrib['Type'] = 'ForEach'
        expression2 = etree.SubElement(operation, 'Expression')
        expression2.text = "as:modconf('Dem')[1]/DemCfhm/CfhmRemoteFaultDecoder/CfhmTedPdu"
        operations3 = etree.SubElement(operation, 'Operations')
        operation_add = etree.SubElement(operations3, 'Operation')
        operation_add.attrib['Type'] = "Add"
        expression_add = etree.SubElement(operation_add, 'Expression')
        expression_add.text = '"TED_' + frame['FRAME'] + '"'
        operation_foreach1 = etree.SubElement(operations3, 'Operation')
        operation_foreach1.attrib['Type'] = "ForEach"
        expression_foreach1 = etree.SubElement(operation_foreach1, 'Expression')
        expression_foreach1.text = "node:current()/TED_" + frame['FRAME'] + "/CfhmTedPduRef"
        operations_foreach1 = etree.SubElement(operation_foreach1, 'Operations')
        operation = etree.SubElement(operations_foreach1, 'Operation')
        operation.attrib['Type'] = 'SetValue'
        expression = etree.SubElement(operation, 'Expression')
        expression.text = "'ASPath:/EcuC/EcuC/EcucPduCollection/" + frame['PDU'].split("/")[-1] + "_" + frame['ID'] + "R'"
        operation_foreach2 = etree.SubElement(operations3, 'Operation')
        operation_foreach2.attrib['Type'] = "ForEach"
        expression_foreach2 = etree.SubElement(operation_foreach2, 'Expression')
        expression_foreach2.text = "node:current()/TED_" + frame['FRAME'] + "/CfhmEcuNbr"
        operations2 = etree.SubElement(operation_foreach2, 'Operations')
        operation = etree.SubElement(operations2, 'Operation')
        operation.attrib['Type'] = 'SetValue'
        expression = etree.SubElement(operation, 'Expression')
        expression.text = "num:i(" + frame['ECU'] + ")"
    fixed_operation = etree.SubElement(operations, 'Operation')
    fixed_operation.attrib['Type'] = "ForEach"
    expression = etree.SubElement(fixed_operation, 'Expression').text = "as:modconf('Dem')[1]/DemCfhm/CfhmRemoteFaultDecoder/CfhmTedPdu/*/CfhmTedPduHandleId"
    operations_fixed = etree.SubElement(fixed_operation, 'Operations')
    operation_fixed = etree.SubElement(operations_fixed, 'Operation')
    operation_fixed.attrib['Type'] = "SetValue"
    expression = etree.SubElement(operation_fixed, 'Expression').text = "node:current()/../@index"
    pretty_xml = prettify_xml(rootScript)
    tree = etree.ElementTree(etree.fromstring(pretty_xml))
    tree.write(output_path + "/CfhmTedPdu.xml", encoding="UTF-8", xml_declaration=True, method="xml", doctype = "<!-- XML file generated by COM_Configurator-18 -->")


def LPhM_config(file_list, output_path, logger):
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    lin_networks = []
    can_networks = []
    for file in file_list:
        if file.endswith('.xml'):
            parser = etree.XMLParser(remove_comments=True)
            tree = objectify.parse(file, parser=parser)
            root = tree.getroot()
            elements = root.findall(".//LIFE-PHASE")
            for element in elements:
                obj_temp = {}
                obj_temp['NAME'] = element.find(".//CLUSTER-REF").text.split('/')[-1]
                obj_temp['CLUSTER-TYPE'] = element.find(".//CLUSTER-REF").attrib['DEST']
                obj_temp['CATEGORY'] = element.find(".//CATEGORY").text
                groups = element.findall(".//I-PDU-GROUP")
                temp_list = []
                for group in groups:
                    obj_group = {}
                    obj_group['GROUP'] = group.find(".//I-PDU-GROUP-REF").text.split('/')[-1]
                    obj_group['TYPE'] = group.find(".//TYPE").text
                    obj_group['DIRECTION'] = group.find(".//DIRECTION").text
                    temp_list.append(obj_group)
                obj_temp['IPDUGROUPS'] = temp_list
                tables = element.findall(".//SCHEDULE-TABLE")
                temp_list = []
                for table in tables:
                    obj_group = {}
                    obj_group['TABLE'] = table.find(".//SCHEDULE-TABLE-REF").text.split('/')[-1]
                    obj_group['TYPE'] = table.find(".//TYPE").text
                    # obj_group['MODE'] = table.find(".//RUN-MODE").text
                    temp_list.append(obj_group)
                obj_temp['SCHEDULE-TABLES'] = temp_list
                if obj_temp['CLUSTER-TYPE'] == "CAN-CLUSTER":
                    can_networks.append(obj_temp)
                else:
                    lin_networks.append(obj_temp)


    # create ouput file: LPhM.epc
    rootLPhM = etree.Element('AUTOSAR', {attr_qname: 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd'}, nsmap=NSMAP)
    packages = etree.SubElement(rootLPhM, 'AR-PACKAGES')
    package = etree.SubElement(packages, 'AR-PACKAGE')
    short_name = etree.SubElement(package, 'SHORT-NAME').text = "LPhM"
    elements = etree.SubElement(package, 'ELEMENTS')
    ecuc_module = etree.SubElement(elements, 'ECUC-MODULE-CONFIGURATION-VALUES')
    short_name = etree.SubElement(ecuc_module, 'SHORT-NAME').text = "LPhM"
    definition = etree.SubElement(ecuc_module, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-MODULE-DEF"
    definition.text = "/AUTOSAR/EcuDefs/LPhM"
    description = etree.SubElement(ecuc_module, 'IMPLEMENTATION-CONFIG-VARIANT').text = "VARIANT-POST-BUILD"
    containers = etree.SubElement(ecuc_module, 'CONTAINERS')
    #LPhM cluster
    ecuc_general = etree.SubElement(containers, "ECUC-CONTAINER-VALUE")
    short_name = etree.SubElement(ecuc_general, "SHORT-NAME").text = "LPhMCluster_0"
    definition_general = etree.SubElement(ecuc_general, "DEFINITION-REF")
    definition_general.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition_general.text = "/AUTOSAR/EcuDefs/LPhM/LPhMCluster"
    subcontainer_master = etree.SubElement(ecuc_general, "SUB-CONTAINERS")
    # lin clusters
    for cluster in lin_networks:
        ecuc_general = etree.SubElement(subcontainer_master, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(ecuc_general, "SHORT-NAME").text = "LPhM_" + cluster['NAME']
        definition_general = etree.SubElement(ecuc_general, "DEFINITION-REF")
        definition_general.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition_general.text = "/AUTOSAR/EcuDefs/LPhM/LPhMCluster/LPhMClusterLIN"
        subcontainer_cluster = etree.SubElement(ecuc_general, "SUB-CONTAINERS")
        ecuc_general = etree.SubElement(subcontainer_cluster, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(ecuc_general, "SHORT-NAME").text = cluster['NAME']
        definition_general = etree.SubElement(ecuc_general, "DEFINITION-REF")
        definition_general.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition_general.text = "/AUTOSAR/EcuDefs/LPhM/LPhMCluster/LPhMClusterLIN/ChannelList"
        references = etree.SubElement(ecuc_general, "REFERENCE-VALUES")
        ecuc_ref_value_1 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
        definition = etree.SubElement(ecuc_ref_value_1, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/LPhM/LPhMCluster/LPhMClusterLIN/ChannelList/ChannelRef"
        value = etree.SubElement(ecuc_ref_value_1, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/Lin/Lin/LinGlobalConfig/" + cluster['NAME'] + "_Channel"
        ecuc_ref_value_2 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
        definition = etree.SubElement(ecuc_ref_value_2, "DEFINITION-REF")
        definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
        definition.text = "/AUTOSAR/EcuDefs/LPhM/LPhMCluster/LPhMClusterLIN/ChannelList/LPhMUser"
        value = etree.SubElement(ecuc_ref_value_2, "VALUE-REF")
        value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
        value.text = "/ComM/ComM/ComMConfigSet/ComMUser_" + cluster['NAME']
        container_ipdu = etree.SubElement(subcontainer_cluster, "ECUC-CONTAINER-VALUE")
        short_name = etree.SubElement(container_ipdu, "SHORT-NAME").text = "IPDUGroupsReferences"
        definition_ipdu = etree.SubElement(container_ipdu, "DEFINITION-REF")
        definition_ipdu.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition_ipdu.text = "/LPhM_TS_2018/LPhM/LPhMCluster/LPhMClusterLIN/IPDUGroupsReferences"
        reference_values_ipdu = etree.SubElement(container_ipdu, "REFERENCE-VALUES")
        for group in cluster['IPDUGROUPS']:
            container_group = etree.SubElement(reference_values_ipdu, 'ECUC-REFERENCE-VALUE')
            direction = ""
            if group['DIRECTION'] == 'IN':
                direction = "RX"
            else:
                direction = "TX"
            type = group['TYPE'] + "_" + direction
            definition_group = etree.SubElement(container_group, "DEFINITION-REF")
            definition_group.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition_group.text = "/LPhM_TS_2018/LPhM/LPhMCluster/LPhMClusterLIN/IPDUGroupsReferences/" + type
            value_group = etree.SubElement(container_group, "VALUE-REF")
            value_group.attrib['DEST'] = "IDENTIFIABLE"
            value_group.text = "/Com/Com/ComConfig/" + group['GROUP']
        subcontainer_table = etree.SubElement(ecuc_general, "SUB-CONTAINERS")
        for table in cluster['SCHEDULE-TABLES']:
            container_table = etree.SubElement(subcontainer_table, "ECUC-CONTAINER-VALUE")
            name = etree.SubElement(container_table, "SHORT-NAME").text = table['TABLE']
            definition_table = etree.SubElement(container_table, "DEFINITION-REF")
            definition_table.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition_table.text = "/LPhM_TS_2018/LPhM/LPhMCluster/LPhMClusterLIN/ChannelList/LPhMScheduleTable"
            parameters_table = etree.SubElement(container_table, "PARAMETER-VALUES")
            param = etree.SubElement(parameters_table, "ECUC-TEXTUAL-PARAM-VALUE")
            definition_param = etree.SubElement(param, "DEFINITION-REF")
            definition_param.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            definition_param.text = "/LPhM_TS_2018/LPhM/LPhMCluster/LPhMClusterLIN/ChannelList/LPhMScheduleTable/ScheduleTableCategory"
            value = etree.SubElement(param, "VALUE").text = table['TYPE']
            references_table = etree.SubElement(container_table, "REFERENCE-VALUES")
            reference = etree.SubElement(references_table, "ECUC-REFERENCE-VALUE")
            definition_ref = etree.SubElement(reference, "DEFINITION-REF")
            definition_ref.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition_ref.text = "/LPhM_TS_2018/LPhM/LPhMCluster/LPhMClusterLIN/ChannelList/LPhMScheduleTable/LPhMScheduleTableRef"
            value_ref = etree.SubElement(reference, "VALUE-REF")
            value_ref.attrib['DEST'] = "IDENTIFIABLE"
            value_ref.text = "/LinSM/LinSM/LinSMConfigSet/" + cluster['NAME'] + "/" + table['TABLE']

    # can clusters
    for cluster in can_networks:
        if cluster['CATEGORY'] not in ['BODY', 'PWT']:
            ecuc_general = etree.SubElement(subcontainer_master, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(ecuc_general, "SHORT-NAME").text = "LPhM_" + cluster['NAME']
            definition_general = etree.SubElement(ecuc_general, "DEFINITION-REF")
            definition_general.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition_general.text = "/AUTOSAR/EcuDefs/LPhM/LPhMCluster/LPhMClusterInternal"
            parameter_values = etree.SubElement(ecuc_general, "PARAMETER-VALUES")
            textual_param = etree.SubElement(parameter_values, "ECUC-TEXTUAL-PARAM-VALUE")
            definition_param = etree.SubElement(textual_param, "DEFINITION-REF")
            definition_param.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
            definition_param.text = "/LPhM_TS_2018/LPhM/LPhMCluster/LPhMClusterInternal/InternalClusterName"
            value = etree.SubElement(textual_param, "VALUE").text = cluster['NAME']
            reference_values = etree.SubElement(ecuc_general, "REFERENCE-VALUES")
            reference_param = etree.SubElement(reference_values, "ECUC-REFERENCE-VALUE")
            definition_reference = etree.SubElement(reference_param, "DEFINITION-REF")
            definition_reference.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition_reference.text = "/LPhM_TS_2018/LPhM/LPhMCluster/LPhMClusterInternal/LPhMUser"
            value = etree.SubElement(reference_param, "VALUE-REF")
            value.attrib['DEST'] = "IDENTIFIABLE"
            value.text = "/ComM/ComM/ComMConfigSet/ComMUser_" + cluster['NAME']
        else:
            ecuc_general = etree.SubElement(subcontainer_master, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(ecuc_general, "SHORT-NAME").text = "LPhM_" + cluster['NAME']
            definition_general = etree.SubElement(ecuc_general, "DEFINITION-REF")
            definition_general.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition_general.text = "/AUTOSAR/EcuDefs/LPhM/LPhMCluster/LPhMClusterCAN"
            references = etree.SubElement(ecuc_general, "REFERENCE-VALUES")
            ecuc_ref_value_2 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(ecuc_ref_value_2, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/LPhM/LPhMCluster/LPhMClusterCAN/LPhMUser"
            value = etree.SubElement(ecuc_ref_value_2, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/ComM/ComM/ComMConfigSet/ComMUser_" + cluster['NAME']
            parameters = etree.SubElement(ecuc_general, 'PARAMETER-VALUES')
            numerical2 = etree.SubElement(parameters, 'ECUC-TEXTUAL-PARAM-VALUE')
            definition = etree.SubElement(numerical2, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/LPhM/LPhMCluster/LPhMClusterCAN/LPhMClusterType"
            value = etree.SubElement(numerical2, 'VALUE').text = cluster['CATEGORY']
            subcontainer = etree.SubElement(ecuc_general, "SUB-CONTAINERS")
            container_ipdu = etree.SubElement(subcontainer, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(container_ipdu, "SHORT-NAME").text = "IPDUGroupsReferences"
            definition_ipdu = etree.SubElement(container_ipdu, "DEFINITION-REF")
            definition_ipdu.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition_ipdu.text = "/AUTOSAR/EcuDefs/LPhM/LPhMCluster/LPhMClusterCAN/IPDUGroupsReferences"
            reference_values_ipdu = etree.SubElement(container_ipdu, "REFERENCE-VALUES")
            for group in cluster['IPDUGROUPS']:
                container_group = etree.SubElement(reference_values_ipdu, 'ECUC-REFERENCE-VALUE')
                direction = ""
                if group['DIRECTION'] == 'IN':
                    direction = "RX"
                else:
                    direction = "TX"
                type = group['TYPE'] + "_" + direction
                definition_group = etree.SubElement(container_group, "DEFINITION-REF")
                definition_group.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition_group.text = "/LPhM_TS_2018/LPhM/LPhMCluster/LPhMClusterCAN/IPDUGroupsReferences/" + type
                value_group = etree.SubElement(container_group, "VALUE-REF")
                value_group.attrib['DEST'] = "IDENTIFIABLE"
                value_group.text = "/Com/Com/ComConfig/" + group['GROUP']

    # generate data
    pretty_xml = prettify_xml(rootLPhM)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/LPhM.epc', encoding='UTF-8', xml_declaration=True, method="xml", doctype="<!-- XML file generated by COM_Configurator-18 -->")
    return


if __name__ == "__main__":                                          # pragma: no cover
    # process = psutil.Process(os.getpid())                         # pragma: no cover
    # start_time = time.clock()                                     # pragma: no cover
    # cov = Coverage()                                                # pragma: no cover
    # cov.start()                                                     # pragma: no cover
    main()                                                          # pragma: no cover
    # cov.stop()                                                      # pragma: no cover
    # cov.html_report(directory='Coverage Report')                      # pragma: no cover
    # print(str(time.clock() - start_time) + " seconds")            # pragma: no cover
    # print(str(process.memory_info()[0]/float(2**20)) + " MB")     # pragma: no cover
