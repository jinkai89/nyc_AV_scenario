from pyomo.environ import (
    maximize, value,
    AbstractModel, SolverFactory,
    Param, Constraint, Var, Objective, Set, RangeSet,
    NonNegativeReals, Binary
)


def add_params(model):
    """This function defines all parameters to the model"""
    # number of vertices
    model.n = Param()
    # vertices
    model.V = RangeSet(1, model.n)
    # extended vertices including 0 for the flow model
    model.W = RangeSet(0, model.n)
    # directed edges, E' in the paper
    model.E = Set(within=model.W * model.W)
    # cost values
    model.cost = Param(model.V)
    # utility values
    model.utility = Param(model.V)
    # terminal vertices
    model.T = Set(within=model.V)
    # bound on cost
    model.C = Param()


def add_vars(model):
    """This function defines all the variables of the model"""
    # This is equation (3) in the paper
    model.x = Var(model.V, domain=Binary)
    model.y = Var(model.E, domain=NonNegativeReals)


###########################################################
# constraint functions

def cost(model):
    # This is equation (2) in the paper
    return sum(model.cost[j] * model.x[j] for j in model.V) <= model.C


def terminal(model, t):
    # This is equation (4) in the paper
    return model.x[t] == 1


def flow_if_selected(model, i, j):
    # This is equation (6) in the paper
    return model.y[i, j] <= model.n * model.x[j]


def flow_balance(model, j):
    # This is equation (7) in the paper
    left = sum(model.y[i, j] for i in model.W if (i, j) in model.E)
    right = (
        model.x[j] + sum(model.y[j, l] for l in model.W if (j, l) in model.E)
    )
    return left == right


def new_formulation(model):
    # This is the constraint coming from the new formulation doc
    t0 = [i for i in model.V if (0, i) in model.E][0]
    left = sum(model.y[t0, j] for j in model.V if (t0, j) in model.E)
    right = sum(model.x[j] for j in model.V) - 1
    return left == right

###########################################################


def add_constraints(model):
    """Function that adds all the previous constraints to the model"""
    model.cost_rule = Constraint(rule=cost)
    model.terminal_rule = Constraint(model.T, rule=terminal)
    model.flow_if_selected_rule = Constraint(model.E, rule=flow_if_selected)
    model.flow_balance_rule = Constraint(model.V, rule=flow_balance)
    model.new_formulation_rule = Constraint(rule=new_formulation)


def objective(model):
    """Accumulate all costs to produce the objective function"""
    # This is equation (1) in the paper
    return sum(model.utility[j] * model.x[j] for j in model.V)


def get_model():
    """This function prepares the abstract model"""
    model = AbstractModel()
    add_params(model)
    add_vars(model)
    add_constraints(model)
    model.OBJ = Objective(rule=objective, sense=maximize)
    return model


def optimize(data):
    """Create an instance of the abstract model and optimize it"""
    model = get_model()
    instance = model.create_instance(data)
    # replace cbc by gurobi to use gurobi
    solver = SolverFactory('gurobi')
    # put tee=True to show solver output
    solver.solve(instance, tee=False)
    return instance
