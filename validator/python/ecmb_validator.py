import re, os, yaml, io, zipfile
from typing import Callable
from lxml import etree
from PIL import ImageFile

class ecmbValidator():

    _schema_location = None
    _error_callback = None
    _is_valid = None

    _xml_image_width = None
    _xml_image_height = None

    _xml_navigation = None
    _xml_content = None
    _xml_files_list = None

    def __init__(self, error_callback: Callable = None):

        self.error_callback = error_callback
        self._load_config()
        

    def validate(self, file_name: str) -> bool:
        return self._validate(file_name, False)
    

    def validate_fast(self, file_name: str) -> bool:
        return self._validate(file_name, True)
    

    def _validate(self, file_name: str, fast: bool) -> bool:
        self._is_valid = True

        if not os.path.isfile(file_name):
            self._write_error('File not found!')
        else: 
            if re.search(r'\.xml$', file_name, re.IGNORECASE):
                with open(file_name, 'rb') as f:
                    xml_content = f.read()
                self._validate_xml(xml_content)
            elif re.search(r'\.ecmb$', file_name, re.IGNORECASE):
                self._validate_ecmb(file_name, fast)
            else:
                self._write_error('Unknown file-type!')
        
        return self._is_valid
        

    def _validate_ecmb(self, file_name: str, fast: bool) -> bool:
        if not zipfile.is_zipfile(file_name):
            self._write_error('Invalid eCMB-File!')
            return False

        try:
            ecmb_file = zipfile.ZipFile(file_name, 'r')
        except:
            self._write_error('Faild to open eCMB-File!')
            return False
        
        zip_file_list = ecmb_file.namelist()
        
        if not 'ecmb.xml' in zip_file_list:
            self._write_error('ecmb.xml is missing!')
            return False

        with ecmb_file.open('ecmb.xml', 'r') as f:
            xml_content = f.read()

        if not self._validate_xml(xml_content):
            return False
        
        for xml_file in self._xml_files_list:
            xml_file_name = xml_file[0][1:]
            double = 2 if xml_file[1] else 1

            if not xml_file_name in zip_file_list:
                self._write_error(f'"/{xml_file_name}" is missing!')
            elif not fast:
                image_size = self._get_image_size(ecmb_file, xml_file_name)
                if not image_size:
                    self._write_error(f'Faild to get image-size from "/{xml_file_name}"!')
                if image_size[0] != self._xml_image_width * double or image_size[1] != self._xml_image_height:
                    self._write_error(f'Image has "/{xml_file_name}" wrong size!')
        
        return True


    def _get_image_size(self, ecmb_file: zipfile.ZipFile, file_name: str) -> (int, int):
        with ecmb_file.open(file_name, "r") as f:
            parser = ImageFile.Parser()
            chunk = f.read(2048)
            count=2048
            while chunk != "":
                parser.feed(chunk)
                if parser.image:
                    return parser.image.size
                chunk = f.read(2048)
                count+=2048
            

    def _validate_xml(self, xml_content: str) -> bool:
        root = self._load_xml(xml_content)
        if root == None:
            return False
        
        self._xml_image_width = int(root.get('width'))
        self._xml_image_height = int(root.get('height'))
        
        self._xml_navigation = []
        self._xml_content = []
        self._xml_files_list = []
        
        content = root.find('content')
        self._read_xml_content(content, '/content')

        if content.get('cover_front'):
            self._xml_files_list.append(('/'+content.get('cover_front'), False))

        if content.get('cover_rear'):
            self._xml_files_list.append(('/'+content.get('cover_rear'), False))

        navigation = root.find('navigation')
        if navigation == None:
            return True
        
        self._read_xml_navigation(navigation)
        for ele in self._xml_navigation:
            if not re.search(r'^/content/[a-z0-9_-]', ele) or not ele in self._xml_content:
                self._write_error(f'Navigation-Target "{ele}" not found!')

        return True
        

    def _read_xml_navigation(self, main_node: etree.Element, path: str = '') -> None:
        for node in main_node:
            match node.tag:
                case 'headline':
                    self._read_xml_navigation(node, path)
                case 'item':
                    self._xml_navigation.append(path + node.get('href'))
                case 'chapter':
                    dir = node.get('dir')
                    self._xml_navigation.append(path + dir)
                    self._xml_navigation.append(path + dir + node.get('href'))
                    self._read_xml_navigation(node, path + dir)


    def _read_xml_content(self, main_node: etree.Element, path: str = '') -> None:
        for node in main_node:
            match node.tag:
                case 'img':
                    src = path + '/' + node.get('src')
                    self._xml_content.append(src)
                    self._xml_files_list.append((src, False))
                case 'dimg':
                    src = path + '/' + node.get('src')
                    self._xml_content.append(src)
                    self._xml_content.append(src + '#auto')
                    self._xml_content.append(src + '#left')
                    self._xml_content.append(src + '#right')
                    self._xml_files_list.append((src, True))
                    self._xml_files_list.append((path + '/' + node.get('src_left'), False))
                    self._xml_files_list.append((path + '/' + node.get('src_right'), False))
                case 'dir':
                    name = node.get('name')
                    self._xml_content.append(path + '/' + name)
                    self._read_xml_content(node, path + '/' + name)


    def _load_xml(self, xml_content: str) -> etree.Element:
        try:
            fp = io.BytesIO(xml_content)
            fp.seek(0)
            xml_doc = etree.parse(fp)
            root = xml_doc.getroot()
            ecmb_version = root.get('version')
        except:
            self._write_error('Invalid XML-File!')
            return

        if not ecmb_version or not re.match(r'^[1-9][0-9]*\.[0-9]+$', ecmb_version):
            self._write_error('Invalid eCMB version-number!')
            return

        xsd_path = self._schema_location + f'ecmb-v{ecmb_version}.xsd'

        if not os.path.exists(xsd_path):
            self._write_error(f'XSD with version "{ecmb_version}" not found!')
            return

        xmlschema_doc = etree.parse(xsd_path)
        xmlschema = etree.XMLSchema(xmlschema_doc)

        if not xmlschema.validate(xml_doc):
            self._write_error('eCMB-XML is invalid!')
            return
        
        return root
    

    def _load_config(self) -> None:
        try: 
            with open('ecmb_validator_config.yml', 'r') as file:
                config = yaml.safe_load(file)
            
            schema_location = config['schema_location']
            if not schema_location:
                raise Exception()
        except:
            raise Exception('Config not found or invalid!')
        
        if not os.path.isdir(schema_location):
            raise Exception('Schema-Location not found or not a directory!')
        
        if not re.search(r'[\/\\]$', schema_location):
            schema_location += '/'
        
        self._schema_location = schema_location
    
    
    def _write_error(self, msg: str) -> None:
        self._is_valid = False
        if self.error_callback and callable(self.error_callback):
            self.error_callback(msg)