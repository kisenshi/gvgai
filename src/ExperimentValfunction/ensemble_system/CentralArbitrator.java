package ExperimentValfunction.ensemble_system;

import ExperimentValfunction.ensemble_system.voices.Opinion;
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
    private List<Opinion> opinions;
    private Random randomGenerator = new Random();

    public CentralArbitrator() {
        this.voices = new ArrayList<>();
        this.opinions = new ArrayList<>();
    }

    public void addVoice(Voice voice) {
        this.voices.add(voice);
    }

    public Types.ACTIONS act(StateObservation stateObs, ElapsedCpuTimer elapsedTimer) {
        opinions.clear();
        int analysisTime = 12;
        elapsedTimer.setMaxTimeMillis(analysisTime);
        for (Voice voice : voices) {
            this.opinions.add(voice.askOpinion(stateObs, elapsedTimer, analysisTime));
        }
        return selectHighestValueOpinion().getAction();
    }

    private Opinion selectHighestValueOpinion() {
        double bestValue = -Double.MAX_VALUE;
        Opinion bestOpinion = new Opinion(Types.ACTIONS.ACTION_NIL, 0);
        for (int i = 0; i < opinions.size(); i++) {
            double value = opinions.get(i).getActionValue();
            if (value > bestValue) {
                bestValue = value;
                bestOpinion = opinions.get(i);
            }
        }
        return bestOpinion;
    }
}
