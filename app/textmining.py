from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score


class TextMiner(object):
	'''
	Gets related words based on a list of texts and the query

	KMeans normally works with numbers only: we need to have numbers. 
	To get numbers, we do a common step known as feature extraction.
	The feature used is TF-IDF, a numerical statistic. 
	This statistic uses term frequency and inverse document frequency. 
	In short: we use statistics to get to numerical features.

	The method TfidfVectorizer() implements the TF-IDF algorithm. 
	Briefly, the method TfidfVectorizer converts a collection of raw 
	documents to a matrix of TF-IDF features

	After we have numerical features, we initialize the KMeans algorithm 
	with K=number of documents.
	then print the top words per cluster

	'''
	def get_cluster_terms(self, query, documents):
		#print(documents)
		prediction_list = []		
		vectorizer = TfidfVectorizer(stop_words='english')#converts a collection of raw documents to a matrix of TF-IDF features
		#print(vectorizer)
		X = vectorizer.fit_transform(documents) #Learn vocabulary and idf, return term-document matrix.
		#print(X)
		true_k = len(documents) 
		print(true_k)
		model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
		model.fit(X) #Compute K-Means Clustering
		order_centroids = model.cluster_centers_.argsort()[:, ::-1]
		terms = vectorizer.get_feature_names()
		'''
		for i in range(true_k):
			print("Cluster %d:" % i),
			for ind in order_centroids[i, :5]:
				print(' %s' % terms[ind]),
		'''
		Y = vectorizer.transform([query]) #Prediction to figure out which cluster the query belongs
		prediction = model.predict(Y) #Predict the closest cluster each sample in X belongs to.
		for ind in order_centroids[int(prediction), :8]:
			prediction_list.append(terms[ind])
		return prediction_list

'''		
print(TextMiner().get_cluster_terms("devices", ["This little kitty came to play when I was eating at a restaurant.",
             "Merley has the best squooshy kitten belly.",
             "Google Translate app is incredible.",
             "If you open 100 tab in google you get a smiley face.",
             "Best cat photo I've ever taken.",
             "Climbing ninja cat.",
             "Impressed with google map feedback.",
             "Key promoter extension for Google Chrome."])) 
'''

