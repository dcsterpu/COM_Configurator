import argparse
import logging
import os
import sys
from lxml import etree
from xml.dom.minidom import parseString
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from coverage import Coverage


def arg_parse(parser):
    parser.add_argument('-in', '--inp', nargs='*', help="input path or file", required=True, default="")
    parser.add_argument('-out', '--out', help="output path", required=False, default="")
    parser.add_argument('-out_epc', '--out_epc', help="output path for configuration file(s)", required=False, default="")
    parser.add_argument('-out_script', '--out_script', help="output path for Scriptor file(s)", required=False, default="")
    parser.add_argument('-out_log', '--out_log', help="output path for log file", required=False, default="")
    parser.add_argument('-NeMo', action="store_const", const="-NeMo", required=False, default="")
    parser.add_argument('-EnGw', action="store_const", const="-EnGw", required=False, default="")


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
    NeMo = False
    if args.NeMo:
        NeMo = True
    EnGw = False
    if args.EnGw:
        EnGw = True
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
                NeMo_script(files_list, paths_list, output_path, logger)
            if EnGw:
                PduR_script(files_list, paths_list, output_path, logger)
                EnGw_config(files_list, paths_list, output_path, logger)
                EcuC_config(files_list, paths_list, output_path, logger)
                PduR_config(files_list, paths_list, output_path, logger)
                CanTp_config(files_list, paths_list, output_path, logger)
                CanIf_config(files_list, paths_list, output_path, logger)
                LinTp_config(files_list, paths_list, output_path, logger)
        else:
            logger = set_logger(output_path)
            if NeMo:
                NeMo_script(files_list, paths_list, output_path, logger)
            if EnGw:
                PduR_script(files_list, paths_list, output_path, logger)
                EnGw_config(files_list, paths_list, output_path, logger)
                EcuC_config(files_list, paths_list, output_path, logger)
                PduR_config(files_list, paths_list, output_path, logger)
                CanTp_config(files_list, paths_list, output_path, logger)
                CanIf_config(files_list, paths_list, output_path, logger)
                LinTp_config(files_list, paths_list, output_path, logger)
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
                    EnGw_config(files_list, paths_list, output_epc, logger)
                    EcuC_config(files_list, paths_list, output_epc, logger)
                    PduR_config(files_list, paths_list, output_epc, logger)
                    CanTp_config(files_list, paths_list, output_epc, logger)
                    CanIf_config(files_list, paths_list, output_epc, logger)
                    LinTp_config(files_list, paths_list, output_epc, logger)
            else:
                logger = set_logger(output_epc)
                if EnGw:
                    EnGw_config(files_list, paths_list, output_epc, logger)
                    EcuC_config(files_list, paths_list, output_epc, logger)
                    PduR_config(files_list, paths_list, output_epc, logger)
                    CanTp_config(files_list, paths_list, output_epc, logger)
                    CanIf_config(files_list, paths_list, output_epc, logger)
                    LinTp_config(files_list, paths_list, output_epc, logger)
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
                    NeMo_script(files_list, paths_list, output_script, logger)
                if EnGw:
                    PduR_script(files_list, paths_list, output_script, logger)
            else:
                logger = set_logger(output_script)
                if NeMo:
                    NeMo_script(files_list, paths_list, output_script, logger)
                if EnGw:
                    PduR_script(files_list, paths_list, output_script, logger)
    else:
        print("\nNo output path defined!\n")
        sys.exit(1)


