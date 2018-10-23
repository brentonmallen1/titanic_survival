import pandas as pd
from typing import List
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

# CONSTANTS
MODEL_NAME = "titanic_model.pkl"
MODEL_LOC = "./models"
LABEL = "Survived"
FEATURES = [
    "Pclass",
    "Sex",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "Embarked"
]
CLASS_FEATURES = FEATURES + ["Alone"]
SEX_MAPPING = {'female': 0, 'male': 1}

cwd = os.path.dirname(os.path.abspath(__file__))
TRAIN_FILE = os.path.join(cwd, "data/train.csv")
TEST_FILE = os.path.join(cwd, "data/test.csv")


def pandas_load(filename: str, **kwargs):
    """
    Read file into a pandas dataframe
    :param filename: filename with location
    :param kwargs: any other keyword args to pass
    :return: pandas df of data from file
    """
    return pd.read_csv(filename, **kwargs)


def save_model(model, fileloc: str, filename: str):
    """
    Save a classifier to disk
    :return:
    """
    try:
        joblib.dump(model,
                    os.path.join(fileloc, filename)
                    )
    except FileNotFoundError:
        if not os.path.exists(fileloc):
            os.makedirs(fileloc)
            joblib.dump(model,
                        os.path.join(fileloc, filename)
                        )


def load_model(fileloc: str, filename: str):
    """
    Load a classifier from disk
    :return: classifier object
    """
    return joblib.load(os.path.join(fileloc, filename))


def fare_groups(fare: float):
    """
    This function puts Fares into groups based of
    a defined interval
    :param fare:
    :return:
    """
    if fare < 7.78:
        return 0
    elif 7.78 <= fare < 8.66:
        return 1
    elif 8.66 <= fare < 14.45:
        return 2
    elif 14.45 <= fare < 26.0:
        return 3
    elif 26.0 <= fare < 52.37:
        return 4
    elif 52.37 <= fare < 512.33:
        return 5
    else:
        return 6


def age_groups(age):
    """
    This function creates age groups
    """
    if age < 10:
        return 0
    elif 10 <= age < 18:
        return 1
    elif 18 <= age < 26:
        return 2
    elif 26 <= age < 36:
        return 3
    elif 36 <= age < 48:
        return 4
    elif 48 <= age < 56:
        return 5
    else:
        return 6


def is_alone(row: pd.Series):
    """
    This function is used to determine if a passenger was not traveling with
    anyone else
    :param row: row of titanic data
    :return: binary output of whether and passenger was traveling alone
    """
    family_size = row['SibSp'] + row['Parch']
    if family_size == 0:
        return 1
    else:
        return 0


def missing_clf(df: pd.DataFrame, features: List,
                label: str) -> RandomForestClassifier:
    """
    This function will train a classifier
    on the data with missing values. This
    classifier is can be used to fill in
    missing data.
    :param df:
    :param features:
    :param label:
    :return:
    """
    # getting an LBACK warning with the linear regressor, this will surpress
    #  that
    import warnings
    warnings.filterwarnings(action="ignore", module="scipy",
                            message="^internal gelsd")

    train_data = df[~df[label].isna()]
    label = train_data[label].astype(int)  # train on integers
    clf = RandomForestClassifier(n_estimators=250,
                                 max_depth=3,
                                 bootstrap=False,
                                 oob_score=False
                                 )
    clf.fit(train_data[features], label)
    return clf


def predict_encode_age(row: pd.Series,
                       features: List = [],
                       clf: RandomForestClassifier = None) -> int:
    """
    This function will predict a passenger's age
    :param row:
    :param features:
    :param clf:
    :return:
    """
    if pd.isnull(row['Age']):
        return age_groups(clf.predict(row[features].values.reshape(1, -1))[0])
    else:
        return age_groups(row['Age'])
