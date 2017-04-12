__author__ = 'cris'

import numpy as np

from valfunction_config import *
from latex import latexTableGameScoreRankings, latexTableGameExplorationRankings, latexTableGlobalRankings, latexBigTableAllGamesScoreRanking, latexBigTableAllGamesExplorationRanking, \
latexTableGameKnowledgeDiscoveryRankings, latexTableGameKnowledgeEstimationRankings,\
latexHeuristicSummaryTableMSH, latexHeuristicSummaryTableMEH, latexHeuristicSummaryTableKD, latexHeuristicSummaryTableKE

from latex import boldify

def gameSetRankingPoints(gu_game):
    last_gu = None
    n_ties = 0

    # It is needed to be sorted beforehand
    gu_game.sort(gameUnitComparator)

    for i, gu in enumerate(gu_game):
        if last_gu is None:
            # It is the first element
            gu.points = F1_RANKING_POINTS[i]
        else:
            if gu.isTie(last_gu):
                n_ties += 1
                gu.points = F1_RANKING_POINTS[i - n_ties]
            else:
                n_ties = 0
                gu.points = F1_RANKING_POINTS[i]

        for gr in controllers_total_points:
            if gr.isController(gu.controller_id):
                gr.points += gu.points
                break

        last_gu = gu


"""
GlobalRanking
Object to contain the controller id and its points

Its comparator order the elements by points in descendent order
to be used in the ranking
"""

class GlobalRankingUnit:

	def __init__(self, controller_id):
		self.controller_id = controller_id
		self.points = 0

	def isController(self, id):
		return self.controller_id == id

	def controllerName(self):
		return CONTROLLERS[self.controller_id]

	def printPoints(self):
		return str(self.points)


def globalRankingUnitComparator(gr1, gr2):
# The one with more victories goes first
	if gr1.points > gr2.points:
		return -1
	
	if gr1.points < gr2.points:
		return 1

	return 0


"""
GameScoreUnit
Object to contain the information belonging to a controller and its results in a game
It contains the points scored in comparison with the rest of the games as well

Its comparator order the elements by:

1) number of victories
2) score
3) less time when winning
4) more survival time when losing

If all the elements are the same, it is considered a tie
"""
class GameScoreUnit:

    def __init__(self, controller_id, all_victories, all_scores, all_winGameticks, all_loseGameticks):
        self.controller_id 		= controller_id
        self.points 			= None
        # Averages
        self.victories_avg 		= np.average(all_victories)
        self.scores_avg 		= np.average(all_scores)
        self.winGameticks_avg 	= np.nanmean(all_winGameticks)
        self.loseGameticks_avg  = np.nanmean(all_loseGameticks)
        # Standard error
        self.victories_sterror		= np.std(all_victories) / np.sqrt(len(all_victories))
        self.scores_sterror			= np.std(all_scores) / np.sqrt(len(all_scores))
        self.winGameticks_sterror 	= np.nanstd(all_winGameticks) / np.sqrt(len(all_winGameticks) - np.count_nonzero(np.isnan(all_winGameticks)))
        self.loseGameticks_sterror	= np.nanstd(all_loseGameticks) / np.sqrt(len(all_loseGameticks) - np.count_nonzero(np.isnan(all_loseGameticks)))

    def isTie(self, gsu2):
    	return self.victories_avg == gsu2.victories_avg \
    	and self.scores_avg == gsu2.scores_avg \
    	and (self.winGameticks_avg == gsu2.winGameticks_avg or np.isnan(self.winGameticks_avg) and np.isnan(gsu2.winGameticks_avg)) \
    	and (self.loseGameticks_avg == gsu2.loseGameticks_avg or np.isnan(self.loseGameticks_avg) and np.isnan(gsu2.loseGameticks_avg)) \


    def printData(self):
    	print CONTROLLERS[self.controller_id] + ": "
    	print
    	print "victories: "+self.printVictories()
    	print "score: "+self.printScore()
    	print "winGametick: "+self.printWinGameticks()
    	print "loseGametick: "+self.printLoseGameticks()
    	print
    	print "POINTS: "+self.printPoints()
    	print "-------------"

    def getVictories(self):
        return self.victories_avg

    def getVictoriesStdErr(self):
        return self.victories_sterror

    def gameName(self, game_id):
        return GAMES[game_id]

    def controllerName(self):
    	return CONTROLLERS[self.controller_id]

    def isWinner(self):
        return self.points == F1_RANKING_POINTS[0]

    def printVictories(self):
    	return "%.2f" % (100.0*self.victories_avg) + " " + self.printVictoriesErr()

    def printVictoriesErr(self):
    	return "(" + "%.2f" % (100.0*self.victories_sterror) + ")"

    def printScore(self):
    	return "%.2f" % (self.scores_avg) + " " + self.printScoreErr()

    def printScoreErr(self):
    	return  "(" + "%.2f" % (self.scores_sterror) + ")"

    def printWinGameticks(self):
    	if np.isnan(self.winGameticks_avg):
    		return ' - '
    	return "%.2f" % (self.winGameticks_avg) + " " + self.printWinGameticksErr()

    def printWinGameticksErr(self):
    	if np.isnan(self.winGameticks_avg):
    		return ''
    	return "(" + "%.2f" % (self.winGameticks_sterror) + ")"

    def printLoseGameticks(self):
    	if np.isnan(self.loseGameticks_avg):
    		return ' - '
    	return "%.2f" % (self.loseGameticks_avg) + " " + self.printLoseGameticksErr()

    def printLoseGameticksErr(self):
    	if np.isnan(self.loseGameticks_avg):
    		return ''
    	return "(" + "%.2f" % (self.loseGameticks_sterror) + ")"

    def printPoints(self):
    	return str(self.points)

