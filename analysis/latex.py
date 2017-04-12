__author__ = 'dperez'

import numpy as np
from valfunction_config import *

def boldify(i):
    return '\\textbf{' + str(i) + '}'

def multicolumn(num_columns, data):
    return '\\multicolumn{' + str(num_columns) + '}'+'{|c|}{' + str(data) + '}'

def print_latex_table_results(data, num_games, num_alg, sig_p_value):

    print '\\begin{table*}[!t]'
    print '\\begin{center}'
    # print '\\begin{tabular}{|>{\\centering\\arraybackslash} m{1.5cm}|c|c|>{\\centering\\arraybackslash} m{1.7cm}|c|>{\\centering\\arraybackslash} m{1.7cm}|c|>{\\centering\\arraybackslash} m{1.7cm}|}'
    print '\\begin{tabular}{|>{\\centering\\arraybackslash} m{1.5cm}|c|c|>{\\centering\\arraybackslash} m{1.7cm}|c|>{\centering\\arraybackslash} m{1.7cm}}'
    print '\hline'
    # print '\\textbf{Game (Repetitions)}  & \\textbf{Algorithm} & \\textbf{Victories (\%)} &  \\textbf{Significantly better than ...} & \\textbf{Scores} &  \\textbf{Significantly better than ...} & \\textbf{Timesteps} &  \\textbf{Significantly better than ...} \\\\'
    print '\\textbf{Game}  & \\textbf{Algorithm} & \\textbf{Victories (\%)} &  \\textbf{Significantly better than ...} & \\textbf{Scores} &  \\textbf{Significantly better than ...}  \\\\'

    for gameidx in range(num_games):


        print '\hline'

        if num_alg > 1:
            #print '\multirow{3}{*}{\\textbf{' + GAME_NAMES[gameidx] + '}}'
            print '\multirow{' + str(num_alg - 1) + '}{*}{' + boldify(data[gameidx*num_alg][0]) + '}'
        else:
            print boldify(data[gameidx*num_alg][0]),


        for algidx in range(num_alg):

            lineidx =  gameidx*num_alg + algidx



            for i in range(len(data[lineidx])):
                strLine = data[lineidx][i]
                if i > 0:
                    if isinstance(strLine, basestring):
                        strLine = strLine.replace('_','\_');

                        if (i == 1):
                            if len(data[lineidx][3]) == (num_alg-1) or len(data[lineidx][5]) == (num_alg-1):

                                print '& ' + boldify(strLine),
                            else:
                                print '& ' + strLine,
                        else:
                            print '& ' + strLine,

                    else:
                        print '& ',
                        if len(strLine) == 0:
                            print '$\O$',
                        else:
                            for j in range(len(strLine)):
                                item = strLine[j]
                                if j < len(strLine)-1:
                                    print item + ',',
                                else:
                                    print item,



            print ' \\\\'



    print '\hline'
    print '\end{tabular}'
    print '\caption{Percentage of victories and average of score achieved (plus standard error) in $%d$ different games. ' \
          'Fourth, sixth and eighth columns indicate the approaches that are significantly worse than that of the row, using the ' \
          'non-parametric Wilcoxon signed-rank test with p-value $<%.2f$.  Bold font for the ' \
          'algorithm that is significantly better than all the other $%d$ in either victories or score.}' % (num_games, sig_p_value, num_alg-1)
    print '\label{tab:weights}'
    print '\end{center}'
    print '\end{table*}'
    print ''



