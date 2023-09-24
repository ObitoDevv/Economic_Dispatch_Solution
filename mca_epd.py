import numpy as np
import random
import math

#defining objective function
def objective_function(x, c1, c2, c0,n_gen,n,pg_min,pg_max):
    # Check if the solution violates prohibited operating zones
    for i in range(n):
        for k in range(n_gen):
            for j in range(len(pg_min[k])):
                if(x[i][k]>pg_min[k][j] and x[i][k]<pg_max[k][j]):
                    mid=(pg_min[k][j]+pg_max[k][j])/2
                    if(x[i][k]<=mid): x[i][k]=pg_min[k][j]
                    elif(x[i][k]>mid): x[i][k]=pg_max[k][j]

    # Evaluate the objective function
    total_cost = []
    for i in range(n):
        total=0
        for j in range(n_gen):
            total+=(c1[j]*(x[i][j]**2)+c2[j]*x[i][j]+c0[j])
        total_cost.append(total)
    return total_cost

#cost of particular generator
def cost_gen(c1,c2,c0,index,nests,n_gen):
    gen_cost=[]
    cost=0
    for i in range(n_gen):
        cost=c1[i]*(nests[index][i]**2)+c2[i]*nests[index][i]+c0[i]
        gen_cost.append(cost)
    return gen_cost

#generating initial nests
def generate_nests(n, p_min, p_max,n_gen,demand,pg_min,pg_max):
    nests = []
    for i in range(n):
        sum=0
        # max_demand=demand+5
        # print(max_demand)
        nest=[]
        while sum<demand:
            sum=0
            nest=[]
            for j in range(n_gen):
            # print(p_min[j])
                sol=max(0,p_min[j]+((random.uniform(0, 1))*(p_max[j]-p_min[j])))
                # for it in range(n_gen):
                #     for it2 in range(len(pg_min[it])):
                #         if(sol>pg_min[it][it2] and sol<pg_max[it][it2]):
                #             mid=(pg_min[it][it2]+pg_max[it][it2])/2
                #             if(sol<=mid): sol=pg_min[it][it2]
                #             elif(sol>mid): sol=pg_max[it][it2]
                nest.append(sol)
            for k in range(n_gen):
                sum+=nest[k]
            # if(sum>max_demand):
            #     sum=0
            # print(sum)
        # print(nest)
        nests.append(nest)
    return nests

#selecting random 5 nests
def random_nest_select(nests,num):
    selected_nests = []
    num_nests = len(nests)
    random_nums = []
    for i in range(num):
        x = random.randint(0, num_nests)
        random_nums.append(x)
    for i in range(num):
        selected_nests.append(nests[i])
        # selected_nests.append(i)
    return selected_nests
    # return random_nums

#self-adaptive step-size
def calculate_alpha(t, tM, a, b):
    numerator = ((b - a) * math.exp(10 * (t - 1) / (tM - 1)))-1
    denominator = math.exp(10) - 1
    alpha_t = numerator / denominator
    return alpha_t

#calculating the minimum cost
def min_cost(total_cost):
    index=0
    mn=1e18
    ans=[]
    for i in range(len(total_cost)):
        if(mn>total_cost[i]):
            mn=total_cost[i]
            index=i
    ans.append(index)
    ans.append(mn)
    return ans

def mantegna_algorithm(beta):
    u = random.normalvariate(0, 1)
    v = math.fabs(random.normalvariate(0, 1))
    sigma_u = (math.gamma(1 + beta) * math.sin(math.pi * beta / 2) / (math.gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)
    sigma_v = 1
    delta = u / math.pow(v, 1 / beta) * sigma_u / sigma_v
    return delta

# Define the function to perform Levy flight for a given solution Xi
def levy_flight(Xi, Xgbest,alpha,beta,p_min,p_max):
    # Calculate the step size and generate a random number for r2
    step = alpha * mantegna_algorithm(beta)
    r2 = random.normalvariate(0, 1)

    # Calculate the new solution Xi_k(new) using the Levy flight formula
    delta_Xi = [(Xi[j] - Xgbest[j]) for j in range(len(Xi))]
    delta_Xi_new = [delta_Xi[j] * step * r2 * mantegna_algorithm(beta) for j in range(len(Xi))]
    Xi_new = [Xi[j] + delta_Xi_new[j] for j in range(len(Xi))]
    for i in range(len(Xi_new)):
        if Xi_new[i] < p_min[i]:
            Xi_new[i] = p_min[i]
        elif Xi_new[i]>p_max[i]:
            Xi_new[i]=p_max[i]
    sum = 0
    for i in range (len(Xi_new)):
        sum += Xi_new[i]
    # print(Xi_new)
    return Xi_new
