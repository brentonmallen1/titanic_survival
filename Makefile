FLASK_PID_FILE=./flask.pid
VENV_NAME?=titanic-venv
VENV=./$(VENV_NAME)/bin
MAIN?=titanic.py
ZAPPA_ENV?=dev

export AWS_PROFILE=zappa

# ---------------
#   DEPENDENCIES
# ---------------
.PHONY: update-requirements
update-requirements:
	(conda env update && \
	source activate titanic && \
	pip freeze > requirements.txt)


# ------------
#   VIRTUALENV
# ------------
.PHONY: init
init:
	rm -rf $(VENV_NAME)
	virtualenv $(VENV_NAME)
	(source $(VENV)/activate && pip install -r requirements.txt)


# ---------------
#   FLASK Locally
# ---------------
.PHONY: start
start:
	$(VENV)/python $(MAIN) & echo $$! > $(FLASK_PID_FILE);
	sleep 1 && \
	$(VENV)/python -m webbrowser "http://127.0.0.1:5000/" &

.PHONY: stop
stop:
	kill `cat $(FLASK_PID_FILE)` && rm $(FLASK_PID_FILE)

.PHONY: restart
restart: stop start

# command to find flask PIDs in use to kill missed processes
.PHONY: find-pid
find-pid:
	sudo lsof -i :5000


# ---------------
#   ZAPPA
# ---------------
.PHONY: deploy
deploy:
	(source $(VENV)/activate && zappa deploy $(ZAPPA_ENV))

.PHONY: redeploy
redeploy:
	(source $(VENV)/activate && zappa update $(ZAPPA_ENV))

.PHONY: remove
remove:
	(source $(VENV)/activate && zappa undeploy $(ZAPPA_ENV))

.PHONY: logs
logs:
	(source $(VENV)/activate && zappa tail $(ENV))

# ------------
#  TESTING
# ------------
.PHONY: test
test:
	$(VENV)/python -m pytest -s

# --------
# TRAINING
# --------
.PHONY: train
train:
	$(VENV)/python train.py

# ------
# KAGGLE
# ------
# TODO run the stored classifier on the test data and submit the results to kaggle
