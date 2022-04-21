def TP(y_true, y_pred): # count how many true positives
    count = 0
    for i in range(len(y_true)):
        if y_true[i] == 1 and y_pred[i] == 1:
            count += 1
    return count

def FP(y_true, y_pred): # count how many false positives
    count = 0
    for i in range(len(y_true)):
        if y_true[i] == 0 and y_pred[i] == 1:
            count += 1
    return count

def TN(y_true, y_pred): # count how many true negatives
    count = 0
    for i in range(len(y_true)):
        if y_true[i] == 0 and y_pred[i] == 0:
            count += 1
    return count

def FN(y_true, y_pred): # count how many false negatives
    count = 0
    for i in range(len(y_true)):
        if y_true[i] == 1 and y_pred[i] == 0:
            count += 1
    return count

def precision(y_true, y_pred):
    return TP(y_true, y_pred)/(TP(y_true, y_pred) + FP(y_true, y_pred))

def recall(y_true, y_pred):
    return TP(y_true, y_pred)/(TP(y_true, y_pred) + FN(y_true, y_pred))

def F1_score(y_true, y_pred):
    return 2 * (precision(y_true, y_pred) * recall(y_true, y_pred)) / (precision(y_true, y_pred) + recall(y_true, y_pred))
