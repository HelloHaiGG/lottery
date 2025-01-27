#!/bin/bash
pyinstaller --noconfirm \
    --onefile \
    --noconsole \
    --add-data "config.yaml:." \
    --add-data "background.mp3:." \
    lottery.py 