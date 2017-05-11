package ExperimentValfunction.ensemble_system.voices;

import core.game.StateObservation;
import ontology.Types;
import tools.ElapsedCpuTimer;

/**
 * Template for a Voice.
 * <p>
 * TODO: Add Opinions and fully integrate the functionality with the {@link ExperimentValfunction.ensemble_system.CentralArbitrator}
 * <p>
 * Created by Damorin on 11/05/2017.
 */
public interface Voice {
    Types.ACTIONS act(StateObservation stateObs, ElapsedCpuTimer elapsedTimer);
}
