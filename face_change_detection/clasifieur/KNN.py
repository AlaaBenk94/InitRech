from face_change_detection.Distence.distense import distence

class KNN :
    def prediction(self,X,base,K):
        x=[0]+X # ajouter une etiq
        knn=[]
        knn_dist=[]
        calcdis=distence()
        for i in range(K):
            knn.append(base[i])
            knn_dist(calcdis.cartesienne(base[i],x))

        for i in range(len(K),len(base)):
            dis=calcdis.cartesienne(x,base[i])
            mini=False
            for j in range(K):
                if dis < knn_dist[j]:
                    mini=True
                    break
            if(mini):
                ind=knn_dist.index(max(knn_dist))
                knn_dist.pop(ind)
                knn.pop(ind)
                knn_dist.append(dis)
                knn.append(base[i])

        classes=[]
        freq=[]

        for i in knn :
            if(i[0] not in classes):
                classes.append(i[0])
                freq.append(0)
            ind=classes.index(i[0])
            freq[ind]=freq[ind]+1

        x[0]=classes[freq.index(min(freq))]

        return x