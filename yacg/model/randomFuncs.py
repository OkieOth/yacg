'''Functions needed by the createRandomData script'''
import yacg.model.random_config as randomConfig


def extendMetaModelWithRandomConfigTypes(loadedTypes):
    '''travers a list of loaded types and replaces all 'processing' attributes
    with types from the random config model
    '''
    for t in loadedTypes:
        if t._processing is not None:
            randomTypeConf = randomConfig.RandomDataTypeConf()
            randomTypeConf.initFromDict(t._processing)
            t._processing = randomTypeConf
        if not hasattr(t, "properties"):
            continue
        for p in t.properties:
            if p._processing is not None:
                randomPropConf = randomConfig.RandomDataPropertyConf()
                randomPropConf.initFromDict(p._processing)
                p._processing = randomPropConf
    pass
