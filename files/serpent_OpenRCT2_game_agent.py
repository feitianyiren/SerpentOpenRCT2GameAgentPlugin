import lib.cv

from lib.game_agent import GameAgent

from lib.machine_learning.context_classification.context_classifiers.cnn_inception_v3_context_classifier import CNNInceptionV3ContextClassifier

import offshoot

import time


class SerpentOpenRCT2GameAgent(GameAgent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.frame_handlers["PLAY"] = self.handle_play

        self.frame_handler_setups["PLAY"] = self.setup_play

        self.analytics_client = None

    def setup_play(self):
        plugin_path = offshoot.config["file_paths"]["plugins"]

        context_classifier_path = f"{plugin_path}/SerpentOpenRCT2GameAgentPlugin/files/ml_models/context_classifier.model"

        context_classifier = CNNInceptionV3ContextClassifier(input_shape=(384, 512, 3))
        context_classifier.prepare_generators()
        context_classifier.load_classifier(context_classifier_path)

        self.machine_learning_models["context_classifier"] = context_classifier

    def handle_play(self, game_frame):
        context = self.machine_learning_models["context_classifier"].predict(game_frame.frame)

        if context == "main_menu":
            self.game.api.MainMenu.click_new_game()
            time.sleep(2)
            self.game.api.MainMenu.click_load_game()
            time.sleep(2)
            self.game.api.MainMenu.click_multiplayer()
            time.sleep(2)
            self.game.api.MainMenu.click_game_tools()
            time.sleep(10)
        elif context == "game":
            self.game.api.Game.click_pause()
            time.sleep(2)
            self.game.api.Game.click_speed()
            time.sleep(2)
            self.game.api.Game.click_floppy()
            time.sleep(10)