def latex_table_all_rankings(prettySumTable, num_games):


    # num_columns = num_games + 4  #rank, algorithm, points, avg_vict.
    # str_columns = '\\begin{tabular}{|'
    # for _ in range(num_columns):
    #     str_columns = str_columns + 'c|'
    # str_columns = str_columns + '}'


    str_columns = '\\begin{tabular}{|>{\\centering\\arraybackslash} m{0.25cm}|>{\\centering\\arraybackslash} m{1.35cm}|>{\\centering\\arraybackslash} m{0.65cm}|>{\\centering\\arraybackslash} m{1.25cm}|>{\\centering\\arraybackslash} m{0.455cm}|>{\\centering\\arraybackslash} m{0.455cm}|>{\\centering\\arraybackslash} m{0.455cm}|>{\\centering\\arraybackslash} m{0.455cm}|}'

    str_col_headers = '\\textbf{$\#$}  & \\textbf{Algorithm} & \\textbf{Points} &  \\textbf{Avg. Wins} '
    for i in range(num_games):
            str_col_headers = str_col_headers + ' & ' + boldify('G-' + str(i))
    str_col_headers = str_col_headers + ' \\\\'

    print '\\begin{table}[!t]'
    print '\\begin{center}'
    print str_columns
    print '\hline'
    print str_col_headers

    for entry in prettySumTable:

        print '\hline'

        for i in range(len(entry)):

            datapiece = str(entry[i])
            if datapiece == '25' or i <= 1:
                datapiece = boldify(datapiece)

            if i < len(entry) - 1:
                print datapiece + ' & ',
            else:
                print datapiece,

        print ' \\\\'

    print '\hline'
    print '\end{tabular}'
    print '\caption{Rankings table for the compared algorithms across all games. In this order, the table shows the ' \
          'rank of the algorithms, their name, total points, average of victories and points achieved on each game, ' \
          'following the F1 Scoring system.}'
    print '\label{tab:weights}'
    print '\end{center}'
    print '\end{table}'


def latex_table_games_rankings(prettyGameTable, list_games, game_names):
    for game_idx in list_games:
        latex_table_game_rankings(prettyGameTable[game_idx], game_names[game_idx])


def latex_table_game_rankings(prettyGameTable, game_name):

    print '\\begin{table*}[!t]'
    print '\\begin{center}'
    print '\\begin{tabular}{|c|c|c|c|c|c|}'
    print '\hline'
    print boldify(game_name) + ' & \\textbf{Algorithm} & \\textbf{Points} &  \\textbf{Winner \\%} & \\textbf{Avg. Score} & \\textbf{Avg. Timesteps} \\\\'

    for entry in prettyGameTable:

        print '\hline'

        for i in range(len(entry)):

            datapiece = str(entry[i])
            if datapiece == '25' or i <= 1:
                datapiece = boldify(datapiece)

            if i < len(entry) - 1:
                print datapiece + ' & ',
            else:
                print datapiece,

        print ' \\\\'

    print '\hline'
    print '\end{tabular}'
    print '\caption{Results for the game ' + game_name + ', showing rank, algorithm, points achieved, percentage of victories across all levels ' \
                                                       'and score and timesteps averages (standard error between parenthesis).}'
    print '\label{tab:weights}'
    print '\end{center}'
    print '\end{table*}'


def latexTableGameScoreRankings(game_name, gu_game):
    print '\\begin{table*}[!t]'
    print '\\begin{center}'
    print '\\begin{tabular}{|c|c|c|c|c|c|}'
    print multicolumn(6, boldify(game_name))+'\\\\'
    print '\hline'
    print '\\textbf{Points} & \\textbf{Controller} & \\textbf{Wins} &  \\textbf{Score} & \\textbf{Timesteps W} & \\textbf{Timesteps L}\\\\'

    for gu in gu_game:
        print '\hline'
        print gu.printPoints() + ' & ' + boldify(gu.controllerName()) + ' & ' + gu.printVictories() + ' & ' + gu.printScore() + ' & ' + gu.printWinGameticks() + ' & ' + gu.printLoseGameticks()
        print ' \\\\'

    print '\hline'
    print '\end{tabular}'
    print '\caption{Results for the game ' + game_name + ', showing points received, controller, average of wins, average of score achieved, ' \
                                                       'timesteps average when winning (W) and timesteps average when losing (L).}'
    print '\label{tab:weights}'
    print '\end{center}'
    print '\end{table*}'


