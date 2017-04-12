__author__ = 'dperez'


all_result_dirs = []
ALG_NAMES = []
ALG_NAMES_LETTER = []
F1_RANKING_POINTS = []
alg_index = []

ALL_GAMES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
# pop_size1 = [1, 2, 5, 10, 20]
# ind_length1 = [6, 8, 10, 14, 20]

pop_size1 = [5]
ind_length1 = [10]
init_type = ["A-Vanilla", "B-1SLA-S", "C-MCTS-S"]
# pop_size1 = [1, 20]
# ind_length1 = [6]

sim_depth = [6, 8, 10, 12, 14, 16]


F1_RANKING_POINTS_BASE = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1, 0]

idx = 0
counter = 65  #'A'
for p in range(len(pop_size1)) :
    #for j in ind_length1 :
    for k in range(2):

        i = pop_size1[p]
        j = ind_length1[p]

        if k == 1 :
            k = 2 #Vanilla & MCTS seedings only

        d = "results_900_" + str(k) + "_" + str(i) + "_" + str(j)

        all_result_dirs.append(d)
        ALG_NAMES.append(init_type[k])
        ALG_NAMES_LETTER.append(chr(counter))
        counter += 1

        if counter == 91:
            counter = 97  # Jump to 'a'

        if idx <+ 10:
            F1_RANKING_POINTS.append(F1_RANKING_POINTS_BASE[idx])
        else:
            F1_RANKING_POINTS.append(0)

        idx += 1

##for i in sim_depth :
##    d = "results_OLMCTS_900_" + str(i)
##    all_result_dirs.append(d)
##    ALG_NAMES.append("OLMCTS-" + str(i))
##    ALG_NAMES_LETTER.append(chr(counter))
##    counter += 1
##
##    if counter == 91:
##        counter = 97  # Jump to 'a'
##
##    if idx <+ 10:
##        F1_RANKING_POINTS.append(F1_RANKING_POINTS_BASE[idx])
##    else:
##        F1_RANKING_POINTS.append(0)
##
##    idx += 1
    


alg_index = [0, 1] #1-6
##alg_index = [2, 3, 13] #2-8
##alg_index = [4, 5, 14] #5-10
##alg_index = [6, 7, 15] #7-12
##alg_index = [8, 9, 16] #10-14
##alg_index = [10, 11, 17] #13-16

##for i in range(len(result_dirs)) : #all
##    alg_index.append(i)

N_ALG = len(all_result_dirs)


# all_result_dirs = ['T480', 'T960', 'T1440', 'T1920', 'TMCTS480']
# N_ALG = len(all_result_dirs)
# F1_RANKING_POINTS = F1_RANKING_POINTS[0:N_ALG]
# ALG_NAMES_LETTER = ALG_NAMES_LETTER[0:N_ALG]
# ALG_NAMES = ['T480', 'T960', 'T1440', 'T1920', 'TMCTS480']


#GAME_NAMES = ["Aliens", "Bait", "Butterflies", "Camel Race", "Chase", "Chopper", "Crossfire", "DigDug", "Escape", "Hungry Birds", "Infection", "Intersection", "Lemmings", "Missile Command", "Modality", "Plaque Attack", "Roguelike", "Seaquest", "Survive Zombies", "Wait For Breakfast"]

GAME_NAMES = [0, 4, 13, 15, 18, 22, 25, 29, 36, 46, 49, 50, 58, 60, 61, 67, 75, 77, 84, 91]  #All games
# GAME_NAMES = [0, 13, 22, 25, 29, 49, 50, 75, 77, 84] # Stochastic
# GAME_NAMES = [4, 15, 18, 36, 46, 58, 60, 61, 67, 91] #Deterministic

# GAME_NAMES = ["aliens", "bait", "blacksmoke", "boloadventures", "boulderchase",              # 0-4
#                 "boulderdash", "brainman", "butterflies", "cakybaky", "camelRace",     # 5-9
#                 "catapults", "chase", "chipschallenge", "chopper", "cookmepasta",        # 10-14
#                 "crossfire", "defem", "defender", "digdug", "eggomania",           # 15-19
#                 "enemycitadel", "escape", "factorymanager", "firecaster",  "firestorms",   # 20-24
#                 "frogs", "gymkhana", "hungrybirds", "iceandfire", "infection",    # 25-29
#                 "intersection", "jaws", "labyrinth", "lasers", "lasers2",        # 30-34
#                 "lemmings", "missilecommand", "modality", "overload", "pacman",             # 35-39
#                 "painter", "plants", "plaqueattack", "portals", "raceBet2",         # 40-44
#                 "realportals", "realsokoban", "roguelike", "seaquest", "sheriff",      # 45-49
#                 "sokoban", "solarfox" ,"superman", "surround", "survivezombies", # 50-54
#                 "tercio", "thecitadel", "waitforbreakfast", "watergame", "whackamole", # 55-59
#                 "zelda", "zenpuzzle", # 60-61
#                 "angelsdemons", "assemblyline", "avoidgeorge", "bomber", "chainreaction", # 62-26
#                 "clusters", "colourescape", "cops", "dungeon", "fireman", # 67-71
#                 "freeway", "islands", "labyrinthdual", "racebet",  "rivers",   # 72-76
#                 "run", "shipwreck", "thesnowman", "waves", "witnessprotection"]


NUM_GAMES = len(GAME_NAMES)
NUM_LEVELS = 5
REPS = 20 * NUM_LEVELS
SIGNIFICANCE_P_VALUE = 0.05

G = NUM_GAMES + 1

all_victories = [[] for i in range(N_ALG)]
overallVictories = [[] for i in range(N_ALG)]
overallScores = [[] for i in range(N_ALG)]
overallTimes = [[] for i in range(N_ALG)]

# all_victories = [[] for i in range(N_ALG-1)]
# overallVictories = [[] for i in range(N_ALG-1)]
# overallScores = [[] for i in range(N_ALG-1)]
# overallTimes = [[] for i in range(N_ALG-1)]

games_repetitions = [REPS for i in range(NUM_GAMES)]

all_scores_avg = [[] for i in range(NUM_GAMES)]
all_scores_stErr = [[] for i in range(NUM_GAMES)]

all_victories_avg = [[] for i in range(NUM_GAMES)]
all_victories_stErr = [[] for i in range(NUM_GAMES)]

all_timesteps_avg = [[] for i in range(NUM_GAMES)]
all_timesteps_stErr = [[] for i in range(NUM_GAMES)]
