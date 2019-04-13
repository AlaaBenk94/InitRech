import dlib
from imutils import face_utils
from numpy import concatenate as cat


class landmarks:
    COLORS = {'right_eyebrow': [255, 255, 0],
              'right_eye': [0, 0, 255],
              'left_eyebrow': [255, 255, 0],
              'left_eye': [0, 0, 255],
              'nose_bridge': [0, 255, 255],
              'nose_tip': [0, 255, 255],
              'top_lip': [0, 0, 128],
              'bottom_lip': [0, 0, 128],
              'chin': [255, 0, 0],
              "position": [0, 0, 0]}

    DEFAULT_PREDICTOR = "shape_predictor_68_face_landmarks.dat"

    def __init__(self, predictor=None):
        """
        constructeur
        :param predictor: le chemin complet vers le model entraine
        """

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor((self.DEFAULT_PREDICTOR, predictor)[predictor is not None])

    def extract_landmarks(self, img):
        """
        extraire les points de saillances du visage
        :param img l'image en greyscale
        :return un couple contenant le dictionnaire des composantes du visage et son centre
         """

        # recuperation de tous les visages sur l'image
        rects = self.detector(img, 0)

        # on sort si aucun visage DETECTE
        if rects.__len__() < 1:
            return False, None, None

        def target_face():
            maxRect = dlib.rectangle(0, 0, 0, 0)
            for rct in rects:
                if rct.area() > maxRect.area():
                    maxRect = rct
            return maxRect

        # detect faces in the grayscale frame)
        rect = target_face()

        # extraction des points de saillances
        points = face_utils.shape_to_np(self.predictor(img, rect))

        def points_dict():
            return {
                "chin": points[0:17],
                "left_eyebrow": points[17:22],
                "right_eyebrow": points[22:27],
                "nose_bridge": points[27:31],
                "nose_tip": points[31:36],
                "left_eye": points[36:42],
                "right_eye": points[42:48],
                "top_lip": cat((points[48:55], [points[64]], [points[63]], [points[62]], [points[61]], [points[60]])),
                "bottom_lip": cat((points[54:60], [points[48]], [points[60]], [points[67]], [points[66]], [points[65]], [points[64]])),
                "facepos": [(int(rect.left()), int(rect.top()), int(rect.right()), int(rect.bottom()))],
                "position": [[rect.center().x, rect.center().y]]
            }

        return True, points_dict(), rect


