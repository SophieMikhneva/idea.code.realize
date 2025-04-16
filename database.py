class DB:
    def __init__(self):
        self.materials = []
        self.users = []
        self.repositories = []

    def add_material(self, material):
        self.materials.append(material)
    def get_material(self, material_id):
        for material in self.materials:
            if material.id == material_id:
                return material
        return None

    def add_user(self, user):
        self.users.append(user)
    def get_user(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def add_repositories(self, repository):
        self.repositories.append(repository)
    def get_repositories(self, repository_id):
        for repository in self.repositories:
            if repository.id == repository_id:
                return repository
        return None