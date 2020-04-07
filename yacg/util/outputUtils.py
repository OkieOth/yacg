from colorama import init, Fore, Style

init()


def getErrorTxt(text='???'):
    return Fore.RED + Style.BRIGHT + text + Style.RESET_ALL


def getOkTxt(text='???'):
    return Fore.GREEN + text + Style.RESET_ALL


def getInfoTxt(text='???'):
    return Fore.YELLOW + text + Style.RESET_ALL


def printError(text='???'):
    print(getErrorTxt(text))


def printOk(text='???'):
    print(getOkTxt(text))


def printInfo(text='???'):
    print(getInfoTxt(text))
