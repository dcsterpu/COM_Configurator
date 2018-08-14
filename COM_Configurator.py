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
    hdlr = logging.FileHandler(path + '/result.log')
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
                EnGw_config(files_list, paths_list, output_path, logger)
                EcuC_config(files_list, paths_list, output_path, logger)
        else:
            logger = set_logger(output_path)
            if NeMo:
                NeMo_script(files_list, paths_list, output_path, logger)
            if EnGw:
                EnGw_config(files_list, paths_list, output_path, logger)
                EcuC_config(files_list, paths_list, output_path, logger)
                PduR_config(files_list, paths_list, output_path, logger)
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
            else:
                logger = set_logger(output_epc)
                if EnGw:
                    EnGw_config(files_list, paths_list, output_epc, logger)
                    EcuC_config(files_list, paths_list, output_epc, logger)
                    PduR_config(files_list, paths_list, output_epc, logger)
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
            else:
                logger = set_logger(output_script)
                if NeMo:
                    NeMo_script(files_list, paths_list, output_script, logger)
    else:
        print("\nNo output path defined!\n")
        sys.exit(1)


def PduR_config(file_list, path_list, output_path, logger):
    NSMAP = {None: 'http://autosar.org/schema/r4.0', "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    mappings = []
    can_frames = []
    items = []
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
    # create ouput file: EcuC.epc
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
    index_id = 0
    for route in routes:
        ecuc_container_value = etree.SubElement(subcontainer_init, 'ECUC-CONTAINER-VALUE')
        short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRRoutingTable_" + route['SOURCE']
        definition = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
        definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable"
        param_values = etree.SubElement(ecuc_container_value, 'ECUC-NUMERICAL-PARAM-VALUE')
        definition_routing = etree.SubElement(param_values, 'DEFINITION-REF')
        definition_routing.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
        definition_routing.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRIsMinimumRouting"
        value_routing = etree.SubElement(param_values, 'VALUE').text = "0"
        subcontainer_route = etree.SubElement(ecuc_container_value, 'SUB-CONTAINERS')
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
        value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/" + route['SOURCE']
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
            ecuc_container_value = etree.SubElement(subcontainer_init, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRRoutingTable_" + route['SOURCE'] + "_" + dest['TARGET'] + "_FROM_CDD"
            definition = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable"
            param_values = etree.SubElement(ecuc_container_value, 'ECUC-NUMERICAL-PARAM-VALUE')
            definition_routing = etree.SubElement(param_values, 'DEFINITION-REF')
            definition_routing.attrib['DEST'] = "ECUC-BOOLEAN-PARAM-DEF"
            definition_routing.text = "/AUTOSAR/EcuDefs/PduR/PduRRoutingTables/PduRRoutingTable/PduRIsMinimumRouting"
            value_routing = etree.SubElement(param_values, 'VALUE').text = "0"
            subcontainer_route = etree.SubElement(ecuc_container_value, 'SUB-CONTAINERS')
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
            value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/" + route['SOURCE'] + "_FROM_CDD"
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
            value = etree.SubElement(ecuc_reference_value, 'VALUE-REF').text = "/EcuC/EcuC/EcucPduCollection/" + dest['TARGET']
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
    # implement TRS.COMCONF.GEN.001(1)
    containers = etree.SubElement(ecuc_module, 'CONTAINERS')
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "LinIfRxNSdu_REQ_" + nad['NETWORK'] + "_1P3"
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
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + nad['NETWORK'] + "_1P3_LinIf"
                # REP part
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "LinIfRxNSdu_REP_" + nad['NETWORK'] + "_1P3"
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
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REP_" + nad['NETWORK'] + "_1P3_LinIf"
    for nad in nads:
        if nad['CONFIG'] == "Config21":
            # REQ part
            comment = etree.Comment("LinTp")
            subcontainers.append(comment)
            ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "LinTpRxNSdu_REQ_" + nad['NETWORK'] + "_" + nad['NAME'] + "_2P1"
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
            value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + nad['NETWORK'] + "_" + nad['NAME'] + "_LinTp"
            # REP part
            ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "LinTpRxNSdu_REP_" + nad['NETWORK'] + "_" + nad['NAME'] + "_2P1"
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
            value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REP_" + nad['NETWORK'] + "_" + nad['NAME'] + "_LinTp"
    for diag_tool in diag_tools:
        for nad in nads:
            if nad['CONFIG'] == "Config21":
                # REQ part
                comment = etree.Comment("CanTp")
                subcontainers.append(comment)
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanTpRxNSdu_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_2P1"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanTpRxNSdu_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_2P1"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanIfRxPduCfg_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_1P3"
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
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanIfRxPduCfg_REP_" + diag_tool + "_" + nad['NETWORK'] + "_" + nad['NAME'] + "_1P3"
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
            if mapping['SOURCE'] == "/"+frame['ROOT']+"/"+frame['PACKAGE']+"/"+frame['CLUSTER']+"/"+frame['CHANNEL']+"/"+frame['NAME']:
                found_source = True
            if mapping['TARGET'] == "/"+frame['ROOT']+"/"+frame['PACKAGE']+"/"+frame['CLUSTER']+"/"+frame['CHANNEL']+"/"+frame['NAME']:
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
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
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
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
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
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
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
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
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
    for mapping in mappings:
        found_source = False
        found_target = False
        for frame in can_frames:
            if mapping['SOURCE'] == "/" + frame['ROOT'] + "/" + frame['PACKAGE'] + "/" + frame['CLUSTER'] + "/" + frame['CHANNEL'] + "/" + frame['NAME']:
                found_source = True
            if mapping['TARGET'] == "/" + frame['ROOT'] + "/" + frame['PACKAGE'] + "/" + frame['CLUSTER'] + "/" + frame['CHANNEL'] + "/" + frame['NAME']:
                found_target = True
            if found_source and found_target and mapping['TYPE'] == "GW-CAN-DIAG":
                # REQ part
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRLowerLayerRxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu/CddPduRLowerLayerHandleId"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerRxPdu/CddPduRLowerLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
                # REP part
                ecuc_container_value = etree.SubElement(subcontainers, 'ECUC-CONTAINER-VALUE')
                short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "PduRLowerLayerTxPdu_" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
                definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu"
                parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                definition_ref = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu/CddPduRLowerLayerHandleId"
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = str(index)
                index = index + 1
                reference_values = etree.SubElement(ecuc_container_value, 'REFERENCE-VALUES')
                ecuc_reference_value = etree.SubElement(reference_values, 'ECUC-REFERENCE-VALUE')
                definition_ref = etree.SubElement(ecuc_reference_value, 'DEFINITION-REF')
                definition_ref.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                definition_ref.text = "/AUTOSAR/EcuDefs/EnGwCCD/CddComStackContribution/CddPduRLowerLayerContribution/CddPduRLowerLayerTxPdu/CddPduRLowerLayerPduRef"
                value_ref = etree.SubElement(ecuc_reference_value, 'VALUE-REF')
                value_ref.attrib['DEST'] = "ECUC-CONTAINER-VALUE"
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
                break
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
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + mapping['TARGET-PDU'].split("/")[-1] + "_FROM_CDD"
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
                value_ref.text = "/EcuC/EcuC/EcucPduCollection/SCA_REQ_" + mapping['TARGET-PDU'].split("/")[-1] + "_TO_CDD"
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
        if error_no != 0:
            print("There is at least one blocking error! Check the generated log.")
            print("\n stopped with: " + str(info_no) + " infos, " + str(warning_no) + " warnings, " + str(error_no) + " errors\n")
            try:
                os.remove(output_path + '/ComCallout.xml')
            except OSError:
                pass
            sys.exit(1)
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
                expression.text = "as:modconf('Com')[1]/ComConfig/*/ComIPdu/*[contains(@name,'" + elem['PDU'].split("/")[-1] + "')]/ComIPduCallout"
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
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
            value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
            value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
            value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
            value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
    # CanIf<=>CanTp
    comment = etree.Comment("CanIf<=>CanTp")
    subcontainer.append(comment)
    for diag_tool in diag_tools:
        network_list = []
        for nad in nads:
            if nad['CONFIG'] == "Config21":
                if nad['NETWORK'] not in network_list:
                    network_list.append(nad['NETWORK'])
                    # REQ part
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
                    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
                    ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
                    short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = "CanTp_REQ_" + diag_tool + "_" + nad['NETWORK'] + "_CanIf"
                    definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
                    definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
                    definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
                    parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
                    ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
                    definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
                    definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
                    definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
                    value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
                value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
    # PduR dependencies
    comment = etree.Comment("PduR dependencies")
    subcontainer.append(comment)
    for item in items:
        ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
        short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = item['SOURCE'] + "_FROM_CDD"
        definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
        definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
        parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
        ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
        definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
        definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
        value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
        # to be deleted because the frame will be automatically imported
        ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
        short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = item['SOURCE']
        definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
        definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
        definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
        parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
        ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
        definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
        definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
        definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
        value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
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
            value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"
            # to be deleted because the frame will be automatically imported
            ecuc_container_value = etree.SubElement(subcontainer, 'ECUC-CONTAINER-VALUE')
            short_name = etree.SubElement(ecuc_container_value, 'SHORT-NAME').text = destination['TARGET']
            definition_ref = etree.SubElement(ecuc_container_value, 'DEFINITION-REF')
            definition_ref.attrib['DEST'] = "ECUC-PARAM-CONF-CONTAINER-DEF"
            definition_ref.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu"
            parameter_values = etree.SubElement(ecuc_container_value, 'PARAMETER-VALUES')
            ecuc_numerical_param_value = etree.SubElement(parameter_values, 'ECUC-NUMERICAL-PARAM-VALUE')
            definition = etree.SubElement(ecuc_numerical_param_value, 'DEFINITION-REF')
            definition.attrib['DEST'] = "ECUC-INTEGER-PARAM-DEF"
            definition.text = "/AUTOSAR/EcuDefs/EcuC/EcucPduCollection/Pdu/PduLength"
            value = etree.SubElement(ecuc_numerical_param_value, 'VALUE').text = "1"


    # generate data
    pretty_xml = prettify_xml(rootEcuC)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/EcuC.epc', encoding='UTF-8', xml_declaration=True, method="xml")
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
