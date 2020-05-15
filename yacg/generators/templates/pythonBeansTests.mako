<%
    import yacg.model.modelFuncs as modelFuncs
    import yacg.util.stringUtils as stringUtils
    import yacg.generators.helper.pythonFuncs as pythonFuncs

    templateFile = 'pythonBeans.mako'
    templateVersion = '1.0.0'

    baseModelDomain = templateParameters.get('baseModelDomain',None)
    domainList = modelFuncs.getDomainsAsList(modelTypes)

    testClassName = templateParameters.get('title','Model')
    testClassName = stringUtils.toUpperCamelCase(testClassName) 

%># Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: ${templateFile} v${templateVersion})

import unittest

% for domain in domainList:
import ${domain}
% endfor


class Test${testClassName} (unittest.TestCase):
% for type in modelTypes:
    def test${type.name}(self):
    % if not modelFuncs.isEnumType(type):
        x = ${pythonFuncs.getTypeWithPackageEnforced(type, 'dummy')}()
        self.assertIsNotNone(x)
    % else:
        % for value in type.values:
        self.assertIsNotNone(${pythonFuncs.getTypeWithPackageEnforced(type, 'dummy')}.${stringUtils.toUpperCaseName(value)})
        % endfor
    % endif

% endfor

if __name__ == '__main__':
    unittest.main()
