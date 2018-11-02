import utils as utils
import pandas as pd
import os
import numpy as np
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier


def test_pandas_load():
    """
    Test loading a pandas dataframe
    :return:
    """

    test_df = utils.pandas_load(utils.TRAIN_FILE)
    assert isinstance(test_df, pd.DataFrame)


def test_save_load_model():
    """
    Test the saving and loading of a sklearn classifier
    *note: this test relies on a model having been made
    using the train.py script. not the best but functional
    for a first iteration
    :return:
    """
    test_floc = '.'
    test_fname = 'test_model.pkl'
    test_clf = joblib.load(os.path.join(
        utils.MODEL_LOC,
        utils.MODEL_NAME
    )
    )
    utils.save_model(test_clf, test_floc, test_fname)
    test_clf2 = utils.load_model(test_floc, test_fname)
    assert isinstance(test_clf2, RandomForestClassifier)
    assert 8 == test_clf2.n_features_


def test_fare_groups():
    """
    Test the grouping of passenger fares
    :return:
    """
    assert 0 == utils.fare_groups(1.00)
    assert 1 == utils.fare_groups(8.00)
    assert 2 == utils.fare_groups(13.00)
    assert 3 == utils.fare_groups(20.00)
    assert 4 == utils.fare_groups(45.00)
    assert 5 == utils.fare_groups(100.00)
    assert 6 == utils.fare_groups(600.00)


def test_age_groups():
    """
    Test the grouping of passenger fares
    :return:
    """
    assert 0 == utils.age_groups(5)
    assert 1 == utils.age_groups(16)
    assert 2 == utils.age_groups(21)
    assert 3 == utils.age_groups(30)
    assert 4 == utils.age_groups(45)
    assert 5 == utils.age_groups(50)
    assert 6 == utils.age_groups(65)


def test_is_alone():
    """
    Test if a passenger is alone
    :return:
    """
    data = [
        {'SibSp': 0, 'Parch': 0}
    ]
    test_df = pd.DataFrame(data, index=[1])
    test_df['Alone'] = test_df.apply(utils.is_alone, axis=1)
    assert 1 == test_df['Alone'].values[0]


def test_missing_age():
    """
    Test building a classifier on missing data
    and test filling age data
    :return:
    """
    data = [
        {'Sex': 1, 'Embarked': 2, 'Age': 20},
        {'Sex': 1, 'Embarked': 2, 'Age': 22},
        {'Sex': 1, 'Embarked': 2, 'Age': 20},
        {'Sex': 1, 'Embarked': 2, 'Age': np.nan},
    ]
    age_features = ['Sex', 'Embarked']
    df = pd.DataFrame(data=data, index=[0, 1, 2, 3])
    age_clf = utils.missing_clf(
        df,
        age_features,
        'Age'
    )
    pred_age = [
        utils.predict_encode_age(x,
                                 features=age_features,
                                 clf=age_clf
                                 )
        for i, x in df.iterrows()
    ]
    assert not np.isnan(pred_age).all()


def test_fill_encode_empark():
    """
    Test filling missing Embark data
    :return:
    """
    data = [
        {'Sex': 1, 'Embarked': 2},
        {'Sex': 1, 'Embarked': 2},
        {'Sex': 1, 'Embarked': 2},
        {'Sex': 1, 'Embarked': np.nan},
    ]
    test_df = pd.DataFrame(data=data)
    utils.fill_encode_embark(test_df)
    assert not test_df['Embarked'].isna().all()
