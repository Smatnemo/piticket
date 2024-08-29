import os
import io
import os.path as osp

from configparser import ConfigParser
from piticket.utils import LOGGER, open_text_editor

PARSER = ConfigParser()
# Get the current language
CURRENT = 'en'

DEFAULT = {
        'en':{'choose':'Welcome, touch screen to continue', 
              'chosen':'Your journey details', 
              'recharge':'Please place your smartcard on the reader to recharge',
              'smartcard':'Recharge your smartcard',
              'date':'Please select a date for your outward journey',
              'quick':'Quick ticket selection for popular destinations',
              'card':'Card payment only',
              'future':'Tickets for\nfuture\ntravel',
              'translate':'Choose your preferred language',
              'back':'Back',
              'cancel':'Cancel',
              'calendar':'Choose or change your travel date',
              'destinations':'A-Z\nTravel\nDestinations',
              'collect':'Collect prepaid\ntickets',
              'pay':'Press to pay for your ticket',
              'card_payment':'Pleaase, tap or insert card to complete purchase'},# English
        'fr':{'choose':'Bienvenue, écran tactile pour continuer', 
              'chosen':'Les détails de votre voyage', 
              'recharge':'Veuillez placer votre carte à puce sur le lecteur pour la recharger',
              'smartcard':'Rechargez votre carte à puce',
              'date':'Veuillez sélectionner une date pour votre voyage aller',
              'quick':'Sélection rapide de billets pour les destinations populaires',
              'card':'Paiement par carte uniquement',
              'future':'Billets pour\nde futurs\nvoyages',
              'translate':'Choisissez votre langue préférée',
              'back':'Précédent',
              'cancel':'Annuler',
              'calendar':'Choisissez ou modifiez votre date de voyage',
              'destinations':'Destinations de\nvoyage de\nA à Z',
              'collect':'Collectez les\nbillets\nprépayés',
              'pay':'Appuyez sur pour payer votre billet',
              'card_payment':"Veuillez appuyer ou ins�rer la carte pour finaliser l'achat"},# French
        'pn':{'choose':'Welcome, abeg touch screen to continue', 
              'chosen':'Your journey details', 
              'recharge':'Abeg touch your card for the reader to recharge am',
              'smartcard':'Recharge your smartcard',
              'date':'Abeg select the day wey you want travel',
              'quick':'Quickly select tickets for popular journey',
              'card':'Only card payment',
              'future':'Tickets for\nfuture\njourney',
              'translate':'Choose language wey you like',
              'back':'Back',
              'cancel':'Cancel',
              'calendar':'Choose or change your travel date',
              'destinations':'A-Z\nTravel\nDestinations',
              'collect':'Collect\ntickets\nwey you\ndone pay for',
              'pay':'Press make you pay for your ticket',
              'card_payment':'Abeg, tap or insert card to complete purchase'},# Pidgin English
        # 'ig':{'choose':'', 
        #       'chosen':'', 
        #       'recharge':'',
        #       'date':'',
        #       'quick':''},# Igbo
        # 'ha':{'choose':'', 
        #       'chosen':'', 
        #       'recharge':'',
        #       'date':'',
        #       'quick':''},# Hausa
        # 'ya':{'choose':'', 
        #       'chosen':'', 
        #       'recharge':'',
        #       'date':'',
        #       'quick':''},# Yoruba
        # 'ib':{'choose':'', 
        #       'chosen':'', 
        #       'recharge':'',
        #       'date':'',
        #       'quick':''},# Ibibio
        # 'ij':{'choose':'', 
        #       'chosen':'', 
        #       'recharge':'',
        #       'date':'',
        #       'quick':''},# Ijaw
        # 'tv':{'choose':'', 
        #       'chosen':'', 
        #       'recharge':'',
        #       'date':'',
        #       'quick':''}# Tiv
}


def init(filename, clear=False):
    """Initialize the translation system.
    :param filename: file to write languages and translations in.
    :type filename: str
    :param clear: Restore default translations
    :type clear: bool
    """
    PARSER.filename = osp.abspath(osp.expanduser(filename))
    if not osp.isfile(PARSER.filename) or clear:
        LOGGER.info("Generating the translation file in '%s'", PARSER.filename)
        dirname = osp.dirname(PARSER.filename)
        if not osp.isdir(dirname):
            os.makedirs(dirname)
        
        with io.open(PARSER.filename, 'w', encoding='utf-8') as fp:
            for section, option in DEFAULT.items():
                fp.write('[{}]\n'.format(section))
                for name, value in option.items():
                    value = value.splitlines()
                    fp.write('{} = {}\n'.format(name,value[0]))
                    for part in value[1:]:
                        fp.write('     {}\n'.format(part))
                fp.write('\n\n')

    PARSER.read(PARSER.filename, encoding='utf-8')

    # Update file if translations have changed
    changed = False 
    for section, options in DEFAULT.items():
        if not PARSER.has_section(section):
            changed = True
            LOGGER.debug("Add [%s] to available language list", section)
            PARSER.add_section(section)
        
        for option, value in options.items():
            if not PARSER.has_option(section, option):
                changed = True 
                LOGGER.debug("Add [%s][%s] to available translations", section, option)
                PARSER.set(section, option, value)

    if changed:
        with io.open(PARSER.filename, 'w', encoding='utf-8') as fp:
            PARSER.write(fp)

def edit():
    if not getattr(PARSER, 'filename', None):
        raise EnvironmentError('Translation system is not initialized')
    open_text_editor(PARSER.filename)

def change_language(config, lang, desc=''):
    # Global keyword must be used here because assigning variable automatically makes it a local variable
    global CURRENT
    if lang in get_supported_languages():
        if CURRENT != lang:
            with io.open('/home/pi/.config/piticket/piticket.cfg', 'w', encoding='utf-8') as fp:
                config.set('GENERAL','language',lang)
                config.save()
            
            CURRENT = lang
            LOGGER.info("Changed language to '%s(%s)'",desc,lang)
    else:
        LOGGER.warning("Unsupported language '%s', fallback to '%s'", lang, CURRENT)

def get_current_lang():
    return CURRENT 

def get_supported_languages():
    """Return a list of the supported languages
    """
    if getattr(PARSER, 'filename', None):
        return list(sorted(lang for lang in PARSER.sections()))
    return list(sorted(DEFAULT.keys()))

def rearrange_supported_languages():
    languages = get_supported_languages()
    if len(languages) <= 1:
        return languages
    for lang in get_supported_languages():
        if lang == CURRENT:
            languages.pop(languages.index(lang))
            languages.insert(1,lang)
    return languages[:3]

def get_translated_text(key):
    """Return the text corresponding to the key in the language defined in the config.

    :param key: key in the translation file
    :type key: str
    """
    if not getattr(PARSER, 'filename', None):
        raise EnvironmentError("Translation system is not initialized")

    if PARSER.has_section(CURRENT) and PARSER.has_option(CURRENT, key):
        return PARSER.get(CURRENT, key).strip('"')
    elif PARSER.has_option('en', key):
        LOGGER.warning("Unsupported language '%s', fallback to English", CURRENT)
        return PARSER.get('en', key).strip('"')

    LOGGER.debug("No translation defined for '%s/%s' key", CURRENT, key)
    return None