def latexTableGameExplorationRankings(game_name, gu_game):
    print '\\begin{table*}[!t]'
    print '\\begin{center}'
    print '\\begin{tabular}{|c|c|c|c|}'
    print multicolumn(4, boldify(game_name))+'\\\\'
    print '\hline'
    print '\\textbf{Points} & \\textbf{Controller} & \\textbf{Perc. Explored} &  \\textbf{Timesteps last discovery}\\\\'

    for gu in gu_game:
        print '\hline'
        print gu.printPoints() + ' & ' + boldify(gu.controllerName()) + ' & ' + gu.printPercentageExplored() + ' & ' + gu.printDiscoveryTimeticks()
        print ' \\\\'

    print '\hline'
    print '\end{tabular}'
    print '\caption{Results for the game ' + game_name + ', showing points received, controller, average of percentage explored, ' \
                                                       'timesteps average for last discovery.}'
    print '\label{tab:weights}'
    print '\end{center}'
    print '\end{table*}'


def latexTableGameKnowledgeDiscoveryRankings(game_name, gu_game):
    print '\\begin{table*}[!t]'
    print '\\begin{center}'
    print '\\begin{adjustbox}{width=1\\textwidth}'
    print '\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|}'
    print multicolumn(10, boldify(game_name))+'\\\\'
    print '\hline'
    print '\\textbf{Points} & \\textbf{Controller} & \\textbf{Ack} & \\textbf{Interactions} & \\textbf{Curiosity Col.} & \\textbf{Curiosity Act.} & \\textbf{Ack ticks} & \\textbf{Int ticks} & \\textbf{CC ticks} & \\textbf{CA ticks}\\\\'

    for gu in gu_game:
        print '\hline'
        print gu.printPoints() + ' & ' + boldify(gu.controllerName()) + ' & ' + gu.printTotalSpritesAcknowledge() + ' & ' + gu.printTotalInteractions()  + ' & ' + gu.printCuriosityCollision()  + ' & ' + gu.printCuriosityActionedonto()  + ' & ' + gu.printTotalSpritesAcknowledgeGameticks()  + ' & ' + gu.printTotalInteractionsGameticks()  + ' & ' + gu.printCuriosityCollisionGameticks()  + ' & ' + gu.printCuriosityActionedontoGameticks()
        print ' \\\\'

    print '\hline'
    print '\end{tabular}'
    print '\end{adjustbox}'
    print '\caption{Results for the game ' + game_name + ', showing total sprites acknowledge (Ack), unique interactions, curiosity collisions, curiosity actions-onto (CA), timesteps average for last acknowledge (Ack), ' \
                                                       ' timesteps average for last unique interaction (Int), timesteps average for last Curiosity Collision (CC) achieved and timesteps average for last Curiosity Action-onto (CA)' \
                                                       ' achieved. Please note that \\textit{timesteps} are tag as \\textit{ticks}}'
    print '\label{tab:weights}'
    print '\end{center}'
    print '\end{table*}'

def latexTableGameKnowledgeEstimationRankings(game_name, gu_game):
    print '\\begin{table*}[!t]'
    print '\\begin{center}'
    print '\\begin{adjustbox}{width=1\\textwidth}'
    print '\\begin{tabular}{|c|c|c|c|}'
    print '\hline'
    print multicolumn(4, boldify(game_name))+'\\\\'
    print '\hline'
    print '\\textbf{Points} & \\textbf{Controller} & \\textbf{Square Error Average} & \\textbf{Interactions estimated}\\\\'

    for gu in gu_game:
        print '\hline'
        print gu.printPoints() + ' & ' + boldify(gu.controllerName()) + ' & ' + gu.printComparableSqErrorEstimatedAvg() + ' & ' + gu.printNInteractionsEstimed()
        print ' \\\\'

    print '\hline'
    print '\end{tabular}'
    print '\end{adjustbox}'
    print '\caption{Results for the game ' + game_name + ', showing total interactions estimated and the square error average obtained}'
    print '\label{tab:weights}'
    print '\end{center}'
    print '\end{table*}'


def latexTableGlobalRankings(heuristic_name, all_gr):
    print '\\begin{table*}[!t]'
    print '\\begin{center}'
    print '\\begin{tabular}{|c|c|c|}'
    print multicolumn(3, boldify(heuristic_name))+'\\\\'
    print '\hline'
    print '\\textbf{Rank} & \\textbf{Controller} & \\textbf{Total points}\\\\'

    for i, gr in enumerate(all_gr):
        print '\hline'
        print boldify(i+1) + ' & ' + gr.controllerName() + ' & ' + gr.printPoints() 
        print ' \\\\'

    print '\hline'
    print '\end{tabular}'
    print '\caption{Global results for the heuristic ' + heuristic_name + ', showing rank, controller and total number of points received.}'
    print '\label{tab:weights}'
    print '\end{center}'
    print '\end{table*}'

