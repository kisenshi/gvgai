package DreamTeam;

import tracks.ArcadeMachine;

import java.util.Random;

/**
 * Created by Cristina on 18/05/2017.
 */
public class TestCris {

    public static void main(String[] args) {
        // Available tracks:
        //String dreamTeamAgent = "DreamTeam.Agent";
        String dreamTeamRSAgent = "DreamTeam.RS.Agent";
        String dreamTeamMCTSAgent = "DreamTeam.Agent";


        String humanController = "tracks.multiPlayer.tools.human.Agent";


        // Set here the tracks used in the games (need 2 separated by space).
        String controllers = dreamTeamMCTSAgent + " " + dreamTeamMCTSAgent;
        // String tracks = sampleMCTSController + " " + sampleMCTSController;

        // Available games:
        String gamesPath = "examples/DreamTeam/";


        // Other settings
        boolean visuals = true;
        int seed = new Random().nextInt();

        // Game and level to play
        int levelIdx = 0; // level names from 0 to 4 (game_lvlN.txt).
        String game = gamesPath + "dreamgame.txt";
        String level1 = gamesPath + "dreamgame_lvl" + levelIdx + ".txt";

        String recordActionsFile = null;// "actions_" + games[gameIdx] + "_lvl"
        // + levelIdx + "_" + seed + ".txt";
        // //where to record the actions
        // executed. null if not to save.

        // 1. This starts a game, in a level, played by two humans.
        //ArcadeMachine.playOneGameMulti(game, level1, recordActionsFile, seed);

        // 2. This plays a game in a level by the tracks. If one of the
        // players is human, change the playerID passed
        // to the runOneGame method to be that of the human player (0 or 1).
	ArcadeMachine.runOneGame(game, level1, visuals, controllers, recordActionsFile, seed, 0);

        // 3. This replays a game from an action file previously recorded
        // String readActionsFile = recordActionsFile;
        // ArcadeMachine.replayGame(game, level1, visuals, readActionsFile);

        // 4. This plays a single game, in N levels, M times :
//	String level2 = gamesPath + games[gameIdx] + "_lvl" + 1 +".txt";
//	int M = 3;
//	for(int i=0; i<games.length; i++){
//         game = gamesPath + games[i] + ".txt";
//         level1 = gamesPath + games[i] + "_lvl" + levelIdx +".txt";
//         ArcadeMachine.runGames(game, new String[]{level1}, M, controllers, null);
//	}

        // 5. This plays N games, in the first L levels, M times each. Actions to file optional (set saveActions to true).
//	 int N = 20, L = 5, M = 5;
//	 boolean saveActions = false;
//	 String[] levels = new String[L];
//	 String[] actionFiles = new String[L*M];
//	 for(int i = 0; i < N; ++i)
//	 {
//         int actionIdx = 0;
//         game = gamesPath + games[i] + ".txt";
//         for(int j = 0; j < L; ++j)
//         {
//             levels[j] = gamesPath + games[i] + "_lvl" + j +".txt";
//             if(saveActions) for(int k = 0; k < M; ++k)
//                actionFiles[actionIdx++] = "actions_game_" + i + "_level_" + j + "_"  + k + ".txt";
//         }
//	    ArcadeMachine.runGames(game, levels, M, controllers, saveActions? actionFiles:null);
//	 }

        // 6. This plays a round robin style tournament between multiple tracks, in N games, first L levels, M times each.
        // Controllers are swapped for each match as well. Actions to file optional (set saveActions to true).
//	 int N = 20, L = 5, M = 2;
//	 boolean saveActions = false;
//	 String[] levels = new String[L];
//	 String[] actionFiles = new String[L*M];
//	 int actionIdx = 0;
//
//     //add all controllers that should play in this array
//	 String[] cont = new String[]{doNothingController, randomController, oneStepController, sampleRHEAController, sampleMCTSController, sampleMCTSController};
//     for(int i = 0; i < N; ++i)
//     {
//        game = gamesPath + games[i] + ".txt";
//        for (int k = 0; k < cont.length - 1; k++) {
//            for (int t = k + 1; t < cont.length; t++) {
//                // set action files for the first controller order
//                for(int j = 0; j < L; ++j){
//                    levels[j] = gamesPath + games[i] + "_lvl" + j +".txt";
//                    if(saveActions){
//                        actionIdx = 0;
//                        for(int p = 0; p < M; ++p) {
//                          actionFiles[actionIdx++] = "actions_" + cont[k] + "_" + cont[t] + "_game_" + i + "_level_" + j + "_" + p + ".txt";
//                        }
//                    }
//                }
//
//                controllers = cont[k] + " " + cont[t];
//
//                System.out.println(controllers);
//                ArcadeMachine.runGames(game, levels, M, controllers, saveActions ? actionFiles : null);
//
//                // reset action files for the swapped tracks
//                if (saveActions) {
//                    actionIdx = 0;
//                    for (int j = 0; j < L; ++j) {
//                        for (int p = 0; p < M; ++p) {
//                            actionFiles[actionIdx++] = "actions_" + cont[t] + "_" + cont[k] + "_game_" + i + "_level_" + j + "_" + p + ".txt";
//                        }
//                    }
//                }
//                controllers = cont[t] + " " + cont[k];
//                System.out.println(controllers);
//                ArcadeMachine.runGames(game, levels, M, controllers, saveActions ? actionFiles : null);
//            }
//        }
//     }



    }
}