def PduR_script(file_list, path_list, output_path, logger):
    mappings = []
    can_frames = []
    diag_tools = []
    frames_port = []
    nads = []
    items = []
    triggerings = []
    can_frames_triggering = []
    routes = []
    for file in file_list:
        if file.endswith('.arxml'):
            tree = etree.parse(file)
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
                if direction == "OUT":
                    obj_elem['WAY'] = "T"
                elif direction == "IN":
                    obj_elem['WAY'] = "R"
                else:
                    logger.error("The communication direction of frame-port " + obj_elem['NAME'] + " is not valid")
                frames_port.append(obj_elem)
        elif file.endswith('.xml'):
            tree = etree.parse(file)
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
        elif file.endswith('.epc'):
            tree = etree.parse(file)
            root = tree.getroot()
            elements = root.findall(".//{http://autosar.org/2.1.2}CONTAINER")
            for element in elements:
                element_type = element.find(".//{http://autosar.org/2.1.2}DEFINITION-REF")
                if element_type.text.split("/")[-1] == "DiagTool":
                    diag_tools.append(element.find(".//{http://autosar.org/2.1.2}VALUE-REF").text.split("/")[-1])
                elif element_type.text.split("/")[-1] == "Nad":
                    obj_nad = {}
                    obj_nad['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                    obj_nad['ID'] = element.find(".//{http://autosar.org/2.1.2}VALUE").text
                    obj_nad['NETWORK'] = element.getparent().getparent().getchildren()[0].text
                    obj_nad['CONFIG'] = element.getparent().getparent().getparent().getparent().getchildren()[0].text
                    nads.append(obj_nad)
    for path in path_list:
        for file in os.listdir(path):
            if file.endswith('.arxml'):
                fullname = os.path.join(path, file)
                tree = etree.parse(fullname)
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
                    if direction == "OUT":
                        obj_elem['WAY'] = "T"
                    elif direction == "IN":
                        obj_elem['WAY'] = "R"
                    else:
                        logger.error("The communication direction of frame-port " + obj_elem['NAME'] + " is not valid")
                    frames_port.append(obj_elem)
            elif file.endswith('.xml'):
                fullname = os.path.join(path, file)
                tree = etree.parse(fullname)
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
            elif file.endswith('.epc'):
                tree = etree.parse(file)
                root = tree.getroot()
                elements = root.findall(".//{http://autosar.org/2.1.2}CONTAINER")
                for element in elements:
                    element_type = element.find(".//{http://autosar.org/2.1.2}DEFINITION-REF")
                    if element_type.text.split("/")[-1] == "DiagTool":
                        diag_tools.append(element.find(".//{http://autosar.org/2.1.2}VALUE-REF").text.split("/")[-1])
                    elif element_type.text.split("/")[-1] == "Nad":
                        obj_nad = {}
                        obj_nad['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                        obj_nad['ID'] = element.find(".//{http://autosar.org/2.1.2}VALUE").text
                        obj_nad['NETWORK'] = element.getparent().getparent().getchildren()[0].text
                        obj_nad['CONFIG'] = element.getparent().getparent().getparent().getparent().getchildren()[0].text
                        nads.append(obj_nad)
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
    for mapping in mappings[:]:
        obj_map = {}
        dest_list = []
        obj_map['SOURCE'] = mapping['SOURCE-PDU']
        obj_map['CLUSTER'] = mapping['SOURCE-CLUSTER']
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
    for route in routes[:]:
        if route['WAY'] is None:
            routes.remove(route)
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
    tree.write(output_path + "/EnGw_PduR_Update.xml", encoding="UTF-8", xml_declaration=True, method="xml")


def PduR_config(file_list, path_list, output_path, logger):
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    mappings = []
    can_frames = []
    diag_tools = []
    frames_port = []
    nads = []
    items = []
    triggerings = []
    can_frames_triggering = []
    routes = []
    for file in file_list:
        if file.endswith('.arxml'):
            tree = etree.parse(file)
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
                if direction == "OUT":
                    obj_elem['WAY'] = "T"
                elif direction == "IN":
                    obj_elem['WAY'] = "R"
                else:
                    logger.error("The communication direction of frame-port " + obj_elem['NAME'] + " is not valid")
                frames_port.append(obj_elem)
        elif file.endswith('.xml'):
            tree = etree.parse(file)
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
        elif file.endswith('.epc'):
            tree = etree.parse(file)
            root = tree.getroot()
            elements = root.findall(".//{http://autosar.org/2.1.2}CONTAINER")
            for element in elements:
                element_type = element.find(".//{http://autosar.org/2.1.2}DEFINITION-REF")
                if element_type.text.split("/")[-1] == "DiagTool":
                    diag_tools.append(element.find(".//{http://autosar.org/2.1.2}VALUE-REF").text.split("/")[-1])
                elif element_type.text.split("/")[-1] == "Nad":
                    obj_nad = {}
                    obj_nad['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                    obj_nad['ID'] = element.find(".//{http://autosar.org/2.1.2}VALUE").text
                    obj_nad['NETWORK'] = element.getparent().getparent().getchildren()[0].text
                    obj_nad['CONFIG'] = element.getparent().getparent().getparent().getparent().getchildren()[0].text
                    nads.append(obj_nad)
    for path in path_list:
        for file in os.listdir(path):
            if file.endswith('.arxml'):
                fullname = os.path.join(path, file)
                tree = etree.parse(fullname)
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
                    if direction == "OUT":
                        obj_elem['WAY'] = "T"
                    elif direction == "IN":
                        obj_elem['WAY'] = "R"
                    else:
                        logger.error("The communication direction of frame-port " + obj_elem['NAME'] + " is not valid")
                    frames_port.append(obj_elem)
            elif file.endswith('.xml'):
                fullname = os.path.join(path, file)
                tree = etree.parse(fullname)
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
            elif file.endswith('.epc'):
                tree = etree.parse(file)
                root = tree.getroot()
                elements = root.findall(".//{http://autosar.org/2.1.2}CONTAINER")
                for element in elements:
                    element_type = element.find(".//{http://autosar.org/2.1.2}DEFINITION-REF")
                    if element_type.text.split("/")[-1] == "DiagTool":
                        diag_tools.append(element.find(".//{http://autosar.org/2.1.2}VALUE-REF").text.split("/")[-1])
                    elif element_type.text.split("/")[-1] == "Nad":
                        obj_nad = {}
                        obj_nad['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                        obj_nad['ID'] = element.find(".//{http://autosar.org/2.1.2}VALUE").text
                        obj_nad['NETWORK'] = element.getparent().getparent().getchildren()[0].text
                        obj_nad['CONFIG'] = element.getparent().getparent().getparent().getparent().getchildren()[0].text
                        nads.append(obj_nad)
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
    for mapping in mappings[:]:
        obj_map = {}
        dest_list = []
        obj_map['SOURCE'] = mapping['SOURCE-PDU']
        obj_map['CLUSTER'] = mapping['SOURCE-CLUSTER']
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

    for item in items:
        # if item['CLUSTER'].find("HS") != -1 or item['CLUSTER'].find("DIAG") != -1:
        #     routes.append(item)
        # else:
            for dest in item['TARGET']:
                # if dest['CLUSTER'].find("HS") != -1 or dest['CLUSTER'].find("DIAG") != -1:
                #     routes.append(item)
                #     continue
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
    for route in routes[:]:
        if route['WAY'] is None:
            routes.remove(route)
            logger.warning('The mapping with source ' + route['SOURCE'] + " has been deleted because the communication direction cannot be established")
        else:
            for dest in route['TARGET']:
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
        short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_' + route['SOURCE']
        definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
        subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
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
            short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_' + route['SOURCE'] + "_" + dest['TARGET'] + "_FROM_CDD"
            definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
            subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
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
        if nad['CONFIG'] == "Config13":
            if nad['NETWORK'] not in network_list:
                network_list.append(nad['NETWORK'])
                ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_LinIf_REQ_' + nad['NETWORK'] + "_1P3"
                definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
                subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
                # src
                ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_LinIf_REQ_" + nad['NETWORK'] + "_1P3"
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
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/LinIf_REQ_" + nad['NETWORK'] + "_1P3_SCA"
                # dest
                ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_LinIf_REQ_" + nad['NETWORK'] + "_1P3"
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
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + nad['NETWORK'] + "_1P3_LinIf"
                # backwards route
                ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_LinIf_REP_' + nad['NETWORK'] + "_1P3"
                definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
                subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
                # src
                ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_LinIf_REP_" + nad['NETWORK'] + "_1P3"
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
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/SCA_REP_" + nad['NETWORK'] + "_1P3_LinIf"
                # dest
                ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_LinIf_REP_" + nad['NETWORK'] + "_1P3"
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
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/LinIf_REP_" + nad['NETWORK'] + "_1P3_SCA"
    for diag_tool in diag_tools:
        for nad in nads:
            if nad['CONFIG'] == "Config21":
                comment = etree.Comment("CanTp")
                subcontainer_route.append(comment)
                ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_CanTp_REQ_' + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME']
                definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
                subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
                # src
                ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_CanTp_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME']
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
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/CanTp_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_SCA"
                # dest
                ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_CanTp_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME']
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
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanTp"
                # backwards route
                ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_CanTp_REP_' + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME']
                definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
                subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
                # src
                ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_CanTp_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME']
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
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/SCA_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanTp"
                # dest
                ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_CanTp_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME']
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
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/CanTp_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_SCA"
            elif nad['CONFIG'] == "Config13":
                comment = etree.Comment("CanIf")
                subcontainer_route.append(comment)
                ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_CanIf_REQ_' + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME']
                definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
                subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
                # src
                ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_CanIf_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME']
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
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/CanIf_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_SCA"
                # dest
                ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_CanIf_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME']
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
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanIf"
                # backwards route
                ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_CanIf_REP_' + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME']
                definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
                subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
                # src
                ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_CanIf_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME']
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
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/SCA_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanIf"
                # dest
                ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_CanIf_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME']
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
                value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/CanIf_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_SCA"
    comment = etree.Comment("LinTp")
    subcontainer_route.append(comment)
    for nad in nads:
        if nad['CONFIG'] == "Config21":
            ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_LinTp_REQ_' + nad['NETWORK'] + "_" + nad['NAME']
            definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
            subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
            # src
            ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_LinTp_REQ_" + nad['NETWORK'] + "_" + nad['NAME']
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
            value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + nad['NETWORK'] + "_" + nad['NAME'] + "_LinTp"
            # dest
            ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_LinTp_REQ_" + nad['NETWORK'] + "_" + nad['NAME']
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
            value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/LinTp_REQ_" + nad['NETWORK'] + "_" + nad['NAME'] + "_SCA"
            # backwards route
            ecuc_container_value_route = etree.SubElement(subcontainer_route, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value_route, 'SHORT-NAME').text = 'PduRRoutingPath_EnGw_LinTp_REP_' + nad['NETWORK'] + "_" + nad['NAME']
            definition = etree.SubElement(ecuc_container_value_route, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRRoutingPath"
            subcontainer_path = etree.SubElement(ecuc_container_value_route, 'SUB-CONTAINERS')
            # src
            ecuc_container_value_src = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value_src, 'SHORT-NAME').text = "PduRSrcPdu_EnGw_LinTp_REP_" + nad['NETWORK'] + "_" + nad['NAME']
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
            value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/LinTp_REP_" + nad['NETWORK'] + "_" + nad['NAME'] + "_SCA"
            # dest
            ecuc_container_value_dest = etree.SubElement(subcontainer_path, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value_dest, 'SHORT-NAME').text = "PduRDestPdu_EnGw_LinTp_REP_" + nad['NETWORK'] + "_" + nad['NAME']
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
            value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/SCA_REP_" + nad['NETWORK'] + "_" + nad['NAME'] + "_LinTp"
    # generate data
    pretty_xml = prettify_xml(rootPduR)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/PduR.epc', encoding='UTF-8', xml_declaration=True, method="xml")
    return


