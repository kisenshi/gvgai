__author__ = 'cris'

import glob
import numpy as np
import pylab

from valfunction_config import *
from valfunction_helper import *

from valfunction_knowledge import *

"""
READ FILE
"""

def getFileResultsData(game_index):
	game_name = GAMES[game_index]

	file_name = "experiment" + str(ID_EXP) + "/results/ExperimentValFunction_results_" + EXPERIMENTS[ID_EXP] + "_" + game_name + ".txt"

	if not LATEX_EXPORT:
		print "Reading "+file_name

	files = glob.glob(file_name)
	if len(files) == 0:
		print "Missing file: ", file_name
		return None

	return pylab.loadtxt(files[0], comments='*', delimiter=' ')

"""
FILE VALIDATION CHECK
"""

def checkMaximizeScoreFileData(game_results):
	"""
	For MaximizeScoreHeuristic the data has the following format
	gameId controllerId randomSeed winnerId score gameTicks

	There must be N_RESULTS per game per controller
	"""
	current_id = 0
	n_results_current = 0
	total_results = 0
	for data_row in game_results:
		total_results = total_results + 1
		if len(data_row) != 6:
			print "ERROR in file: the number of elements in the data is not correct"
			return False
		
		if n_results_current >= N_RESULTS:
			current_id = current_id + 1
			n_results_current = 0

		if data_row[1] == current_id:
			n_results_current = n_results_current + 1
		else:
			print "ERROR in file: not correct number of results for controller "+str(current_id)
			return False

	if N_RESULTS*len(CONTROLLERS) != total_results:
		print "ERROR in file: there is not the number of results expected"
		return False

	return True


def checkMaximizeExplFileData(game_results):
	"""
	For MaximizeExplorationHeuristic the data has the following format
	gameId controllerId randomSeed winnerId score gameTicks mapSize nExplored navigationSize percentageExplored lastDiscoveredTick

	There must be N_RESULTS per game per controller
	"""
	current_id = 0
	n_results_current = 0
	total_results = 0
	for data_row in game_results:
		total_results = total_results + 1
		if len(data_row) != 11:
			print "ERROR in file: the number of elements in the data is not correct"
			return False
		
		if n_results_current >= N_RESULTS:
			current_id = current_id + 1
			n_results_current = 0

		if data_row[1] == current_id:
			n_results_current = n_results_current + 1
		else:
			print "ERROR in file: not correct number of results for controller "+str(current_id)
			return False

	if N_RESULTS*len(CONTROLLERS) != total_results:
		print "ERROR in file: there is not the number of results expected"
		return False

	return True

def checkFileData():
	# The results in the file must be consistent in order to process them
	print "Checking validity of file for "+EXPERIMENTS[ID_EXP]

	for i in range(0, len(GAMES)):
		game_results = getFileResultsData(i)

		if game_results is None:
			print "ERROR in file"
			continue

		validity = False
		if ID_EXP == MAXSCORE_ID:
			validity = checkMaximizeScoreFileData(game_results)
		elif ID_EXP == MAXEXPL_ID:
			validity = checkMaximizeExplFileData(game_results)
		elif ID_EXP == KNW_DISCOVERY_ID:
			validity = checkKnowledgeDiscoveryFileData(game_results)
		else:
			print "ERROR: not valid heuristic ID provided"
			continue

		if not validity:
			print "NOT VALID"
			continue
		else:
			print "VALID"
		

"""
EXPEIMENTS DATA ANALYSIS
"""

def statsMaximizeScore(game_results, game_id):
	#gameId controllerId randomSeed winnerId score gameTicks
	game_victories_avg 		= [0 for _ in range(len(CONTROLLERS))]
	game_scores_avg	 		= [0 for _ in range(len(CONTROLLERS))]
	game_winGameticks_avg 	= [0 for _ in range(len(CONTROLLERS))]
	game_loseGameticks_avg 	= [0 for _ in range(len(CONTROLLERS))]

	gsu_game = []
	for controller_id in range(0, len(CONTROLLERS)):
		firs_result = N_RESULTS * controller_id
		last_result = N_RESULTS + firs_result
		
		victoriesController = game_results[:,3][firs_result:last_result]
		scoresController 	= game_results[:,4][firs_result:last_result]

		gameticksRawController = game_results[:,5][firs_result:last_result]

		#The gameticks will be used for untie, it is stored the winning and losing ticks. It is set nan if the element should not be considered later on for the average
		winGameticksCrontroller = [ gameticksRawController[j] if victoriesController[j] == 1.0 else np.nan for j in range(len(gameticksRawController))]
		loseGameticksCrontroller = [ gameticksRawController[j] if victoriesController[j] == 0.0 else np.nan for j in range(len(gameticksRawController))]
		
		#avgVictoriesController = 
		# print "victories: "
		# print victoriesController
		# print "scores: "
		# print scoresController
		# print "gamticks: "
		# print gameticksRawController
		# print winGameticksCrontroller
		# print loseGameticksCrontroller

		gsu = GameScoreUnit(controller_id, victoriesController, scoresController, winGameticksCrontroller, loseGameticksCrontroller)
		gsu_game.append(gsu)


	gameSetRankingPoints(gsu_game)

	# Set to global var
	controllers_total_rankings[game_id] = gsu_game

	# Printing results
	#printGameResults(game_id, gsu_game)



def statsMaximizeExploration(game_results, game_id):
	#gameId controllerId randomSeed winnerId score gameTicks mapSize nExplored navigationSize percentageExplored lastDiscoveredTick
	percentage_explored_avg	= [0 for _ in range(len(CONTROLLERS))]
	last_discovery_tick_avg = [0 for _ in range(len(CONTROLLERS))]

	ge_game = []
	for controller_id in range(0, len(CONTROLLERS)):
		firs_result = N_RESULTS * controller_id
		last_result = N_RESULTS + firs_result

		percentagExploredController 	= game_results[:,9][firs_result:last_result]
		lastDiscoverytickController 	= game_results[:,10][firs_result:last_result]

		ge = GameExplorationUnit(controller_id, percentagExploredController, lastDiscoverytickController)
		ge_game.append(ge)

	gameSetRankingPoints(ge_game)

	# Set to global var
	controllers_total_rankings[game_id] = ge_game

	#Printing results
	#printGameResults(game_id, ge_game)



def readExperimentData():
	if not LATEX_EXPORT:
		print "Reading data for "+EXPERIMENTS[ID_EXP]
		print
	
	for i in range(0, len(GAMES)):
		game_results = getFileResultsData(i)

		if game_results is None:
			continue

		statsFunction(game_results, i)

	#print controllers_total_rankings
	#printTotalRankingBigTable()
	#printGlobalRanking()
	printHeuristicSummaryTable()


#checkFileData()

"""
Set elements that depends on the heuristic
"""
readData = readExperimentData
checkFile = checkFileData
if ID_EXP == MAXSCORE_ID:
	statsFunction 			= statsMaximizeScore
	latexTableGameRankings 	= latexTableGameScoreRankings
elif ID_EXP == MAXEXPL_ID:
	statsFunction 			= statsMaximizeExploration
	latexTableGameRankings 	= latexTableGameExplorationRankings
elif ID_EXP == KNW_DISCOVERY_ID:
	statsFunction 			= statsKnowledgeDiscovery
elif ID_EXP == KNW_ESTIMATION_ID:
	checkFile 				= checkKEFileData
	readData 				= readKEData
else:
	print "ERROR:valfunction_experiment not valid heuristic ID provided"
	exit()

#checkFile()
readData()