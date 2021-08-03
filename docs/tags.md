# General
The models can use the 'x-tags' array to annotate types and properties.

Usually this tags are designed to customize the codeGen. Some tags also
influence the creation of the internal model. The internal used tags start
with a 'yacg' prefix. 

# List of internal used tags
## 'yacgFlattenType'
This tag removes "inheritence" from the type. If it is defined with an allOf
construct, then the properties of the super-class are copied to "inherited" class. The 'extendsType' property is removed.

This tag is processed in the end of the internal model build process.

## 'yacgIgnoreForModel'
If this tag is put to a type it is removed in a post model build step. With
that the type is not available in the templates.