def EnGw_config(file_list, path_list, output_path, logger):
    # create config
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    mappings = []
    can_frames = []
    diag_tools = []
    nads = []
    for file in file_list:
        if file.endswith('.arxml'):
            tree = etree.parse(file)
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
        elif file.endswith('.xml'):
            tree = etree.parse(file)
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
        elif file.endswith('.epc'):
            tree = etree.parse(file)
            root = tree.getroot()
            elements = root.findall(".//{http://autosar.org/2.1.2}CONTAINER")
            for element in elements:
                element_type = element.find(".//{http://autosar.org/2.1.2}DEFINITION-REF")
                if element_type.text.split("/")[-1] == "DiagTool":
                    diag_tools.append(element.find(".//{http://autosar.org/2.1.2}VALUE-REF").text.split("/")[-1])
                elif element_type.text.split("/")[-1] == "Nad":
                    obj_nad = {}
                    obj_nad['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                    obj_nad['ID'] = element.find(".//{http://autosar.org/2.1.2}VALUE").text
                    obj_nad['NETWORK'] = element.getparent().getparent().getchildren()[0].text
                    obj_nad['CONFIG'] = element.getparent().getparent().getparent().getparent().getchildren()[0].text
                    nads.append(obj_nad)
    for path in path_list:
        for file in os.listdir(path):
            if file.endswith('.arxml'):
                fullname = os.path.join(path, file)
                tree = etree.parse(fullname)
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
            elif file.endswith('.xml'):
                fullname = os.path.join(path, file)
                tree = etree.parse(fullname)
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
            elif file.endswith('.epc'):
                fullname = os.path.join(path, file)
                tree = etree.parse(fullname)
                root = tree.getroot()
                elements = root.findall(".//{http://autosar.org/2.1.2}CONTAINER")
                for element in elements:
                    element_type = element.find(".//{http://autosar.org/2.1.2}DEFINITION-REF")
                    if element_type.text.split("/")[-1] == "DiagTool":
                        diag_tools.append(element.find(".//{http://autosar.org/2.1.2}VALUE-REF").text.split("/")[-1])
                    elif element_type.text.split("/")[-1] == "Nad":
                        obj_nad = {}
                        obj_nad['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                        obj_nad['ID'] = element.find(".//{http://autosar.org/2.1.2}VALUE").text
                        obj_nad['NETWORK'] = element.getparent().getparent().getchildren()[0].text
                        obj_nad['CONFIG'] = element.getparent().getparent().getparent().getparent().getchildren()[0].text
                        nads.append(obj_nad)
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
    # implement TRS.COMCONF.GEN.001(1)
    ecuc_container = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddComStackContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution"
    subcontainer = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    ecuc_container = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddPduRUpperLayerContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution"
    subcontainers = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    index = 0
    network_list = []
    for nad in nads:
        if nad['CONFIG'] == "Config13":
            if nad['NETWORK'] not in network_list:
                network_list.append(nad['NETWORK'])
                # REQ part
                comment = etree.Comment("LinIf")
                subcontainers.append(comment)
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerRxPdu_REP_" + nad['NETWORK'] + "_1P3"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerHandleId"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                index = index + 1
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REP_" + nad['NETWORK'] + "_1P3_LinIf"
                # REP part
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerTxPdu_REQ_" + nad['NETWORK'] + "_1P3"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerHandleId"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                index = index + 1
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + nad['NETWORK'] + "_1P3_LinIf"
    for nad in nads:
        if nad['CONFIG'] == "Config21":
            # REQ part
            comment = etree.Comment("LinTp")
            subcontainers.append(comment)
            ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerRxPdu_REP_" + nad['NETWORK'] + "_" + nad['NAME'] + "_2P1"
            definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu"
            parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
            ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
            definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerHandleId"
            value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
            index = index + 1
            reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
            ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerPduRef"
            value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
            value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REP_" + nad['NETWORK'] + "_" + nad['NAME'] + "_LinTp"
            # REP part
            ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerTxPdu_REQ_" + nad['NETWORK'] + "_" + nad['NAME'] + "_2P1"
            definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu"
            parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
            ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
            definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerHandleId"
            value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
            index = index + 1
            reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
            ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
            definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerPduRef"
            value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
            value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + nad['NETWORK'] + "_" + nad['NAME'] + "_LinTp"
    for diag_tool in diag_tools:
        for nad in nads:
            if nad['CONFIG'] == "Config21":
                # REQ part
                comment = etree.Comment("CanTp")
                subcontainers.append(comment)
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerRxPdu_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_2P1"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerHandleId"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                index = index + 1
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanTp"
                # REP part
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerTxPdu_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_2P1"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerHandleId"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                index = index + 1
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanTp"
            elif nad['CONFIG'] == "Config13":
                # REQ part
                comment = etree.Comment("CanIf")
                subcontainers.append(comment)
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerRxPdu_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_1P3"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerHandleId"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                index = index + 1
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerRxPdu/CddPduRUpperLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanIf"
                # REP part
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRUpperLayerTxPdu_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_1P3"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerHandleId"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                index = index + 1
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddComStackContribution/CddPduRUpperLayerContribution/CddPduRUpperLayerTxPdu/CddPduRUpperLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanIf"
    # implement diag part
    ecuc_container = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "DiagConfiguration"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddDiagConfiguration"
    subcontainer_general = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    ecuc_container = etree.SubElement(subcontainer_general, 'ECUC-CONTAINER-VALUE')
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "DiagConfiguration"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddDiagConfiguration/DiagConfiguration"
    subcontainer = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    lin_list = []
    lin_config = []
    for nad in nads:
        if nad['NETWORK'] not in lin_list:
            lin_list.append(nad['NETWORK'])
    for lin in lin_list:
        obj_lin = {}
        obj_lin['NAME'] = lin
        obj_lin['1P3'] = False
        obj_lin['2P1'] = False
        lin_config.append(obj_lin)
    for nad in nads:
        if nad['CONFIG'] == "Config21":
            for lin in lin_config:
                if nad['NETWORK'] == lin['NAME']:
                        lin['2P1'] = True
        else:
            for lin in lin_config:
                if nad['NETWORK'] == lin['NAME']:
                        lin['1P3'] = True
    for diag_tool in diag_tools:
        ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
        short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = diag_tool
        definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
        definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddDiagConfiguration/DiagConfiguration/DiagTool"
        for nad in nads:
            if nad['CONFIG'] == "Config21":
                ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = diag_tool + "_" + nad['NAME']
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddDiagConfiguration/DiagConfiguration/Nad21"
                param_values = etree.SubElement(ecuc_container_value, "PARAMETER-VALUES")
                ecuc_numerical_value = etree.SubElement(param_values, "ECUC-NUMERICAL-PARAM-VALUE")
                definition_ref = etree.SubElement(ecuc_numerical_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddDiagConfiguration/DiagConfiguration/Nad21/NadId"
                value = etree.SubElement(ecuc_numerical_value, "VALUE").text = nad['ID']
                ecuc_textual_value = etree.SubElement(param_values, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_ref = etree.SubElement(ecuc_textual_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddDiagConfiguration/DiagConfiguration/Nad21/LIN"
                value = etree.SubElement(ecuc_textual_value, "VALUE").text = nad['NETWORK']
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddDiagConfiguration/DiagConfiguration/Nad21/DiagTool"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EnGwCLD/EnGwCLD/DiagConfiguration/DiagConfiguration/" + diag_tool
            elif nad['CONFIG'] == "Config13":
                ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = diag_tool+ "_" + nad['NAME']
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddDiagConfiguration/DiagConfiguration/Nad13"
                param_values = etree.SubElement(ecuc_container_value, "PARAMETER-VALUES")
                ecuc_numerical_value = etree.SubElement(param_values, "ECUC-NUMERICAL-PARAM-VALUE")
                definition_ref = etree.SubElement(ecuc_numerical_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddDiagConfiguration/DiagConfiguration/Nad13/NadId"
                value = etree.SubElement(ecuc_numerical_value, "VALUE").text = nad['ID']
                ecuc_textual_value = etree.SubElement(param_values, "ECUC-TEXTUAL-PARAM-VALUE")
                definition_ref = etree.SubElement(ecuc_textual_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddDiagConfiguration/DiagConfiguration/Nad13/LIN"
                value = etree.SubElement(ecuc_textual_value, "VALUE").text = nad['NETWORK']
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddDiagConfiguration/DiagConfiguration/Nad13/DiagTool"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EnGwCLD/EnGwCLD/DiagConfiguration/DiagConfiguration/" + diag_tool
    for lin in lin_config:
        ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
        short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = lin['NAME']
        definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
        definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddDiagConfiguration/DiagConfiguration/Lin"
        parameter_values = etree.SubElement(ecuc_container_value, "PARAMETER-VALUES")
        boolean_1 = etree.SubElement(parameter_values, "ECUC-NUMERICAL-PARAM-VALUE")
        definition_1 = etree.SubElement(boolean_1, "DEFINITION-REF")
        definition_1.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
        definition_1.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddDiagConfiguration/DiagConfiguration/Lin/LinConfig2P1"
        if lin['2P1']:
            value_1 = etree.SubElement(boolean_1, "VALUE").text = "1"
        else:
            value_1 = etree.SubElement(boolean_1, "VALUE").text = "0"
        boolean_2 = etree.SubElement(parameter_values, "ECUC-NUMERICAL-PARAM-VALUE")
        definition_2 = etree.SubElement(boolean_2, "DEFINITION-REF")
        definition_2.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
        definition_2.text = "/AUTOSAR/EcuDefs/EnGwCLD/CddDiagConfiguration/DiagConfiguration/Lin/LinConfig1P3"
        if lin['1P3']:
            value_1 = etree.SubElement(boolean_2, "VALUE").text = "1"
        else:
            value_1 = etree.SubElement(boolean_2, "VALUE").text = "0"
    # generate data
    pretty_xml = prettify_xml(rootCLD)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/EnGwCLD.epc', encoding='UTF-8', xml_declaration=True, method="xml")

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
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddPduRLowerLayerContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution"
    subcontainers = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    index = 0
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRLowerLayerRxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu/CddPduRLowerLayerHandleId"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRLowerLayerTxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu/CddPduRLowerLayerHandleId"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "RoutingPathCCLD_" + mapping['SOURCE-PDU'] + "_TO_" + mapping['TARGET-PDU']
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCLDRoutingPath"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_textual_param_value, "DEFINITION-REF")
                definition_ref.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCLD/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCLDRoutingPath/EnGwAuthorizationCallout"
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
    output.write(output_path + '/EnGwCCLD.epc', encoding='UTF-8', xml_declaration=True, method="xml")

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
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddPduRLowerLayerContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution"
    subcontainers = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    index = 0
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRLowerLayerRxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu/CddPduRLowerLayerHandleId"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRLowerLayerTxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu/CddPduRLowerLayerHandleId"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "RoutingPathCCB_" + mapping['SOURCE-PDU'] + "_TO_" + mapping['TARGET-PDU']
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCBRoutingPath"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_textual_param_value, "DEFINITION-REF")
                definition_ref.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCB/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCBRoutingPath/EnGwAuthorizationCallout"
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
    output.write(output_path + '/EnGwCCB.epc', encoding='UTF-8', xml_declaration=True, method="xml")

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
    # implement TRS.COMCONF.GEN.00D(1)
    containers = etree.SubElement(ecuc_module, 'CONTAINERS')
    ecuc_container = etree.SubElement(containers, 'ECUC-CONTAINER-VALUE')
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddComStackContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution"
    subcontainer = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    ecuc_container = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddPduRLowerLayerContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution"
    subcontainers = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    index = 0
    data_elements_to = []
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
                obj_sort['SHORT-NAME'] = "PduRLowerLayerTxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
                obj_sort['ID'] = 0
                obj_sort['REF'] = "/EcuC/EcuC/EcucPduCollection/" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
                obj_sort['CLUSTER'] = target_cluster
                data_elements_to.append(obj_sort)
                # Routing path
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "RoutingPathCCD_" + mapping['SOURCE-PDU'] + "_TO_" + mapping['TARGET-PDU']
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCDRoutingPath"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_textual_param_value, "DEFINITION-REF")
                definition_ref.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/EnGwCCDRoutingPath/EnGwAuthorizationCallout"
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
                obj_sort['SHORT-NAME'] = "PduRLowerLayerRxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
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
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddDiagIndexing"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddDiagIndexing"
    parameter_values = etree.SubElement(ecuc_container, 'PARAMETER-VALUES')
    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
    definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
    definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
    definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddDiagIndexing/IndexToDiagBegin"
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
    output.write(output_path + '/EnGwCCD.epc', encoding='UTF-8', xml_declaration=True, method="xml")

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
    short_name = etree.SubElement(ecuc_container, 'SHORT-NAME').text = "CddPduRLowerLayerContribution"
    definition = etree.SubElement(ecuc_container, 'DEFINITION-REF')
    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
    definition.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution"
    subcontainers = etree.SubElement(ecuc_container, 'SUB-CONTAINERS')
    index = 0
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRLowerLayerRxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu/CddPduRLowerLayerHandleId"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRLowerLayerTxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu/CddPduRLowerLayerHandleId"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "RoutingPathFonc_" + mapping['SOURCE-PDU'] + "_TO_" + mapping['TARGET-PDU']
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/EnGwFoncRoutingPath"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_textual_param_value = etree.SubElement(parameter_values, 'ECUC-TEXTUAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_textual_param_value, "DEFINITION-REF")
                definition_ref.attrib['DEST'] = "ECUC-STRING-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwFonc/CddComStackContribution/CddPduRLowerLayerContribution/EnGwFoncRoutingPath/EnGwAuthorizationCallout"
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
    output.write(output_path + '/EnGwFonc.epc', encoding='UTF-8', xml_declaration=True, method="xml")


def NeMo_script(file_list, path_list, output_path, logger):
    logger.info('======================================NeMo===========================================')
    error_no = 0
    warning_no = 0
    info_no = 0
    mappings = []
    callouts = []
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
                tree = etree.parse(file)
                root = tree.getroot()
                callout = root.findall(".//SPECIFIC-CALLOUT")
                for elem in callout:
                    obj_elem = {}
                    obj_elem['NAME'] = elem.find("SHORT-NAME").text
                    if elem.find("PDU-REF") is not None:
                        obj_elem['PDU'] = elem.find("PDU-REF").text
                    else:
                        obj_elem['PDU'] = ""
                    if elem.find("SYSTEM-SIGNAL-REF") is not None:
                        obj_elem['SIGNAL'] = elem.find("SYSTEM-SIGNAL-REF").text
                    else:
                        obj_elem['SIGNAL'] = ""
                    callouts.append(obj_elem)
            elif file.endswith(".arxml"):
                try:
                    check_if_xml_is_wellformed(file)
                    logger.info('The file: ' + file + ' is well-formed')
                    info_no = info_no + 1
                except Exception as e:
                    logger.error('The file: ' + file + ' is not well-formed: ' + str(e))
                    print('ERROR: The file: ' + file + ' is not well-formed: ' + str(e))
                tree = etree.parse(file)
                root = tree.getroot()
                mapping = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-TO-SIGNAL-MAPPING")
                for elem in mapping:
                    obj_elem = {}
                    obj_elem['DATA'] = elem
                    obj_elem['SIGNAL'] = elem.find(".//{http://autosar.org/schema/r4.0}SYSTEM-SIGNAL-REF").text
                    mappings.append(obj_elem)
        for path in path_list:
            for file in os.listdir(path):
                if file.endswith('.xml'):
                    fullname = os.path.join(path, file)
                    try:
                        check_if_xml_is_wellformed(fullname)
                        logger.info('The file: ' + fullname + ' is well-formed')
                        info_no = info_no + 1
                    except Exception as e:
                        logger.error('The file: ' + fullname + ' is not well-formed: ' + str(e))
                        print('ERROR: The file: ' + fullname + ' is not well-formed: ' + str(e))
                        error_no = error_no + 1
                    tree = etree.parse(fullname)
                    root = tree.getroot()
                    callout = root.findall(".//SPECIFIC-CALLOUT")
                    for elem in callout:
                        obj_elem = {}
                        obj_elem['NAME'] = elem.find("SHORT-NAME").text
                        if elem.find("PDU-REF") is not None:
                            obj_elem['PDU'] = elem.find("PDU-REF").text
                        else:
                            obj_elem['PDU'] = ""
                        if elem.find("SYSTEM-SIGNAL-REF") is not None:
                            obj_elem['SIGNAL'] = elem.find("SYSTEM-SIGNAL-REF").text
                        else:
                            obj_elem['SIGNAL'] = ""
                        callouts.append(obj_elem)
                elif file.endswith('.arxml'):
                    fullname = os.path.join(path, file)
                    try:
                        check_if_xml_is_wellformed(fullname)
                        logger.info('The file: ' + fullname + ' is well-formed')
                        info_no = info_no + 1
                    except Exception as e:
                        logger.error('The file: ' + fullname + ' is not well-formed: ' + str(e))
                        print('ERROR: The file: ' + fullname + ' is not well-formed: ' + str(e))
                    tree = etree.parse(fullname)
                    root = tree.getroot()
                    mapping = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-TO-SIGNAL-MAPPING")
                    for elem in mapping:
                        obj_elem = {}
                        obj_elem['DATA'] = elem
                        obj_elem['SIGNAL'] = elem.find(".//{http://autosar.org/schema/r4.0}SYSTEM-SIGNAL-REF").text
                        mappings.append(obj_elem)
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
        # create Scriptor script
        rootScript = etree.Element('Script')
        name = etree.SubElement(rootScript, 'Name').text = "ComCallout"
        description = etree.SubElement(rootScript, 'Decription').text = "Fix the parameters"
        expression = etree.SubElement(rootScript, 'Expression').text = "as:modconf('Com')[1]"
        operations = etree.SubElement(rootScript, 'Operations')
        for elem in callouts:
            if elem['SIGNAL'] != "":
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
                operation = etree.SubElement(operations, 'Operation')
                operation.attrib['Type'] = "ForEach"
                expression = etree.SubElement(operation, 'Expression')
                expression.text = "as:modconf('Com')[1]/ComConfig/*/ComSignal/*[contains(@name,'" + elem['SIGNAL'].split("/")[-1] + "')]/ComNotification"
                operations2 = etree.SubElement(operation, 'Operations')
                operation_enable = etree.SubElement(operations2, 'Operation')
                operation_enable.attrib['Type'] = "SetEnabled"
                expression_enable = etree.SubElement(operation_enable, 'Expression').text = "boolean(1)"
                operation2 = etree.SubElement(operations2, 'Operation')
                operation2.attrib['Type'] = "SetValue"
                expression2 = etree.SubElement(operation2, 'Expression').text = '"NmLib_COMCbk_' + elem['SIGNAL'].split("/")[-1] + '"'
            if elem['PDU'] != "":
                # set ComIPduCallout
                operation = etree.SubElement(operations, 'Operation')
                operation.attrib['Type'] = "ForEach"
                expression = etree.SubElement(operation, 'Expression')
                expression.text = "as:modconf('Com')[1]/ComConfig/*/ComIPdu/*[text:match(@name,'^PD" + elem['PDU'].split("/")[-1] + "_\d+[RT]$')]/ComIPduCallout"
                operations2 = etree.SubElement(operation, 'Operations')
                operation_enable = etree.SubElement(operations2, 'Operation')
                operation_enable.attrib['Type'] = "SetEnabled"
                expression_enable = etree.SubElement(operation_enable, 'Expression').text = "boolean(1)"
                operation2 = etree.SubElement(operations2, 'Operation')
                operation2.attrib['Type'] = "SetValue"
                expression2 = etree.SubElement(operation2, 'Expression').text = '"NmLib_COMCallout_' + elem['PDU'].split("/")[-1] + '"'
        pretty_xml = prettify_xml(rootScript)
        tree = etree.ElementTree(etree.fromstring(pretty_xml))
        tree.write(output_path + "/ComCallout.xml", encoding="UTF-8", xml_declaration=True, method="xml")
        print("\nNeMo execution finished with: " + str(info_no) + " infos, " + str(warning_no) + " warnings, " + str(error_no) + " errors\n")
    except Exception as e:
        print("Unexpected error: " + str(e))
        print("\nExecution stopped with: " + str(info_no) + " infos, " + str(warning_no) + " warnings, " + str(error_no) + " errors\n")
        try:
            os.remove(output_path + '/ComCallout.xml')
        except OSError:
            pass
        sys.exit(1)


def EcuC_config(file_list, path_list, output_path, logger):
    # create config
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    mappings = []
    can_frames = []
    diag_tools = []
    nads = []
    items = []
    for file in file_list:
        if file.endswith('.arxml'):
            tree = etree.parse(file)
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
        elif file.endswith('.xml'):
            tree = etree.parse(file)
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
        elif file.endswith('.epc'):
            tree = etree.parse(file)
            root = tree.getroot()
            elements = root.findall(".//{http://autosar.org/2.1.2}CONTAINER")
            for element in elements:
                element_type = element.find(".//{http://autosar.org/2.1.2}DEFINITION-REF")
                if element_type.text.split("/")[-1] == "DiagTool":
                    diag_tools.append(element.find(".//{http://autosar.org/2.1.2}VALUE-REF").text.split("/")[-1])
                elif element_type.text.split("/")[-1] == "Nad":
                    obj_nad = {}
                    obj_nad['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                    obj_nad['ID'] = element.find(".//{http://autosar.org/2.1.2}VALUE").text
                    obj_nad['NETWORK'] = element.getparent().getparent().getchildren()[0].text
                    obj_nad['CONFIG'] = element.getparent().getparent().getparent().getparent().getchildren()[0].text
                    nads.append(obj_nad)
    for path in path_list:
        for file in os.listdir(path):
            if file.endswith('.arxml'):
                fullname = os.path.join(path, file)
                tree = etree.parse(fullname)
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
            elif file.endswith('.xml'):
                fullname = os.path.join(path, file)
                tree = etree.parse(fullname)
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
            elif file.endswith('.epc'):
                fullname = os.path.join(path, file)
                tree = etree.parse(fullname)
                root = tree.getroot()
                elements = root.findall(".//{http://autosar.org/2.1.2}CONTAINER")
                for element in elements:
                    element_type = element.find(".//{http://autosar.org/2.1.2}DEFINITION-REF")
                    if element_type.text.split("/")[-1] == "DiagTool":
                        diag_tools.append(element.find(".//{http://autosar.org/2.1.2}VALUE-REF").text.split("/")[-1])
                    elif element_type.text.split("/")[-1] == "Nad":
                        obj_nad = {}
                        obj_nad['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                        obj_nad['ID'] = element.find(".//{http://autosar.org/2.1.2}VALUE").text
                        obj_nad['NETWORK'] = element.getparent().getparent().getchildren()[0].text
                        obj_nad['CONFIG'] = element.getparent().getparent().getparent().getparent().getchildren()[0].text
                        nads.append(obj_nad)
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
    for diag_tool in diag_tools:
        for nad in nads:
            if nad['CONFIG'] == "Config21":
                # REQ part
                ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "SCA_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanTp"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanTp_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_SCA"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "SCA_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanTp"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanTp_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_SCA"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    # LinTp<=>LinTp
    comment = etree.Comment("LinTp<=>LinTp")
    subcontainer.append(comment)
    for nad in nads:
        if nad['CONFIG'] == "Config21":
            # REQ part
            ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "SCA_REQ_" + nad['NETWORK'] + "_" + nad['NAME'] + "_LinTp"
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
            short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "LinTp_REQ_" + nad['NETWORK'] + "_" + nad['NAME'] + "_SCA"
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
            short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "SCA_REP_" + nad['NETWORK'] + "_" + nad['NAME'] + "_LinTp"
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
            short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "LinTp_REP_" + nad['NETWORK'] + "_" + nad['NAME'] + "_SCA"
            definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
            parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
            ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
            definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
            value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    # CanIf<=>CanTp
    comment = etree.Comment("CanIf<=>CanTp")
    subcontainer.append(comment)
    for diag_tool in diag_tools:
        network_list = []
        for nad in nads:
            if nad['CONFIG'] == "Config21":
                if nad['NETWORK'] not in network_list:
                    network_list.append(nad['NETWORK'])
                    ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                    short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanIf_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_CanTp"
                    definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                    definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                    definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
                    parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                    definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                    definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                    definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
                    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    for diag_tool in diag_tools:
        for nad in nads:
            if nad['CONFIG'] == "Config21":
                ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanTp_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanIf"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanTp_FC_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanIf"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "8"
    # CanIf<=>CanIf
    comment = etree.Comment("CanIf<=>CanIf")
    subcontainer.append(comment)
    for diag_tool in diag_tools:
        for nad in nads:
            if nad['CONFIG'] == "Config13":
                # REQ part
                ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "SCA_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanIf"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanIf_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_SCA"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "SCA_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanIf"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanIf_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_SCA"
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
        if nad['CONFIG'] == "Config13":
            if nad['NETWORK'] not in network_list:
                network_list.append(nad['NETWORK'])
                # REQ part
                ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "SCA_REQ_" + nad['NETWORK'] + "_1P3_LinIf"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "LinIf_REQ_" + nad['NETWORK'] + "_1P3_SCA"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "SCA_REP_" + nad['NETWORK'] + "_1P3_LinIf"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "LinIf_REP_" + nad['NETWORK'] + "_1P3_SCA"
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
    # only for testing
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
    output.write(output_path + '/EcuC.epc', encoding='UTF-8', xml_declaration=True, method="xml")
    return


def CanIf_config(file_list, path_list, output_path, logger):
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    diag_tools = []
    nads = []
    lins = []
    for file in file_list:
        if file.endswith('.epc'):
            tree = etree.parse(file)
            root = tree.getroot()
            elements = root.findall(".//{http://autosar.org/2.1.2}CONTAINER")
            for element in elements:
                element_type = element.find(".//{http://autosar.org/2.1.2}DEFINITION-REF")
                if element_type.text.split("/")[-1] == "DiagTool":
                    diag_tools.append(element.find(".//{http://autosar.org/2.1.2}VALUE-REF").text.split("/")[-1])
                elif element_type.text.split("/")[-1] == "NetworkLin" and element_type.text.split("/")[-2] == "ConfigLin21":
                    obj_lin = {}
                    obj_lin['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                    ids = element.findall(".//{http://autosar.org/2.1.2}VALUE")
                    for id in ids:
                        if id.getparent().getchildren()[0].text.split("/")[-1] == "ReqId":
                            obj_lin['REQ-ID'] = id.text
                        if id.getparent().getchildren()[0].text.split("/")[-1] == "RepId":
                            obj_lin['REP-ID'] = id.text
                    lins.append(obj_lin)
                elif element_type.text.split("/")[-1] == "Nad":
                    obj_nad = {}
                    obj_nad['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                    obj_nad['ID'] = element.find(".//{http://autosar.org/2.1.2}VALUE").text
                    obj_nad['NETWORK'] = element.getparent().getparent().getchildren()[0].text
                    obj_nad['CONFIG'] = element.getparent().getparent().getparent().getparent().getchildren()[0].text
                    nads.append(obj_nad)
    for path in path_list:
        for file in os.listdir(path):
            if file.endswith('.epc'):
                tree = etree.parse(file)
                root = tree.getroot()
                elements = root.findall(".//{http://autosar.org/2.1.2}CONTAINER")
                for element in elements:
                    element_type = element.find(".//{http://autosar.org/2.1.2}DEFINITION-REF")
                    if element_type.text.split("/")[-1] == "DiagTool":
                        diag_tools.append(element.find(".//{http://autosar.org/2.1.2}VALUE-REF").text.split("/")[-1])
                    elif element_type.text.split("/")[-1] == "NetworkLin" and element_type.text.split("/")[-2] == "ConfigLin21":
                        obj_lin = {}
                        obj_lin['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                        ids = element.findall(".//{http://autosar.org/2.1.2}VALUE")
                        for id in ids:
                            if id.getparent().getchildren()[0].text.split("/")[-1] == "ReqId":
                                obj_lin['REQ-ID'] = id.text
                            if id.getparent().getchildren()[0].text.split("/")[-1] == "RepId":
                                obj_lin['REP-ID'] = id.text
                        lins.append(obj_lin)
                    elif element_type.text.split("/")[-1] == "Nad":
                        obj_nad = {}
                        obj_nad['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                        obj_nad['ID'] = element.find(".//{http://autosar.org/2.1.2}VALUE").text
                        obj_nad['NETWORK'] = element.getparent().getparent().getchildren()[0].text
                        obj_nad['CONFIG'] = element.getparent().getparent().getparent().getparent().getchildren()[0].text
                        nads.append(obj_nad)

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
        for lin in lins:
            ecuc_container_value = etree.SubElement(subcontainer_init, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(ecuc_container_value, "SHORT-NAME").text = "CanIfRxPduCfg_REQ_" + diag_tool + "_" + lin['NAME']
            definition = etree.SubElement(ecuc_container_value, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg"
            parameters = etree.SubElement(ecuc_container_value, "PARAMETER-VALUES")
            numerical_0 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
            definition_0 = etree.SubElement(numerical_0, "DEFINITION-REF")
            definition_0.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_0.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg/CanIfRxPduCanId"
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
            val_textual_1 = etree.SubElement(textual_1, "VALUE").text = "STANDARD_CAN"
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
            value.text = "/EcuC/EcuC/EcucPduCollection/CanIf_REQ_" + diag_tool + "_" + lin['NAME'] + "_CanTp"
            ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfRxPduCfg/CanIfRxPduHrhIdRef"
            value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/CanIf/CanIf/CanIfInitCfg/CanIfInitHohCfg/HOH_0_VSM_" + diag_tool
    for diag_tool in diag_tools:
        for nad in nads:
            if nad['CONFIG'] == "Config21":
                # Tx N PDU
                ecuc_container_value = etree.SubElement(subcontainer_init, "ECUC-CONTAINER-VALUE")
                short_name = etree.SubElement(ecuc_container_value, "SHORT-NAME").text = "CanIfTxPduCfg_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME']
                definition = etree.SubElement(ecuc_container_value, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg"
                parameters = etree.SubElement(ecuc_container_value, "PARAMETER-VALUES")
                for lin in lins:
                    if lin['NAME'] == nad['NETWORK']:
                        numerical_0 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_0 = etree.SubElement(numerical_0, "DEFINITION-REF")
                        definition_0.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                        definition_0.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduCanId"
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
                val_textual_3 = etree.SubElement(textual_3, "VALUE").text = "CAN_TP"
                references = etree.SubElement(ecuc_container_value, "REFERENCE-VALUES")
                ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
                definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduRef"
                value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
                value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value.text = "/EcuC/EcuC/EcucPduCollection/CanTp_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanIf"
                ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
                definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduBufferRef"
                value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
                value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value.text = "/CanIf/CanIf/CanIfInitCfg/HOH_2_VSM_" + diag_tool
                # Tx N FC PDU
                ecuc_container_value = etree.SubElement(subcontainer_init, "ECUC-CONTAINER-VALUE")
                short_name = etree.SubElement(ecuc_container_value, "SHORT-NAME").text = "CanIfTxPduCfg_FC_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME']
                definition = etree.SubElement(ecuc_container_value, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg"
                parameters = etree.SubElement(ecuc_container_value, "PARAMETER-VALUES")
                for lin in lins:
                    if lin['NAME'] == nad['NETWORK']:
                        numerical_0 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                        definition_0 = etree.SubElement(numerical_0, "DEFINITION-REF")
                        definition_0.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                        definition_0.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduCanId"
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
                val_textual_3 = etree.SubElement(textual_3, "VALUE").text = "CAN_TP"
                references = etree.SubElement(ecuc_container_value, "REFERENCE-VALUES")
                ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
                definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduRef"
                value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
                value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value.text = "/EcuC/EcuC/EcucPduCollection/CanTp_FC_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_CanIf"
                ecuc_ref_value = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
                definition = etree.SubElement(ecuc_ref_value, "DEFINITION-REF")
                definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
                definition.text = "/AUTOSAR/EcuDefs/CanIf/CanIfInitCfg/CanIfTxPduCfg/CanIfTxPduBufferRef"
                value = etree.SubElement(ecuc_ref_value, "VALUE-REF")
                value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value.text = "/CanIf/CanIf/CanIfInitCfg/HOH_2_VSM_" + diag_tool
    # generate data
    pretty_xml = prettify_xml(rootCanIf)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/CanIf.epc', encoding='UTF-8', xml_declaration=True, method="xml")
    return


def CanTp_config(file_list, path_list, output_path, logger):
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    diag_tools = []
    nads = []
    lins = []
    for file in file_list:
        if file.endswith('.epc'):
            tree = etree.parse(file)
            root = tree.getroot()
            elements = root.findall(".//{http://autosar.org/2.1.2}CONTAINER")
            for element in elements:
                element_type = element.find(".//{http://autosar.org/2.1.2}DEFINITION-REF")
                if element_type.text.split("/")[-1] == "DiagTool":
                    diag_tools.append(element.find(".//{http://autosar.org/2.1.2}VALUE-REF").text.split("/")[-1])
                elif element_type.text.split("/")[-1] == "NetworkLin" and element_type.text.split("/")[-2] == "ConfigLin21":
                    lins.append(element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text)
                elif element_type.text.split("/")[-1] == "Nad":
                    obj_nad = {}
                    obj_nad['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                    obj_nad['ID'] = element.find(".//{http://autosar.org/2.1.2}VALUE").text
                    obj_nad['NETWORK'] = element.getparent().getparent().getchildren()[0].text
                    obj_nad['CONFIG'] = element.getparent().getparent().getparent().getparent().getchildren()[0].text
                    nads.append(obj_nad)
    for path in path_list:
        for file in os.listdir(path):
            if file.endswith('.epc'):
                tree = etree.parse(file)
                root = tree.getroot()
                elements = root.findall(".//{http://autosar.org/2.1.2}CONTAINER")
                for element in elements:
                    element_type = element.find(".//{http://autosar.org/2.1.2}DEFINITION-REF")
                    if element_type.text.split("/")[-1] == "DiagTool":
                        diag_tools.append(element.find(".//{http://autosar.org/2.1.2}VALUE-REF").text.split("/")[-1])
                    elif element_type.text.split("/")[-1] == "NetworkLin" and element_type.text.split("/")[-2] == "ConfigLin21":
                        lins.append(element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text)
                    elif element_type.text.split("/")[-1] == "Nad":
                        obj_nad = {}
                        obj_nad['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                        obj_nad['ID'] = element.find(".//{http://autosar.org/2.1.2}VALUE").text
                        obj_nad['NETWORK'] = element.getparent().getparent().getchildren()[0].text
                        obj_nad['CONFIG'] = element.getparent().getparent().getparent().getparent().getchildren()[0].text
                        nads.append(obj_nad)

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
            ecuc_container_value = etree.SubElement(subcontainer_init, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(ecuc_container_value, "SHORT-NAME").text = "CanTpChannel_Gw_" + diag_tool + "_" + lin
            definition = etree.SubElement(ecuc_container_value, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel"
            parameter = etree.SubElement(ecuc_container_value, "PARAMETER-VALUES")
            ecuc_textual_param_value = etree.SubElement(parameter, "ECUC-TEXTUAL-PARAM-VALUE")
            definition_ref = etree.SubElement(ecuc_textual_param_value, "DEFINITION-REF")
            definition_ref.attrib['DEST'] = "ECUC-ENUMERATION-PARAM-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpChannelMode"
            value = etree.SubElement(ecuc_textual_param_value, "VALUE").text = "CANTP_MODE_HALF_DUPLEX"
            subcontainer_nad = etree.SubElement(ecuc_container_value, "SUB-CONTAINERS")
            # REQ part
            for nad in nads:
                if nad['NETWORK'] == lin and nad['CONFIG'] == "Config21":
                    ecuc_container_nad = etree.SubElement(subcontainer_nad, "ECUC-CONTAINER-VALUE")
                    short_name = etree.SubElement(ecuc_container_nad, "SHORT-NAME").text = "CanTpRxNSdu_REQ_" + diag_tool + "_" + lin + "_" + nad['NAME']
                    definition = etree.SubElement(ecuc_container_nad, "DEFINITION-REF")
                    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                    definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu"
                    parameters = etree.SubElement(ecuc_container_nad, "PARAMETER-VALUES")
                    numerical_0 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                    definition_0 = etree.SubElement(numerical_0, "DEFINITION-REF")
                    definition_0.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                    definition_0.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpRxNSdu/CanTpRxNSduId"
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
                    value.text = "/EcuC/EcuC/EcucPduCollection/CanTp_REQ_" + diag_tool + "_" + lin + "_" + nad['NAME'] + "_SCA"
                    subcontainers = etree.SubElement(ecuc_container_nad, "SUB-CONTAINERS")
                    ecuc_container_1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
                    short_name = etree.SubElement(ecuc_container_1, "SHORT-NAME").text = "CanTpNSa_REQ_" + diag_tool + "_" + lin + "_" + nad['NAME']
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
                    short_name = etree.SubElement(ecuc_container_2, "SHORT-NAME").text = "CanTpNTa_REQ_" + diag_tool + "_" + lin + "_" + nad['NAME']
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
                    short_name = etree.SubElement(ecuc_container_3, "SHORT-NAME").text = "CanTpRxNPdu_REQ_" + diag_tool + "_" + lin + "_" + nad['NAME']
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
                    value.text = "/EcuC/EcuC/EcucPduCollection/CanIf_REQ_" + diag_tool + "_" + lin + "_CanTp"
                    ecuc_container_4 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
                    short_name = etree.SubElement(ecuc_container_4, "SHORT-NAME").text = "CanTpTxFcNPdu_REQ_" + diag_tool + "_" + lin + "_" + nad['NAME']
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
                    value.text = "/EcuC/EcuC/EcucPduCollection/CanTp_FC_REP_" + diag_tool + "_" + lin + "_" + nad['NAME'] + "_CanIf"
                    # REP part
                    ecuc_container_nad = etree.SubElement(subcontainer_nad, "ECUC-CONTAINER-VALUE")
                    short_name = etree.SubElement(ecuc_container_nad, "SHORT-NAME").text = "CanTpTxNSdu_REP_" + diag_tool + "_" + lin + "_" + nad['NAME']
                    definition = etree.SubElement(ecuc_container_nad, "DEFINITION-REF")
                    definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                    definition.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu"
                    parameters = etree.SubElement(ecuc_container_nad, "PARAMETER-VALUES")
                    numerical_0 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
                    definition_0 = etree.SubElement(numerical_0, "DEFINITION-REF")
                    definition_0.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                    definition_0.text = "/AUTOSAR/EcuDefs/CanTp/CanTpConfig/CanTpChannel/CanTpTxNSdu/CanTpTxNSduId"
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
                    value.text = "/EcuC/EcuC/EcucPduCollection/CanTp_REP_" + diag_tool + "_" + lin + "_" + nad['NAME'] + "_SCA"
                    subcontainers = etree.SubElement(ecuc_container_nad, "SUB-CONTAINERS")
                    ecuc_container_1 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
                    short_name = etree.SubElement(ecuc_container_1, "SHORT-NAME").text = "CanTpNSa_REP_" + diag_tool + "_" + lin + "_" + nad['NAME']
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
                    short_name = etree.SubElement(ecuc_container_2, "SHORT-NAME").text = "CanTpNTa_REP_" + diag_tool + "_" + lin + "_" + nad['NAME']
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
                    short_name = etree.SubElement(ecuc_container_3, "SHORT-NAME").text = "CanTpTxNPdu_REP_" + diag_tool + "_" + lin + "_" + nad['NAME']
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
                    value.text = "/EcuC/EcuC/EcucPduCollection/CanTp_REP_" + diag_tool + "_" + lin + "_" + nad['NAME'] + "_CanIf"
                    ecuc_container_4 = etree.SubElement(subcontainers, "ECUC-CONTAINER-VALUE")
                    short_name = etree.SubElement(ecuc_container_4, "SHORT-NAME").text = "CanTpRxFcNPdu_REP_" + diag_tool + "_" + lin + "_" + nad['NAME']
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
                    value.text = "/EcuC/EcuC/EcucPduCollection/CanIf_REQ_" + diag_tool + "_" + lin + "_CanTp"
    # generate data
    pretty_xml = prettify_xml(rootCanTp)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/CanTp.epc', encoding='UTF-8', xml_declaration=True, method="xml")
    return


def LinTp_config(file_list, path_list, output_path, logger):
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    nads = []
    lins = []
    for file in file_list:
        if file.endswith('.epc'):
            tree = etree.parse(file)
            root = tree.getroot()
            elements = root.findall(".//{http://autosar.org/2.1.2}CONTAINER")
            for element in elements:
                element_type = element.find(".//{http://autosar.org/2.1.2}DEFINITION-REF")
                if element_type.text.split("/")[-1] == "NetworkLin" and element_type.text.split("/")[-2] == "ConfigLin21":
                    lins.append(element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text)
                elif element_type.text.split("/")[-1] == "Nad":
                    obj_nad = {}
                    obj_nad['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                    obj_nad['ID'] = element.find(".//{http://autosar.org/2.1.2}VALUE").text
                    obj_nad['NETWORK'] = element.getparent().getparent().getchildren()[0].text
                    obj_nad['CONFIG'] = element.getparent().getparent().getparent().getparent().getchildren()[0].text
                    nads.append(obj_nad)
    for path in path_list:
        for file in os.listdir(path):
            if file.endswith('.epc'):
                tree = etree.parse(file)
                root = tree.getroot()
                elements = root.findall(".//{http://autosar.org/2.1.2}CONTAINER")
                for element in elements:
                    element_type = element.find(".//{http://autosar.org/2.1.2}DEFINITION-REF")
                    if element_type.text.split("/")[-1] == "NetworkLin" and element_type.text.split("/")[-2] == "ConfigLin21":
                        lins.append(element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text)
                    elif element_type.text.split("/")[-1] == "Nad":
                        obj_nad = {}
                        obj_nad['NAME'] = element.find(".//{http://autosar.org/2.1.2}SHORT-NAME").text
                        obj_nad['ID'] = element.find(".//{http://autosar.org/2.1.2}VALUE").text
                        obj_nad['NETWORK'] = element.getparent().getparent().getchildren()[0].text
                        obj_nad['CONFIG'] = element.getparent().getparent().getparent().getparent().getchildren()[0].text
                        nads.append(obj_nad)

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
    for nad in nads:
        if nad['CONFIG'] == "Config21":
            lin = ""
            if nad['NETWORK'] == "LIN1":
                lin = "LIN_VSM_1_Channel"
            elif nad['NETWORK'] == "LIN2":
                lin = "LIN_VSM_2_Channel"
            elif nad['NETWORK'] == "LIN3":
                lin = "LIN_VSM_3_Channel"
            elif nad['NETWORK'] == "LIN4":
                lin = "LIN_VSM_4_Channel"
            elif nad['NETWORK'] == "LIN5":
                lin = "LIN_VSM_5_Channel"
            elif nad['NETWORK'] == "LIN6":
                lin = "LIN_VSM_6_Channel"
            elif nad['NETWORK'] == "LIN7":
                lin = "LIN_VSM_7_Channel"
            elif nad['NETWORK'] == "LIN8":
                lin = "LIN_VSM_8_Channel"
            # REP part
            ecuc_nad = etree.SubElement(subcontainer_general, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(ecuc_nad, "SHORT-NAME").text = "LinTpRxNSdu_REP_" + nad['NETWORK'] + "_" + nad['NAME']
            definition_nad = etree.SubElement(ecuc_nad, "DEFINITION-REF")
            definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition_nad.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpRxNSdu"
            parameters = etree.SubElement(ecuc_nad, "PARAMETER-VALUES")
            numerical_1 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
            definition_1 = etree.SubElement(numerical_1, "DEFINITION-REF")
            definition_1.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_1.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpRxNSdu/LinTpDl"
            value_1 = etree.SubElement(numerical_1, "VALUE").text = "1"
            numerical_2 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
            definition_2 = etree.SubElement(numerical_2, "DEFINITION-REF")
            definition_2.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_2.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpRxNSdu/LinTpRxNSduNad"
            value_2 = etree.SubElement(numerical_2, "VALUE").text = str(nad['ID'])
            numerical_3 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
            definition_3 = etree.SubElement(numerical_3, "DEFINITION-REF")
            definition_3.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
            definition_3.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpRxNSdu/LinTpNcr"
            value_3 = etree.SubElement(numerical_3, "VALUE").text = "1.0"
            references = etree.SubElement(ecuc_nad, "REFERENCE-VALUES")
            ecuc_ref_value_1 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(ecuc_ref_value_1, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpRxNSdu/LinTpRxNSduPduRef"
            value = etree.SubElement(ecuc_ref_value_1, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/EcuC/EcuC/EcucPduCollection/LinTp_REP_" + nad['NETWORK'] + "_" + nad['NAME'] + "_SCA"
            ecuc_ref_value_2 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(ecuc_ref_value_2, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpRxNSdu/LinTpRxNSduChannelRef"
            value = etree.SubElement(ecuc_ref_value_2, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/LinIf/LinIf/LinIfGlobalConfig/" + lin
            ecuc_ref_value_2 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(ecuc_ref_value_2, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpRxNSdu/LinTpRxNSduTpChannelRef"
            value = etree.SubElement(ecuc_ref_value_2, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/LinTp/LinTp/LinTpGlobalConfig/LinTpChannel_" + nad['NETWORK']
            # REQ part
            ecuc_nad = etree.SubElement(subcontainer_general, "ECUC-CONTAINER-VALUE")
            short_name = etree.SubElement(ecuc_nad, "SHORT-NAME").text = "LinTpTxNSdu_REQ_" + nad['NETWORK'] + "_" + nad['NAME']
            definition_nad = etree.SubElement(ecuc_nad, "DEFINITION-REF")
            definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition_nad.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpTxNSdu"
            parameters = etree.SubElement(ecuc_nad, "PARAMETER-VALUES")
            numerical_1 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
            definition_1 = etree.SubElement(numerical_1, "DEFINITION-REF")
            definition_1.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
            definition_1.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpTxNSdu/LinTpNas"
            value_1 = etree.SubElement(numerical_1, "VALUE").text = "0.1"
            numerical_2 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
            definition_2 = etree.SubElement(numerical_2, "DEFINITION-REF")
            definition_2.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition_2.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpTxNSdu/LinTpTxNSduNad"
            value_2 = etree.SubElement(numerical_2, "VALUE").text = str(nad['ID'])
            numerical_3 = etree.SubElement(parameters, "ECUC-NUMERICAL-PARAM-VALUE")
            definition_3 = etree.SubElement(numerical_3, "DEFINITION-REF")
            definition_3.attrib['DEST'] = "ECUC-FLOAT-PARAM-DEF"
            definition_3.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpTxNSdu/LinTpNcs"
            value_3 = etree.SubElement(numerical_3, "VALUE").text = "0.1"
            references = etree.SubElement(ecuc_nad, "REFERENCE-VALUES")
            ecuc_ref_value_1 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(ecuc_ref_value_1, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpTxNSdu/LinTpTxNSduPduRef"
            value = etree.SubElement(ecuc_ref_value_1, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/EcuC/EcuC/EcucPduCollection/LinTp_REQ_" + nad['NETWORK'] + "_" + nad['NAME'] + "_SCA"
            ecuc_ref_value_2 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(ecuc_ref_value_2, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpTxNSdu/LinTpTxNSduChannelRef"
            value = etree.SubElement(ecuc_ref_value_2, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/LinIf/LinIf/LinIfGlobalConfig/" + lin
            ecuc_ref_value_2 = etree.SubElement(references, "ECUC-REFERENCE-VALUE")
            definition = etree.SubElement(ecuc_ref_value_2, "DEFINITION-REF")
            definition.attrib['DEST'] = "ECUC-REFERENCE-DEF"
            definition.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpTxNSdu/LinTpTxNSduTpChannelRef"
            value = etree.SubElement(ecuc_ref_value_2, "VALUE-REF")
            value.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
            value.text = "/LinTp/LinTp/LinTpGlobalConfig/LinTpChannel_" + nad['NETWORK']
    network_list = []
    for nad in nads:
        if nad['CONFIG'] == "Config21":
            if nad['NETWORK'] not in network_list:
                network_list.append(nad['NETWORK'])
                ecuc_nad = etree.SubElement(subcontainer_general, "ECUC-CONTAINER-VALUE")
                short_name = etree.SubElement(ecuc_nad, "SHORT-NAME").text = "LinTpChannel_" + nad['NETWORK']
                definition_nad = etree.SubElement(ecuc_nad, "DEFINITION-REF")
                definition_nad.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_nad.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpChannelConfig"
                parameter_values = etree.SubElement(ecuc_nad, "PARAMETER-VALUES")
                boolean_1 = etree.SubElement(parameter_values, "ECUC-NUMERICAL-PARAM-VALUE")
                definition_1 = etree.SubElement(boolean_1, "DEFINITION-REF")
                definition_1.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
                definition_1.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpChannelConfig/LinTpDropNotRequestedNad"
                value_1 = etree.SubElement(boolean_1, "VALUE").text = "0"
                boolean_2 = etree.SubElement(parameter_values, "ECUC-NUMERICAL-PARAM-VALUE")
                definition_2 = etree.SubElement(boolean_2, "DEFINITION-REF")
                definition_2.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
                definition_2.text = "/AUTOSAR/EcuDefs/LinTp/LinTpGlobalConfig/LinTpChannelConfig/LinTpScheduleChangeDiag"
                value_2 = etree.SubElement(boolean_2, "VALUE").text = "1"

    # generate data
    pretty_xml = prettify_xml(rootLinTp)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/LinTp.epc', encoding='UTF-8', xml_declaration=True, method="xml")
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
