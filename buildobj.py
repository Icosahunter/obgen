from xml.etree import ElementTree, Element
import random
import math
import sys
import string


if __name__ == "__main__":
    obj_builder_path = sys.argv[0]
    obj_def_path = sys.argv[1]

    obj_build = ElementTree.parse(obj_builder_path)
    obj_def = ElementTree.parse(obj_def_path)

    dest_path = './' + ''.join(random.choice(string.ascii_lowercase) for i in range(5)) + '.obg'
    if len(sys.argv) >= 3 :
        dest_path = sys.argv[2]

    obj_el = build_object(obj_build, obj_def)
    with open(dest_path, 'w') as f:
        f.write(ElementTree.dump(obj_el))

def build_object(obj_builder, obj_def):
    obj_def_root = obj_def.getroot()
    obj_build_root = obj_builder.getroot()
    obj_el = create_obj(obj_def_root)

    for attr_build in obj_build_root.findall('attr_build'):
        for attr_def in obj_def_root.findall(attr_build.find('target').text):
            attr_el = build_attribute(attr_build, attr_def)
            obj_el.append(attr_el)


def create_obj(obj):
    name = obj.find('name')
    description = obj.find('description')
    tags = obj.findall('tag')

    obj_el = Element('obj')
    obj_el.append(Element('name'))
    obj_el.find('name').text = name.text

    if description is not None:
        obj_el.append(Element('description'))
        obj_el.find('description').text = description.text

    for tag in tags:
        tag_el = Element('tag')
        tag_el.text = tag.text
        obj_el.append(tag_el)

    return obj_el


def build_attribute(attr_build, attr_def):
    attr = None

    if attr_build[0].tag == 'xpath':
        attr = attr_def.findall(attr_build[0].get('path'))
    elif attr_build[0].tag == 'linear':
        attr = attr_lin(attr_def, attr_build.attrib)
    elif attr_build[0].tag == 'exp':
        attr = attr_exp(attr_def, attr_build.attrib)
    elif attr_build[0].tag == 'manual':
        attr = attr_manual(attr_def, attr_build.attrib)
    elif attr_build[0].tag == 'auto':
        attr = attr_auto(attr_def, attr_build.attrib)

    return create_attr(attr.find('name').text, attr.find('description').text, attr[1], attr[0])


def create_attr(name, description, value, norm):
    attr_el = Element('attr')

    attr_el.append(Element('name'))
    attr_el.append(Element('description'))
    attr_el.append(Element('value'))
    attr_el.append(Element('norm'))

    attr_el.find('name').text = name
    attr_el.find('description').text = description
    attr_el.find('value').text = value
    attr_el.find('norm').text = norm


def attr_lin(attr_def, **kwargs):

    min, max, typ = get_min_max_typ(attr_def, **kwargs)

    nval = random.random()
    rval = (max - min) * nval + min
    return (nval, rval)


def attr_exp(attr_def, **kwargs):

    min, max, typ = get_min_max_typ(attr_def, **kwargs)

    nval = random.random()
    nval = math.pow(nval, math.log(typ, 0.5))
    rval = (max - min) * nval + min
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
            while rval is None or rval > double(max.text):
                rval = input(f'Enter a value for {atnm.text} less than {max.text}')
    elif max is None:
        while rval is None or rval < double(min.text):
            rval = input(f'Enter a value for {atnm.text} greater than {min.text} ')
    else:
        while rval is None or rval < double(min.text) or rval > double(max.text):
            rval = input(f'Enter a value for {atnm.text} between {min.text} and {max.text}')

    min = 0 if attr_def.find('min') is None else double(attr_def.find('min').text)
    max = 1 if attr_def.find('max') is None else double(attr_def.find('max').text)
    rval = double(rval)
    nval = (rval - min) / (max - min)

    return (nval, rval)


def attr_auto(attr_def, **kwargs):
    min = attr_def.find('min')
    max = attr_def.find('max')
    typ = attr_def.find('typical')
    dft = attr_def.find('default')

    if min is not None and max is not None:
        return attr_exp(attr_def)
    else:
        if typ is not None:
            return (0.5, {double(typ.text)})
        else:
            if dft is not None:
                return (0.5, {double(dft.text)})
            else:
                return (0, 0)

def get_min_max_typ(attr_def, **kwargs):

    max = None
    min = None
    typ = None

    if attr_def.find('min'):
        mn = double(attr_def.find('min').text)
        if 'min' in kwargs and double(kwargs['min']) > mn:
            min = double(kwargs['min'])
        else:
            min = mn
    else:
        if 'min' in kwargs:
            min = double(kwargs['min'])
        else:
            min = 0

    if attr_def.find('max'):
        mx = double(attr_def.find('max').text)
        if 'max' in kwargs and double(kwargs['max']) < mx:
            max = double(kwargs['max'])
        else:
            max = mx
    else:
        if 'max' in kwargs:
            max = double(kwargs['max'])
        else:
            max = 1


    if 'typ' in kwargs and double(kwargs['typ']) < max and double(kwargs['typ']) > min:
        typ = double(kwargs['typ'])
    else:
        if attr_def.find('typ'):
            typ = double(attr_def.find('typ').text)
        else:
            typ = (max - min)/2

    return (min, max, typ)
