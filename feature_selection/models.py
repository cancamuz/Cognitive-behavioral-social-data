from feature_selection.utils import save_plot,select_features , cramers_corrected_stat, theils_u, save_plot_sns, get_metrics

# intrinsic methods
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

# dimensionality reduction methods
# instead of PCA we can use Fisher's Linear Discriminant
from sklearn.decomposition import PCA
from sklearn import metrics


# permutation importance
from sklearn.neighbors import KNeighborsClassifier
from sklearn.inspection import permutation_importance

# filter methods

# considering input datatype:ordinal, output datatype:categorical
from sklearn.feature_selection import chi2
from sklearn.feature_selection import mutual_info_classif

# considering input datatype:numerical, output datatype:categorical
from sklearn.feature_selection import f_classif
# kendalls rank correlation method df.corr(method='kendall')


from sklearn.feature_selection import SelectFromModel, SelectKBest
import pandas as pd
import numpy as np
from itertools import combinations


def dtree(X, y, X_test, y_test, dir, print_features = True, plot = True):
    # define the model
    model = DecisionTreeClassifier()
    # fit the model
    model.fit(X, y)
    # predict
    y_pred = model.predict(X_test)
    metrics_dict = get_metrics(y_test, y_pred)

    # get importances
    importance = model.feature_importances_
    # Print all feature scores
    if print_features:
        for k,v in zip(X.columns, importance):
            print('Feature', k, ':', round(v,2))

    if plot:
        save_plot(X.columns, importance, 'dtree.png', dir)

    return metrics_dict


def rforest(X, y, X_test, y_test, dir, print_features = True, plot = True):

    model = RandomForestClassifier()
    # fit the model
    model.fit(X, y)
    # predict
    y_pred = model.predict(X_test)
    metrics_dict = get_metrics(y_test, y_pred)

    # get importances
    importance = model.feature_importances_
    # Print all feature scores
    if print_features:
        for k,v in zip(X.columns, importance):
            print('Feature', k, ':', round(v,2))

    if plot:
        save_plot(X.columns, importance, 'rforest.png', dir)

    return metrics_dict


def xgboost(X, y, X_test, y_test, dir, print_features = True, plot = True):
    # define the model
    model = XGBClassifier()
    # fit the model
    model.fit(X, y)
    # predict
    y_pred = model.predict(X_test)
    metrics_dict = get_metrics(y_test, y_pred)

    importance = model.feature_importances_
    # Print all feature scores
    if print_features:
        for k,v in zip(X.columns, importance):
            print('Feature', k, ':', round(v,2))

    if plot:
        save_plot(X.columns, importance, 'xgboost.png', dir)

    return metrics_dict

def log_reg(X, y, X_test, y_test, dir, print_features = True, plot = True):
    
    # define the model
    model = LogisticRegression()
    # fit the model
    model.fit(X, y)
    # predict
    y_pred = model.predict(X_test)
    metrics_dict = get_metrics(y_test, y_pred)

    importance = model.coef_[0]
    # Print all feature scores
    if print_features:
        for k,v in zip(X.columns, importance):
            print('Feature', k, ':', round(v,2))

    # plot feature importance
    if plot:
        save_plot(X.columns, importance, 'log_reg.png', dir)

    return metrics_dict


def svm(X, y, X_test, y_test, dir, print_features = True, plot = True):

    # define the model
    model = SVC(kernel = "linear")
    # fit the model
    model.fit(X, y)
    # predict
    y_pred = model.predict(X_test)
    metrics_dict = get_metrics(y_test, y_pred)

    importance = model.coef_[0]
    # Print all feature scores
    if print_features:
        for k,v in zip(X.columns, importance):
            print('Feature', k, ':', round(v,2))

    # plot feature importance
    if plot:
        save_plot(X.columns, importance, 'svm.png', dir)

    return metrics_dict


