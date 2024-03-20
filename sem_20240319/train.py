from sklearn import svm
from sklearn import datasets
from joblib import dump

clf = svm.SVC()
X, y = datasets.load_iris(return_X_y=True)
clf.fit(X, y)
dump(clf, 'model.joblib')