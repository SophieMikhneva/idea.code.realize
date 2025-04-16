from datetime import datetime
#Модель учебного материала
class Material:
    def __init__(self, id, title, author_id, file_path, material_type, parent_id=None):
        """
        Модель учебного материала

        id: уникальный идентификатор
        title: название материала
        author_id: ID пользователя, загрузившего материал
        file_path: путь к файлу на сервере
        material_type: тип материала (презентация, статья и т.д.)
        parent_id: если это дополнение к другому материалу
        """
        self.id = id
        self.title = title
        self.author_id = author_id
        self.file_path = file_path
        self.material_type = material_type
        self.rating = 0.0
        self.ratings_count = 0
        self.parent_id = parent_id
        self.created_at = datetime.now()

    def rate(self, new_rating: int):
        """Обновляет рейтинг материала"""
        self.rating = (self.rating * self.ratings_count + new_rating) / (self.ratings_count + 1)
        self.ratings_count += 1