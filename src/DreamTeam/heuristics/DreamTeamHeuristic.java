package DreamTeam.heuristics;

import core.game.Game;
import core.game.StateObservationMulti;
import ontology.Types;
import tools.Vector2d;

import java.awt.*;
import java.util.ArrayList;

/**
 * Created by Cristina on 18/05/2017.
 */
public class DreamTeamHeuristic extends KnowledgeHeuristicMulti {
    double last_score;
    private ArrayList<Integer> sprites_acknowledge;
    private int last_spriteAcknowledge_tick;
    private int block_size;
    private int grid_width;
    private int grid_height;
    private int exploration_matrix[][];
    private Vector2d last_position;
    private int n_positions_visited;

    public DreamTeamHeuristic(StateObservationMulti stateObs, int playerID) {
        super(stateObs, playerID);

        // Exploration
        block_size = stateObs.getBlockSize();
        Dimension grid_dimension = stateObs.getWorldDimension();

        grid_width = grid_dimension.width / block_size;
        grid_height = grid_dimension.height / block_size;

        exploration_matrix = new int[grid_width][grid_height];
        intiExplorationMatrix();

        Vector2d initialPosition = stateObs.getAvatarPosition(this.player_id);

        //markNewPositionAsVisited(initialPosition);
        n_positions_visited = 0;
        increasePositionCounter(initialPosition);

        // Acknowledge is initialised
        sprites_from_avatar_acknowledge = new ArrayList<>();
        sprites_acknowledge = new ArrayList<>();
        updateSpriteAcknowledge(stateObs);

        interaction_history.setUseCuriosity(true);
       // interaction_history.setUseStats(true);
    }

    /*+++++ EXPLORATION ++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
    private int getMapSize(){
        return grid_width * grid_height;
    }

    private void intiExplorationMatrix(){
        for (int i=0; i<grid_width; i++){
            for (int j=0; j<grid_height; j++){
                exploration_matrix[i][j] = 0;
            }
        }
    }

    private void increasePositionCounter(Vector2d position){
        if (isOutOfBounds(position)){
            return;
        }

        int x = (int)position.x / block_size;
        int y = (int)position.y / block_size;

        exploration_matrix[x][y] = exploration_matrix[x][y] + 1;
        n_positions_visited = n_positions_visited + 1;
    }

    private int calculateExplorationHeuristic(Vector2d position){
        int x = (int)position.x / block_size;
        int y = (int)position.y / block_size;

        int n_times_visited = exploration_matrix[x][y];

        //System.out.println("N visited" + n_positions_visited);

        return -10*n_times_visited;
    }

    /**
     * Marks the position as visited in the exploration_matrix
     * The position is provided as a Vector2d object so it is needed to
     * calculate the valid coordinates to be considered for the matrix
     * It would be used the block_size int set when initialised
     * @param position The position as a Vector2d object
     */
    /*private void markNewPositionAsVisited(Vector2d position){
        if (isOutOfBounds(position)){
            return;
        }

        int x = (int)position.x / block_size;
        int y = (int)position.y / block_size;

        //System.out.println("Marking ("+x+" , "+y+") as VISITED");

        exploration_matrix[x][y] = true;
    }*/

    /**
     * Checks if the position has already been visited. As it is provided as Vector2d objects,
     * it is needed to convert it to valid coordinates to be considered for the matrix
     */
    /*private boolean hasBeenBefore(Vector2d position){
        if (isOutOfBounds(position)){
            return false;
        }

        int x = (int)position.x / block_size;
        int y = (int)position.y / block_size;

        //System.out.println("Been before to ("+x+" , "+y+")? "+exploration_matrix[x][y]);

        return exploration_matrix[x][y];
    }*/

    /*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

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

    /*private void updateSpriteStats(ArrayList<core.game.Event> last_gametick_events, StateObservationMulti stateObs, StateObservationMulti last_stateObs){
        int avatar_stype =  last_stateObs.getAvatarType(this.player_id);
        for (core.game.Event last_event : last_gametick_events) {
            interaction_history.updateSpritesStatsKnowledge(last_event, stateObs, last_stateObs, avatar_stype, sprites_from_avatar_acknowledge);
        }
    }*/

