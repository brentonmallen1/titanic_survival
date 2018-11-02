import train
import utils as _utils
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def test_fill_encode_embark():
    """
    Test the filling and encoding of Embark data
    :return:
    """
    data = [
        {'Age': 12, 'Embarked': None},
        {'Age': 13, 'Embarked': 'S'},
        {'Age': 14, 'Embarked': 'S'},
    ]
    test_df = pd.DataFrame(data, index=range(len(data)))
    _utils.fill_encode_embark(test_df)
    assert 0 == test_df[test_df['Age'] == 12]['Embarked'].values[0]


def test_process_data():
    """
    Test the handling of training data. Make sure no data is missing
    :return:
    """
    data = train.process_data(_utils.TRAIN_FILE)
    assert not data[_utils.CLASS_FEATURES].isna().any(axis=1).any()


def test_train():
    """
    test the training of a random forest classifier
    :return:
    """
    test_clf = train.train()
    assert isinstance(test_clf, RandomForestClassifier)
    assert 8 == test_clf.n_features_
