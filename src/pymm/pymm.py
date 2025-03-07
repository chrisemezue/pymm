#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import collections
from .cmdexecutor import MetamapCommand
from .mmoparser import parse
from os.path import exists
import tempfile
from os import remove
from subprocess import TimeoutExpired
from xml.parsers.expat import ExpatError

__author__ = "Srikanth Mujjiga"
__copyright__ = "Srikanth Mujjiga"
__license__ = "mit"

class MetamapStuck(Exception):
    """ MetaMap Stuck Exception """
    pass

class Metamap:
    """ MetaMap Concept Extractor """

    def __init__(self, metamap_path,output_file,input_file,use_only_snomed,debug=False):
        """ MetaMap Wrapper parameters

        Args:
            metamap_path (str): Path to metamap
            debug (boolean): Debug On/Off
        """
        self.metamap_path = metamap_path
        self.debug = debug
        self.output_file = output_file
        self.input_file = input_file
        self.input_file_, self.output_file_ = self._get_temp_files()
        self.use_only_snomed=use_only_snomed
        
        self.metamap_command = MetamapCommand(self.metamap_path,
                self.input_file, self.output_file,self.use_only_snomed, self.debug)

    def is_alive(self):
        """Check if MetaMap is running

        Returns:
            True if MetaMap is running, False otherwise
        """
        try:
            mmos = self.parse(["heart attack"])
            concepts = [concept for _, mmo in enumerate(mmos) for _, concept in enumerate(mmo)]
            return True if len(concepts) > 1 else False
        except ExpatError:
            return False

    def _get_temp_files(self):
        TEMP_DIR = None

        if exists('/dev/shm'):
            print ("Exists")
            TEMP_DIR = '/dev/shm'
        
        with tempfile.NamedTemporaryFile(delete=False, dir=TEMP_DIR) as fp:
            input_file = fp.name

        with tempfile.NamedTemporaryFile(delete=False, dir=TEMP_DIR) as fp:
            output_file = fp.name

        if self.debug:
            print (f"Input File: {input_file}, Output File: {self.output_file}")

        return input_file, output_file


    def parse(self, inp_file, timeout=10):
        """Returns the UMLS concetps

        Args:
            sentences (:obj:`list` of :obj:`str`): Input sentences for which concepts are to be extracted
            timeout (int): Timeout interval for MetaMap

        Returns:
            Iterator over MetaMap Objects
        """
        '''
        with open(self.input_file, mode="wb") as fp:
            for idx, sentence in enumerate(sentences):
                fp.write("{0}\n".format(sentence).encode('utf8'))
        '''
        self.input_file = inp_file
        #try:
        self.metamap_command.execute(inp_file,timeout=timeout)
        #return parse(self.output_file)
        return 'All Done'
        #except TimeoutExpired:
        #    print ("Execution of command Timedout; try increasing the timeout")
        #    raise MetamapStuck()


    def close(self):
        """Close the input and output file
        """
        if not self.debug:
            remove(self.input_file)
            remove(self.output_file)
