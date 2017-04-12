from valfunction_config import *
from valfunction_helper import *

import glob
import numpy as np
import pylab
import sys 
from latex import latexTableStypeEstimation

"""
KNOWLEDGE DISCOVERY FUNCTIONS
"""

def checkKnowledgeDiscoveryFileData(game_results):
	"""
	For KnowledgeDiscovery the data has the following format
	
	gameId controllerId randomSeed winnerId score gameTicks nSpritesAck nSpritesFromAvatarAck nTotalAck gameticksAck nCollided nActioned nTotalInteracions gameTicksColl gameTicksAct gameTicksInt curiosity gameTicksCur curiosityAction gameTicksCurAction

	There must be N_RESULTS per game per controller
	"""
	current_id = 0
	n_results_current = 0
	total_results = 0
	for data_row in game_results:
		total_results = total_results + 1
		if len(data_row) != 20:
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

def setHighestForRelativePercentagesKDH(gu_game, game_id):
    best_ack = 0
    best_int = 0
    best_cc = 0
    best_ca = 0

    # It is needed to be sorted beforehand
    gu_game.sort(gameUnitComparator)

    for i, gu in enumerate(gu_game):
    	ack = gu.getotalSpritesAcknowledge()
    	interaction = gu.getTotalInteractions()
    	cc = gu.getCuriosityCollision()
    	ca = gu.getCuriosityActionedonto()

    	if ack > best_ack:
    		best_ack = ack

    	if interaction > best_int:
    		best_int = interaction

    	if cc > best_cc:
    		best_cc = cc

    	if ca > best_ca:
    		best_ca = ca

    games_highest_for_relative_summary[game_id] = dict(ack=best_ack, interaction=best_int, cc=best_cc, ca=best_ca)


def setHighestForRelativePercentagesKEH(gu_game, game_id):
    best_intest = 0

    # It is needed to be sorted beforehand
    gu_game.sort(gameUnitComparator)

    for i, gu in enumerate(gu_game):
    	intest = gu.getNInteractionsEstimated()

    	if intest > best_intest:
    		best_intest = intest

    games_highest_for_relative_summary[game_id] = dict(intest=best_intest)


def statsKnowledgeDiscovery(game_results, game_id):
	#gameId controllerId randomSeed winnerId score gameTicks nSpritesAck nSpritesFromAvatarAck nTotalAck gameticksAck nCollided nActioned nTotalInteracions gameTicksColl gameTicksAct gameTicksInt curiosity gameTicksCur curiosityAction gameTicksCurAction

	gkdu_game = []
	for controller_id in range(0, len(CONTROLLERS)):
		firs_result = N_RESULTS * controller_id
		last_result = N_RESULTS + firs_result

		#TODO TO CHANGE THIS
		
		controller_total_sprites_ack 		= game_results[:,8][firs_result:last_result]
		controller_total_interactions 		= game_results[:,12][firs_result:last_result]
		controller_curiosity_collision 		= game_results[:,16][firs_result:last_result]
		controller_curiosity_actiononto 	= game_results[:,18][firs_result:last_result]

		controller_acknowledge_ticks 		= game_results[:,9][firs_result:last_result]
		controller_interactions_ticks 		= game_results[:,15][firs_result:last_result]
		controller_curiosityColl_ticks 		= game_results[:,17][firs_result:last_result]
		controller_curiosityAct_ticks 		= game_results[:,19][firs_result:last_result]
		
		gkdu = GameKnowledgeDiscoveryUnit(controller_id, controller_total_sprites_ack, controller_total_interactions, controller_curiosity_collision, controller_curiosity_actiononto, \
			controller_acknowledge_ticks, controller_interactions_ticks, controller_curiosityColl_ticks, controller_curiosityAct_ticks)

		#gkdu.printData();
		gkdu_game.append(gkdu)


	gameSetRankingPoints(gkdu_game)

	# Set to global var
	setHighestForRelativePercentagesKDH(gkdu_game, game_id)
	controllers_total_rankings[game_id] = gkdu_game

	# print 
	#Printing results
	# printGameResults(game_id, gkdu_game)

"""
KNOWLEDGE ESTIMATION FUNCTIONS
"""

"""
"""
def getFileKEResultsData(game_index):
	game_name = GAMES[game_index]

	file_name = "experiment" + str(ID_EXP) + "/results/ExperimentValFunction_results_" + EXPERIMENTS[ID_EXP] + "_" + game_name + ".txt"

	if not LATEX_EXPORT:
		print "Reading "+file_name

	files = glob.glob(file_name)
	if len(files) == 0:
		print "Missing file: ", file_name
		return None

	return files[0]


