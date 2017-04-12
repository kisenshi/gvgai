package tracks.ExperimentValfunction;

import java.util.Random;

import tracks.ArcadeMachine;

/**
 * Created by kisenshi on 03/03/17.
 * Args provided MUST BE
 * 0: heuristicId
 * 1: gameId
 * 2: controllerId
 */
public class valFunctionExperiment {
    public static void main(String[] args)
    {
        // SETUP

        // PATHS
        String gamesPath = "examples/valFunction/";
        String heuristicsPath = "tracks.ExperimentValfunction.heuristics.";
        String controllersPath = "tracks.ExperimentValfunction.controllers.";

        // EXPERIMENT SETUP

        //All available games:
        String games[] = new String[]{};

        //All public games
        /*games = new String[]{"aliens", "angelsdemons", "assemblyline", "avoidgeorge", "bait", //0-4
                "blacksmoke", "boloadventures", "bomber", "boulderchase", "boulderdash",      //5-9
                "brainman", "butterflies", "cakybaky", "camelRace", "catapults",              //10-14
                "chainreaction", "chase", "chipschallenge", "clusters", "colourescape",       //15-19
                "chopper", "cookmepasta", "cops", "crossfire", "defem",                       //20-24
                "defender", "digdug", "dungeon", "eggomania", "enemycitadel",                 //25-29
                "escape", "factorymanager", "firecaster",  "fireman", "firestorms",           //30-34
                "freeway", "frogs", "gymkhana", "hungrybirds", "iceandfire",                  //35-39
                "infection", "intersection", "islands", "jaws", "labyrinth",                  //40-44
                "labyrinthdual", "lasers", "lasers2", "lemmings", "missilecommand",           //45-49
                "modality", "overload", "pacman", "painter", "plants",                        //50-54
                "plaqueattack", "portals", "racebet", "raceBet2", "realportals",              //55-59
                "realsokoban", "rivers", "roguelike", "run", "seaquest",                      //60-64
                "sheriff", "shipwreck", "sokoban", "solarfox" ,"superman",                    //65-69
                "surround", "survivezombies", "tercio", "thecitadel", "thesnowman",           //70-74
                "waitforbreakfast", "watergame", "waves", "whackamole", "witnessprotection",  //75-79
                "zelda", "zenpuzzle" };
        */

        // HEURISTICS

        String heuristics_experiment[] = new String[]{
            "MaximizeScoreHeuristic",       //0
            "MaximizeExplorationHeuristic", //1
            "KnowledgeDiscoveryHeuristic",  //2
            "KnowledgeEstimationHeuristic", //3
            "DataPrintingPlayer",           //4
        };

        int heuristic_id = Integer.parseInt(args[0]); //0;
        String heuristicName = heuristics_experiment[heuristic_id];
        String heuristic = heuristicsPath + heuristicName;

        // GAMES

        String games_experiment[] = new String[]{
            "aliens",           //0
            "bait",             //1
            "butterflies",      //2
            "camelRace",        //3
            "chase",            //4
            "chopper",          //5
            "crossfire",        //6
            "digdug",           //7
            "escape",           //8
            "hungrybirds",      //9
            "infection",        //10
            "intersection",     //11
            "lemmings",         //12
            "missilecommand",   //13
            "modality",         //14
            "plaqueattack",     //15
            "roguelike",        //16
            "seaquest",         //17
            "survivezombies",   //18
            "waitforbreakfast"  //19
        };

        //Game and level to play
        int level_idx = 0; // This experiment runs just for the first level
        int game_id = Integer.parseInt(args[1]); //2

        String gameName = games_experiment[game_id];
        String game = gamesPath + gameName + ".txt";
        String level1 = gamesPath + gameName + "_lvl" + level_idx +".txt";

        // CONTROLLERS

        String controllers_experiment[] = new String[]{
            "olets",                    //0
            "sampleOLMCTS",             //1
            "sampleonesteplookahead",   //2
            "sampleRHEA",               //3
            "sampleRS",                 //4
        };

        int controller_id = Integer.parseInt(args[2]); //5

        String controllerName = controllers_experiment[controller_id];
        String controller = controllersPath + controllerName + ".Agent";

        // As the data is appended at the end of the file, it is needed to store the game and controllers id
        int[] recordIds = new int[]{
                game_id,
                controller_id,
        };

        // OTHER SETTINGS
        boolean visuals = false;
        int seed;

        int n_games = 20;

        String actionFile = null; //controller+"_actions_" + games[gameIdx] + "_lvl" + levelIdx + "_" + seed + ".txt";
        String resultsHeuristicFile = "ExperimentValFunction_results_"+heuristicName+"_"+gameName+".txt";

        // TESTS

        // Execute each game once with the heuristic provided
//        for (game_id=0; game_id<games_experiment.length; game_id++){
//            seed = new Random().nextInt();
//
//            gameName = games_experiment[game_id];
//            game = gamesPath + gameName + ".txt";
//            level1 = gamesPath + gameName + "_lvl" + level_idx +".txt";
//
//            recordIds = new int[]{
//                game_id,
//                controller_id,
//            };
//
//            resultsHeuristicFile = "ExperimentValFunction_results_"+heuristicName+"_"+gameName+".txt";
//
//            System.out.println("Running: "+heuristicName+" in "+gameName+" by "+controllerName+" seed "+seed);
//            ArcadeMachine.runOneGameUsingHeuristic(game, level1, visuals, controller, actionFile, seed, 0, heuristic, resultsHeuristicFile, recordIds);
//        }

        // This plays a game in a level by the controller using a certain heuristic
        //ArcadeMachine.runOneGameUsingHeuristic(game, level1, visuals, controller, actionFile, seed, 0, maximizeScoreHeuristic, recordMaximizeScoreFile);
        //ArcadeMachine.runOneGameUsingHeuristic(game, level1, visuals, controller, actionFile, seed, 0, maximizeExplorationHeuristic, recordMaximizeExplorationFile);

//        seed = new Random().nextInt();
//        System.out.println("Running: "+heuristicName+" in "+gameName+" by "+controllerName+" seed "+seed);
//        ArcadeMachine.runOneGameUsingHeuristic(game, level1, visuals, controller, actionFile, seed, 0, heuristic, resultsHeuristicFile, recordIds);

        /*
        game_id = 12; //lemmings
        for (int i=0; i<controllers_experiment.length; i++){
            seed = new Random().nextInt();

            controllerName = controllers_experiment[i];
            controller = controllersPath + controllerName + ".Agent";

            recordIds = new int[]{
                    game_id,
                    i,
            };

            System.out.println("Running "+i+": "+heuristicName+" in "+gameName+" by "+controllerName+" seed "+seed);
            ArcadeMachine.runOneGameUsingHeuristic(game, level1, visuals, controller, actionFile, seed, 0, heuristic, resultsHeuristicFile, recordIds);
        }*/

        // EXPERIMENT

       for (int i=0; i<n_games; i++){
            seed = new Random().nextInt();
            System.out.println("Running "+i+": "+heuristicName+" in "+gameName+" by "+controllerName+" seed "+seed);
            ArcadeMachine.runOneGameUsingHeuristic(game, level1, visuals, controller, actionFile, seed, 0, heuristic, resultsHeuristicFile, recordIds);
       }
    }
}
