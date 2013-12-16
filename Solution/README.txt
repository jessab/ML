------------------------------------
README
------------------------------------

This program can be used for both classification of one sample or to perform experiment on whole datasets.


------------------------------------
SETUP
------------------------------------
To setup the program...


------------------------------------
CLASSIFY
------------------------------------
To indicate you want to classify, use the keyword 'classify' followed by the path to the ankle data  and this again followed by the path to the hip data.

several options can be set:

The class to predict:
	keyword:	'-c'
	possibilities: 	trained, surface, combined
	default: 	trained

The classification algorithm to use:
	keyword:	'-a'
	possibilities:	SVM, DT, KNN, LogReg
	default: 	SVM

The method to select features: 
	keyword:	'-f'
	possibilities:	all, 
			K n (KBest, n is the number of features),
			KUC (KBestUncorrelated, n is the number of features),
			RFECV (Recursive Feature Elimination Cross Validation, can only be used in combination with SVM or LogReg)
	default:	RFECV


examples:
	$programmanaam$ classify C:\anklePath C:\hipPath -a DT -f KUC 10 (classify trained with decision trees, using the k best, filtered on correlation
	$programmanaam$ classify C:\anklePath C:\hipPath -c combined -a LogReg (classify combined with Logistic Regression using RFECV)

------------------------------------
EXPERIMENT
------------------------------------
Experimenting means obtaining the cross validation values for all classes with all classification algorithms. You can specify which feature selection to use.

To indicate you want to experiment, use the keyword 'experiment'

optionally the method to select features can be set:
	keyword:	'-f'
	possibilities:	all, 
			K n (KBest, n is the number of features),
			KUC (KBestUncorrelated, n is the number of features),
			RFECV (Recursive Feature Elimination Cross Validation, will only return info on SVM or LogReg)
	default:	all


examples:
	$programmanaam$ experiment (prints the cross validation values for all classes with all classification algorithms using all features)
	$programmanaam$ experiment -f K 10 (prints the cross validation values for all classes with all classification algorithms using the K best features)