def gameScoreUnitComparator(gsu1, gsu2):

	# The one with more victories goes first
	if gsu1.victories_avg > gsu2.victories_avg:
		return -1
	
	if gsu1.victories_avg < gsu2.victories_avg:
		return 1

	# If tie in victories, it is considered the score: the one with higher score goes first
	if gsu1.scores_avg > gsu2.scores_avg:
		return -1

	if gsu1.scores_avg < gsu2.scores_avg:
		return 1

    # If tie in scores, it is considered first the one that wins the game first (winGametick)
	if not np.isnan(gsu1.winGameticks_avg) and not np.isnan(gsu2.winGameticks_avg):
		if gsu1.winGameticks_avg < gsu2.winGameticks_avg:
			return -1
		if gsu1.winGameticks_avg > gsu2.winGameticks_avg:
			return 1

	# If not winnings or tie in winGameticks average too, it is considered first the one that survives more time when losing (loseGametick)
	if not np.isnan(gsu1.loseGameticks_avg) and not np.isnan(gsu2.loseGameticks_avg):
		if gsu1.loseGameticks_avg > gsu2.loseGameticks_avg:
			return -1
		if gsu1.loseGameticks_avg < gsu2.loseGameticks_avg:
			return 1
	
	# If still tie, just keep calm & carry on
	return 0

"""
For printing the huge table, the results will be reordered by controller id
"""
def gameUnitComparatorByController(gu1, gu2):
    # The controller with less id goes first
    if gu1.controller_id < gu2.controller_id:
        return -1

    if gu1.controller_id > gu2.controller_id:
        return 1

    return 0

def isDeterministicGame(game_id):
    return game_id in DETERMINISTIC_GAMES

def isStochasticGame(game_id):
    return game_id in STOCHASTIC_GAMES

"""
GameExplorationUnit
Object to contain the information belonging to a controller and its results in a game when using exploration
It contains the percentaged of the map explored and the number of ticks when the last discover occurred

Its comparator order the elements by:

1) percentage explored
2) less time taken for discovery

If all the elements are the same, it is considered a tie
"""
class GameExplorationUnit:

    def __init__(self, controller_id, all_percentage_explored, all_last_discovery_tick):
        self.controller_id 				= controller_id
        self.points 					= None
        # Averages
        self.percentage_explored_avg 	= np.average(all_percentage_explored)
        self.last_discovery_tick_avg 	= np.average(all_last_discovery_tick)
     	# Standard Errors
     	self.percentage_explored_sterror	= np.std(all_percentage_explored) / np.sqrt(len(all_percentage_explored))
     	self.last_discovery_tick_sterror	= np.std(all_last_discovery_tick) / np.sqrt(len(all_last_discovery_tick))

    def isTie(self, gsu2):
    	return self.percentage_explored_avg == gsu2.percentage_explored_avg \
    	and self.last_discovery_tick_avg == gsu2.last_discovery_tick_avg

    def printData(self):
    	print CONTROLLERS[self.controller_id] + ": "
    	print
    	print "perc explored: "+self.printPercentageExplored()
    	print "last discovery: "+self.printDiscoveryTimeticks()
    	print
    	print "POINTS: "+self.printPoints()
    	print "-------------"

    def getPercentageExplored(self):
        return self.percentage_explored_avg

    def getPercentageExploredStdErr(self):
        return self.percentage_explored_sterror

    def gameName(self, game_id):
        return GAMES[game_id]

    def controllerName(self):
    	return CONTROLLERS[self.controller_id]

    def isWinner(self):
        return self.points == F1_RANKING_POINTS[0]

    def printPercentageExplored(self):
    	return "%.2f" % (100.0*self.percentage_explored_avg) + " " + self.printPercentageExploredErr()

    def printPercentageExploredErr(self):
    	return  "(" + "%.2f" % (100.0*self.percentage_explored_sterror) + ")"

    def printDiscoveryTimeticks(self):
    	return "%.2f" % (self.last_discovery_tick_avg) + " " + self.printDiscoveryTimeticksErr()

    def printDiscoveryTimeticksErr(self):
    	return  "(" + "%.2f" % (self.last_discovery_tick_sterror) + ")"

    def printPoints(self):
    	return str(self.points)

def gameExplorationUnitComparator(ge1, ge2):

	# The one with more percentage explored goes first
	if ge1.percentage_explored_avg > ge2.percentage_explored_avg:
		return -1
	
	if ge1.percentage_explored_avg < ge2.percentage_explored_avg:
		return 1

	# If tie in exploration, it is considered the less time it took to discover it. It is considerd the tick where the last discovered was done
	if ge1.last_discovery_tick_avg < ge2.last_discovery_tick_avg:
		return -1

	if ge1.last_discovery_tick_avg > ge2.last_discovery_tick_avg:
		return 1

	return 0

