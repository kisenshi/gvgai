__author__ = 'dperez'

import matplotlib
matplotlib.use("Agg")
import glob
import numpy as np
import pylab
from config import *


def calc_results(this_result_dirs):

    alg = 0

    for directory in this_result_dirs:

        victories = []
        scores = []
        times = []

        for game in range(NUM_GAMES):

            victories_game = []
            scores_game = []
            times_game = []

            # print directory + "/results_" + str(game) + "_*.txt"
            fileprefix = directory
            if directory[0] == 'T':
                fileprefix = 'results_24_20'
                if directory[1] == 'M':
                    fileprefix = 'results'

            dir = "results/" + directory + "/" + directory + "_" + str(GAME_NAMES[game]) + ".txt"
            files = glob.glob(dir)
            if len(files) == 0:
                print "Missing file: ", dir
                continue

            file = files[0]
            
            resultsGame = pylab.loadtxt(file, comments='*', delimiter=' ', usecols=range(5))
            # print "Reading", file

            numLines = min(REPS, resultsGame.shape[0])

            victoriesAll = resultsGame[:,0][0:numLines]
            scoresAll = resultsGame[:,1][0:numLines]

            # Use 2000-times as time in all games where the game was lost.
            timesAllRaw = resultsGame[:,2][0:numLines]
            timesAll = [ timesAllRaw[i] if victoriesAll[i] == 1.0 else (2000 - timesAllRaw[i]) for i in range(len(timesAllRaw))]

            all_victories_avg[game].append(np.average(victoriesAll))
            all_victories_stErr[game].append(np.std(victoriesAll) / np.sqrt(len(victoriesAll)))
            all_scores_avg[game].append(np.average(scoresAll))
            all_scores_stErr[game].append(np.std(scoresAll) / np.sqrt(len(scoresAll)))
            all_timesteps_avg[game].append(np.average(timesAll))
            all_timesteps_stErr[game].append(np.std(timesAll) / np.sqrt(len(timesAll)))

            victories_game.extend(victoriesAll)
            scores_game.extend(scoresAll)
            times_game.extend(timesAll)

            games_repetitions[game] = np.min([games_repetitions[game], len(victoriesAll)])

            victories.append(victories_game)
            scores.append(scores_game)
            times.append(times_game)

        overallVictories[alg].extend(victories)
        overallScores[alg].extend(scores)
        overallTimes[alg].extend(times)

        v = np.hstack(victories)
        all_victories[alg] = [v]

        # perc_vict = np.average(v)
        # stdErr_vict = np.std(v) / np.sqrt(len(v))
        # print ALG_NAMES[alg], "Perc. victories: %.2f (%.2f), n=%.2f " % (perc_vict*100, stdErr_vict*100, len(v))

        alg += 1



def calc_results_game(game_idx, this_result_dirs):



    NUM_GONFIGS = 6
    all_scores_avg = [[] for i in range(NUM_GONFIGS)]
    all_scores_stErr = [[] for i in range(NUM_GONFIGS)]

    all_victories_avg = [[] for i in range(NUM_GONFIGS)]
    all_victories_stErr = [[] for i in range(NUM_GONFIGS)]

    all_timesteps_avg = [[] for i in range(NUM_GONFIGS)]
    all_timesteps_stErr = [[] for i in range(NUM_GONFIGS)]

    games_repetitions = [REPS for i in range(NUM_GONFIGS)]
    config = 0


    for directory in this_result_dirs:

        victories = []
        scores = []
        times = []

        victories_game = []
        scores_game = []
        times_game = []
        alg = 0

        for dir in directory:

            # print dir + "/results_" + str(game_idx) + "_*.txt"

            files = glob.glob(dir + "/results_" + str(game_idx) + "_*.txt")
            if len(files) == 0:
                continue

            file = files[0]
            resultsGame = pylab.loadtxt(file, comments='*', delimiter=' ')
            # print "Reading", file

            numLines = min(REPS, resultsGame.shape[0])

            victoriesAll = resultsGame[:,0][0:numLines]
            scoresAll = resultsGame[:,1][0:numLines]

            # Use 2000-times as time in all games where the game was lost.
            timesAllRaw = resultsGame[:,2][0:numLines]
            timesAll = [ timesAllRaw[i] if victoriesAll[i] == 1.0 else (2000 - timesAllRaw[i]) for i in range(len(timesAllRaw))]

            all_victories_avg[alg].append(np.average(victoriesAll))
            all_victories_stErr[alg].append(np.std(victoriesAll) / np.sqrt(len(victoriesAll)))
            all_scores_avg[alg].append(np.average(scoresAll))
            all_scores_stErr[alg].append(np.std(scoresAll) / np.sqrt(len(scoresAll)))
            all_timesteps_avg[alg].append(np.average(timesAll))
            all_timesteps_stErr[alg].append(np.std(timesAll) / np.sqrt(len(timesAll)))

            # victories_game.extend(victoriesAll)
            # scores_game.extend(scoresAll)
            # times_game.extend(timesAll)

            games_repetitions[alg] = np.min([games_repetitions[alg], len(victoriesAll)])

            victories.append(victoriesAll)
            scores.append(scoresAll)
            times.append(timesAll)

            alg += 1



        overallVictories[config].extend(victories)
        overallScores[config].extend(scores)
        overallTimes[config].extend(times)

        v = np.hstack(victories)
        all_victories[config] = [v]

        config += 1


def compute_table_victories(data, data_stdErr, alg_names):

    dim1 = []
    dim2 = []

    data_idxs = dict()

    i = 0
    for alg in alg_names:
        dims = str.split(alg, '-')

        if not dim1.__contains__(dims[0]):
            dim1.append(dims[0])
        if not dim2.__contains__(dims[1]):
            dim2.append(dims[1])

        data_idxs[alg] = i
        i+=1


    table = [[0 for _ in range(len(dim2))] for _ in range(len(dim1))]
    table_std = [[0 for _ in range(len(dim2))] for _ in range(len(dim1))]


    for d1 in range(len(dim1)):
        for d2 in range(len(dim2)):
            alg_name = str(dim1[d1]) + '-' + str(dim2[d2])

            #print alg_name

            if data_idxs.has_key(alg_name):
                data_i = data_idxs[alg_name]
                table[d1][d2] = data[data_i]
                table_std[d1][d2] = data_stdErr[data_i]
            else:
                table[d1][d2] = '-'
                table_std[d1][d2] = '-'



    return dim1, dim2, table, table_std



def compute_table_victories_budget(data, data_stdErr, alg_names):

    dim1 = alg_names
    dim2 = ['24-20']

    data_idxs = dict()


    i = 0
    for alg in alg_names:
        data_idxs[alg] = i
        i+=1


    table = [[0 for _ in range(len(dim2))] for _ in range(len(dim1))]
    table_std = [[0 for _ in range(len(dim2))] for _ in range(len(dim1))]


    for d1 in range(len(alg_names)):
        alg_name = alg_names[d1]

        #print alg_name

        if data_idxs.has_key(alg_name):
            data_i = data_idxs[alg_name]
            table[d1][0] = data[data_i]
            table_std[d1][0] = data_stdErr[data_i]
        else:
            table[d1][0] = '-'
            table_std[d1][0] = '-'



    return dim1, dim2, table, table_std

