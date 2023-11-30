from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture

def kmeans(k, data):
    cluster = KMeans(n_clusters=int(k), random_state=2407)
    labels = cluster.fit_predict(data)    
    return labels

def dbscan(eps, min_samples, data):
    cluster = DBSCAN(eps=eps, min_samples=min_samples).fit(data)
    labels = cluster.labels_    
    return labels

def GMM(clusters, data, probas = False):
    gm = GaussianMixture(n_components=clusters, random_state=2407)
    if probas:
        gm_fit = gm.fit(data)
        probas = gm_fit.predict_proba(data)
        return probas
    else:
        labels = gm.fit_predict(data)
        return labels