"""
GameKnowledgeDiscoveryUnit
Object to contain the information belonging to a controller and its results in a game when using knowledge discovery
It contains different elements related with the ackknowledge of the agent about the sprites in the game and its interactions with them

Its comparator order the elements by:

1) total number of different sprites ackknowledge
2) total number of unique interactions with sprites 
3) total collision curiosity
4) total actioned-onto curiosity
5) less time acknoledging the sprites
6) less time achieving the unique interactions
7) less time achieving the collision curiosity
7) less time achieving the actioned-onto curiosity

If all the elements are the same, it is considered a tie
"""
class GameKnowledgeDiscoveryUnit:

    def __init__(self, controller_id, all_total_sprites_ack, all_total_interactions, all_curiosity_collision, all_curiosity_actiononto, all_acknowledge_ticks, all_interactions_ticks, all_curiosityColl_ticks, all_curiosityAct_ticks):
        self.controller_id      = controller_id
        self.points             = None
        # Averages
        self.total_sprites_ack_avg    = np.average(all_total_sprites_ack)
        self.total_interactions_avg   = np.average(all_total_interactions)
        self.curiosity_collision_avg  = np.average(all_curiosity_collision)
        self.curiosity_actiononto_avg = np.average(all_curiosity_actiononto)
        self.acknowledge_ticks_avg    = np.average(all_acknowledge_ticks)
        self.interactions_ticks_avg   = np.average(all_interactions_ticks)
        self.curiosityColl_ticks_avg  = np.average(all_curiosityColl_ticks)
        self.curiosityAct_ticks_avg   = np.average(all_curiosityAct_ticks)
        # Standard error
        self.total_sprites_ack_sterror      = np.std(all_total_sprites_ack) / np.sqrt(len(all_total_sprites_ack))
        self.total_interactions_sterror     = np.std(all_total_interactions) / np.sqrt(len(all_total_interactions))
        self.curiosity_collision_sterror    = np.std(all_curiosity_collision) / np.sqrt(len(all_curiosity_collision))
        self.curiosity_actiononto_sterror   = np.std(all_curiosity_actiononto) / np.sqrt(len(all_curiosity_actiononto))
        self.acknowledge_ticks_sterror      = np.std(all_acknowledge_ticks) / np.sqrt(len(all_acknowledge_ticks))
        self.interactions_ticks_sterror     = np.std(all_interactions_ticks) / np.sqrt(len(all_interactions_ticks))
        self.curiosityColl_ticks_sterror    = np.std(all_curiosityColl_ticks) / np.sqrt(len(all_curiosityColl_ticks))
        self.curiosityAct_ticks_sterror     = np.std(all_curiosityAct_ticks) / np.sqrt(len(all_curiosityAct_ticks))

    def isTie(self, gsu2):
        return self.total_sprites_ack_avg == gsu2.total_sprites_ack_avg \
        and self.total_interactions_avg   == gsu2.total_interactions_avg \
        and self.curiosity_collision_avg  == gsu2.curiosity_collision_avg \
        and self.curiosity_actiononto_avg == gsu2.curiosity_actiononto_avg \
        and self.acknowledge_ticks_avg    == gsu2.acknowledge_ticks_avg \
        and self.interactions_ticks_avg   == gsu2.interactions_ticks_avg \
        and self.curiosityColl_ticks_avg  == gsu2.curiosityColl_ticks_avg \
        and self.curiosityAct_ticks_avg   == gsu2.curiosityAct_ticks_avg


    def printData(self):
        print CONTROLLERS[self.controller_id] + ": "
        print
        print "total_sprites_ack: " +self.printTotalSpritesAcknowledge()
        print "total_interactions: "+self.printTotalInteractions()
        print "curiosity_collision: "+self.printCuriosityCollision()
        print "curiosity_actiononto: "+self.printCuriosityActionedonto()
        print "acknowledge_ticks: "+self.printTotalSpritesAcknowledgeGameticks()
        print "interactions_ticks: "+self.printTotalInteractionsGameticks()
        print "curiosityColl_ticks: "+self.printCuriosityCollisionGameticks()
        print "curiosityAct_ticks: "+self.printCuriosityActionedontoGameticks()
        print
        print "POINTS: "+self.printPoints()
        print "-------------"

    def getotalSpritesAcknowledge(self):
        return self.total_sprites_ack_avg

    def getTotalInteractions(self):
        return self.total_interactions_avg

    def getCuriosityCollision(self):
        return self.curiosity_collision_avg

    def getCuriosityActionedonto(self):
        return self.curiosity_actiononto_avg

    def gameName(self, game_id):
        return GAMES[game_id]

    def controllerName(self):
        return CONTROLLERS[self.controller_id]

    def isWinner(self):
        return self.points == F1_RANKING_POINTS[0]

    # Sprites Acknowledge
    def printTotalSpritesAcknowledge(self):
        return "%.2f" % (self.total_sprites_ack_avg) + " " + self.printTotalSpritesAcknowledgeErr()

    def printTotalSpritesAcknowledgeErr(self):
        return  "(" + "%.2f" % (self.total_sprites_ack_sterror) + ")"

    # Total unique interactions
    def printTotalInteractions(self):
        return "%.2f" % (self.total_interactions_avg) + " " + self.printTotalInteractionsErr()

    def printTotalInteractionsErr(self):
        return  "(" + "%.2f" % (self.total_interactions_sterror) + ")"

    # Collisions curiosity
    def printCuriosityCollision(self):
        return "%.2f" % (self.curiosity_collision_avg) + " " + self.printCuriosityCollisionErr()

    def printCuriosityCollisionErr(self):
        return  "(" + "%.2f" % (self.curiosity_collision_sterror) + ")"

    # Actioned-onto curiosity
    def printCuriosityActionedonto(self):
        return "%.2f" % (self.curiosity_actiononto_avg) + " " + self.printCuriosityActionedontoErr()

    def printCuriosityActionedontoErr(self):
        return  "(" + "%.2f" % (self.curiosity_actiononto_sterror) + ")"

    # Sprites acknowledge gameticks
    def printTotalSpritesAcknowledgeGameticks(self):
        return "%.2f" % (self.acknowledge_ticks_avg) + " " + self.printTotalSpritesAcknowledgeGameticksErr()

    def printTotalSpritesAcknowledgeGameticksErr(self):
        return  "(" + "%.2f" % (self.acknowledge_ticks_sterror) + ")"

     # Total unique interactions gameticks
    def printTotalInteractionsGameticks(self):
        return "%.2f" % (self.interactions_ticks_avg) + " " + self.printTotalInteractionsGameticksErr()

    def printTotalInteractionsGameticksErr(self):
        return  "(" + "%.2f" % (self.interactions_ticks_sterror) + ")"

    # Collisions curiosity gameticks
    def printCuriosityCollisionGameticks(self):
        return "%.2f" % (self.curiosityColl_ticks_avg) + " " + self.printCuriosityCollisionGameticksErr()

    def printCuriosityCollisionGameticksErr(self):
        return  "(" + "%.2f" % (self.curiosityColl_ticks_sterror) + ")"

    # Actioned-onto curiosity gameticks
    def printCuriosityActionedontoGameticks(self):
        return "%.2f" % (self.curiosityAct_ticks_avg) + " " + self.printCuriosityActionedontoGameticksErr()

    def printCuriosityActionedontoGameticksErr(self):
        return  "(" + "%.2f" % (self.curiosityAct_ticks_sterror) + ")"

    def printPoints(self):
        return str(self.points)

