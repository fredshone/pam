from .core import Population, Household, Person, Activity, Leg
import random


class Policy:

    def __init__(self):
        self.population = Population

    def apply_to(self, household):
        raise NotImplementedError


class HouseholdQuarantined(Policy):
    """
    Probabilistic everyone in household stays home
    """

    def __init__(self, probability):
        super().__init__()

        assert 0 < probability <= 1
        self.probability = probability

    def apply_to(self, household):
        if random.random() < self.probability:
            for pid, person in household.people.items():
                person.plan = []
                person.add(Activity(1, 'home', household.area, start_time=None, end_time=None))


class PersonStayAtHome(Policy):
    """
    Probabilistic person stays home
    """

    def __init__(self, probability):
        super().__init__()

        assert 0 < probability <= 1
        self.probability = probability

    def apply_to(self, household):
        for pid, person in household.people.items():
            if random.random() < self.probability:
                person.plan = []
                person.add(Activity(1, 'home', household.area, start_time=None, end_time=None))


class RemoveEducationActivity(Policy):
    """
    Probabilistic remove activities
    """

    def __init__(self, probability):
        super().__init__()

        assert 0 < probability <= 1
        self.probability = probability

    def apply_to(self, household):
        for pid, person in household.people.items():

            seq = 0
            while seq < len(person.plan):
                p = person.plan[seq]
                is_education = p.act.lower() in ['education', 'education_escort']
                selected = random.random() < self.probability
                if is_education and selected:
                    person.remove_activity(seq)
                    seq -= 1
                else:
                    seq += 1




    # if plan[seq-2].act == plan[seq+2].act and plan[seq-2].area == plan[seq+2].area:
    #     new_plan = plan[:seq-1] + plan[seq+2:]
    #     new_plan[seq-2].end_time = plan[seq+2].end_time
    #     del new_plan[seq-1]
    #
    # else:  # need new leg
    #     leg_duration = 0
    #     mode = 0
    #     # todo
    #     raise NotImplementedError
    #
    # return new_plan


def apply_policies(population: Population, policies: list):

    """
    Apply policies to modify population.
    :param population:
    :param policies:
    :return:
    """

    for hid, household in population.households.items():
        for policy in policies:
            policy.apply_to(household)

