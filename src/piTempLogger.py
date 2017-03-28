#!/usr/bin/env python
###############################################################################################
#  Author: 
__author__ = '<a href="mailto:debuti@gmail.com">Borja Garcia</a>'
# Program: 
__program__ = 'tempLogger'
# Package:
__package__ = ''
# Descrip: 
__description__ = '''RPi temperature logger to dweet.io service'''
# Version: 
__version__ = '0.0.1'
#    Date:
__date__ = '20170328'
# License: This script doesn't require any license since it's not intended to be redistributed.
#          In such case, unless stated otherwise, the purpose of the author is to follow GPLv3.
# History: 
#          0.0.0 (YYYYMMDD)
#            -Initial release
###############################################################################################

# Imports
import logging
import sys
import doctest
import datetime, time
import os
import optparse
import inspect
import ConfigParser
import glob
import traceback

# Parameters, Globals n' Constants
KIBI = 1024
MEBI = 1024 * KIBI
LOG_MODE = "Screen"
LOG_LEVEL = logging.DEBUG
LOG_MAX_BYTES = 1 * MEBI

realScriptPath = os.path.realpath(__file__)
realScriptDirectory = os.path.dirname(realScriptPath)
callingDirectory = os.getcwd()
if os.path.isabs(__file__ ):
    linkScriptPath = __file__
else:
    linkScriptPath = os.path.join(callingDirectory, __file__)
linkScriptDirectory = os.path.dirname(linkScriptPath)

propertiesName = __program__ + ".properties"
propertiesPath = os.path.join(realScriptDirectory, '..', propertiesName) 

logFileName = __program__ + '_' + time.strftime("%Y%m%d%H%M%S") + '.log'
logDirectory = os.path.join(realScriptDirectory, '..', 'logs')
logPath = os.path.join(logDirectory, logFileName)
loggerName = __package__ + "." + __program__

# User-libs imports (This is the correct way to do this)
libPath =  os.path.join(realScriptDirectory, '..', 'lib')
sys.path.insert(0, libPath)
for infile in glob.glob(os.path.join(libPath, '*.*')):
    sys.path.insert(0, infile)
    
#import thepyutilities.shellutils as shellutils



# Error declaration
error = { "" : "",
          "" : "",
          "" : "" }

# Usage function, logs, utils and check input
def openLog(mode, desiredLevel):
    '''This function is for initialize the logging job
    '''
    def openScreenLog(formatter, desiredLevel):
        logging.basicConfig(level = desiredLevel, format = formatter)
       
    def openScreenAndFileLog(fileName, formatter, desiredLevel):
        logger = logging.getLogger('')
        logger.setLevel(desiredLevel)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(fileName)
        fh.setLevel(desiredLevel)
        fh.setFormatter(formatter)
        # add the handler to logger
        logger.addHandler(fh)

    def openScreenAndRotatingFileLog(fileName, formatter, desiredLevel, maxBytes):
        logger = logging.getLogger('')
        logger.setLevel(desiredLevel)
        # create file handler which logs even debug messages
        fh = logging.handlers.RotatingFileHandler(fileName, maxBytes)
        fh.setLevel(desiredLevel)
        fh.setFormatter(formatter)
        # add the handler to logger
        logger.addHandler(fh)

    format = "%(asctime)-15s - %(levelname)-6s - %(funcName)10.10s - %(message)s"
    formatter = logging.Formatter(format)
    # Clean up root logger
    for handler in logging.getLogger('').handlers:
        logging.getLogger('').removeHandler(handler)
    openScreenLog(format, desiredLevel)
    
    if mode == "File" or mode == "RollingFile":
        if not os.path.isdir(logDirectory):
            shellutils.mkdir(logDirectory)
  
        if mode == "File":
            openScreenAndFileLog(logPath, formatter, desiredLevel)
    
        elif mode == "RollingFile":
            openScreenAndRotatingFileLog(logPath, formatter, desiredLevel, LOG_MAX_BYTES)

def closeLog():
    '''This function is for shutdown the logging job
    '''
    logging.shutdown()