def perm_knn(X,y, X_test, dir, n_features_to_select, print_features = True):
    # define the model
    model = KNeighborsClassifier()
    # fit the model
    model.fit(X, y)
    # perform permutation importance
    results = permutation_importance(model, X, y, scoring='accuracy')
    # get importance
    importance = results.importances_mean

    dict_name_score = dict(zip(X.columns, importance))
    max_scores = sorted(importance)[-n_features_to_select:]
    selected_feat_names = [k for k, v in dict_name_score.items() if v in max_scores]

    # summarize feature importance
    if print_features:
        for i,v in enumerate(importance):
            print('Feature: %0d, Score: %.5f' % (i,v))
    # plot feature importance
    save_plot(X.columns, importance, 'perm_knn.png', dir)
    return selected_feat_names 

 
def chi_2(X_train, y_train, X_test, dir, n_features_to_select, print_features = True):
    # feature selection
    X_train_fs, X_test_fs, fs = select_features(X_train, y_train, X_test, chi2)

    dict_name_score = dict(zip(fs.get_feature_names_out(), fs.scores_))
    max_scores = sorted(fs.scores_)[-n_features_to_select:]
    selected_feat_names = [k for k, v in dict_name_score.items() if v in max_scores]

    # Print all feature scores
    if print_features:
        for k,v in dict_name_score.items():
            print('Feature', k, ':', round(v,2))

    # plot the scores
    save_plot(X_train.columns, fs.scores_, 'chi_2.png', dir)
    return selected_feat_names


def mutual_inf(X_train, y_train, X_test, dir, n_features_to_select, print_features = True):
    # feature selection
    X_train_fs, X_test_fs, fs = select_features(X_train, y_train, X_test, mutual_info_classif)
    

    dict_name_score = dict(zip(fs.get_feature_names_out(), fs.scores_))
    max_scores = sorted(fs.scores_)[-n_features_to_select:]
    selected_feat_names = [k for k, v in dict_name_score.items() if v in max_scores]

    # Print all feature scores
    if print_features:
        for k,v in dict_name_score.items():
            print('Feature', k, ':', round(v,2))

    # plot the scores
    save_plot(X_train.columns, fs.scores_, 'mutual_inf.png', dir)
    return selected_feat_names


def categorical_corr(df, dir):
    cols = df.columns
    corrM = np.zeros((len(cols),len(cols)))
    for col1, col2 in combinations(cols, 2):
        idx1, idx2 = cols.get_loc(col1), cols.get_loc(col2)
        corrM[idx1, idx2] = cramers_corrected_stat(pd.crosstab(df[col1], df[col2]))
        corrM[idx2, idx1] = corrM[idx1, idx2]

    corr = pd.DataFrame(corrM, index=cols, columns=cols)
    save_plot_sns(corr, 'categorical_correlation.png', dir)


def unc_coeff(df, dir):
    cols = df.columns
    corrM = np.zeros((len(cols),len(cols)))
    for col1, col2 in combinations(cols, 2):
        idx1, idx2 = cols.get_loc(col1), cols.get_loc(col2)
        corrM[idx1, idx2] = theils_u(df[col1], df[col2])
        corrM[idx2, idx1] = corrM[idx1, idx2]

    corr = pd.DataFrame(corrM, index=cols, columns=cols)
    save_plot_sns(corr, 'uncertainty_coefficients.png', dir)

def anova(X_train, y_train, X_test, dir, n_features_to_select, print_features = True):
    # feature selection
    X_train_fs, X_test_fs, fs = select_features(X_train, y_train, X_test, f_classif)

    dict_name_score = dict(zip(fs.get_feature_names_out(), fs.scores_))
    max_scores = sorted(fs.scores_)[-n_features_to_select:]
    selected_feat_names = [k for k, v in dict_name_score.items() if v in max_scores]

    # Print all feature scores
    if print_features:
        for k,v in dict_name_score.items():
            print('Feature', k, ':', round(v,2))

    # plot the scores
    save_plot(X_train.columns, fs.scores_, 'anova.png', dir)
    return selected_feat_names





    