"""
"""
def checkKnowledgeEstimationFileData(results_file):
	"""
	For KnowledgeEstimation the data has the following format
	
	gameId controllerId randomSeed winnerId score gameTicks totalIntChecked n_stypestats
	1 stype interType n_win n_los score_diff n_totalChecked winEstimation scoreEstimation
	....
	n_stypestats stype interType n_win n_los score_diff n_totalChecked winEstimation scoreEstimation

	There must be N_RESULTS per game per controller
	"""
	current_id = 0
	n_results_current = 0
	total_results = 0
	n_stypestats = 0
	n_stypestats_counter = 0
	n_total_int_checked = 0
	with open(results_file) as f:
		for row in f:
			data_row = row.strip('\n').split(' ')

			if n_stypestats == 0:
				total_results = total_results + 1
				if len(data_row) != 8:
					print "ERROR in file: the number of elements in the data is not correct"
					return False

				if n_total_int_checked != 0:
					print "ERROR in total interactions sanity check. There is something weird in the data"
					return False
				
				if n_results_current >= N_RESULTS:
					current_id = current_id + 1
					n_results_current = 0

				if int(data_row[1]) == current_id:
					n_results_current = n_results_current + 1
				else:
					print "ERROR in file: not correct number of results for controller "+str(current_id)
					return False

				n_total_int_checked = int(data_row[6])
				n_stypestats = int(data_row[7])
				n_stypestats_counter = 0
			else:
				if len(data_row) != 9:
					print "ERROR in file: the number of elements in the estimation is not correct"
					return False

				if int(data_row[0]) != n_stypestats_counter:
					print "ERROR in file: not correct number of stypestats for controller "+str(current_id)
					return False

				int_type = int(data_row[2])
				if int_type != INT_COLLISION and int_type != INT_ACTIONONTO:
					print "ERROR in file: The interaction type "+str(int_type)+" is not valid, please check the data"
					return False

				n_total_int_checked = n_total_int_checked - int(data_row[6])
				n_stypestats_counter = n_stypestats_counter + 1
				n_stypestats = n_stypestats - 1

	if N_RESULTS*len(CONTROLLERS) != total_results:
		print "ERROR in file: there is not the number of results expected"
		return False

	return True


"""
"""
def checkKEFileData():
	# The results in the file must be consistent in order to process them
	print "Checking validity of file for "+EXPERIMENTS[ID_EXP]

	for game_index in range(0, len(GAMES)):
		
		results_file = getFileKEResultsData(game_index)
		if results_file is None:
			print "ERROR in file"
			continue

		validity = checkKnowledgeEstimationFileData(results_file)

		if not validity:
			print "NOT VALID"
			continue
		else:
			print "VALID"


"""
"""
def readKEData():
	if not LATEX_EXPORT:
		print "Reading data for "+EXPERIMENTS[ID_EXP]
		print
	
	for game_index in range(0, len(GAMES)):

		sprites_info = getFileSpritesInfo(game_index)
		if sprites_info is None:
			print "ERROR in file"
			continue

		results_file = getFileKEResultsData(game_index)
		if results_file is None:
			print "ERROR in file"
			continue

		statsKnowledgeEstimation(results_file, game_index, sprites_info)

	#print controllers_total_rankings
	#printTotalRankingBigTable()
	
	printGlobalRanking()
	# printHeuristicSummaryTable()


"""
"""
def getFileSpritesInfo(game_index):
	game_name = GAMES[game_index]

	file_name = "experiment" + str(ID_EXP) + "/spritesInfo/ExperimentValFunction_SpritesInfo_" + game_name + ".txt"

	if not LATEX_EXPORT:
		print "Reading spritesInfo "+file_name

	files = glob.glob(file_name)
	if len(files) == 0:
		print "Missing file: ", file_name
		return None

	return pylab.loadtxt(files[0], comments='*', delimiter='\t', dtype=str)


"""
"""
def getStypeInteractionsRealData(game_id, sprites_info):
	# alias stype collision_wins collision_score actiononto_wins actiononto_score
	real_stype_info_data = {}

	for data_row in sprites_info:
		stype = int(data_row[1])

		if data_row[2] == '-':
			collision_wins = None
		else:
			collision_wins = int(data_row[2])

		if data_row[3] == '-':
			collision_score = None
		else:
			collision_score = float(data_row[3])

		if data_row[4] == '-':
			actiononto_wins = None
		else:
			actiononto_wins = int(data_row[4])

		if data_row[5] == '-':
			actiononto_score = None
		else:
			actiononto_score = float(data_row[5])

		real_stype_info_data[stype] = StypeInformation(collision_wins, collision_score, actiononto_wins, actiononto_score)

	return real_stype_info_data

