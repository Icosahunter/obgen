# Obgen

---

## Overview
Obgen is a command line tool for generating xml objects.
It is particularly geared towards content generation for games.
The Obgen toolchain is broken into 3 parts:
  - Objects
  - Object Definitions
  - Builders
  
### Objects
Objects are what Obgen generates. They are xml objects with a form resembling
objects in program. Objects have a name, description, tags, and attributes.

### Object Definitions
Object definitions define an type of object. An object definition stores things
like the minimum and maximum values for an attribute and tags that are added to
all objects of this type.

### Builders
Builders define how to generate an object. It specifies how to generate values
for all the attributes of an object.

---

## Syntax
Below are some example xml documents for each part of the system, as well as
some references for tags.

### Object
```xml
<obj>
  <name>hibiscus</name>
  <class>flower</class>
  <desc>a beautiful red hibiscus flower</desc>
  <tag>plant</tag>
  <attr>
    <name>hue</name>
    <desc>the color of the flower</desc>
    <value>345</value>
    <norm>0.95833333333</value>
  </attr>
</obj>
```

### Object Definition
```xml
<obj_def>
  <name>flower</name>
  <desc>a colorful plant</desc>
  <tag>plant</tag>
  <attr_def>
    <name>hue</name>
    <desc>the color of the flower</desc>
    <min>0</min>
    <max>360</max>
  </attr_def>
</obj_def>
```

### Builder
```xml
<obj_build>
  <name>red flower builder</name>
  <desc>a builder for generating red flowers</desc>
  <target>flower</target>
  <attr_build>
    <name>hue builder</name>
    <desc>generates red hues</desc>
    <target>hue</target>
    <random min="335"/>
  </attr_build>
</obj_build>
```

### Tag Reference
`<obj>`
The tag for an object.

`<attr>`:
The tag for an attribute.

`<obj_def>`
 The tag for an object definition.
 
`<attr_def>`
 The tag for an attribute definition.
 
`<obj_build>`
 The tag for an object builder.
 
`<attr_build>`
 The tag for an attribute builder.
 
`<name>`
 The name of the parent element. This could be an object, object definition,
 attribute, attribute definition, builder, or attribute builder.
 
`<desc>`
 A description of the parent element. This could be an object, object
 definition, attribute, attribute definition, builder, or attribute builder.
 
`<tag>`
 A tag to help locate an element. These can be present in objects, object
 definitions, attributes, attribute definitions, builders, or attribute
 builders. They are particularly helpful to include in object definitions
 and attribute definitions however because builders can use them in targeting.
 
`<class>`
 The type of an object. This will be the name of the object definition used
 to generate the object.
 
`<target>`
 Used to select an object or an attribute from within an object to apply a
 builder to. The value of target should be a valid xpath.
 
`<min>`
 The minimum value for an attribute. Used only in attribute definitions.
 
`<max>`
 The maximum value for an attribute. Used only in attribute definitions.
 
`<typ>`
 The typical/average value for an attribute. Used only in attribute
 definitions.
 
`<default>`
 The default value for an attribute. Used only in attribute definitions.
 
`<valence>`
 A value of "positive" indicates it is "good" for the attribute to be
 larger, while a value of "negative" indicates it is "good" for the attribute
 to be smaller. Used only in attribute definitions.
 
`<build>`
 The value of this defines the type of builder to use for an attribute builder.
 The value must be a valid builder tag.
 
`<auto>`
 The automatic builder tag. This chooses a random value if enough information
 is supplied by the attribute definition, otherwise it chooses the typical or
 default value if supplied by the definition, and finally it defaults to 0 if
 nothing is provided.
 
`<lin>`
 The linear random builder tag. Selects a random value between min and max.
 
`<exp>`
 The exponential random builder tag. Selects a random value between min and
 max using an exponential that passes through typ at the halfway point, such
 that the average will be typ.
 
`<manual>`
 The manual builder tag. Prompts the user to enter a value between min and max.
 
`<xpath>`
 The xpath builder tag. Takes a valid xpath as an argument and sets the
 attribute the value of that path. The xpath must be provided as the value
 of the 'path' xml attribute like so:
 `<xpath path="/node1/node2"`
 The root of the path is the definition of the attribute being generated. In
 other words the root will be a <attr_def> tag.

For any of the build tags you can set a min, max, typ, or default in the tag
using xml attributes like so:
`<auto min="0" max="30" typ="20" default="0"/>`
These values will only work if they are within any existing bounds provided
by the attribute definition.
Another option is round, the value of this is how many decimal places to
round the result to.

---

## Runing Obgen
Currently to generate an object you will need to execute the file 'buildobj'
with several arguments as follows:
```python buildobj.py <builder path> <object definition path> [<destination path>]
```
Where [] indicate an optional parameter.

---

## Give it a Whirl!
The test.bat file contains the command to generate an object using the included
test files.
