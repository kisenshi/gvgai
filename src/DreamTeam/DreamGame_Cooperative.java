package DreamTeam;

import tracks.ArcadeMachine;

import java.util.Random;

/**
 * Created by Cristina on 23/05/2017.
 */
public class DreamGame_Cooperative {

    public static void main(String[] args) {

        String dreamTeamMCTSAgent = "DreamTeam.Agent";
        String sampleMCTSController = "tracks.multiPlayer.advanced.sampleMCTS.Agent";


        String humanController = "tracks.multiPlayer.tools.human.Agent";


        // Set here the tracks used in the games (need 2 separated by space).
        String controllers = humanController + " " + dreamTeamMCTSAgent;

        // Available games:
        String gamesPath = "examples/DreamTeam/";


        // Other settings
        boolean visuals = true;
        int seed = new Random().nextInt();

        // Game and level to play
        String game = gamesPath + "dreamgame_cooperative.txt";
        String level1 = gamesPath + "dreamgame_lvl_cooperative.txt";

        String recordActionsFile = null;// "actions_" + games[gameIdx] + "_lvl"
        // + levelIdx + "_" + seed + ".txt";
        // //where to record the actions
        // executed. null if not to save.

        // 1. This starts a game, in a level, played by two humans.
        //ArcadeMachine.playOneGameMulti(game, level1, recordActionsFile, seed);

        // 2. This plays a game in a level by the tracks. If one of the
        // players is human, change the playerID passed
        // to the runOneGame method to be that of the human player (0 or 1).
        ArcadeMachine.runOneGame(game,level1,visuals,controllers,recordActionsFile,seed,0);
    }
}
