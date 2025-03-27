class Camera:
    def __init__(self, width, height):
        self.x_offset = 0  # Décalage horizontal de la caméra
        self.width = width
        self.height = height

    def update(self, target_x):
        """Met à jour la caméra en fonction de la position du joueur"""
        self.x_offset = target_x - self.width // 2  # Centre la caméra sur le joueur

    def apply(self, rect):
        """Applique le décalage caméra à un objet"""
        return rect.move(-self.x_offset, 0)