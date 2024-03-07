license_text = '''
    Case studies for Theoretical Computer Science journal.
    Copyright (C) 2015-2016  Cristian Ioan Vasile <cvasile@bu.edu>
    Hybrid and Networked Systems (HyNeSs) Group, BU Robotics Lab,
    Boston University

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
'''
.. module:: examples_tcs.py
   :synopsis: Case studies for Theoretical Computer Science journal.

.. moduleauthor:: Cristian Ioan Vasile <cvasile@bu.edu>

'''

import logging, sys
# from io import StringIO

import networkx as nx
# import matplotlib.pyplot as plt

import twtl
from dfa import DFAType
from synthesis import expand_duration_ts, compute_control_policy, ts_times_fsa, \
    verify
# from learning import learn_deadlines
from lomap.ts import Ts


def Verification(formula, ts_file):
    _, dfa_inf, bdd = twtl.translate(formula, kind=DFAType.Infinity, norm=True)

    logging.info('The bound of formula "%s" is (%d, %d)!', formula, *bdd)
    logging.info('Translated formula "%s" to infinity DFA of size (%d, %d)!',
                 formula, *dfa_inf.size())

    ts = Ts(directed=True, multi=False)
    ts.read_from_file(ts_file)
    ts.g = nx.DiGraph(ts.g)
    ts.g.add_edges_from(ts.g.edges(), weight=1)

    for u, v in ts.g.edges():
        print(u, '->', v)
    result = verify(ts, dfa_inf)
    logging.info('The result of the verification procedure is %s!', result)


def setup_logging():
    fs, dfs = '%(asctime)s %(levelname)s %(message)s', '%m/%d/%Y %I:%M:%S %p'
    loglevel = logging.DEBUG
    logging.basicConfig(filename='../data/examples_tcs.log', level=loglevel,
                        format=fs, datefmt=dfs)

    root = logging.getLogger()
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(loglevel)
    ch.setFormatter(logging.Formatter(fs, dfs))
    root.addHandler(ch)


if __name__ == '__main__':
    setup_logging()
    print("Verification")
    phi_learn = '[H^1 A]^[0, 2] * [H^2 B]^[0, 3]'
    phi = '[H^2 A]^[0, 6] * ([H^1 B]^[0, 3] | [H^1 C]^[1, 4]) * [H^1 D]^[0, 6]'
    phi1 = '[H^1 A]^[1, 2]'
    phi2 = '[H^3 !B]^[1, 4]'
    Verification(phi1, '../data/ts_verification.txt')
    # case2_verification(phi1,'../data/new.txt')