def gameKnowledgeDiscoveryUnitComparator(gkdu1, gkdu2):
    # The one with more sprites acknowledge goes first
    if gkdu1.total_sprites_ack_avg > gkdu2.total_sprites_ack_avg:
        return -1
    
    if gkdu1.total_sprites_ack_avg < gkdu2.total_sprites_ack_avg:
        return 1

    # If tie in sprites acknowledge, it is considered the total number of unique interactions with sprites
    if gkdu1.total_interactions_avg > gkdu2.total_interactions_avg:
        return -1

    if gkdu1.total_interactions_avg < gkdu2.total_interactions_avg:
        return 1

    # If tie in interaction, it is considered the number of collision curiosity
    if gkdu1.curiosity_collision_avg > gkdu2.curiosity_collision_avg:
        return -1

    if gkdu1.curiosity_collision_avg < gkdu2.curiosity_collision_avg:
        return 1

    # If tie in collision curiosity, it is considered the number of action-onto curiosity
    if gkdu1.curiosity_actiononto_avg > gkdu2.curiosity_actiononto_avg:
        return -1

    if gkdu1.curiosity_actiononto_avg < gkdu2.curiosity_actiononto_avg:
        return 1

    # If tie in everything, it is considered the gameticks

    # first the one that discovered the sprites first
    if gkdu1.acknowledge_ticks_avg < gkdu2.acknowledge_ticks_avg:
        return -1
    if gkdu1.acknowledge_ticks_avg > gkdu2.acknowledge_ticks_avg:
        return 1

    # If tie, it is considered the one that interacts with the sprites first
    if gkdu1.interactions_ticks_avg < gkdu2.interactions_ticks_avg:
        return -1
    if gkdu1.interactions_ticks_avg > gkdu2.interactions_ticks_avg:
        return 1

    # If tie, it is considered the one that achieved the collision curiosity first
    if gkdu1.curiosityColl_ticks_avg < gkdu2.curiosityColl_ticks_avg:
        return -1
    if gkdu1.curiosityColl_ticks_avg > gkdu2.curiosityColl_ticks_avg:
        return 1

     # If tie, it is considered the one that achieved the action-onto curiosity first
    if gkdu1.curiosityAct_ticks_avg < gkdu2.curiosityAct_ticks_avg:
        return -1
    if gkdu1.curiosityAct_ticks_avg > gkdu2.curiosityAct_ticks_avg:
        return 1
    
    # If still tie, just keep calm & carry on
    return 0

class StypeInformation:
    def __init__(self, collision_wins, collision_score, actiononto_wins, actiononto_score):
        self.collision_wins = collision_wins
        self.collision_score = collision_score
        self.actiononto_wins = actiononto_wins
        self.actiononto_score = actiononto_score

    def printCollisionWins(self):
        if self.collision_wins is not None:
            return "%.0f" % (self.collision_wins)
        return '-'

    def printCollisionScore(self):
        if self.collision_score is not None:
            return "%.0f" % (self.collision_score)
        return '-'

    def printActionontoWins(self):
        if self.actiononto_wins is not None:
            return "%.0f" % (self.actiononto_wins)
        return '-'

    def printActionontoScore(self):
        if self.actiononto_score is not None:
            return "%.0f" % (self.actiononto_score)
        return '-'

    def printData(self):
        if not LATEX_EXPORT:
            print "----Real:"
            print "Collisions: "+self.printCollisionWins()+" "+self.printCollisionScore()
            print "Actiononto: "+self.printActionontoWins()+" "+self.printActionontoScore()
        else:
            return self.printCollisionWins()+' & '+self.printCollisionScore()+' & '+self.printActionontoWins()+' & '+self.printActionontoScore()

