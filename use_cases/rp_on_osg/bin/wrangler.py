#!/usr/bin/env python
"""This script does x.

Example:

Attributes:

Todo:

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import os
import glob
import sys
import pandas as pd
import radical.analytics as ra


def load_dfs(datadir, dfs, dfspaths):
    for df in dfspaths.keys():
        if os.path.exists(dfspaths[df]):
            try:
                dfs[df] = pd.read_csv(dfspaths[df])
            except:
                print "WARNING: File %s is empty or not valid." % dfspaths[df]
    return dfs


def load_data(datadir, sessions):
    old_df = sessions
    new_sids = {}
    new_sessions = {}
    new_experiments = {}
    start = datadir.rfind(os.sep)+1

    for path, dirs, files in os.walk(datadir):
        folders = path[start:].split(os.sep)
        if len(path[start:].split(os.sep)) == 2:

            # Get session ID from .json file name.
            sid = os.path.basename(glob.glob('%s/*.json' % path)[0])[:-5]

            # Skip sessions we have already loaded it into a DataFrame.
            if old_df is not None:
                print 'I got sessions'
                # print sessions.index.values
                # sys.exit(0)

                if sid in old_df['SID'].values:
                    print 'Skipping %s' % sid
                    continue
                else:
                    print "Loading %s" % sid

            # Add session and the experiment to which it belongs to the new
            # dict.
            if sid not in new_sessions.keys():
                new_sessions[sid] = {}
            new_sessions[sid] = ra.Session(sid, 'radical.pilot', src=path)
            new_experiments[sid] = folders[0]
            new_sids[sid] = sid

    if new_sessions:
        new_df = pd.DataFrame({'SID': new_sids,
                               'session': new_sessions,
                               'experiment': new_experiments})

        if old_df is not None:
            old_df.append(new_df)
        else:
            old_df = new_df

    return old_df.reset_index(drop=True)


def sessions_TTC():
    pass


def sessions_nunits():
    pass


if __name__ == '__main__':
    datadir = '../data/'

    dfs = {'sessions': None,
           'pilots': None,
           'units': None}

    dfspaths = {'sessions': '%s/sessions.csv' % datadir,
                'pilots': '%s/pilots.csv' % datadir,
                'units': '%s/units.csv' % datadir}

    old_dfs = load_dfs(datadir, dfs, dfspaths)

    print old_dfs
    sessions = load_data(datadir, old_dfs['sessions'])
    print sessions

    # Save session DataFrame to a csv file.
    sessions.to_csv(dfspaths['sessions'], index=False)

    # # Populate sessions DataFrame with derivative values
    # # Time To Completion (TTC)
    # for sid in sessions.index:
    #     sessions.ix[sid, 'TTC'] = sessions.ix[sid, 'session'].ttc
    #
    # # Save session DataFrame to a csv file.
    # sessions.to_csv(dfspaths['sessions'])
    #
    # # Number of units for each session (nunit)
    # for sid in sessions.index:
    #     nunit = sessions.ix[sid, 'session'].filter(etype='unit',
    #                                                inplace=False).get()
    #     sessions.ix[sid, 'nunit'] = len(nunit)
    #
    # # Save session DataFrame to a csv file.
    # sessions.to_csv(dfspaths['sessions'])

    # # Pilots
