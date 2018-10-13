# **************************************************************************
# *
# * Authors:     Grigory Sharov (gsharov@mrc-lmb.cam.ac.uk)
# *
# * MRC Laboratory of Molecular Biology (MRC-LMB)
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import os
import pyworkflow.em
from pyworkflow.utils import Environ, join

_logo = "nysbc_logo.png"
_references = ['tan2017']

NYSBC_3DFSC_HOME = 'NYSBC_3DFSC_HOME'


class Plugin(pyworkflow.em.Plugin):
    _homeVar = NYSBC_3DFSC_HOME
    _pathVars = [NYSBC_3DFSC_HOME]
    _supportedVersions = ['2.5', '3.0']

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar(NYSBC_3DFSC_HOME, 'nysbc-3DFSC-2.5')

    @classmethod
    def getEnviron(cls):
        """ Setup the environment variables needed to launch 3DFSC. """
        environ = Environ(os.environ)
        environ.update({'PATH': cls.getHome('ThreeDFSC')},
                       position=Environ.BEGIN)

        # FIXME: program does not start due to virtualenv issues..
        #if 'PYTHONPATH' in environ:
        #    # this is required for python virtual env to work
        #    environ.set('PYTHONPATH', '', position=Environ.BEGIN)
        return environ

    @classmethod
    def getProgram(cls):
        """ Return the program binary that will be used. """
        if NYSBC_3DFSC_HOME not in os.environ:
            return None
        cmd = cls.getHome('ThreeDFSC', 'ThreeDFSC_Start.py')
        return str(cmd)

    @classmethod
    def defineBinaries(cls, env):
        fsc_commands = [('conda env create -f environment.yml && touch IS_INSTALLED',
                         'IS_INSTALLED')]

        env.addPackage('nysbc-3DFSC', version='2.5',
                       tar='nysbc-3DFSC_2.5.tgz',
                       commands=fsc_commands,
                       neededProgs=['conda'],
                       default=True)

        env.addPackage('nysbc-3DFSC', version='3.0',
                       tar='nysbc-3DFSC_3.0.tgz',
                       commands=fsc_commands,
                       neededProgs=['conda'])


pyworkflow.em.Domain.registerPlugin(__name__)