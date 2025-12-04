import logging
import random
from collections.abc import Sequence
from copy import deepcopy

from investopy.genetic.termination import Stagnation
from .chromosome import StockChromosome
from .definitions import Population, Selection, Recombination, Reproduction, Mutation, Termination
from .gene import StockGene
from .objective_function import IndexWeight


class StockPopulation(Population):

    def __init__(self, size: int,
                 genome: Sequence[StockGene],
                 selection: Selection,
                 recombination: Recombination,
                 reproduction: Reproduction,
                 mutation: Mutation,
                 objective: IndexWeight,
                 termination: Termination):
        super().__init__(selection, recombination, reproduction, mutation, objective, termination)
        self.size = size
        self.genome = genome

    def evolve(self, gene_lower_limit: int, gene_upper_limit: int) -> Sequence[StockChromosome]:
        if gene_lower_limit <= 0:
            logging.error("Gene parameter cannot be 0 or less")
            return []
        # Initial population
        population = self.get_initial_population(gene_lower_limit, gene_upper_limit)
        # Set condition if a condition is required
        if isinstance(self.termination, Stagnation):
            self.termination.condition = deepcopy(population)
        generation = 1
        while not self.termination.terminate():
            survivors = self.selection.get_survivors(population)
            pairs = self.recombination.pair(survivors)
            # Breed each pair of parents
            children = []
            for parent_pair in pairs:
                [children.append(child) for child in self.reproduction.breed(parent_pair)]
            # Mutate children
            for child in children:
                self.mutation.mutate(child)
            # Update population and their fitness
            population = [*survivors, *children]
            for individual in population:
                individual.fitness = self.objective.fitness(individual)
            # Sort by highest fitness first
            population.sort(key=lambda individual: individual.fitness, reverse=True)
            if isinstance(self.termination, Stagnation):
                self.termination.condition = deepcopy(population)
            generation += 1
            # Logg
            if generation % 1000 == 0:
                print("Generation: ", generation,
                      "Average fitness: ", sum([individual.fitness for individual in population]) / len(population),
                      "Best individual: ", population[0])
        return population

    def get_initial_population(self, lower_limit: int, upper_limit: int) -> Sequence[StockChromosome]:
        population = []
        for _ in range(self.size):
            genome = deepcopy(self.genome)
            # Set random initial gene parameters for each individual
            for gene in genome:
                gene.parameter = random.randint(lower_limit, upper_limit)
            chromosome = StockChromosome(genes=genome)
            # Set fitness
            chromosome.fitness = self.objective.fitness(chromosome)
            population.append(chromosome)
        # Sort by highest fitness and return population
        return sorted(population, key=lambda individual: individual.fitness, reverse=True)


if __name__ == "__main__":
    ib_pop = StockPopulation()
    ib_pop.selection = tuple([0])