def latexNColumns(n_columns):
    text = '\\begin{adjustbox}{width=1\\textwidth}'
    text += '\\begin{tabular}{|'
    for c in range(0,n_columns):
        text += 'c|'
    text += '}'

    return text

def latexTableStart(n_columns):
    print '\\begin{table*}[!t]'
    print '\\begin{center}'
    print latexNColumns(n_columns)

def latexTableEnd(caption):
    print '\hline'
    print '\end{tabular}'
    print '\end{adjustbox}'
    print '\caption{' + caption + '}'
    print '\label{tab:weights}'
    print '\end{center}'
    print '\end{table*}'

def latexTableHeader(columns_data):
    print '\hline'
    header = ''
    for i, data in enumerate(columns_data):
        if i != 0:
            header += ' & '

        header += boldify(data)

    print header

def latexTableStypeEstimation(game_name, gu_game):
    """
        print '\\textbf{Points} & \\textbf{Controller} & \\textbf{Interactions estimed} & \\textbf{Square Error Average}\\\\'

        print
        print "Estimations "+GAMES[game_id]
        print
        for gu in gu_game:
            gu.printEstimationTable()
    """
    for gu in gu_game:
        print '\\begin{table*}[!t]'
        print '\\begin{center}'
        print '\\begin{adjustbox}{width=1\\textwidth}'
        print '\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|}'
        print '\hline'
        print multicolumn(13, boldify(game_name + ' ' + gu.controllerName()))+'\\\\'
        print '\hline'
        print '\\textbf{Stype} & '+multicolumn(4, boldify("Real"))+' & '+multicolumn(4, boldify("Estimations"))+' & '+multicolumn(4, boldify("SqError"))+'\\\\'
        print '\hline'
        print ' & \\textbf{CW} & \\textbf{CS} & \\textbf{AW} & \\textbf{AS} & \\textbf{CW} & \\textbf{CS} & \\textbf{AW} & \\textbf{AS} & \\textbf{CW} & \\textbf{CS} & \\textbf{AW} & \\textbf{AS}\\\\'

       
        gu.printEstimationTable()

        print '\hline'
        print '\end{tabular}'
        print '\end{adjustbox}'
        print '\caption{Results for the game '+game_name+', showing stypes estimations for the controller '+gu.controllerName()+' displaying' \
        ' the id of the sprite, the real information and the estimations and square error obtained by the agent for every interaction: ' \
        ' Collision wins (CW), Collision score (CS), Action-onto win (AW), Action-onto score (AS)}'
        print '\label{tab:weights}'
        print '\end{center}'
        print '\end{table*}'

    print'\clearpage'


def latexBigTableAllGamesScoreRanking(experiment, all_rankings_data, comparator):
    latexTableStart(7)
    
    print '\hline'
    print '\\textbf{Game} & \\textbf{Controller} & \\textbf{Wins} &  \\textbf{Score} & \\textbf{Timesteps W} & \\textbf{Timesteps L} & \\textbf{Points}\\\\'
    print '\hline'
    print '\hline'

    for i, game_ranking in enumerate(all_rankings_data):
        game_ranking.sort(comparator)
        for j, gu in enumerate(game_ranking):
            print '\cline{2-7}'

            if j == 0:
                row = '\\multirow{'+ str(len(game_ranking)) +'}{*}{'+ boldify(gu.gameName(i)) +'} & '
            else:
                row = ' & '
            
            if gu.isWinner():
                row += boldify(gu.controllerName()) + ' & ' + boldify(gu.printVictories()) + ' & ' + boldify(gu.printScore()) + ' & ' + boldify(gu.printWinGameticks()) + ' & ' + boldify(gu.printLoseGameticks()) + ' & '+ boldify(gu.printPoints())
            else:
                row += gu.controllerName() + ' & ' + gu.printVictories() + ' & ' + gu.printScore() + ' & ' + gu.printWinGameticks() + ' & ' + gu.printLoseGameticks() + ' & '+ gu.printPoints()
            
            print row
            print ' \\\\'

        print '\hline'
        print '\hline'

    latexTableEnd(experiment)

