import dlib
from imutils import face_utils


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
            return (shape, (rect.center().x, rect.center().y))

        return ()

    def target_face(self, rects: dlib.rectangles):
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
            'right_eyebrow': points[22:27],
            'right_eye': points[42:48],
            'left_eyebrow': points[17:22],
            'left_eye': points[36:42],
            'nose_bridge': points[27:31],
            'nose_tip': points[31:36],
            'mouth': points[48:68],
            'chin': points[0:17]
        }