class StypeEstimationStats:
    def __init__(self, all_collision_wins, all_collision_score, all_actiononto_wins, all_actiononto_score):
        self.n_collision_estimations = 0
        self.n_actiononto_estimations = 0

        if len(all_collision_wins) > 0:
            # there is estimation for both wins and score
            self.n_collision_estimations = 2

            # averages
            self.collision_wins_avg = self.getEstimationsAverage(all_collision_wins)
            self.collision_score_avg = self.getEstimationsAverage(all_collision_score)
            # Standard error
            self.collision_wins_sterror = self.getEstimationsStError(all_collision_wins)
            self.collision_score_sterror = self.getEstimationsStError(all_collision_score)
        else:
            # averages
            self.collision_wins_avg = None
            self.collision_score_avg = None
            # Standard error
            self.collision_wins_sterror = None
            self.collision_score_sterror = None

        if len(all_actiononto_wins) > 0:
            # there is estimation for both wins and score
            self.n_actiononto_estimations = 2

            # averages
            self.actiononto_wins_avg = self.getEstimationsAverage(all_actiononto_wins)
            self.actiononto_score_avg = self.getEstimationsAverage(all_actiononto_score)
            # Standard error
            self.actiononto_wins_sterror = self.getEstimationsStError(all_actiononto_wins)
            self.actiononto_score_sterror = self.getEstimationsStError(all_actiononto_score)
        else:
            # averages
            self.actiononto_wins_avg = None
            self.actiononto_score_avg = None
            # Standard error
            self.actiononto_wins_sterror = None
            self.actiononto_score_sterror = None

        self.collision_wins_sqerror = None
        self.collision_score_sqerror = None
        self.actiononto_wins_sqerror = None
        self.actiononto_score_sqerror = None

    def getNEstimations(self):
        return self.n_collision_estimations + self.n_actiononto_estimations

    def getNInteractionsEstimated(self):
        return self.getNEstimations()/2

    def getSumSqerrors(self):
        if self.getNEstimations() == 0:
            return None

        sqerror_sum = 0
        if self.n_collision_estimations > 0:
            sqerror_sum = sqerror_sum + self.collision_wins_sqerror + self.collision_score_sqerror
    
        if self.n_actiononto_estimations > 0:
            sqerror_sum = sqerror_sum + self.actiononto_wins_sqerror + self.actiononto_score_sqerror

        return sqerror_sum


    def setSqErrors(self, real_collision_wins, real_collision_score, real_actiononto_wins, real_actiononto_score):
        self.collision_wins_sqerror = self.getCollisionWinsMSE(real_collision_wins)
        self.collision_score_sqerror = self.getCollisionScoreMSE(real_collision_score)
        self.actiononto_wins_sqerror = self.getActionontoWinsMSE(real_actiononto_wins)
        self.actiononto_score_sqerror = self.getActionontoScoreMSE(real_actiononto_score)

    # Data average and sterror
    def getEstimationsAverage(self, all_estimations):
        return np.average(all_estimations)

    def getEstimationsStError(self, all_estimations):
        return np.std(all_estimations) / np.sqrt(len(all_estimations))

    # Mean Square Error (MSE)
    def getMSE(self, estimated, expected):
        "Returns the Mean Square Error: (X - u)^2"
        return (estimated - expected)**2

    def getCollisionWinsMSE(self, real_collision_wins):
        if self.collision_wins_avg is not None:
            return self.getMSE(self.collision_wins_avg, real_collision_wins)
        return None    

    def getCollisionScoreMSE(self, real_collision_score):
        if self.collision_score_avg is not None:
            return self.getMSE(self.collision_score_avg, real_collision_score)
        return None    

    def getActionontoWinsMSE(self, real_actiononto_wins):
        if self.actiononto_wins_avg is not None:
            return self.getMSE(self.actiononto_wins_avg, real_actiononto_wins)
        return None    

    def getActionontoScoreMSE(self, real_actiononto_score):
        if self.actiononto_score_avg is not None:
            return self.getMSE(self.actiononto_score_avg, real_actiononto_score)
        return None

    # Collision wins
    def printCollisionWinsEstimation(self):
        if self.n_collision_estimations > 0:
            return "%.2f" % (self.collision_wins_avg) + " " + self.printCollisionWinsStErr()
        return '-'

    def printCollisionWinsStErr(self):
        return  "(" + "%.2f" % (self.collision_wins_sterror) + ")"

    def printCollisionWinsSqError(self):
        if self.collision_wins_sqerror is not None:
            return "%.2E" % (self.collision_wins_sqerror)
        return '-'

    # Collision score
    def printCollisionScoreEstimation(self):
        if self.n_collision_estimations > 0:
            return "%.2f" % (self.collision_score_avg) + " " + self.printCollisionScoreStErr()
        return '-'

    def printCollisionScoreStErr(self):
        return  "(" + "%.2f" % (self.collision_score_sterror) + ")"

    def printCollisionScoreSqError(self):
        if self.collision_score_sqerror is not None:
            return "%.2E" % (self.collision_score_sqerror)
        return '-'

    # Actiononto wins
    def printActionontoWinsEstimation(self):
        if self.n_actiononto_estimations > 0:
            return "%.2f" % (self.actiononto_wins_avg) + " " + self.printActionontoWinsStErr()
        return '-'

    def printActionontoWinsStErr(self):
        return  "(" + "%.2f" % (self.actiononto_wins_sterror) + ")"

    def printActionontoWinsSqError(self):
        if self.actiononto_wins_sqerror is not None:
            return "%.2E" % (self.actiononto_wins_sqerror)
        return '-'
        
    # Actiononto score
    def printActionontoScoreEstimation(self):
        if self.n_actiononto_estimations > 0:
            return "%.2f" % (self.actiononto_score_avg) + " " + self.printActionontoScoreStErr()
        return '-'

    def printActionontoScoreStErr(self):
        return  "(" + "%.2f" % (self.actiononto_score_sterror) + ")"

    def printActionontoScoreSqError(self):
        if self.actiononto_score_sqerror is not None:
            return "%.2E" % (self.actiononto_score_sqerror)
        return '-'

    def printEstimations(self):
        if not LATEX_EXPORT:
            print "----Estimations:"
            print "Collisions: "+self.printCollisionWinsEstimation()+" "+self.printCollisionScoreEstimation()
            print "Actiononto: "+self.printActionontoWinsEstimation()+" "+self.printActionontoScoreEstimation()
        else:
            return self.printCollisionWinsEstimation()+' & '+self.printCollisionScoreEstimation()+' & '+self.printActionontoWinsEstimation()+' & '+self.printActionontoScoreEstimation()
 
    def printSqErros(self):
        if not LATEX_EXPORT:
            print "----SqErrors:"
            print "Collisions: "+self.printCollisionWinsSqError()+" "+self.printCollisionScoreSqError()
            print "Actiononto: "+self.printActionontoWinsSqError()+" "+self.printActionontoScoreSqError()
        else:
            return self.printCollisionWinsSqError()+' & '+self.printCollisionScoreSqError()+' & '+self.printActionontoWinsSqError()+' & '+self.printActionontoScoreSqError()

