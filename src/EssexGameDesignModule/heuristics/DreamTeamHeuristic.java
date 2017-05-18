package EssexGameDesignModule.heuristics;

import core.game.Game;
import core.game.StateObservationMulti;

import java.awt.*;

/**
 * Created by Cristina on 18/05/2017.
 */
public class DreamTeamHeuristic extends MultiStateHeuristic {

    public DreamTeamHeuristic(StateObservationMulti stateObs) {
        initHeuristicAccumulation();
    }

    @Override
    public double evaluateState(StateObservationMulti stateObs) {
        return 0;
    }

    @Override
    public void updateHeuristicBasedOnCurrentState(StateObservationMulti stateObs) {

    }

    @Override
    public void recordDataOnFile(Game played, String fileName, int randomSeed, int[] recordIds) {

    }

    @Override
    public void drawInScreen(Graphics2D g) {

    }
}
