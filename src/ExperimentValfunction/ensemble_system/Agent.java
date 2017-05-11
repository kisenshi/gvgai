package ExperimentValfunction.ensemble_system;

import core.game.StateObservation;
import core.player.AbstractPlayer;
import ontology.Types;
import tools.ElapsedCpuTimer;

/**
 * A basic Ensemble Decision System agent.
 * <p>
 * Needs a lot of work!
 * <p>
 * Created by kisenshi on 11/05/17.
 */
public class Agent extends AbstractPlayer {

    private CentralArbitrator ensemble;

    public Agent(StateObservation stateObs, ElapsedCpuTimer elapsedCpuTimer) {
        ensemble = new CentralArbitrator();
        ensemble.addVoice(new ExperimentValfunction.controllers.sampleOLMCTS.Agent(stateObs, elapsedCpuTimer, "ExperimentValfunction.heuristics.MaximizeScoreHeuristic"));
        ensemble.addVoice(new ExperimentValfunction.controllers.sampleOLMCTS.Agent(stateObs, elapsedCpuTimer, "ExperimentValfunction.heuristics.MaximizeExplorationHeuristic"));
    }

    @Override
    public Types.ACTIONS act(StateObservation stateObs, ElapsedCpuTimer elapsedTimer) {
        return ensemble.act(stateObs, elapsedTimer);
    }
}