def latexBigTableAllGamesExplorationRanking(experiment, all_rankings_data, comparator):
    latexTableStart(5)
    
    print '\hline'
    print '\\textbf{Game} & \\textbf{Controller} & \\textbf{Perc. Explored} &  \\textbf{Timesteps last discovery} & \\textbf{Points}\\\\'
    print '\hline'
    print '\hline'

    for i, game_ranking in enumerate(all_rankings_data):
        game_ranking.sort(comparator)
        for j, gu in enumerate(game_ranking):
            print '\cline{2-5}'

            if j == 0:
                row = '\\multirow{'+ str(len(game_ranking)) +'}{*}{'+ boldify(gu.gameName(i)) +'} & '
            else:
                row = ' & '
            
            if gu.isWinner():
                row += boldify(gu.controllerName()) + ' & ' + boldify(gu.printPercentageExplored()) + ' & ' + boldify(gu.printDiscoveryTimeticks()) + ' & '+ boldify(gu.printPoints())
            else:
                row += gu.controllerName() + ' & ' + gu.printPercentageExplored() + ' & ' + gu.printDiscoveryTimeticks() + ' & '+ gu.printPoints()

            print row
            print ' \\\\'

        print '\hline'
        print '\hline'

    latexTableEnd(experiment)


def latexHeuristicSummaryTableMSH(experiment, all_rankings_data, comparator, not_used):

    heuristic_victories_avg = [0 for _ in range(len(CONTROLLERS))]
    heuristic_victories_sterror = [0 for _ in range(len(CONTROLLERS))]

    for game_ranking in all_rankings_data:
        game_ranking.sort(comparator)
        for controller_id, gu in enumerate(game_ranking):
            heuristic_victories_avg[controller_id] = heuristic_victories_avg[controller_id] + gu.getVictories()
            heuristic_victories_sterror[controller_id] = heuristic_victories_sterror[controller_id] + gu.getVictoriesStdErr()

    print '\\begin{table*}[!t]'
    print '\\begin{center}'
    print '\\begin{tabular}{|c|c|}'
    print '\hline'
    print multicolumn(2, boldify('MSH Stats'))+'\\\\'
    print '\hline'
    print '\\textbf{Controller} & \\textbf{Total average \\% of Wins}\\\\'

    for controller_id in range(len(CONTROLLERS)):
        controller_avg_victories_avg = (heuristic_victories_avg[controller_id] * 100)/len(GAMES)
        controller_avg_victories_sterror = (heuristic_victories_sterror[controller_id] * 100)/len(GAMES)
        print '\hline'
        print CONTROLLERS[controller_id] + ' & ' + "%.2f" % (controller_avg_victories_avg) + "(" + "%.2f" % (controller_avg_victories_sterror) + ")"
        print ' \\\\'

    print '\hline'
    print '\end{tabular}'
    print '\caption{Total percentage of wins average obtained for each of the controllers fpr MSH}'
    print '\label{table:stats_MSH}'
    print '\end{center}'
    print '\end{table*}'