class StypeEstimations:
    """Estimations for a certain stype"""
    def __init__(self, stype, real_stype_info_data):
        self.stype = stype
        
        # Estimations
        self.collision_wins = []
        self.collision_score = []
        self.actiononto_wins = []
        self.actiononto_score = []

        # Real data
        self.collision_wins_real = real_stype_info_data.collision_wins
        self.collision_score_real = real_stype_info_data.collision_score
        self.actiononto_wins_real = real_stype_info_data.actiononto_wins
        self.actiononto_score_real = real_stype_info_data.actiononto_score

        self.stats = None
    
    def isInteractionEstimed(self, int_type):
        if int_type == INT_COLLISION:
            return self.isCollisionEstimed()
        if int_type == INT_ACTIONONTO:
            return self.isActionontoEstimed()
        return None

    def isCollisionEstimed(self):
        return self.collision_wins

    def isActionontoEstimed(self):
        return self.actiononto_wins

    def addInteractionEstimations(self, int_type, wins, score):
        if int_type == INT_COLLISION:
            self.addCollisionEstimations(wins, score)
        elif int_type == INT_ACTIONONTO:
            self.addActionontoEstimations(wins, score)

    def addCollisionEstimations(self, wins, score):
        self.collision_wins.append(wins)
        self.collision_score.append(score)

    def addActionontoEstimations(self, wins, score):
        self.actiononto_wins.append(wins)
        self.actiononto_score.append(score)

    def getNStypeEstimations(self):
        return self.stats.getNEstimations()

    def getNStypeInteractionsEstimated(self):
        return self.stats.getNInteractionsEstimated()

    def getStypeTotalSqerror(self):
        return self.stats.getSumSqerrors()

    def setStats(self):
        """
        The average and Standard error are calculated using the stored data and set onto the class
        """
        self.stats = StypeEstimationStats(self.collision_wins, self.collision_score, self.actiononto_wins, self.actiononto_score)
        self.stats.setSqErrors(self.collision_wins_real, self.collision_score_real, self.actiononto_wins_real, self.actiononto_score_real)
    
