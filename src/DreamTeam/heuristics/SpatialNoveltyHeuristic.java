package DreamTeam.heuristics;

import core.game.Game;
import core.game.Observation;
import core.game.StateObservationMulti;
import ontology.Types;
import tools.Vector2d;

import java.awt.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;

/**
 * Created by Andy on 19/05/2017.
 */
public class SpatialNoveltyHeuristic extends MultiStateHeuristic {

    static class SpriteInfo {
        int timesVisited = 0;
        public boolean isWall = true;

        public double valuation(){
            return 1000.0 / (double)timesVisited;
        }
    }

    protected int block_size;
    protected int grid_width;
    protected int grid_height;

    HashMap<Integer, SpriteInfo> spriteInfo = new HashMap<>();

    public SpatialNoveltyHeuristic(StateObservationMulti stateObs, int playerID) {
        // Log some basic information about the game world
        this.player_id = playerID;
        block_size = stateObs.getBlockSize();
        Dimension grid_dimension = stateObs.getWorldDimension();
        grid_width = grid_dimension.width / block_size;
        grid_height = grid_dimension.height / block_size;

        // Find unique sprites, and initialise default sprite info
        ArrayList<Observation>[][] obsGrid = stateObs.getObservationGrid();
        for(int x=0;x<obsGrid.length; x++){
            ArrayList<Observation>[] col = obsGrid[x];
            for(int y=0;y<col.length; y++){
                ArrayList<Observation> obs = col[y];
                for(int i=0; i<obs.size(); i++){
                    Observation o = obs.get(i);
                    if(!spriteInfo.containsKey(o.itype)) {
                        spriteInfo.put(o.itype, new SpriteInfo());
                    }
                }
            }
        }
    }

    private void printMapState(StateObservationMulti stateObs){
        ArrayList<Observation>[][] obsGrid = stateObs.getObservationGrid();
        StringBuilder b = new StringBuilder();
        for(int x=0;x<obsGrid.length; x++){
            ArrayList<Observation>[] col = obsGrid[x];
            for(int y=0;y<col.length; y++){
                ArrayList<Observation> obs = col[y];
                if(obs.isEmpty()) b.append('_');
                else if(obs.size()>1) b.append('@');
                else b.append((char)('a' + obs.get(0).itype));
                b.append(' ');
            }
            b.append('\n');
        }
        String s = b.toString();
        return;
    }

    private void updateSpriteInfo(StateObservationMulti stateObs) {
        Vector2d pos = stateObs.getAvatarPosition(player_id);
        int x = (int)(pos.x / (double)block_size);
        int y = (int)(pos.y / (double)block_size);
        ArrayList<Observation> obs = stateObs.getObservationGrid()[x][y];
        for(int i=0; i<obs.size(); i++){
            Observation o = obs.get(i);
            //if(stateObs.getAvatarType()
        }
    }

    @Override
    public double evaluateState(StateObservationMulti stateObs){

        updateSpriteInfo(stateObs);

        //printMapState(stateObs);

        boolean gameOver = stateObs.isGameOver();
        Types.WINNER winner = stateObs.getMultiGameWinner()[this.player_id];
        double rawScore = stateObs.getGameScore(this.player_id);

        if(gameOver && winner == Types.WINNER.PLAYER_WINS) {
            return HUGE_POSITIVE;
        }

        if(gameOver && winner == Types.WINNER.PLAYER_LOSES){
            return HUGE_NEGATIVE;
        }

        return 0;
    }

    @Override
    public void updateHeuristicBasedOnCurrentState(StateObservationMulti stateObs){

    }

    @Override
    public void recordDataOnFile(Game played, String fileName, int randomSeed, int[] recordIds){

    }

    @Override
    public void drawInScreen(Graphics2D g) {

    }
}
