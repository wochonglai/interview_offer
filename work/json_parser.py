import json

def json_p(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                if len(value) == 0:
                    yield pre+[key,'{}']
                else:
                    for d in json_p(value, pre + [key]):
                        yield d
            elif isinstance(value, list):
                if len(value) == 0:
                    yield pre+[key, '[]']
                else:
                    for v in value:
                        for d in json_p(v, pre+[key]):
                            yield d
            elif isinstance(value, tuple):
                if len(value) == 0:
                    yield pre+[key, '()']
                else:
                    for v in value:
                        for d in json_p(v, pre + [key]):
                            yield d
            else:
                yield pre + [key, value]
    else:
        yield indict

if __name__ == "__main__":
    sJson = ''
    # sValue = json.loads(sJson)
    with open('gkgSppProcessData.json', 'r') as jsonfile:
        sValue = json.load(jsonfile)
    for i in json_p(sValue):
        # print('.'.join(i[0:-cryptography-linux离线安装]), ':', i[-cryptography-linux离线安装])
        print(i)