class GameKnowledgeEstimationUnit:

    def __init__(self, controller_id, controller_estimations, real_stype_info_data):
        self.controller_id = controller_id
        self.points = None

        # estimations
        self.estimations = controller_estimations
        self.real_stypes_info = real_stype_info_data
        
        # Game stypes encounters but every controller
        self.all_controllers_stype_estimations = None
        
        # Ranking data
        self.n_total_interactions_estimed = 0
        self.n_total_sqerror_estimations = 0

        self.missed_estimations = {}
        self.missed_n_total_interactions_estimed = 0
        self.missed_n_total_sqerror_estimations = 0

        # It is set the stats for the estimations of every stype interaction
        for stype, stype_estimations in self.estimations.items():
            stype_estimations.setStats()
            self.n_total_interactions_estimed = self.n_total_interactions_estimed + stype_estimations.getNStypeInteractionsEstimated()
            self.n_total_sqerror_estimations = self.n_total_sqerror_estimations + stype_estimations.getStypeTotalSqerror()
        

    def setStats(self, all_controllers_stype_estimations):
        self.all_controllers_stype_estimations = all_controllers_stype_estimations

        default_win_estimation = 0
        default_score_estimation = 0
        for game_stype, stype_ints in all_controllers_stype_estimations.items():
            for int_type in stype_ints:  

                is_missed = False              
                if game_stype not in self.estimations:
                    is_missed = True
                else:
                    # It is checked if the interaction consiered has been considered as well
                    if not self.estimations[game_stype].isInteractionEstimed(int_type):
                        is_missed = True

                if is_missed:
                    # This controller has missed a stype estimated by another, set the default values for Stype
                    if game_stype not in self.missed_estimations:
                        self.missed_estimations[game_stype] = StypeEstimations(game_stype, self.real_stypes_info[game_stype])
                    
                    self.missed_estimations[game_stype].addInteractionEstimations(int_type, default_win_estimation, default_score_estimation)

        for missed_stype, miss_stype_estimations in self.missed_estimations.items():
            miss_stype_estimations.setStats()
            self.missed_n_total_interactions_estimed = miss_stype_estimations.getNStypeInteractionsEstimated()
            self.missed_n_total_sqerror_estimations = miss_stype_estimations.getStypeTotalSqerror()

    def getNInteractionsEstimated(self):
        return self.n_total_interactions_estimed

    def getPerformanceSqerrorEstimedAvg(self):
        return self.getSqerrorEstimedAverage()

    def gameName(self, game_id):
        return GAMES[game_id]

    def controllerName(self):
        return CONTROLLERS[self.controller_id]

    def isWinner(self):
        return self.points == F1_RANKING_POINTS[0]

    def getPerformanceSqerrorEstimedAverage(self):
        return self.n_total_sqerror_estimations/(self.n_total_interactions_estimed*2)

    def getComparableSqerrorEstimatedAverage(self):
        comparable_n_total_sqerror_estimations = self.n_total_sqerror_estimations + self.missed_n_total_sqerror_estimations
        comparable_n_total_interactions_estimed = self.n_total_interactions_estimed + self.missed_n_total_interactions_estimed
        return comparable_n_total_sqerror_estimations/(comparable_n_total_interactions_estimed*2)

    def printEstimationTable(self):
        if not LATEX_EXPORT:

            print "ESTIMATIONS "+CONTROLLERS[self.controller_id]+" (total interactions: "+str(self.n_total_interactions_estimed)+")"
            print "sqerror sum "+str(self.n_total_sqerror_estimations)
            print "sqerror average (total estimations): "+str(self.getSqerrorEstimedAverage())
            for stype, stype_estimations in self.estimations.items():
                print
                print "STYPE "+str(stype)
                self.real_stypes_info[stype].printData()
                stype_estimations.stats.printEstimations()
                stype_estimations.stats.printSqErros()
            print "-------------------------------------------------------------"

        else:
            for stype, stype_estimations in self.estimations.items():
                print '\hline'
                print boldify(str(stype)) + ' & ' + self.real_stypes_info[stype].printData() + ' & ' + stype_estimations.stats.printEstimations() + ' & ' +stype_estimations.stats.printSqErros()
                print ' \\\\'

    def isTie(self, gkeu2):
        return self.getComparableSqerrorEstimatedAverage() == gkeu2.getComparableSqerrorEstimatedAverage() \
        and self.n_total_interactions_estimed == gkeu2.n_total_interactions_estimed

    def printComparableSqErrorEstimatedAvg(self):
        return "%.2E" % (self.getComparableSqerrorEstimatedAverage())

    def printNInteractionsEstimed(self):
        return str(self.n_total_interactions_estimed)

    def printSqerrorEstimedAvg(self):
        return "BLue"
        # return "%.2E" % (self.getSqerrorEstimedAverage())

    def printPoints(self):
        return str(self.points)

    def printData(self):
        print CONTROLLERS[self.controller_id] + ": "
        print
        print "comparable_sqerror_estimed_avg: "+self.printComparableSqErrorEstimatedAvg()
        print "n_total_interactions_estimed: "+ self.printNInteractionsEstimed()
        print "total_sqerror_estimed_avg: "+self.printSqerrorEstimedAvg()
        print
        print "POINTS: "+self.printPoints()
        print "-------------"

def gameKnowledgeEstimationUnitComparator(gkeu1, gkeu2):
    # It is needed to calculate teh SqErrorEstimated considering the missing values
    # If tie, give preference to the one more accurated 
    if gkeu1.getComparableSqerrorEstimatedAverage() < gkeu2.getComparableSqerrorEstimatedAverage():
        return -1
    
    if gkeu1.getComparableSqerrorEstimatedAverage() > gkeu2.getComparableSqerrorEstimatedAverage():
        return 1

    # The there is a tie in the estimation (very unprobably) it is considered it performs better the one that
    # has been capable of estimating more
    if gkeu1.n_total_interactions_estimed > gkeu2.n_total_interactions_estimed:
        return -1
    
    if gkeu1.n_total_interactions_estimed < gkeu2.n_total_interactions_estimed:
        return 1

    # Still tie (yeah sure), just keep calm & carry on
    return 0


