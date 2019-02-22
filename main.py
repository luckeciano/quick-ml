from data_ingestor import DataIngestor
from metrics_tracker import MetricsTracker
import matplotlib.pyplot as plt
from linear_regression import LinearRegression
from logistic_regression import LogisticRegression
from linear_regression_mle import LinearRegressionMLE
import numpy as np


def main():
    #test_linear_regression()
    #test_logistic_regression()
    #test_linear_regression_mle_simple()
    test_linear_regression_mle_poly()

def test_logistic_regression():
    data_ingestor = DataIngestor()
    metrics_tracker = MetricsTracker()
    train_x, train_y = data_ingestor.read_csv("train_india_diabetes.csv")
    print("Shape train_x: " + str(train_x.shape))
    print("Shape train_y: " + str(train_y.shape))
    

    logisticRegression = LogisticRegression()
    accuracies, costs = logisticRegression.train(train_x, train_y, nb_epochs=100000, batch_size=128, lr=0.001)
    test_y_logistic = logisticRegression.predict(train_x) > 0.5

    print(test_y_logistic)
    print("Accuracy: " + str(metrics_tracker.accuracy(train_y, test_y_logistic)))

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex='col')
    ax1.plot(costs)
    ax2.plot(accuracies)
    plt.show()


def test_linear_regression():
    metrics_tracker = MetricsTracker()
    n_samples = 200
    x = np.linspace(0, 2 * np.pi, n_samples).reshape(n_samples, 1)
    noise = np.random.randn(x.shape[0]).reshape(n_samples, 1)
    y = -4*x + 7  + noise*2.0
    y.reshape(n_samples, 1)
    linearRegression = LinearRegression()
    metrics_tracker.profile(linearRegression.train, x, y, 1000, 128, 0.01)
    test_y_linear = metrics_tracker.profile(linearRegression.predict, x)
    err = metrics_tracker.mean_squared_error(test_y_linear, y)
    print("Squared Mean Error: " + str(err))

    plt.scatter(x, y)
    plt.plot(x, test_y_linear)
    plt.show()

def test_linear_regression_mle_simple():
    print("Test Linear Regression MLE:  ")
    metrics_tracker = MetricsTracker()
    n_samples = 200
    x = np.linspace(0, 2 * np.pi, n_samples).reshape(n_samples, 1)
    noise = np.random.randn(x.shape[0]).reshape(n_samples, 1)
    y = -4*x + 7  + noise*2.0
    y = y.reshape(n_samples, 1)

    linearRegressionMLE = LinearRegressionMLE()
    metrics_tracker.profile(linearRegressionMLE.train, x, y)
    test_y_linear = metrics_tracker.profile(linearRegressionMLE.predict, x)
    metrics_tracker.mean_squared_error(test_y_linear, y)
    err = metrics_tracker.mean_squared_error(test_y_linear, y)
    print("Squared Mean Error: " + str(err))

    plt.scatter(x, y)
    plt.plot(x, test_y_linear)
    plt.show()

def test_linear_regression_mle_poly():
    #This test shows how MLE is prone to overfitting
    print("Test Linear Regression MLE:  ")
    metrics_tracker = MetricsTracker()
    n_samples = 20
    initial_x = np.linspace(0, 2 * np.pi, n_samples).reshape(n_samples, 1)
    degree_x = 12
    noise = np.random.randn(initial_x.shape[0]).reshape(n_samples, 1)
    for degree_x in range(1, 12, 4):
        x = initial_x

        for i in range(2, degree_x + 1):
            x = np.concatenate((x, pow(initial_x, i)), axis = 1)


        
        y = -4.0*np.sin(initial_x) + noise*0.5
        y = y.reshape((n_samples, 1))


        linearRegressionMLE = LinearRegressionMLE()
        metrics_tracker.profile(linearRegressionMLE.train, x, y)
        test_y_linear = metrics_tracker.profile(linearRegressionMLE.predict, x)
        metrics_tracker.mean_squared_error(test_y_linear, y)
        err = metrics_tracker.mean_squared_error(test_y_linear, y)
        print("Squared Mean Error: " + str(err))

        print (test_y_linear.shape, y.shape, x[:,0].shape)

        
        plt.plot(x[:, 0], test_y_linear, label = str(degree_x))
    plt.scatter(x[:, 0], y)
    plt.legend(loc='best')
    plt.show()

main()