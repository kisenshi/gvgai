package EssexGameDesignModule.heuristics;

import core.game.Game;
import core.game.StateObservationMulti;
import tools.ElapsedCpuTimer;

import java.awt.*;
import java.awt.Event;
import java.util.ArrayList;

/**
 * Created by Cristina on 18/05/2017.
 */
public class DreamTeamHeuristic extends KnowledgeHeuristicMulti {
    private ArrayList<Integer> sprites_acknowledge;
    private int last_spriteAcknowledge_tick;

    public DreamTeamHeuristic(StateObservationMulti stateObs, int playerID) {
        super(stateObs, playerID);

        // Acknowledge is initialised
        sprites_from_avatar_acknowledge = new ArrayList<>();
        sprites_acknowledge = new ArrayList<>();
        updateSpriteAcknowledge(stateObs);

        interaction_history.setUseCuriosity(true);
        interaction_history.setUseStats(true);
    }

    /*+++++ DISCOVERY HEURISTIC +++++++++++++++++++++++++++++++++++++++++++++++++*/

    @Override
    protected boolean updateSpriteAcknowledge(StateObservationMulti stateObs){
        boolean ack_updated = false;

        // NPC sprites
        if (addObservationToAcknowledgeSprites(stateObs.getNPCPositions(), sprites_acknowledge)){
            ack_updated = true;
        }
        // Fixed sprites
        if (addObservationToAcknowledgeSprites(stateObs.getImmovablePositions(), sprites_acknowledge)){
            ack_updated = true;
        }
        // Movable sprites
        if (addObservationToAcknowledgeSprites(stateObs.getMovablePositions(), sprites_acknowledge)){
            ack_updated = true;
        }
        // Resources sprites
        if (addObservationToAcknowledgeSprites(stateObs.getResourcesPositions(), sprites_acknowledge)){
            ack_updated = true;
        }
        // Portal sprites
        if (addObservationToAcknowledgeSprites(stateObs.getPortalsPositions(), sprites_acknowledge)){
            ack_updated = true;
        }

        // From avatar sprites
        if (addObservationToAcknowledgeSprites(stateObs.getFromAvatarSpritesPositions(), sprites_from_avatar_acknowledge)){
            ack_updated = true;
        }

        if (ack_updated){
            last_spriteAcknowledge_tick = current_gametick;
        }

        return ack_updated;
    }

    /**
     * getNSpritesAcknowledge
     * Returns the number of sprites acknowledge (NOT considering those related with the avatar!)
     * The sprites have been stored in the sprites_acknowledge list during the game
     * @return number of non-avatar-related sprites acknowledge
     */
    private int getNSpritesAcknowledge(){
        return sprites_acknowledge.size();
    }

    /**
     * getNSpritesFromAvatarAcknowledge
     * Returns the number of sprites created by the avatar acknowledge
     * The sprites have been stored in the sprites_from_avatar_acknowledge list during the game
     * @return number of sprites created by the avatar acknowledge
     */
    private int getNSpritesFromAvatarAcknowledge(){
        return sprites_from_avatar_acknowledge.size();
    }

    /**
     * getTotalNSpritesAcknowledge
     * Returns the total number of sprites acknowledge.
     * The total number of sprites acknowledge consider both the ones generated and not from the avatar
     * @return number of total sprites acknowledge
     */
    private int getTotalNSpritesAcknowledge(){
        return getNSpritesAcknowledge() + getNSpritesFromAvatarAcknowledge();
    }

    /**
     * isNewCollisionCuriosity
     * Checks if one of the last events considered should be included to the 'curiosity' collision
     * The curiosity stores collisions with sprites in different positions of the map
     */
    private boolean isNewCollisionCuriosity(ArrayList<core.game.Event> last_gametick_events, int avatar_stype){
        for (int i=0; i<last_gametick_events.size(); i++){
            core.game.Event last_event = last_gametick_events.get(i);
            if (interaction_history.isNewCollitionCuriosity(last_event, avatar_stype)){
                return true;
            }
        }

        return false;
    }

    /**
     * isNewActionCuriosity
     * Checks if one of the last events considered should be included to the 'curiosity' action-onto list
     * The action curiosity stores the sprites from avatar collisions with other sprites in different positions of the map
     */
    private boolean isNewActionCuriosity(ArrayList<core.game.Event> last_gametick_events, int avatar_stype) {
        for (int i=0; i<last_gametick_events.size(); i++){
            core.game.Event last_event = last_gametick_events.get(i);
            if (interaction_history.isNewActionCuriosity(last_event, sprites_from_avatar_acknowledge)){
                return true;
            }
        }

        return false;
    }

