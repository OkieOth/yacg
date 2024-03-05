<%
    import yacg.model.modelFuncs as modelFuncs
    import yacg.model.model as model
    import yacg.util.stringUtils as stringUtils
    import yaml
%>
MODEL:
${ yaml.dump(modelTypes, default_flow_style=False) }