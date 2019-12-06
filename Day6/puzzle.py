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


class mapping:
    def __init__(self, center, orbiting):
        self.center = center
        self.orbiting = orbiting


class orbitParser:
    def parse_mappings(self):
        for mapping in self.mappings:
            if not mapping.center in self.objects:
                self.objects[mapping.center] = object(mapping.center)

            if not mapping.orbiting in self.objects:
                self.objects[mapping.orbiting] = object(mapping.orbiting)

            self.objects[mapping.orbiting].set_parent(self.objects[mapping.center])

        self.count_orbits()

    def count_orbits(self):
        orbits = 0
        for key, value in self.objects.items():
            orbits += value.count_parents()
        print("Orbits = {}".format(orbits))

    def __init__(self):
        self.mappings = []
        self.objects = dict()
        for line in iter(input, ""):
            bodies = line.split(")")
            self.mappings.append(mapping(bodies[0], bodies[1]))


op = orbitParser()
op.parse_mappings()
