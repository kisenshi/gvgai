# valFunction Experiment

The purpose of the experiment is comparing the performance of different agents in different games when they are focused on a series of goals:

- MaximizeScore: Maximizing the score and winning, penalising losing. Current agents are focused on this.
- MaximizeExploration: Maximizing the exploration of the level, ignoring score and penalising winning and losing.
- MaximizeCuriosity

The controllers that will be used are:

- SampleOLMCTS
- SampleOneStepLookAhead
- SampleRHEA
- SampleRS
- SampleFlatMCTS
- Olets

For the experiment, 20 games from the framework are used. This selection has been done following the same criteria as for previous experiments (EvoPaper):

- aliens
- bait
- butterflies
- camel race
- chase
- chopper
- crossfire
- dig dug
- escape
- hungry birds
- infection
- intersection
- lemmings
- missile command
- modality
- plaque attack
- roguelike
- sea quest
- survive zombies
- wait for breakfast



