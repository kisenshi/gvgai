package EssexGameDesignModule;

import core.game.Game;
import core.game.StateObservationMulti;
import core.player.AbstractMultiPlayer;
import tools.ElapsedCpuTimer;
import EssexGameDesignModule.heuristics.MultiStateHeuristic;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

/**
 * Created by Cristina on 18/05/2017.
 */
public abstract class AbstractHeuristicMultiPlayer extends AbstractMultiPlayer {

    private String heuristicsPath = "EssexGameDesignModule.heuristics.";
    private String heuristicName = heuristicsPath + "DreamTeamHeuristic";
    protected MultiStateHeuristic heuristic;

    public AbstractHeuristicMultiPlayer(StateObservationMulti stateObs, ElapsedCpuTimer elapsedTimer, int playerID){
        setPlayerHeuristic(heuristicName);
        this.heuristic = createPlayerHeuristic(stateObs, playerID);
    }

    public void recordHeuristicData(Game played, String fileName, int randomSeed, int[] recordIds) {
        heuristic.recordDataOnFile(played, fileName, randomSeed, recordIds);
    }

    protected void setPlayerHeuristic(String heuristicName){
        this.heuristicName = heuristicName;
    }

    protected MultiStateHeuristic createPlayerHeuristic(StateObservationMulti stateObs, int playerID) {
        MultiStateHeuristic heuristic = null;
        try {
            Class<? extends MultiStateHeuristic> heuristicClass = Class.forName(heuristicName)
                    .asSubclass(MultiStateHeuristic.class);

            // It is pass the stateObs as argument when instantiating the class
            Class[] heuristicArgsClass = new Class[] { StateObservationMulti.class, int.class };
            Object[] constructorArgs = new Object[] { stateObs, playerID };

            Constructor heuristicArgsConstructor = heuristicClass.getConstructor(heuristicArgsClass);

            heuristic = (MultiStateHeuristic) heuristicArgsConstructor.newInstance(constructorArgs);

        } catch (NoSuchMethodException e) {
            e.printStackTrace();
            System.err.println("Constructor " + heuristicName + "() not found :");
            System.exit(1);

        } catch (ClassNotFoundException e) {
            System.err.println("Class " + heuristicName + " not found :");
            e.printStackTrace();
            System.exit(1);

        } catch (InstantiationException e) {
            System.err.println("Exception instantiating " + heuristicName + ":");
            e.printStackTrace();
            System.exit(1);
        } catch (IllegalAccessException e) {
            System.err.println("Illegal access exception when instantiating " + heuristicName + ":");
            e.printStackTrace();
            System.exit(1);
        } catch (InvocationTargetException e) {
            System.err.println("Exception calling the constructor " + heuristicName + "():");
            e.printStackTrace();
            System.exit(1);
        }

        return heuristic;
    }
}
