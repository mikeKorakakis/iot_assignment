#!/bin/bash

# Ορισμός διαδρομής virtual environment
VENV_PATH="$HOME/Desktop/env"

# Πλήρης διαδρομή των scripts
PUB_SCRIPT="$HOME/Desktop/publisher.py"
SUB_SCRIPT="$HOME/Desktop/subscriber.py"

# Εκκίνηση subscriber σε νέο παράθυρο
lxterminal --title="Subscriber" --working-directory="$HOME/Desktop" \
  --command="bash -c 'source $VENV_PATH/bin/activate && python3 $SUB_SCRIPT; exec bash'" &

# Εκκίνηση publisher σε νέο παράθυρο
lxterminal --title="Publisher" --working-directory="$HOME/Desktop" \
  --command="bash -c 'source $VENV_PATH/bin/activate && python3 $PUB_SCRIPT; exec bash'" &
