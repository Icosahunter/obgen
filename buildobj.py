from xml.etree import ElementTree

def build_object(obj_builder, obj_def):
    obj_def_root = obj_def.getroot()
    obj_build_root = obj_builder.getroot()
    for attr in obj_def_root.findall('attr_def'):
        if attr.get('name') in 
