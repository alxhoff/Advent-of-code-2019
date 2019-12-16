#!/bin/python

import math
import re




class MaterialAmount:
    def __init__(self, info):

        self.material = info[1]
        self.quantity = int(info[0])


class Conversion:
    def __init__(self, output, inputs):

        self.output = output
        self.inputs = inputs

def insert_list(out_list, list_to_insert, pos):

    for i in range(len(list_to_insert)):
        out_list.insert(i + pos, list_to_insert[i])

class RecipeBook:
    def __init__(self):

        self.conversions = self._get_input()

        self.recipe = self._find_conversion('FUEL')

        self.waste = dict()

    def _get_input(self):
        conversions = []

        for line in iter(input, ""):
            regex_line = re.findall(r"(\d+) ([A-Z]+)", line)
            no_inputs = len(regex_line) - 1

            output = MaterialAmount(regex_line[-1])
            inputs = list(map(MaterialAmount, regex_line[:-1]))

            conversions.append(Conversion(output, inputs))

        return conversions

    def _get_waste(self, material):
        if material not in self.waste:
            self.waste[material] = 0

        return self.waste[material]

    def _set_waste(self, material, amount):

        if material not in self.waste:
            self.waste[material] = amount
            return
        else:
            self.waste[material] = amount

    def _add_waste(self, material, amount):

        current = self._get_waste(material)

        current += amount

        self._set_waste(material, current)

    def _use_waste(self, material, amount):

        current = self._get_waste(material)

        current -= amount

        self._set_waste(material, current)

    def iterate(self):

        # for each item in recipe, try to replace item with it's own recipe
            #first check for existing units that could be used
                # use existing units

            # perfom substitution

        all_ore = False

        while not all_ore:
            new_recipe = []
            all_ore = True

            for input in self.recipe.inputs:

                if input.material == 'ORE':
                    new_recipe.append(input)
                    continue

                all_ore = False

                recipe = self._find_conversion(input.material)

                required_amount = input.quantity

                existing_amount = self._get_waste(input.material)

                required_amount_after_using_waste = required_amount

                if existing_amount:
                    if existing_amount >= required_amount:
                        self._use_waste(input.material, required_amount)
                        required_amount_after_using_waste = 0
                    else:
                        self._use_waste(input.material, existing_amount)
                        required_amount_after_using_waste -= existing_amount

                output_batch_size = recipe.output.quantity

                batches_required = math.ceil(required_amount_after_using_waste/output_batch_size)

                produced_amount = batches_required * output_batch_size

                waste_produced = produced_amount - required_amount_after_using_waste

                self._add_waste(input.material, waste_produced)

                for mat in recipe.inputs:

                    new_recipe.append(MaterialAmount([batches_required * mat.quantity, mat.material]))

            self.recipe.inputs = new_recipe

        total_ore = 0

        for input in self.recipe.inputs:
            total_ore += input.quantity

        print("total ore: {}".format(total_ore))

    def print_recipe(self, recipe):

        inputs = ""
        for input in recipe.inputs:
            inputs += " {} x {} ".format(input.quantity, input.material)

        print("{} X {} <= {}".format(recipe.output.quantity, recipe.output.material, inputs))

    def _find_conversion(self, material):

        for conversion in self.conversions:
            if conversion.output.material == material:
                return conversion

        return None



rb = RecipeBook()
rb.iterate()
rb.print_recipe(rb.recipe)

#  print("Ore for fuel: {}".format(rb.getOreForFuel()))