    /*++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

    /*+++++ ESTIMATION HEURISTIC +++++++++++++++++++++++++++++++++++++++++++++++++*/

    private void updateSpriteStats(ArrayList<core.game.Event> last_gametick_events, StateObservationMulti stateObs, StateObservationMulti last_stateObs){
        int avatar_stype =  last_stateObs.getAvatarType(this.player_id);
        for (core.game.Event last_event : last_gametick_events) {
            interaction_history.updateSpritesStatsKnowledge(last_event, stateObs, last_stateObs, avatar_stype, sprites_from_avatar_acknowledge);
        }
    }

    private double getHeuristicForInteractionsInState(ArrayList<core.game.Event> last_gametick_events, StateObservationMulti stateObs, StateObservationMulti last_stateObs){
        int avatar_stype =  last_stateObs.getAvatarType(this.player_id);
        int min_n_times_checked = -1;

        for (core.game.Event last_event : last_gametick_events) {
            int n_times_checked = interaction_history.getNTimesInteractionChecked(last_event, avatar_stype, sprites_from_avatar_acknowledge);

            if ((min_n_times_checked == -1) || (min_n_times_checked > n_times_checked)){
                min_n_times_checked = n_times_checked;
            }
        }

        /* The heuristic is obtained considering the total number of states checked already.
        * It is obtained the percentage of the times checked the current state onto the total
        * If this percentage is small, it is because it has not been checked as usual as others, so the
        * heuristic must be big for these cases.
        * So the heuristic will be calculated using the formula:
        * h = (1 - percentage)*100
        * It will always be returned a number between 0 an 100
        * */

        double percentage_checked = (double)min_n_times_checked/interaction_history.getNTotalStatesChecked();

        return (1 - percentage_checked)*100;
    }

    /*++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

    @Override
    public double evaluateState(StateObservationMulti stateObs) {
        return 0;
    }

    @Override
    public void updateHeuristicBasedOnCurrentState(StateObservationMulti stateObs) {

    }

    // TODO THIS IS NEVER CALLED
    @Override
    public void recordDataOnFile(Game played, String fileName, int randomSeed, int[] recordIds) {
        endOfGameProcess(played.getObservationMulti(this.player_id));
        printStats(played.getObservationMulti(this.player_id));

    }

    public void drawInScreen(Graphics2D g) {
        //
    }

    public void printStats(StateObservationMulti stateObs)
    {
        interaction_history.printStatsResult();

        System.out.println("--- GAME FINISHED at "+stateObs.getGameTick() + " ----------------- ");
        System.out.println("Last tick acknowledge: "+last_spriteAcknowledge_tick);
        System.out.println("Ack :"+sprites_acknowledge);
        System.out.println("Ack Sprites from: "+sprites_from_avatar_acknowledge);
        System.out.println("sprites ack: "+getNSpritesAcknowledge());
        System.out.println("from-avatar ack: "+getNSpritesFromAvatarAcknowledge());
        System.out.println("Total ack: "+getTotalNSpritesAcknowledge());
        System.out.println("Last new collision tick: "+interaction_history.getLastNewCollitionTick());
        System.out.println("Last new action-onto tick: "+interaction_history.getLastNewActionontoTick());
        System.out.println("Last new interaction tick: "+interaction_history.getLastNewInteractonTick());
        System.out.println("Collided with: "+interaction_history.getStypesCollidedWith());
        System.out.println("Actioned onto: "+interaction_history.getStypesActionedOnto());
        System.out.println("Last curiosity tick: "+interaction_history.getLastCuriosityTick());
        System.out.println("Curiosity: "+interaction_history.getCuriosityMap());
        System.out.println("Curiosity: "+interaction_history.getNCuriosity());
        System.out.println("last Curiosity action tick: "+interaction_history.getLastCuriosityActionTick());
        System.out.println("Curiosity action: "+interaction_history.getCuriosityActionMap());
        System.out.println("Curiosity action: "+interaction_history.getNCuriosityAction());
        System.out.println("---------------------------------------------------------------------");
    }
}
