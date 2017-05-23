package DreamTeam;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import core.game.Game;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by cg16604 on 23/05/2017.
 */
public class DreamTeamDataCollection {

    ArrayList<Double> scoresHuman = new ArrayList<>();
    ArrayList<Double> scoresAI = new ArrayList<>();

    double score(Game game, int player){
        return game.getAvatars()[player].getScore();
    }

    public void UpdateStatsOnTick(Game game) {
        scoresHuman.add(score(game,0));
        scoresAI.add(score(game,1));
    }

    public void WriteLogFile(String json){
        // Find a unique log ID, counting upwards
        int logId = 0;
        File logFile;
        do {
            logId += 1;
            logFile = new File("DreamTeamExperimentLog_" + logId + ".json");
        }
        while(logFile.isFile());
        // Write the json to the file
        try {
            BufferedWriter out = new BufferedWriter(new FileWriter(logFile));
            out.write(json);
            out.close();
        }
        catch (IOException e) {
            throw new RuntimeException("Error: your programming language supports checked exceptions");
        }
    }

    public void CollectFinalStats(Game game){
        // Get the score, win, score diff, total ticks elapsed
        HashMap<String, Object> stats = new HashMap<>();
        double score_human = score(game, 0);
        double score_ai = score(game, 1);

        stats.put("final_score_human", score_human);
        stats.put("final_score_ai", score_ai);
        stats.put("winner", score_ai == score_human ? "draw" : (score_ai > score_human ? "ai" : "human")); // sorry
        stats.put("ticks_elapsed", game.getGameTick());
        stats.put("score_over_time_human", scoresHuman);
        stats.put("score_over_time_ai", scoresAI);
        stats.put("ai_controller", game.getAvatars()[1].player.getClass().toString());

        // Convert it to json
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        String json = gson.toJson(stats);

        // Write json to disk
        WriteLogFile(json);
    }
}
