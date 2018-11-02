"""
This script trains a random forest classifier on the kaggle titanic data
"""
import utils as _utils
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def process_data(train_fname: str) -> pd.DataFrame:
    """
    Process the training data to extract the classification
    features
    :param train_fname: name of the training data file
    :return: dataframe with the formatted training data
    """
    # load training data
    train_data = _utils.pandas_load(train_fname)
    # process the embarked data
    _utils.fill_encode_embark(train_data)
    # encode the sex data
    train_data['Sex'] = train_data['Sex'].map(_utils.SEX_MAPPING)
    # Fill missing ages and encode them into age groups
    age_features = [f for f in _utils.FEATURES if f != 'Age']
    age_clf = _utils.missing_clf(train_data,
                                 age_features,
                                 'Age'
                                 )
    train_data['Age'] = (train_data.
        apply(
        lambda x: _utils.predict_encode_age(
            x,
            features=age_features,
            clf=age_clf
        ),
        axis=1
    )
    )
    # encode Fare into groups
    train_data['Fare'] = train_data['Fare'].apply(_utils.fare_groups)
    # determine if the passenger is alone
    train_data['Alone'] = train_data.apply(_utils.is_alone, axis=1)
    return train_data


def train() -> RandomForestClassifier:
    """
    Train a random forest classifier on some training data
    :return: trained classifier
    """
    train_data = process_data(_utils.TRAIN_FILE)
    clf = RandomForestClassifier(n_estimators=300,
                                 min_samples_leaf=7,
                                 min_samples_split=5,
                                 max_features=0.5,
                                 oob_score=True,
                                 n_jobs=-1,
                                 random_state=42
                                 )
    clf.fit(train_data[_utils.CLASS_FEATURES], train_data[_utils.LABEL])
    return clf


def main(fileloc=_utils.MODEL_LOC, filename=_utils.MODEL_NAME):
    """
    Build a model on the training data and then save it off
    :return: saved trained sklearn classifier
    """
    model = train()
    # save model
    _utils.save_model(model,
                      fileloc,
                      filename
                      )


if __name__ == '__main__':
    main()
