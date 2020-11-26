import asyncio
import datetime
import logging
import os
import time

import yaml


class Config:
    def __init__(self, logger=logging.getLogger(__name__), config_path=None, auto_reload=False, auto_reload_timeout=60):
        self.logger = logger
        self.config_path = config_path
        self.st_mtime = None
        self.contents = {}
        self.auto_reload = auto_reload
        self.auto_reload_timeout = auto_reload_timeout
        self.last_load_attempt = None


    def load_config(self):
        """
        Use default config if None
        """
        print("loading!")
        self.last_load_attempt = datetime.datetime.now()
        new_contents = None
        if not self.config_path or not os.path.exists(self.config_path) or not os.path.isfile(self.config_path):
            self.logger.error("Could not load config, the config path or file was incorrect/invalid!")
        try:
            with open(self.config_path, "r") as configfile:
                yconfig = yaml.load(configfile, Loader=yaml.SafeLoader)
                new_contents = yconfig.copy()
            self.st_mtime = os.stat(self.config_path).st_mtime
        except Exception as e:
            self.logger.error("Could not load config due to unexpected error!: %s", e)
            return False
        else:
            self.contents = new_contents
            return True

    def get(self, *args, **kwargs):
        return self.contents.get(*args, **kwargs)

    def has_changed(self):
        """
        """
        try:
            return os.stat(self.config_path).st_mtime != self.st_mtime
        except Exception as e:
            self.logger.error("Error querying config! Has the file been moved or deleted?: %s", e)


    def reload_on_change(self):
        if self.has_changed():
            self.logger.info("Detected change in config, reloading config!")
            self.load_config()

    def should_be_reloaded(self):
        if not self.auto_reload:
            return False
        elif not self.last_load_attempt:
            return True
        elif (self.last_load_attempt + datetime.timedelta(seconds=self.auto_reload_timeout)) < datetime.datetime.now():
            return True
        return False


    async def auto_reload_loop(self):
        while True:
            if self.should_be_reloaded():
                self.reload_on_change()
            await asyncio.sleep(self.auto_reload_timeout)
