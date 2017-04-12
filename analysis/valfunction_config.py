__author__ = 'cris'

N_RESULTS = 20 		#Number of results for each controller in each game

# DEBUG TODO REMOVE
# N_RESULTS = 2 		#Number of results for each controller in each game

EXPERIMENTS = {
	1 : "MaximizeScoreHeuristic", 
	2 : "MaximizeExplorationHeuristic",
	3 : "KnowledgeDiscoveryHeuristic",
	4 : "KnowledgeEstimationHeuristic",
}

GAMES = (
	"aliens",           #0
	"bait",             #1
	"butterflies",      #2
	"camelRace",        #3
	"chase",            #4
	"chopper",          #5
	"crossfire",        #6
	"digdug",           #7
	"escape",           #8
	"hungrybirds",      #9
	"infection",        #10
	"intersection",     #11
	"lemmings",         #12
	"missilecommand",   #13
	"modality",         #14
	"plaqueattack",     #15
	"roguelike",        #16
	"seaquest",         #17
	"survivezombies",   #18
	"waitforbreakfast"  #19
	)

# DEBUG TODO REMOVE
# GAMES = (
# 	"infection",
# 	)

DETERMINISTIC_GAMES = (
	"bait",             #1
	"camelRace",        #3
	"chase",            #4
	"escape",           #8
	"hungrybirds",      #9
	"lemmings",         #12
	"missilecommand",   #13
	"modality",         #14
	"plaqueattack",     #15
	"waitforbreakfast"  #19
	)

STOCHASTIC_GAMES = (
	"aliens",           #0
	"butterflies",      #2
	"chopper",          #5
	"crossfire",        #6
	"digdug",           #7
	"infection",        #10
	"intersection",     #11
	"roguelike",        #16
	"seaquest",         #17
	"survivezombies",   #18
	)

CONTROLLERS = (
	"olets",                    #0
	"sampleOLMCTS",             #1
	"sampleonesteplookahead",   #2
	"sampleRHEA",               #3
	"sampleRS",                 #4
	)


MAXSCORE_ID = 1
MAXEXPL_ID = 2
KNW_DISCOVERY_ID = 3
KNW_ESTIMATION_ID = 4

PRIORITY_INTERACTIONS = 0
PRIORITY_ACCURACY = 1

# ID_EXP = MAXSCORE_ID
# ID_EXP = MAXEXPL_ID
# ID_EXP = KNW_DISCOVERY_ID
ID_EXP = KNW_ESTIMATION_ID

ESTIMATION_PRIORITY = PRIORITY_INTERACTIONS

INT_COLLISION = 0
INT_ACTIONONTO = 1

LATEX_EXPORT = True

# Ranking 

F1_RANKING_POINTS = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

# If there are more than 10 controllers, add 0 to have the same number of points as controllers
if len(CONTROLLERS) > 10:
	for x in range(0,(len(CONTROLLERS) - 10)):
		F1_RANKING_POINTS.append(0)