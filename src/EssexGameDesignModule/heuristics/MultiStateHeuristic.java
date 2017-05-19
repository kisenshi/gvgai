package EssexGameDesignModule.heuristics;

import core.game.Game;
import core.game.StateObservationMulti;

import java.awt.*;
import java.io.BufferedWriter;

/**
 * Created by Cristina on 18/05/2017.
 */
public abstract class MultiStateHeuristic {

    protected static final double HUGE_NEGATIVE = -10000.0;
    protected static final double LESS_HUGE_NEGATIVE = -5000.0;
    protected static final double HUGE_POSITIVE =  10000.0;
    protected BufferedWriter writer;
    protected double heuristic_acc;
    protected StateObservationMulti last_stateObs;
    protected StateObservationMulti last_visited_stateObs;
    protected int player_id;

    abstract public double evaluateState(StateObservationMulti stateObs);

    abstract public void updateHeuristicBasedOnCurrentState(StateObservationMulti stateObs);

    abstract public void recordDataOnFile(Game played, String fileName, int randomSeed, int[] recordIds);

    abstract public void drawInScreen(Graphics2D g);

    public void initHeuristicAccumulation(){
        heuristic_acc = 0;
        last_stateObs = last_visited_stateObs;
    }

    public void accumulateHeuristic(StateObservationMulti stateObs){
        heuristic_acc += evaluateState(stateObs);
        if (stateObs != null){
            last_stateObs = stateObs.copy();
        }
        //System.out.println("Heuristic acc: "+heuristic_acc);
    }

    public double endHeuristicAccumulation(StateObservationMulti stateObs){
        double h = heuristic_acc;
        initHeuristicAccumulation();
        //System.out.println("Total heuristic: "+h);
        //System.out.println("");
        return h;
    }
}
