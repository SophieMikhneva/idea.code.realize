class Repository:
    def __init__(self, id, name, owner_id):
        """
        Модель группы материалов
        id: уникальный идентификатор
        name: название репозитория
        owner_id: ID владельца (пользователя)
        """
        self.id = id
        self.name = name
        self.owner_id = owner_id
        self.materials = []  # список ID материалов

    def add_material(self, material_id: int):
        """Добавляет материал в репозиторий"""
        if material_id not in self.materials:
            self.materials.append(material_id)