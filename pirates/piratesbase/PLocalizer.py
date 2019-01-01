import string
import types

from panda3d.core import *

try:
    language = ConfigVariableString('language', 'english').getValue()
    checkLanguage = ConfigVariableBool('check-language', True).getValue()
except:
    language = simbase.config.GetString('language', 'english')
    checkLanguage = simbase.config.GetBool('check-language', True)
else:
    def getLanguage():
        return language


    print 'PLocalizer: Running in language: %s' % language
    _languageModule = 'pirates.piratesbase.PLocalizer' + string.capitalize(language)
    _questStringModule = 'pirates.piratesbase.PQuestStrings' + string.capitalize(language)
    _greetingStringModule = 'pirates.piratesbase.PGreetingStrings' + string.capitalize(language)
    exec 'from ' + _languageModule + ' import *'
    exec 'from ' + _questStringModule + ' import *'
    exec 'from ' + _greetingStringModule + ' import *'
    if checkLanguage:
        l = {}
        g = {}
        englishModule = __import__('pirates.piratesbase.PLocalizerEnglish', g, l)
        foreignModule = __import__(_languageModule, g, l)
        for key, val in englishModule.__dict__.items():
            if not foreignModule.__dict__.has_key(key):
                print 'WARNING: Foreign module: %s missing key: %s' % (_languageModule, key)
                locals()[key] = val
            elif isinstance(val, types.DictType):
                fval = foreignModule.__dict__.get(key)
                for dkey, dval in val.items():
                    if not fval.has_key(dkey):
                        print 'WARNING: Foreign module: %s missing key: %s.%s' % (_languageModule, key, dkey)
                        fval[dkey] = dval

                for dkey in fval.keys():
                    if not val.has_key(dkey):
                        print 'WARNING: Foreign module: %s extra key: %s.%s' % (_languageModule, key, dkey)

        for key in foreignModule.__dict__.keys():
            if not englishModule.__dict__.has_key(key):
                print 'WARNING: Foreign module: %s extra key: %s' % (_languageModule, key)
