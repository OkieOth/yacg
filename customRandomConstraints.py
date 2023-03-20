
def doPostProcessing(typeName, obj):
    if isinstance(obj, list):
        ret = []
        for e in obj:
            if (isinstance(e, dict) or isinstance(e, list)) and (len(e) == 0):
                continue
            ret.append(e)
        if len(ret) == 0:
            return False, None
        else:
            return True, ret
    else:
        if len(obj) == 0:
            return False, None
        else:
            return True, obj
