import math
import random
from matplotlib import pyplot as plt

class ACO:
    class Edge:
        def __init__(self, a, b, weight, initial_pheromone):
            self.a = a
            self.b = b
            self.weight = weight #euclidean
            self.pheromone = initial_pheromone

    class Ant:
        def __init__(self, alpha, beta, num_nodes, edges):
            self.alpha = alpha
            self.beta = beta
            self.num_nodes = num_nodes
            self.edges = edges
            self.tour = None
            self.distance = 0.0

        def _select_node(self): #roulette wheel
            total_sum = 0.0
            unvisited_nodes = [node for node in range(self.num_nodes) if node not in self.tour] 
            heuristic_total = 0.0
            for unvisited_node in unvisited_nodes:
                heuristic_total += self.edges[self.tour[-1]][unvisited_node].weight 
            for unvisited_node in unvisited_nodes:
                total_sum += pow(self.edges[self.tour[-1]][unvisited_node].pheromone, self.alpha) * \
                                  pow((heuristic_total / self.edges[self.tour[-1]][unvisited_node].weight), self.beta) 
            random_value = random.uniform(0.0, total_sum)
            partial_sum = 0.0
            for unvisited_node in unvisited_nodes:
                partial_sum += pow(self.edges[self.tour[-1]][unvisited_node].pheromone, self.alpha) * \
                                  pow((heuristic_total / self.edges[self.tour[-1]][unvisited_node].weight), self.beta)
                if partial_sum >= random_value:
                    return unvisited_node
            
        def find_tour(self):
            self.tour = [random.randint(0, self.num_nodes - 1)]
            while len(self.tour) < self.num_nodes:
                self.tour.append(self._select_node())
            return self.tour

        def get_distance(self):
            self.distance = 0.0
            for i in range(self.num_nodes):
                self.distance += self.edges[self.tour[i]][self.tour[(i + 1) % self.num_nodes]].weight
            return self.distance

    def __init__(self, colony_size=10, alpha=1.0, beta=3.0, rho=0.1, pheromone_deposit_weight=1.0, initial_pheromone=1.0, steps=100, nodes=None):
        self.colony_size = colony_size
        self.rho = rho
        self.pheromone_deposit_weight = pheromone_deposit_weight
        self.steps = steps
        self.num_nodes = len(nodes)
        self.nodes = nodes
        self.labels = range(1, self.num_nodes + 1)
        self.edges = [[None] * self.num_nodes for _ in range(self.num_nodes)]
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                self.edges[i][j] = self.edges[j][i] = self.Edge(i, j, math.sqrt(
                    pow(self.nodes[i][0] - self.nodes[j][0], 2.0) + pow(self.nodes[i][1] - self.nodes[j][1], 2.0)),
                                                                initial_pheromone)
        self.ants = [self.Ant(alpha, beta, self.num_nodes, self.edges) for _ in range(self.colony_size)]
        self.global_best_tour = None
        self.global_best_distance = float("inf")

    def _add_pheromone(self, tour, distance, weight=1.0):
        pheromone_to_add = self.pheromone_deposit_weight / distance
        for i in range(self.num_nodes):
            self.edges[tour[i]][tour[(i + 1) % self.num_nodes]].pheromone += weight * pheromone_to_add
            
    def _aco(self):
        for step in range(self.steps):
            for i in range(self.num_nodes):
                  for j in range(i + 1, self.num_nodes):
                      self.edges[i][j].pheromone *= (1.0 - self.rho) 
            for ant in self.ants:
                self._add_pheromone(ant.find_tour(), ant.get_distance())
                if ant.distance < self.global_best_distance:
                    self.global_best_tour = ant.tour
                    self.global_best_distance = ant.distance

    def run(self):
        self._aco()
        print('Sequence : <- {0} ->'.format(' - '.join(str(self.labels[i]) for i in self.global_best_tour)))
        print('Total distance travelled to complete the tour : {0}\n'.format(round(self.global_best_distance, 2)))

    def plot(self, point_radius=math.sqrt(2.0), save=True, name=None):
        x = [self.nodes[i][0] for i in self.global_best_tour]
        x.append(x[0])
        y = [self.nodes[i][1] for i in self.global_best_tour]
        y.append(y[0])
        plt.plot(x, y, linewidth=2)
        plt.scatter(x, y, s=math.pi * (point_radius ** 2.0))
        for i in self.global_best_tour:
            plt.annotate(self.labels[i], self.nodes[i], size=10)
        if save:
            if name is None:
                name = '{0}.png'
            plt.savefig(name, dpi=200)
        plt.show()
        plt.gcf().clear()


if __name__ == '__main__':
    _colony_size = 4
    _steps = 100
    _nodes = [(-4,4),(16,-5),(22,8),(0,-16),(3,-19),(24,-20),(24,-15),(16,-1),(10,-15),(-7,-2),(13,10),(17,-6),(19,1),(19,-16),(-8,-8),(-4,-1),(20,-3),(17,-17),(-2,9),(23,-24),(31,-26),(37,-20),(30,-30),(26,-22),(37,-16),(25,-18),(17,-30),(26,-28),(27,-15),(18,-24)]
    #print(_nodes)
    choice=1
    while choice!=0:
        print("0. Exit")
        print("1. Append")
        print("2. Delete")
        print("3. Edit")
        print("4. Show")
        choice=int(input("Enter choice: "))
        if choice==1:
            x=int(input("Enter x : "))
            y=int(input("Enter y : "))
            _nodes.append((x,y))
            print("City Coords: ", _nodes)
        elif choice==2:
            n=int(input("Enter index to remove: "))
            _nodes.pop(n)
            print("City Coords: ", _nodes) 
        elif choice==3:
            n=int(input("Enter index to edit: "))
            x=int(input("Enter x : "))
            y=int(input("Enter y : "))
            _nodes[n]=(x,y)
            print("City Coords: ", _nodes)
        elif choice==4:
            acs = ACO(colony_size=_colony_size, steps=_steps, nodes=_nodes)
            acs.run()
            acs.plot()
        elif choice==0:
            print("Exiting!")
        else:
            print("Invalid choice!!")
