# Fil Rouge ICO 2024 

## Objective
Compare the result of multiple methods to solve the Vehicle Routing Problem (VRP) with a restriction on carrying capacity

## Problem description

The problem consists of a generalisation of the classic traveling salesman problem where, instead of a single agent visiting every node in the graph, there's a group of agents that must achieve the same feat. In other words, given *n* agents, a graph and a starting point in said graph a solution is a set of *n* *cycles*, all including the starting point, with the condition that, jointly, these cycles contain all nodes in the graph only once.

The second part of the problem's definition, the carrying capacity restriction, imposes that the sum of the value of each node in a cycle must not exceed the capacity of the agent responsible for it.

### Input
- *n* : the number of agents 
- *graph*: adjacency matrix with the cost of each edge
- *values*: an array with a value for each node

### Output
- *path*: a path containing *n* cycles that passes every node in the graph at most once 