    /*private double getHeuristicForInteractionsInState(ArrayList<core.game.Event> last_gametick_events, StateObservationMulti stateObs, StateObservationMulti last_stateObs){
        int avatar_stype =  last_stateObs.getAvatarType(this.player_id);
        int min_n_times_checked = -1;

        for (core.game.Event last_event : last_gametick_events) {
            int n_times_checked = interaction_history.getNTimesInteractionChecked(last_event, avatar_stype, sprites_from_avatar_acknowledge);

            if ((min_n_times_checked == -1) || (min_n_times_checked > n_times_checked)){
                min_n_times_checked = n_times_checked;
            }
        }*/

        /* The heuristic is obtained considering the total number of states checked already.
        * It is obtained the percentage of the times checked the current state onto the total
        * If this percentage is small, it is because it has not been checked as usual as others, so the
        * heuristic must be big for these cases.
        * So the heuristic will be calculated using the formula:
        * h = (1 - percentage)*100
        * It will always be returned a number between 0 an 100
        * */
/*
        double percentage_checked = (double)min_n_times_checked/interaction_history.getNTotalStatesChecked();

        return (1 - percentage_checked)*100;
    }*/

    /*++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

    @Override
    public double evaluateState(StateObservationMulti stateObs) {

        // ------------- KNOWLEDGE ACQUIREMENT
        // The different sprites in the evaluated state are added to the 'sprite acknowledgement' of the agent
        ArrayList<core.game.Event> last_gametick_events = getLastGametickEvents(stateObs, last_stateObs);

        // The different sprites in the evaluated state are added to the 'sprite acknowledgement' of the agent
        boolean ack_update = updateSpriteAcknowledge(stateObs);
        //updateSpriteStats(last_gametick_events, stateObs, last_stateObs);

        //-------------------------------

        boolean gameOver = stateObs.isGameOver();
        Types.WINNER winner = stateObs.getMultiGameWinner()[this.player_id];
        double rawScore = stateObs.getGameScore(this.player_id);

        if(gameOver && winner == Types.WINNER.PLAYER_WINS) {
            return HUGE_POSITIVE;
        }

        if(gameOver && winner == Types.WINNER.PLAYER_LOSES){
            return HUGE_NEGATIVE;
        }

        // It is returned the score change as heuristic
        Vector2d currentPosition = stateObs.getAvatarPosition(this.player_id);

        if (isOutOfBounds(currentPosition)){
            // If the new position is out of bounds then dont go there
            return HUGE_NEGATIVE;
        }

        int reward_value = 0;

        int n_positions_during_exploration;
        if (currentPosition.equals(last_position)){

        }

        reward_value = calculateExplorationHeuristic(currentPosition);
        //System.out.println(reward_value);

        /*if (!last_gametick_events.isEmpty()){
            if (isNewStypeInteraction(last_gametick_events, last_stateObs.getAvatarType(this.player_id))){
                //System.out.println("Is new");
                reward_value = 1000;
            } else if (isNewCollisionCuriosity(last_gametick_events, last_stateObs.getAvatarType(this.player_id))){
                //System.out.println("New collision");
                reward_value = 25;
            } else if (isNewActionCuriosity(last_gametick_events, last_stateObs.getAvatarType(this.player_id))){
                reward_value = 25;
            }

        }*/

        /*if (!hasBeenBefore(currentPosition)){
            // If it hasnt been before, it is rewarded
            reward_value = reward_value + 1000;
        } else {
            reward_value = reward_value - 100;
        }

        // If it has been before, it is penalised
        if (currentPosition.equals(last_position)){
            // As it is tried to reward exploration, it is penalised more if it is the last position visited
            //System.out.println("Last position visited");
            reward_value = reward_value -50;
        }*/

        reward_value += (rawScore - last_score);

        return reward_value;
    }

    @Override
    public void updateHeuristicBasedOnCurrentState(StateObservationMulti stateObs) {
        // For EXPLORATION is needed to update the exploration_matrix to mark
        Vector2d currentPosition = stateObs.getAvatarPosition(this.player_id);

        /*if (!hasBeenBefore(currentPosition)) {
            markNewPositionAsVisited(currentPosition);
        }*/

        // For EXPLORATION
        last_position = currentPosition.copy();
        increasePositionCounter(currentPosition);

        // For SCORE
        last_score = stateObs.getGameScore(this.player_id);

        super.updateHeuristicBasedOnCurrentState(stateObs);
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
