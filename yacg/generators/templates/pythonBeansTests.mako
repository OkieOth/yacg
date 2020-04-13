<%
    import yacg.model.model as model
    import yacg.templateHelper as templateHelper
    import yacg.model.modelFuncs as modelFuncs
    import yacg.util.stringUtils as stringUtils

    templateFile = 'pythonBeans.mako'
    templateVersion = '1.0.0'

    modelPackage = templateParameters.get('modelPackage','<<"modelPackage" template param is missing>>')
    testClassName = templateParameters.get('title','Model')
    testClassName = stringUtils.toUpperCamelCase(testClassName) 

%># Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: ${templateFile} v${templateVersion})

import unittest

% for type in modelTypes:
from ${modelPackage} import ${type.name}
% endfor


class Test${testClassName} (unittest.TestCase):
% for type in modelTypes:
    def test${type.name}(self):
    % if not modelFuncs.isEnumType(type):
        x = ${type.name}()
        self.assertIsNotNone(x)
    % else:
        % for value in type.values:
        self.assertIsNotNone(${type.name}.${value.upper()})
        % endfor
    % endif

% endfor

if __name__ == '__main__':
    unittest.main()