# def gameKnowledgeEstimationUnitComparatorNInteractionsPriority(gkeu1, gkeu2):
#     # The one with more interactions estimed goes first
#     if gkeu1.n_total_interactions_estimed > gkeu2.n_total_interactions_estimed:
#         return -1
    
#     if gkeu1.n_total_interactions_estimed < gkeu2.n_total_interactions_estimed:
#         return 1

#     # If tie, give preference to the one more accurated 
#     if gkeu1.getSqerrorEstimedAverage() < gkeu2.getSqerrorEstimedAverage():
#         return -1
    
#     if gkeu1.getSqerrorEstimedAverage() > gkeu2.getSqerrorEstimedAverage():
#         return 1
    
#     # If still tie, just keep calm & carry on
#     return 0

# def gameKnowledgeEstimationUnitComparatorAccuracyPriority(gkeu1, gkeu2):
#     # The one more accurate goes first
#     if gkeu1.getSqerrorEstimedAverage() < gkeu2.getSqerrorEstimedAverage():
#         return -1
    
#     if gkeu1.getSqerrorEstimedAverage() > gkeu2.getSqerrorEstimedAverage():
#         return 1
    
#     # If tie, give preference to the one with more interactions
#     if gkeu1.n_total_interactions_estimed > gkeu2.n_total_interactions_estimed:
#         return -1
    
#     if gkeu1.n_total_interactions_estimed < gkeu2.n_total_interactions_estimed:
#         return 1
    
#     # If still tie, just keep calm & carry on
#     return 0


"""
PRINTING
"""

def printGlobalRanking():
	controllers_total_points.sort(globalRankingUnitComparator)

	if LATEX_EXPORT:
		latexTableGlobalRankings(EXPERIMENTS[ID_EXP], controllers_total_points)
	else:
		print
		print "RANKING"
		print
		for i in range(0, len(CONTROLLERS)):
			gr = controllers_total_points[i]
			print str(i+1) + ")" + CONTROLLERS[gr.controller_id] + " " + str(gr.points)
	
	print

def printGameResults(game_id, gu_game):

	if LATEX_EXPORT:
		latexTableGameRankings(GAMES[game_id], gu_game)
	else:
		print
		print "Results "+GAMES[game_id]
		print
		for gu in gu_game:
			gu.printData()

		printGlobalRanking()

def printTotalRankingBigTable():
    if LATEX_EXPORT:
        latexBigTableAllGamesRanking(EXPERIMENTS[ID_EXP], controllers_total_rankings, gameUnitComparatorByController)
    else:
        pass

def printHeuristicSummaryTable():
    if LATEX_EXPORT:
        pass
        latexHeuristicSummaryTable(EXPERIMENTS[ID_EXP], controllers_total_rankings, gameUnitComparatorByController, games_highest_for_relative_summary)
    else:
        pass

"""
INIT GLOBAL VARS
"""
# Intialize the global var that will contain the total number of points of each controller
controllers_total_points = [GlobalRankingUnit(i) for i in range(len(CONTROLLERS))]
controllers_total_rankings = [[] for i in range(len(GAMES))]
games_highest_for_relative_summary = [[] for i in range(len(GAMES))]
games_stype_info_data = [[] for i in range(len(GAMES))]

if ID_EXP == MAXSCORE_ID:
    gameUnitComparator      = gameScoreUnitComparator
    latexTableGameRankings = latexTableGameScoreRankings
    latexBigTableAllGamesRanking = latexBigTableAllGamesScoreRanking
    latexHeuristicSummaryTable = latexHeuristicSummaryTableMSH

elif ID_EXP == MAXEXPL_ID:
    gameUnitComparator  = gameExplorationUnitComparator
    latexTableGameRankings 	= latexTableGameExplorationRankings
    latexBigTableAllGamesRanking = latexBigTableAllGamesExplorationRanking
    latexHeuristicSummaryTable = latexHeuristicSummaryTableMEH

elif ID_EXP == KNW_DISCOVERY_ID:
    gameUnitComparator      = gameKnowledgeDiscoveryUnitComparator
    latexTableGameRankings  = latexTableGameKnowledgeDiscoveryRankings
    latexHeuristicSummaryTable  = latexHeuristicSummaryTableKD

elif ID_EXP == KNW_ESTIMATION_ID and ESTIMATION_PRIORITY == PRIORITY_INTERACTIONS:
    gameUnitComparator = gameKnowledgeEstimationUnitComparator
    latexTableGameRankings  = latexTableGameKnowledgeEstimationRankings
    # latexHeuristicSummaryTable  = latexHeuristicSummaryTableKEOLD
    latexHeuristicSummaryTable  = latexHeuristicSummaryTableKE

# elif ID_EXP == KNW_ESTIMATION_ID and ESTIMATION_PRIORITY == PRIORITY_INTERACTIONS:
#     gameUnitComparator = gameKnowledgeEstimationUnitComparatorNInteractionsPriority
# elif ID_EXP == KNW_ESTIMATION_ID and ESTIMATION_PRIORITY == PRIORITY_ACCURACY:
#     gameUnitComparator = gameKnowledgeEstimationUnitComparatorAccuracyPriority
else:
	print "ERROR valfunction_helper: not valid heuristic ID provided"
	exit()