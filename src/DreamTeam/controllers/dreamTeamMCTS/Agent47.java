package DreamTeam.controllers.dreamTeamMCTS;

import core.game.Observation;
import core.game.StateObservationMulti;
import core.player.AbstractMultiPlayer;
import ontology.Types.*;
import tools.ElapsedCpuTimer;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by Adam(andy) on 18/05/2017.
 */
public class Agent47 extends AbstractMultiPlayer {

    int playerID;

    public Agent47(StateObservationMulti stateObs, ElapsedCpuTimer elapsedTimer, int playerID) {
        this.playerID = playerID;
    }

    @Override
    public ACTIONS act(StateObservationMulti stateObs, ElapsedCpuTimer elapsedTimer) {
        ArrayList<ACTIONS> actions = stateObs.getAvailableActions();
        ArrayList<Observation>[] immovables = stateObs.getImmovablePositions();
        ArrayList<Observation>[] movables = stateObs.getMovablePositions();
        ArrayList<Observation>[] blah = stateObs.getFromAvatarSpritesPositions();
        ArrayList<Observation>[][] grid = stateObs.getObservationGrid();
        HashMap<Integer, Integer> itypeCounts = new HashMap<>();
        for(int x=0;x<grid.length; x++){
            ArrayList<Observation>[] col = grid[x];
            for(int y=0;y<col.length; y++){
                ArrayList<Observation> obs = col[y];
                for(Observation o : obs){
                    int val = 0;
                    if(itypeCounts.containsKey(o.itype)){
                        val = itypeCounts.get(o.itype);
                    }
                    itypeCounts.put(o.itype, val + 1);
                }
            }
        }

        // List of actions
        // List of tokens

        // Collide with all immovables
        // Collide with all movables


        return ACTIONS.ACTION_UP;
    }

}
