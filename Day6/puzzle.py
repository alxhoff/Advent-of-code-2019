#!/bin/python


class object:
    def __init__(self, identifier):

        self.identifier = identifier
        self.parent = None

    def set_parent(self, parent):

        self.parent = parent

    def count_parents(self):

        parents = 0
        iterator = self

        while (iterator.parent):
            parents += 1
            iterator = iterator.parent

        return parents

    def get_parents(self):

        parents = []
        iterator = self
        while (iterator.parent):
            parents.append(iterator.parent.identifier)
            iterator = iterator.parent

        return parents

    def steps_to_object(self, o_identifier):

        steps = -1
        iterator = self

        while (iterator.parent):
            steps += 1
            if iterator.parent.identifier == o_identifier:
                return steps
            else:
                iterator = iterator.parent

        return steps


class mapping:
    def __init__(self, center, orbiting):
        self.center = center
        self.orbiting = orbiting


class orbitParser:
    def __init__(self):
        self.mappings = []
        self.objects = dict()
        for line in iter(input, ""):
            bodies = line.split(")")
            self.mappings.append(mapping(bodies[0], bodies[1]))

    def find_common_objects(self):
        your_objects = self.objects["YOU"].get_parents()
        santas_objects = self.objects["SAN"].get_parents()

        return [object for object in your_objects if object in santas_objects]

    def parse_mappings(self):
        for mapping in self.mappings:
            if not mapping.center in self.objects:
                self.objects[mapping.center] = object(mapping.center)

            if not mapping.orbiting in self.objects:
                self.objects[mapping.orbiting] = object(mapping.orbiting)

            self.objects[mapping.orbiting].set_parent(
                self.objects[mapping.center])

        self.count_orbits()

    def count_orbits(self):
        orbits = 0
        for key, value in self.objects.items():
            orbits += value.count_parents()
        print("Orbits = {}".format(orbits))


op = orbitParser()
op.parse_mappings()

earliest_common_object = op.find_common_objects()[0]

my_steps = op.objects["YOU"].steps_to_object(earliest_common_object)
his_steps = op.objects["SAN"].steps_to_object(earliest_common_object)

print("Common object: {}, my steps: {}, his steps: {}, total steps: {}".format(
    earliest_common_object, my_steps, his_steps, my_steps + his_steps))
