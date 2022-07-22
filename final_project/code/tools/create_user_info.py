import allure
import faker

from final_project.code.tools.randomizer import RandomGenerate


class UserInfo:
    def __init__(self):
        self.fake = faker.Faker()

    @allure.step("Создание персональных даннных")
    def create_human_data(self, option_middle_name=0):
        human_data = {}
        human_data["name"] = self.fake.name().split(" ")[0]
        human_data["surname"] = self.fake.name().split(" ")[1]
        if option_middle_name:
            human_data["middle_name"] = human_data["name"] + human_data["surname"]

        return human_data

    @allure.step("Создание юзерских даннных")
    def create_user_data(self):
        user_data = {}
        user_data["username"] = RandomGenerate.generate_random_user_name()
        user_data["password"] = RandomGenerate.generate_random_password()
        user_data["email"] = RandomGenerate.generate_random_email()

        return user_data
