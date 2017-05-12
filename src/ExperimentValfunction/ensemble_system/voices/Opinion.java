package ExperimentValfunction.ensemble_system.voices;

import ontology.Types;

/**
 * The recommended action from a {@link Voice}.
 * <p>
 * Created by Damorin on 12/05/2017.
 */
public class Opinion {

    private Types.ACTIONS action;
    private double actionValue;

    public Opinion(Types.ACTIONS action, double actionValue) {
        this.action = action;
        this.actionValue = actionValue;
    }

    public Types.ACTIONS getAction() {
        return this.action;
    }

    public double getActionValue() {
        return this.actionValue;
    }

}
