import dlib
from imutils import face_utils
from numpy import concatenate as cat

class landmarks:

    def __init__(self, predictor=None):
        """
        constructeur
        :param predictor: le chemin complet vers le model entraine
        """

        self.DEFAULT_PREDICTOR = "shape_predictor_68_face_landmarks.dat"
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor( (self.DEFAULT_PREDICTOR, predictor)[predictor is not None] )

    def extract_landmarks(self, img):
        """
        extraire les points de saillances du visage
        :param img l'image en greyscale
        :return un couple contenant le dictionnaire des composantes du visage et son centre
         """

        # detect faces in the grayscale frame)
        rect = self.target_face(self.detector(img, 0))

        if rect is not None:
            shape = self.points_dict(face_utils.shape_to_np(self.predictor(img, rect)))
            return shape, rect

        return ()

    def target_face(self, rects):
        """
        permet de recuperer le visage le cible parmi les visage detectes
        :param rects: les visages detectes
        :return: le visage cible le plus proche de la camera
        """

        maxRect = dlib.rectangle(0,0,0,0)

        for rect in rects:
            if rect.area() > maxRect.area():
                maxRect = rect

        return maxRect

    def points_dict(self, points):
        """
        regrouper les points de saillances dans un dictionnaires
        reference : https://cdn-images-1.medium.com/max/1600/1*AbEg31EgkbXSQehuNJBlWg.png
        :param points liste des points de saillances
        :return dictionnaires
        """
        return {
            "chin": points[0:17],
            "left_eyebrow": points[17:22],
            "right_eyebrow": points[22:27],
            "nose_bridge": points[27:31],
            "nose_tip": points[31:36],
            "left_eye": points[36:42],
            "right_eye": points[42:48],
            "top_lip": cat((points[48:55], [points[64]], [points[63]], [points[62]], [points[61]], [points[60]])),
            "bottom_lip": cat((points[54:60], [points[48]], [points[60]], [points[67]], [points[66]], [points[65]], [points[64]]))
        }
