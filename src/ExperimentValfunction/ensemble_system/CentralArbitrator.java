package ExperimentValfunction.ensemble_system;

import ExperimentValfunction.ensemble_system.voices.Voice;
import core.game.StateObservation;
import ontology.Types;
import tools.ElapsedCpuTimer;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * The central arbitrator which houses the {@link Voice}s and makes the final decision on what action to take.
 * <p>
 * Created by Damorin on 11/05/2017.
 */
public class CentralArbitrator {

    private List<Voice> voices;
    private Random randomGenerator = new Random();

    public CentralArbitrator() {
        this.voices = new ArrayList<>();
    }

    public void addVoice(Voice voice) {
        this.voices.add(voice);
    }

    public Types.ACTIONS act(StateObservation stateObs, ElapsedCpuTimer elapsedTimer) {
        int voice = randomGenerator.nextInt(voices.size());
        System.out.println("Voice selected: " + voice);
        return this.voices.get(voice).askOpinion(stateObs, elapsedTimer).getAction();
    }
}
