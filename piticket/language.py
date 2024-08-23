import os
import io
import os.path as osp
from piticket.utils import LOGGER 
from configparser import ConfigParser

PARSER = ConfigParser()
CURRENT = 'fr'

DEFAULT = {
        'en':{'choose':'Welcome, touch screen to continue', 
              'chosen':'Your journey details', 
              'recharge':'Please touch your card on the reader',
              'date':'Please select a date for your outward journey',
              'quick':'Quick ticket selection for popular destinations',
              'card':'Card payment only',
              'future':'Tickets for\nfuture\ntravel'},# English
        'fr':{'choose':'Bienvenue, écran tactile pour continuer', 
              'chosen':'Les détails de votre voyage', 
              'recharge':'Veuillez toucher votre carte sur le lecteur',
              'date':'Veuillez sélectionner une date pour votre voyage aller',
              'quick':'Sélection rapide de billets pour les destinations populaires',
              'card':'Paiement par carte uniquement',
              'future':'Billets pour\nde futurs\nvoyages'},# French
        'pn':{'choose':'Welcome, abeg touch screen to continue', 
              'chosen':'Your journey details', 
              'recharge':'Abeg touch your card for the reader',
              'date':'Abeg select the day wey you want travel',
              'quick':'Quickly select tickets for popular journey',
              'card':'Only card payment',
              'future':'Tickets for\nfuture\njourney'},# Pidgin English
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