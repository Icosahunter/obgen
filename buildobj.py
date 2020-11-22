from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.dom import minidom
import random
import math
import sys
import string
import math


def build_object(obj_builder, obj_def):
    obj_def_root = obj_def.getroot()
    obj_build_root = obj_builder.getroot()
    obj_el = create_obj(obj_def_root)

    for attr_build in obj_build_root.findall('attr_build'):
        for attr_def in obj_def_root.findall(attr_build.find('target').text):
            attr_el = build_attribute(attr_build, attr_def)
            obj_el.append(attr_el)

    return obj_el


def create_obj(obj):
    name = obj.find('name')
    desc = obj.find('desc')
    tags = obj.findall('tag')

    obj_el = Element('obj')
    obj_el.append(Element('class'))
    obj_el.find('class').text = name.text

    if desc is not None:
        obj_el.append(Element('desc'))
        obj_el.find('desc').text = desc.text

    for tag in tags:
        tag_el = Element('tag')
        tag_el.text = tag.text
        obj_el.append(tag_el)

    return obj_el


def build_attribute(attr_build, attr_def):
    attr = None

    build = attr_build.find('build')[0]

    if build.tag == 'xpath':
        attr = attr_def.find(build[0].get('path'))
    elif build.tag == 'linear':
        attr = attr_lin(attr_def, **build.attrib)
    elif build.tag == 'exp':
        attr = attr_exp(attr_def, **build.attrib)
    elif build.tag == 'manual':
        attr = attr_manual(attr_def, **build.attrib)
    elif build.tag == 'auto':
        attr = attr_auto(attr_def, **build.attrib)

    tags = attr_def.findall('tag')
    return create_attr(attr_def.find('name').text, attr_def.find('desc').text, attr[1], attr[0], tags)


def create_attr(name, desc, value, norm, tags=None):
    attr_el = Element('attr')

    attr_el.append(Element('name'))
    attr_el.append(Element('desc'))
    attr_el.append(Element('value'))
    attr_el.append(Element('norm'))

    attr_el.find('name').text = name
    attr_el.find('desc').text = desc
    attr_el.find('value').text = f'{value}'
    attr_el.find('norm').text = f'{norm}'

    if tags is not None:
        for tag in tags:
            tag_el = Element('tag')
            tag_el.text = tag.text
            attr_el.append(tag_el)

    return attr_el


def attr_lin(attr_def, **kwargs):
    min, max, typ = get_min_max_typ(attr_def, **kwargs)

    nval = random.random()
    rval = (max - min) * nval + min

    if 'round' in kwargs:
        rval = round(rval, int(kwargs['round']))

    return (nval, rval)


def attr_exp(attr_def, **kwargs):
    min, max, typ = get_min_max_typ(attr_def, **kwargs)

    typ = (typ - min) / (max - min)
    nval = random.random()
    nval = math.pow(nval, math.log(typ, 0.5))
    rval = (max - min) * nval + min

    if 'round' in kwargs:
        rval = round(rval, int(kwargs['round']))

    return (nval, rval)


def attr_manual(attr_def, **kwargs):
    atnm = attr_def.find('name')
    min = attr_def.find('min')
    max = attr_def.find('max')
    rval = None

    if min is None:
        if max is None:
            rval = input(f'Enter a value for {atnm.text}:')
        else:
            while rval is None or rval > float(max.text):
                rval = input(f'Enter a value for {atnm.text} less than {max.text}')
    elif max is None:
        while rval is None or rval < float(min.text):
            rval = input(f'Enter a value for {atnm.text} greater than {min.text} ')
    else:
        while rval is None or rval < float(min.text) or rval > float(max.text):
            rval = input(f'Enter a value for {atnm.text} between {min.text} and {max.text}')

    min = 0 if attr_def.find('min') is None else float(attr_def.find('min').text)
    max = 1 if attr_def.find('max') is None else float(attr_def.find('max').text)
    rval = float(rval)
    nval = (rval - min) / (max - min)

    if 'round' in kwargs:
        rval = round(rval, int(kwargs['round']))

    return (nval, rval)


def attr_auto(attr_def, **kwargs):
    min = attr_def.find('min')
    max = attr_def.find('max')
    typ = attr_def.find('typical')
    dft = attr_def.find('default')
    nval = 0
    rval = 0

    if min is not None and max is not None:
        nval, rval = attr_exp(attr_def)
    else:
        nval = 0.5
        if typ is not None:
            rval = float(typ.text)
        else:
            if dft is not None:
                rval = float(dft.text)

    if 'round' in kwargs:
        rval = round(rval, int(kwargs['round']))

    return (nval, rval)


def get_min_max_typ(attr_def, **kwargs):
    max = None
    min = None
    typ = None

    if attr_def.find('min') is not None:
        mn = float(attr_def.find('min').text)
        if 'min' in kwargs and float(kwargs['min']) > mn:
            min = float(kwargs['min'])
        else:
            min = mn
    else:
        if 'min' in kwargs:
            min = float(kwargs['min'])
        else:
            min = 0

    if attr_def.find('max') is not None:
        mx = float(attr_def.find('max').text)
        if 'max' in kwargs and float(kwargs['max']) < mx:
            max = float(kwargs['max'])
        else:
            max = mx
    else:
        if 'max' in kwargs:
            max = float(kwargs['max'])
        else:
            max = 1

    if 'typ' in kwargs and float(kwargs['typ']) < max and float(kwargs['typ']) > min:
        typ = float(kwargs['typ'])
    else:
        if attr_def.find('typ') is not None:
            typ = float(attr_def.find('typ').text)
        else:
            typ = (max - min)/2 + min

    return (min, max, typ)


if __name__ == "__main__":
    obj_builder_path = sys.argv[1]
    obj_def_path = sys.argv[2]

    obj_build = ElementTree.parse(obj_builder_path)
    obj_def = ElementTree.parse(obj_def_path)

    dest_path = './' + ''.join(random.choice(string.ascii_lowercase) for i in range(5)) + '.obg'
    if len(sys.argv) >= 4:
        dest_path = sys.argv[3]

    obj_el = build_object(obj_build, obj_def)
    obj_str = ElementTree.tostring(obj_el)
    obj_str = minidom.parseString(obj_str).toprettyxml(indent="    ")
    with open(dest_path, 'w') as f:
        f.write(obj_str)
