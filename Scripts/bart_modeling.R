install.packages("bartMachine", dependencies=TRUE)
setwd("/Users/rakeshravi/Documents/GitHub/Sites/bayesian_cyber/")
library(BART)
library(BayesTree)
library(bartMachine)
library(BayesTree)
library(logitnorm)
library(caret)
rm(list =ls())
X.train = read.csv("X_train.csv")
y.train = read.csv("y_train.csv")
y.train$Malicious <- as.factor(y.train$Malicious)
levels(y.train) <- c("1","0")
X.test = read.csv("X_test.csv")
y.test = read.csv("y_test.csv")
y.test$Malicious <- as.factor(y.test$Malicious)
bartFit = bart(X.train, y.train$Malicious, X.test,ndpost=400)
fit <- bartMachine(X.train, y.train$Malicious, num_burn_in = 1000,
                   num_iterations_after_burn_in = 5000)
y_hat = predict(fit, X.test, type = "class")
confusionMatrix(y_hat, y.test$Malicious)

plot_convergence_diagnostics(fit)