def latexHeuristicSummaryTableMEH(experiment, all_rankings_data, comparator, not_used):

    heuristic_exploration_avg = [0 for _ in range(len(CONTROLLERS))]
    heuristic_exploration_sterror = [0 for _ in range(len(CONTROLLERS))]

    for game_ranking in all_rankings_data:
        game_ranking.sort(comparator)
        for controller_id, gu in enumerate(game_ranking):
            heuristic_exploration_avg[controller_id] = heuristic_exploration_avg[controller_id] + gu.getPercentageExplored()
            heuristic_exploration_sterror[controller_id] = heuristic_exploration_sterror[controller_id] + gu.getPercentageExploredStdErr()

    print '\\begin{table}[h!]'
    print '\\begin{center}'
    print '\\begin{adjustbox}{width=0.5\\textwidth}'
    print '\\begin{tabular}{|c|c|}'
    print '\\hline'
    print multicolumn(2, boldify('MEH Stats'))+'\\\\'
    print '\hline\hline'
    print '\\textbf{Controller} & \\textbf{Total average \\% Explored}\\\\'
    print '\\hline'

    for controller_id in range(len(CONTROLLERS)):
        controller_avg_exploration_avg = (heuristic_exploration_avg[controller_id] * 100)/len(GAMES)
        controller_avg_exploration_sterror = (heuristic_exploration_sterror[controller_id] * 100)/len(GAMES)
        print '\\hline'
        print CONTROLLERS[controller_id] + ' & ' + "%.2f" % (controller_avg_exploration_avg) + "(" + "%.2f" % (controller_avg_exploration_sterror) + ")"
        print ' \\\\'

    print '\\hline'
    print '\\end{tabular}'
    print '\\end{adjustbox}'
    print '\\caption{Total average of percentage explored obtained for each of the controllers fpr MEH}'
    print '\\label{table:stats_MEH}'
    print '\\end{center}'
    print '\\end{table}'

def latexHeuristicSummaryTableKD(experiment, all_rankings_data, comparator, games_highest_for_relative_summary):
    # print games_highest_for_relative_summary

    heuristic_ack_relative = [0 for _ in range(len(CONTROLLERS))]
    heuristic_int_relative = [0 for _ in range(len(CONTROLLERS))]
    heuristic_cc_relative = [0 for _ in range(len(CONTROLLERS))]
    heuristic_ca_relative = [0 for _ in range(len(CONTROLLERS))]
    n_ca_counter = 0
    for game_id, game_ranking in enumerate(all_rankings_data):
        game_ranking.sort(comparator)
        # print
        # print "GAME"
        if games_highest_for_relative_summary[game_id]['ca'] > 0:
            n_ca_counter = n_ca_counter + 1

        for controller_id, gu in enumerate(game_ranking):
            # print CONTROLLERS[controller_id]
            heuristic_ack_relative[controller_id] = heuristic_ack_relative[controller_id] + (float(gu.getotalSpritesAcknowledge())/games_highest_for_relative_summary[game_id]['ack'])
            heuristic_int_relative[controller_id] = heuristic_int_relative[controller_id] + (float(gu.getTotalInteractions())/games_highest_for_relative_summary[game_id]['interaction'])
            heuristic_cc_relative[controller_id] = heuristic_cc_relative[controller_id] + (float(gu.getCuriosityCollision())/games_highest_for_relative_summary[game_id]['cc'])
            if games_highest_for_relative_summary[game_id]['ca'] > 0:
                heuristic_ca_relative[controller_id] = heuristic_ca_relative[controller_id] + (float(gu.getCuriosityActionedonto())/games_highest_for_relative_summary[game_id]['ca'])

            # print str(gu.getotalSpritesAcknowledge()) + " " + str(heuristic_ack_relative)
            # print str(gu.getTotalInteractions()) + " " + str(heuristic_int_relative)
            # print str(gu.getCuriosityCollision()) + " " + str(heuristic_cc_relative)
            # print str(gu.getCuriosityActionedonto()) + " " + str(heuristic_ca_relative)
            # print "---"
           
    print '\\begin{table}[h!]'
    print '\\begin{center}'
    print '\\begin{adjustbox}{width=0.5\\textwidth}'
    print '\\begin{tabular}{|c|c|c|c|c|}'
    print '\\hline'
    print multicolumn(5, boldify('KDH Stats'))+'\\\\'
    print '\hline\hline'
    print '\\textbf{Controller} & \\textbf{\\% Ack} & \\textbf{\\% Int} & \\textbf{\\% CC} & \\textbf{\\% CA}\\\\'
    print '\\hline'

    for controller_id in range(len(CONTROLLERS)):
        controller_ack_relative = (heuristic_ack_relative[controller_id] * 100)/len(GAMES)
        controller_int_relative = (heuristic_int_relative[controller_id] * 100)/len(GAMES)
        controller_cc_relative = (heuristic_cc_relative[controller_id] * 100)/len(GAMES)
        controller_ca_relative = (heuristic_ca_relative[controller_id] * 100)/n_ca_counter
        print '\\hline'
        print CONTROLLERS[controller_id] + ' & ' + "%.2f" % (controller_ack_relative) + ' & ' + "%.2f" % (controller_int_relative) + ' & ' + "%.2f" % (controller_cc_relative) + ' & ' + "%.2f" % (controller_ca_relative) 
        print ' \\\\'

    print '\\hline'
    print '\\end{tabular}'
    print '\\end{adjustbox}'
    print '\\caption{}'
    print '\\label{table:stats_KDH}'
    print '\\end{center}'
    print '\\end{table}'


