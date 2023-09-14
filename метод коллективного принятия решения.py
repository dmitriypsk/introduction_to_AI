import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# создаем коллектив решающих правил
class RuleEnsemble():
    
    def __init__(self, n_rules=5, max_depth=3, random_state=42):
        self.n_rules = n_rules
        self.max_depth = max_depth
        self.random_state = random_state
        self.rules = []
        self.weights = []

    def fit(self, X, y):
        for i in range(self.n_rules):
            # создаем правило, например, дерево решений
            rule = DecisionTreeClassifier(max_depth=self.max_depth, random_state=self.random_state+i)
            # обучаем правило на части данных
            sample_indices = np.random.choice(len(X), size=int(0.7*len(X)), replace=False)
            X_sample = X[sample_indices]
            y_sample = y[sample_indices]
            rule.fit(X_sample, y_sample)
            # вычисляем вес правила на основе его точности на оставшейся части данных
            y_pred = rule.predict(X[~sample_indices])
            weight = accuracy_score(y[~sample_indices], y_pred)
            # добавляем правило и его вес в коллектив
            self.rules.append(rule)
            self.weights.append(weight)

    def predict(self, X):
        # вычисляем прогноз каждого правила и умножаем на его вес
        rules_pred = np.array([rule.predict(X) for rule in self.rules])
        weighted_pred = np.multiply(rules_pred.T, self.weights).T
        # вычисляем средневзвешенный прогноз
        ensemble_pred = np.mean(weighted_pred, axis=0)
        return np.round(ensemble_pred)


X = np.random.rand(1000, 10)
y = np.random.randint(2, size=1000)

ensemble = RuleEnsemble(n_rules=5, max_depth=3, random_state=42)
ensemble.fit(X, y)

X_test = np.random.rand(100, 10)
y_pred = ensemble.predict(X_test)

print(y_pred)