def checkInput():
    '''This function is for treat the user command line parameters.
    '''

    #####THIS SECTION IS A EXAMPLE#####
    # Create instance of OptionParser Module, included in Standard Library
    p = optparse.OptionParser(description=__description__,
                              prog=__program__,
                              version=__version__,
                              usage='''%prog [options]''') 
    # Define the options. Do not use -h nor -v, the are reserved to help and version automaticly
    p.add_option('--old', '-o', action="store", type="string", dest="old_regexp", help='Regular expression to search for')
    p.add_option('--new', '-n', action="store", type="string", dest="new_string", help='New text to replace it')
    p.add_option('--preview','-p', action="store_true", dest="do_preview", help='Ask to replace the coincidence before doing it')
    p.add_option('--file','-f', action="store", type="string", dest="filename", help='The input/output file')

    # Parse the commandline
    options, arguments = p.parse_args()

    # Decide what to do
    if options.old_regexp is None or options.new_string is None or options.filename is None :
        p.print_help()
        sys.exit(-1)
    else:
        old_regexp = options.old_regexp
        new_string = options.new_string
        do_preview = options.do_preview
        filename = options.filename
        return [old_regexp, new_string, do_preview, filename]

    #####/THIS SECTION IS A EXAMPLE#####


# Helper functions
def areToolsInstalled():
    '''
    '''
    #####THIS SECTION IS A EXAMPLE#####
    result = True
    softwareNeeded = [{'sw':"ecdhoprint-codegen", 
                       'message':"""Tool needed not found. Install it by typing: 
 sudo apt-get install ffmpeg libboost-all-dev libtag1-dev zlib1g-dev git eyed3
 git clone -b release-4.12 git://github.com/echonest/echoprint-codegen.git
 cd echoprint-codegen/
 cd src/
 make
 cd ..
 cd ..
 mv echoprint-codegen /usr/local/.
 ln -s /usr/local/echoprint-codegen/echoprint-codegen /usr/bin/echoprint-codegen"""},
                      {'sw':"eyes3", 'message':"""Tool needed not found. Install it by typing: 
 sudo apt-get install eyed3"""},
]
    for software in softwareNeeded:
        if not shellutils.executableExists(software['sw']):
            print software['message']
            result = False
            
    return result
    #####/THIS SECTION IS A EXAMPLE#####

def createWorkDir():
    '''This function is for creating the working directory, if its not already
    '''
    #####THIS SECTION IS A EXAMPLE#####
    if not os.path.isdir(APP_PATH):
        os.mkdir(APP_PATH)
    if not os.path.isdir(LOG_PATH):
        os.mkdir(LOG_PATH)
    if not os.path.isfile(LOG_FILENAME):
        f = open(LOG_FILENAME, "w")
        f.close()
    #####/THIS SECTION IS A EXAMPLE#####

def readConfig(propertiesPath):
    '''This procedure returns the program properties file
    '''
    config = ConfigParser.RawConfigParser()
    config.read(propertiesPath)
    return config
    
def saveConfig(config, propertiesPath):
    '''This procedure returns the program properties file
    '''
    configfile = open(propertiesPath, 'wb')
    config.write(configfile)
    configfile.close()

# Main function
def core():
    '''This is the core, all program logic is performed here
    '''
    createWorkDir()
    properties = readConfig(propertiesPath)

#####THIS SECTION IS A EXAMPLE#####
    properties.get('General', 'foo')
    properties.set('General', 'foo', "hola")
#####/THIS SECTION IS A EXAMPLE#####

    # DO STUFF HERE
    
    saveConfig(properties, propertiesPath)
    
def main():
    '''This is the main procedure, is detached to provide compatibility with the updater
    '''
    openLog(LOG_MODE, LOG_LEVEL)
    checkInput()
    core()
    closeLog()

# Entry point
if __name__ == '__main__':
    try:
        if areToolsInstalled():
            main()
    
    except KeyboardInterrupt:
        print "Shutdown requested. Exiting"
    except SystemExit:
        pass
    except:
        logging.error("Unexpected error:" + traceback.format_exc())
        raise