def latexHeuristicSummaryTableKE(experiment, all_rankings_data, comparator, games_highest_for_relative_summary):
    # print games_highest_for_relative_summary

    heuristic_intest_relative = [0 for _ in range(len(CONTROLLERS))]
    heuristic_sqerravg_avg = [0 for _ in range(len(CONTROLLERS))]

    for game_id, game_ranking in enumerate(all_rankings_data):
        game_ranking.sort(comparator)
        # print
        # print "GAME"

        for controller_id, gu in enumerate(game_ranking):
            # print CONTROLLERS[controller_id]
            heuristic_intest_relative[controller_id] = heuristic_intest_relative[controller_id] + (float(gu.getNInteractionsEstimated())/games_highest_for_relative_summary[game_id]['intest'])
            heuristic_sqerravg_avg[controller_id] = heuristic_sqerravg_avg[controller_id] + gu.getComparableSqerrorEstimatedAverage()

            # print str(gu.getNInteractionsEstimated()) + " " + str(heuristic_intest_relative[controller_id])
            # print str(gu.getSqerrorEstimedAvg()) + " " + str(heuristic_sqerravg_avg[controller_id])
            # print "---"
           
    print '\\begin{table}[h!]'
    print '\\begin{center}'
    print '\\begin{adjustbox}{width=0.5\\textwidth}'
    print '\\begin{tabular}{|c|c|c|}'
    print '\\hline'
    print multicolumn(3, boldify('KDE Stats'))+'\\\\'
    print '\hline\hline'
    print '\\textbf{Controller} & textbf{Square Error Average} & \\textbf{\\% Int estimated}\\\\'
    print '\\hline'

    for controller_id in range(len(CONTROLLERS)):
        controller_intest_relative = (heuristic_intest_relative[controller_id] * 100)/len(GAMES)
        controller_sqerravg_avg = heuristic_sqerravg_avg[controller_id]/len(GAMES)
        print '\\hline'
        print CONTROLLERS[controller_id] + ' & ' + "%.3f" % (controller_sqerravg_avg) + ' & ' + "%.2f" % (controller_intest_relative)
        print ' \\\\'

    print '\\hline'
    print '\\end{tabular}'
    print '\\end{adjustbox}'
    print '\\caption{}'
    print '\\label{table:stats_KEH}'
    print '\\end{center}'
    print '\\end{table}'

def latex_table_array(dim1, dim2, table1, table2, caption, is_perc = True):

    num_rows = len(dim1)
    num_cols = len(dim2)

    str_columns = '\\begin{tabular}{|c|'
    col_header = ' '

    for x in range(num_cols):
        str_columns = str_columns + 'c|'
        col_header += ' & \\textbf{' + dim2[x] + '} '

    str_columns = str_columns + '}' + ' \\\\'
    col_header += ' \\\\'

    print '\\begin{table*}[!t]'
    print '\\begin{center}'
    print str_columns
    print '\hline'
    print col_header

    row_idx = 0
    for row in table1:

        print '\hline'

        print' \\textbf{' + dim1[row_idx] + '} ',

        for i in range(len(row)):

            str_val = '-'
            try:
               val = float(row[i])
               val2 = float(table2[row_idx][i])
               str_val = "%.2f (%.2f)" % (float(100*val), float(100*val2)) if is_perc else str(val)
            except ValueError:
               pass


            print ' & ' + str_val,

        print ' \\\\'
        row_idx += 1


    print '\hline'
    print '\end{tabular}'
    print '\caption{' + caption + '}'
    print '\label{tab:avgData}'
    print '\end{center}'
    print '\end{table*}'

