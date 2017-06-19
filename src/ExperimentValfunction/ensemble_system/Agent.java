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

    private CentralArbitrator ensemble = new CentralArbitrator();

    public Agent(StateObservation stateObs, ElapsedCpuTimer elapsedCpuTimer) {
//        ensemble.addVoice(new ExperimentValfunction.ensemble_system.voices.mcts.Agent(stateObs, elapsedCpuTimer, "ExperimentValfunction.heuristics.MaximizeScoreHeuristic"));
//        ensemble.addVoice(new ExperimentValfunction.ensemble_system.voices.rhea.Agent(stateObs, elapsedCpuTimer, "ExperimentValfunction.heuristics.MaximizeExplorationHeuristic"));
        ensemble.addVoice((new ExperimentValfunction.ensemble_system.voices.rs.Agent(stateObs, elapsedCpuTimer, "ExperimentValfunction.heuristics.MaximizeScoreHeuristic")));
        ensemble.addVoice((new ExperimentValfunction.ensemble_system.voices.olets.Agent(stateObs, elapsedCpuTimer, "ExperimentValfunction.heuristics.MaximizeScoreHeuristic")));
    }

    @Override
    public Types.ACTIONS act(StateObservation stateObs, ElapsedCpuTimer elapsedTimer) {
        return ensemble.act(stateObs, elapsedTimer);
    }
}
