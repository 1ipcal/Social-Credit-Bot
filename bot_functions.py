import json


def get_credits(user_id: int) -> int:
    """
    Returns the Social Credits of the user

    :param int user_id: Discord Id of the user in question
    :return: int social credit of the user
    """
    # Check if the user is in the JSON file
    make_user_data(user_id)

    # Get dictionary
    dict = get_user_data()

    return dict[str(user_id)]["socialCredits"]


def add_credits(user_id: int, num_credits: int) -> int:
    """
    Adds and returns the new social credit of the user

    :param int user_id: Discord Id of the user in question
    :param int num_credits: amount of credits to be added
    :return: int - NEW social credit of the user
    """
    # Check if the user is in the JSON file
    make_user_data(user_id)

    # Get dictionary
    dict = get_user_data()

    # Add Credits
    dict[str(user_id)]["socialCredits"] += num_credits
    new_credit = dict[str(user_id)]["socialCredits"]

    # Save Changes
    with open("citizens.json", "w") as file:
        dict = json.dump(dict, file, indent=4)

    return new_credit

def remove_credits(user_id: int, num_credits: int) -> int:
    """
    Subtracts and returns the new social credit of the user

    :param int user_id: Discord Id of the user in question
    :param int num_credits: amount of credits to be added
    :return: int - NEW social credit of the user
    """
    # Check if the user is in the JSON file
    make_user_data(user_id)

    # Get dictionary
    dict = get_user_data()

    # Add Credits
    dict[str(user_id)]["socialCredits"] -= num_credits
    new_credit = dict[str(user_id)]["socialCredits"]

    # Save Changes
    with open("citizens.json", "w") as file:
        dict = json.dump(dict, file, indent=4)

    return new_credit

def set_credits(user_id: int, set_credits: int) -> int:
    """
    Hard sets and returns the new social credit of the user

    :param int user_id: Discord Id of the user in question
    :param int set_credits: amount of credits to be added
    :return: int - NEW social credit of the user
    """
    # Check if the user is in the JSON file
    make_user_data(user_id)

    # Get dictionary
    dict = get_user_data()

    # Add Credits
    dict[str(user_id)]["socialCredits"] = set_credits
    new_credit = dict[str(user_id)]["socialCredits"]

    # Save Changes
    with open("citizens.json", "w") as file:
        dict = json.dump(dict, file, indent=4)

    return new_credit

# Helper Function. Gets user data
def get_user_data():
    with open("citizens.json", "r") as file:
        dict = json.load(file)
        return dict


# Helper Function. Adds user to citizen file
def make_user_data(user_id: int) -> bool:
    """
    Adds the user to the json file. If the user exists, do nothing

    :param int user_id: Discord Id of the user in question
    :return: bool if an entry in the JSON file is created or not
    """
    dict = get_user_data()

    # Check if the user exists in the system
    if str(user_id) in dict:
        return False
    else:
        # Make a new user. Default starting with 1000
        dict[str(user_id)] = {}
        dict[str(user_id)]["socialCredits"] = 1000

        with open("citizens.json", "w") as file:
            dict = json.dump(dict, file, indent=4)

        return True
