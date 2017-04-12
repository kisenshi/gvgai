__author__ = 'dperez'

import matplotlib.pyplot as plt
import pylab
import numpy as np


def drawHistogram(all_data, result_dirs, title, xlab, ylab, outputFile, game_names, alg_names, showPlot=True, saveToFile=True):

    # print "Writing to ", outputFile

    #Create a figure
    fig = pylab.figure()
    fig.set_canvas(plt.gcf().canvas)

    #Add a subplot (Grid of plots 1x1, adding plot 1)
    ax = fig.add_subplot(111)

    width = 0.15
    colors = ['yellow','green','red','black','w','black']
    hatches = ['//',':','//','.','//',':']
    n_alg = len(result_dirs)
    ind = np.arange(len(all_data[0]))
    n_games = len(all_data[0])

    avg_plot = []
    err_plot = []
    StartingGamePlot = 0
    n_algorithms = len(result_dirs)

    for i in range(n_algorithms):
        avg_plot.append([0 for x in range(n_games)])
        err_plot.append([0 for x in range(n_games)])
        for j in range(n_games):
            #j = j + n_games/2
                avg_plot[i][j] = np.average(all_data[i][j])
                err_plot[i][j] = np.std(all_data[i][j]) / np.sqrt(len(all_data[i][j]))
            # if j < 17 :
            #     avg_plot[i][j - n_games/2] = np.average(all_data[i][j])
            #     err_plot[i][j - n_games/2] = np.std(all_data[i][j]) / np.sqrt(len(all_data[i][j]))
            # if j > 17 :
            #     avg_plot[i][j - n_games/2 -1] = np.average(all_data[i][j])
            #     err_plot[i][j - n_games/2 -1] = np.std(all_data[i][j]) / np.sqrt(len(all_data[i][j]))
                

    rects = [0 for x in range(n_alg)]
    for i in range(n_alg):
        rects[i] = ax.bar(ind+width*i , avg_plot[i], width,
                          color=colors[i], yerr=err_plot[i],
                          edgecolor='black', hatch=hatches[i], ecolor='black', label=alg_names[i])


    ax.set_xticks(ind+width*2)


    ax.yaxis.grid(True)
    ax.set_xlabel('xlabel')
    ax.set_ylabel('ylabel')

    maps_txt = []
    for j in range(n_games):
        #ss = 'Map ' + str(StartingMapPlot+j+1)
        #j = j + n_games
        #if j != 17 :
            ss = game_names[StartingGamePlot+j]
            maps_txt.append(ss)
            

    ax.set_xticklabels(maps_txt)

    #Titles and labels
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)

    #plt.xlim([8,22])
    #plt.ylim([0,200]) #175

    plt.legend(alg_names)
    plt.legend(bbox_to_anchor=(0.05, 0.8, 0.9, .102), loc=3,
               ncol=3, mode="expand", borderaxespad=0.)

    # plt.xlim([8,22])
    plt.ylim([0, 1.4])  # 175

    fig.set_size_inches(15,5)

    if saveToFile:
        fig.savefig(outputFile)

    # And show it:
    if showPlot:
        plt.show()


def drawPlot(all_data, result_dirs, title, xlab, ylab, outputFile, alg_configs, alg_names, showPlot=True, saveToFile=True):

    #Create a figure
    fig = pylab.figure()

    #Add a subplot (Grid of plots 1x1, adding plot 1)
    ax = fig.add_subplot(111)

    num_configs = len(all_data) #algorithms
    num_algs = len(all_data[0]) #games

##    alg_index = [0, 1, 2] #1-6
##    alg_index = [3, 4, 5] #2-8
##    alg_index = [6, 7, 8] #5-10
##    alg_index = [9, 10, 11] #7-12
##    alg_index = [12, 13, 14] #10-14
    alg_index = [0, 1, 2] #13-16
##    alg_index = [0, 3, 6, 9, 12, 15] #vanilla
##    alg_index = [1, 4, 7, 10, 13, 16] #OneStep
##    alg_index = [2, 5, 8, 11, 14, 17] #MCTS
##    alg_index = alg_configs #all algorithms

    # width = 0.15
    # colors = ['w','grey','w','black','w','black']
    # hatches = ['//',':',':','.','//',':']
    # n_alg = len(result_dirs)
    # ind = np.arange(len(all_data[0]))
    # n_games = len(all_data[0])
    #
    avg_plot = []
    err_plot = []
    line_styles=['-','--','-.',':','dotted','dashdot']

    # StartingGamePlot = 0
    # n_algorithms = len(result_dirs)


    for i in range(len(alg_index)):
         avg_plot.append([0 for x in range(num_algs)])
         err_plot.append([0 for x in range(num_algs)])
         for j in range(num_algs):
             avg_plot[i][j] = np.average(all_data[alg_index[i]][j])
             err_plot[i][j] = np.std(all_data[alg_index[i]][j]) / np.sqrt(len(all_data[alg_index[i]][j]))

##    for i in range(num_algs):
##        avg_plot.append([0 for x in range(num_configs)])
##        err_plot.append([0 for x in range(num_configs)])
##        for j in range(num_configs):
##            avg_plot[i][j] = np.average(all_data[j][i])
##            err_plot[i][j] = np.std(all_data[j][i]) / np.sqrt(len(all_data[j][i]))



    rects = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    for i in range(len(alg_index)):        
        ax.errorbar(rects, avg_plot[i], yerr=err_plot[i], label=alg_configs[alg_index[i]], linewidth=2)
                          # , color=colors[i], linestyle=line_styles[i],
                          # edgecolor='black', hatch=hatches[i], ecolor='black')


    # ax.set_xticks(ind+width*2)
    # ax.yaxis.grid(True)
    # ax.set_xlabel('xlabel')
    # ax.set_ylabel('ylabel')
    #
    # maps_txt = []
    # for j in range(n_games):
    #     #ss = 'Map ' + str(StartingMapPlot+j+1)
    #     ss = game_names[StartingGamePlot+j]
    #     maps_txt.append(ss)
    #
    plt.xticks(rects)
    ax.set_xticklabels(alg_names)

    #Titles and labels
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)

    plt.legend(alg_configs)
    plt.legend(bbox_to_anchor=(0.05, 0.8, 0.9, .102), loc=3,
           ncol=3, mode="expand", borderaxespad=0.)

    #plt.xlim([8,22])
    plt.ylim([0,1.4]) #175

    # fig.set_size_inches(15,5)

    if saveToFile:
        fig.savefig(outputFile)

    # And show it:
    if showPlot:
        plt.show()
