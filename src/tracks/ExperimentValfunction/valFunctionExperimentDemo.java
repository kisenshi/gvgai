package tracks.ExperimentValfunction;

import tracks.ArcadeMachine;

import java.util.Random;

/**
 * Created by Cristina on 07/04/2017.
 */
public class valFunctionExperimentDemo {

    public static void main(String[] args) {
        // SETUP

        // PATHS
        String gamesPath = "examples/valFunction/";
        String heuristicsPath = "ExperimentValfunction.ValFunctions.";
        String controllersPath = "ExperimentValfunction.controllers.";

        // EXPERIMENT SETUP

        //All available games:
        String games[] = new String[]{};

        // HEURISTICS

        String heuristics_experiment[] = new String[]{
                "MaximizeScoreHeuristic",       //0
                "MaximizeExplorationHeuristic", //1
                "KnowledgeDiscoveryHeuristic",  //2
                "KnowledgeEstimationHeuristic", //3
                //"DataPrintingPlayer",           //4
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
        String level1 = gamesPath + gameName + "_lvl" + level_idx + ".txt";

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
        boolean visuals = true;
        int seed;

        int n_games = 20;

        String actionFile = null; //controller+"_actions_" + games[gameIdx] + "_lvl" + levelIdx + "_" + seed + ".txt";
        String resultsHeuristicFile = "ExperimentValFunction_results_" + heuristicName + "_" + gameName + ".txt";

        // SUPERVISORY BOARD DEMO
        // The game provided is run once per each controller

        for (heuristic_id = 0; heuristic_id < heuristics_experiment.length; heuristic_id++) {
            seed = new Random().nextInt();

            heuristicName = heuristics_experiment[heuristic_id];
            heuristic = heuristicsPath + heuristicName;

            resultsHeuristicFile = "ExperimentValFunction_results_" + heuristicName + "_" + gameName + ".txt";

            System.out.println("Running : " + heuristicName + " in " + gameName + " by " + controllerName + " seed " + seed);

            ArcadeMachine.runOneGameUsingHeuristic(game, level1, visuals, controller, actionFile, seed, 0, heuristic, resultsHeuristicFile, recordIds);
        }

    }
}
