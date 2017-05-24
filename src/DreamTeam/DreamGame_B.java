package DreamTeam;

import tracks.ArcadeMachine;

import java.util.Random;

/**
 * Created by Cristina on 23/05/2017.
 * GameB with sampleMCTS
 */
public class DreamGame_B {

    public static void main(String[] args) {

        String sampleMCTSController = "tracks.multiPlayer.advanced.sampleMCTS.Agent";
        String humanController = "tracks.multiPlayer.tools.human.Agent";


        // Set here the tracks used in the games (need 2 separated by space).
        //String controllers = sampleMCTSController + " " + dreamTeamMCTSAgent;
        //String controllers = humanController + " " + dreamTeamMCTSAgent;
        //String controllers = dreamTeamMCTSAgent + " " + sampleMCTSController;
        String controllers = humanController + " " + sampleMCTSController;

        // Available games:
        String gamesPath = "examples/DreamTeam/";


        // Other settings
        boolean visuals = true;
        int seed = new Random().nextInt();

        // Game and level to play
        String game = gamesPath + "dreamgame_competitive_v2.txt";
        String level1 = gamesPath + "dreamgame_lvl_experiment_small.txt";

        String recordActionsFile = null;// "actions_" + games[gameIdx] + "_lvl"

        ArcadeMachine.runOneGame(game,level1,visuals,controllers,recordActionsFile,seed,0);
    }
}
