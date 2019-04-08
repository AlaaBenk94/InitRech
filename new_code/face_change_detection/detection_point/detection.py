import face_recognition

class facedetection:

    def __init__(self):
        self.col = {'right_eyebrow': [255, 255, 0]
            , 'right_eye': [0, 0, 255]
            , 'left_eyebrow': [255, 255, 0]
            , 'left_eye': [0, 0, 255]
            , 'nose_bridge': [0, 255, 255]
            , 'nose_tip': [0, 255, 255]
            , 'top_lip': [0, 0, 128]
            , 'bottom_lip':[0, 0, 128]
            , 'chin': [255, 0, 0]
               }

        self.vectelem=[
            'right_eyebrow'
            ,'right_eye'
            ,'left_eyebrow'
            ,'left_eye'
            ,'nose_bridge'
            ,'nose_tip'
            ,'top_lip'
            ,'bottom_lip'
            ,'chin'
            ,'facepos'
        ]


    def get_vecteur(self,img):
        vecteur={}
        face_landmarks_list = face_recognition.face_landmarks(img)
        facepos = face_recognition.face_locations(img)
        for k in range(len(face_landmarks_list)):
            ps = face_landmarks_list[k]

            for y in ps:
                 p = face_landmarks_list[k][y]
                 vecteur[y]=p
                 z = 0
                 for i in p:
                    #if(z==3 or z==0):
                        for j in range(-2, 3):
                            img[i[1] + j, i[0]] = self.col[y]
                        for j in range(-2, 3):
                            img[i[1], i[0] + j] = self.col[y]
                    #z = z + 1

        if(len(facepos)>0):
         vecteur['facepos']=facepos

        #img[facepos[j][2], facepos[j][3]] = [124, 252, 0]

        for j in range(len(facepos)):
            for i in range(facepos[j][0], facepos[j][2]):
                img[i, facepos[j][1]] = 0#[124, 252, 0]
                img[i, facepos[j][3]] = 0#[124, 252, 0]

            for i in range(facepos[j][3], facepos[j][1]):
                img[facepos[j][0], i] = 0# [124, 252, 0]
                img[facepos[j][2], i] = 0#[124, 252, 0]

        return vecteur,img