"""
"""
def statsKnowledgeEstimation(results_file, game_id, sprites_info):
	#gameId controllerId randomSeed winnerId score gameTicks totalIntChecked n_stypestats
	# 1 stype interType n_win n_los score_diff n_totalChecked winEstimation scoreEstimation
	# ....
	# n_stypestats stype interType n_win n_los score_diff n_totalChecked winEstimation scoreEstimation
	# 0 0 0 42 0 27.0 124687 3.368434560138587E-4 2.1654222172319489E-4

	if not LATEX_EXPORT:
		#print sprites_info
		pass

	real_stype_info_data = getStypeInteractionsRealData(game_id, sprites_info)
	games_stype_info_data[game_id] = real_stype_info_data

	gkeu_game = []

	total_results = 0
	n_stypestats = 0
	n_results_current = 0
	controller_estimations = {}
	controller_id = None

	# Store the stypes estimated in this game for any of the controllers
	# This information will be used to extract comparable stats
	# As if a certain controller hasnt managed to find a certain sprite but other of the controllers did
	all_controllers_stype_estimations = {}

	with open(results_file) as f:
		for row in f:
			data_row = row.strip('\n').split(' ')

			if n_stypestats == 0:
				# Information about the game played
				total_results = total_results + 1
				n_results_current = n_results_current + 1

				if controller_id is None:
					n_results_current = 1
					controller_id = int(data_row[1])
					controller_estimations = {}

				if n_results_current > N_RESULTS:
					gkeu = GameKnowledgeEstimationUnit(controller_id, controller_estimations, real_stype_info_data)
					gkeu_game.append(gkeu)

					n_results_current = 1
					controller_id = int(data_row[1])
					controller_estimations = {}
				
				# n_total_int_checked = int(data_row[6])
				n_stypestats = int(data_row[7])
			else:
				# n_win 			= int(data_row[3])
				# n_los 			= int(data_row[4])
				# score_diff 		= float(data_row[5])
				# n_total_checked = int(data_row[6])
				stype = int(data_row[1])
				int_type = int(data_row[2])
				win_estimation 	= float(data_row[7])
				score_estimation = float(data_row[8])
				
				if stype not in controller_estimations:
					if not real_stype_info_data[stype]:
						# sanity check
						sys.exit('RESULT '+ total_results +' ERROR. The stype '+str(stype)+' interaction '+str(int_type)+'data found for controller '+str(controller_id)+' does not exists in the real data provided... please check')

					controller_estimations[stype] = StypeEstimations(stype, real_stype_info_data[stype])
				
				controller_estimations[stype].addInteractionEstimations(int_type, win_estimation, score_estimation)

				# Stype included to all controllers estimations
				if stype not in all_controllers_stype_estimations:
					all_controllers_stype_estimations[stype] = {}

				if int_type not in all_controllers_stype_estimations[stype]:
					all_controllers_stype_estimations[stype][int_type] = True

				n_stypestats = n_stypestats - 1


	# It is set information for last block processed
	gkeu = GameKnowledgeEstimationUnit(controller_id, controller_estimations, real_stype_info_data)
	gkeu_game.append(gkeu)

	# For this heuristic is needed to consider possible stypes estimated by some controllers but not others. It is needed to take
	# this into consideration and set the stats and ranking based on this
	for gkeu_toreview in gkeu_game:
		gkeu_toreview.setStats(all_controllers_stype_estimations)


	# TODO EVERHTING NEEDS TO BE REVIEWED
	# All the data has been read and stored, the rankings can be set
	gameSetRankingPoints(gkeu_game)

	# Set to global vars
	setHighestForRelativePercentagesKEH(gkeu_game, game_id)
	controllers_total_rankings[game_id] = gkeu_game

	#Printing results
	printGameResults(game_id, gkeu_game)
	# printStypeEstimationsTable(game_id, gkeu_game)

def printStypeEstimationsTable(game_id, gu_game):
	if LATEX_EXPORT:
		latexTableStypeEstimation(GAMES[game_id], gu_game)
	else:
		print
		print "Estimations "+GAMES[game_id]
		print
		for gu in gu_game:
			gu.printEstimationTable()