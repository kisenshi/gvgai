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

    public static final int ANALYSIS_TIME = 12; // Constant to define the amount of analysis time per voice
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
        for (Voice voice : voices) {
            elapsedTimer.setMaxTimeMillis(ANALYSIS_TIME);
            this.opinions.add(voice.askOpinion(stateObs, elapsedTimer, ANALYSIS_TIME));
        }
        for (Opinion opinion : opinions) {
            System.out.println(opinion.getEstimatedValue());
        }
        return selectHighestValueOpinion().getAction();
//        return selectRandomOpinion().getAction();
    }

    private Opinion selectHighestValueOpinion() {
        List<Opinion> bestActions = new ArrayList<>();
        double bestValue = -Double.MAX_VALUE;
        int bestVoice = -1;
        Opinion bestOpinion = null;
        for (int i = 0; i < opinions.size(); i++) {
            double value = opinions.get(i).getEstimatedValue();
            if (value > bestValue) {
                bestActions.clear();
                bestValue = value;
                bestOpinion = opinions.get(i);
                bestVoice = i;
                bestActions.add(opinions.get(i));
            } else if (value == bestValue) {
                bestActions.add(opinions.get(i));
            }
        }

        if (bestActions.size() > 1) {
            return bestActions.get(randomGenerator.nextInt(bestActions.size()));
        }
        return bestOpinion;
    }

    private Opinion selectRandomOpinion() {
        int opinion = randomGenerator.nextInt(opinions.size());
        return opinions.get(opinion);
    }
}
