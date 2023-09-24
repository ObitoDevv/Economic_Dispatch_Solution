from mca_epd import generate_nests,objective_function,min_cost,levy_flight,cost_gen,random_nest_select,calculate_alpha
import random
import copy
def ed():
    # total number of generators
    n_gen=3
    # power needed to be produced
    demand=200
    # minimum power of each generator
    p_min=[0,0,0]
    # maximum power of each generator
    p_max=[100,80,60]
    # ci- coefficient of x^2
    c1=[0.1,0.01,7]
    # bi- coefficient of x
    c2=[3,0.01,0.7]
    # ai- constant
    c0=[4,7,6]
    #pozs of each generator
    pg_min=[[91,95],[25,45,65],[30]]
    pg_max=[[93,98],[30,55,70],[45]]
    #alpha < beta
    beta=1.5  #0-2
    # alpha=0.01  #0.01 to o.39
    #inputs for self-adaptive size
    itr = 100
    a = 0.39
    b = 0.40
    n=random.randint(50*n_gen,100*n_gen)
    nests = generate_nests(n,p_min,p_max,n_gen,demand,pg_min,pg_max)
    # print(nests)
    num=5
    selected_nests = random_nest_select(nests,num)
    # print("SELECTD_NEST: ", selected_nests)

    #     total_nests.append(nests[index_arr[i]])
    # costs = objective_function(nests,c1,c2,c0,n_gen,n,pg_min,pg_max)
    # print("costs  : ",costs)
    # mn = min_cost(costs)
    # print("MINIMUM_COST : ",mn)
    # index=mn[0]
    # cost_min=mn[1]
    # gen_cost=cost_gen(c1,c2,c0,index,nests,n_gen)
    # print("gen_cost : ",gen_cost)
    # hash = []
    # for i in range (len(nests)):
    #     hash.append(0)

    # print("",nests[index])
    # arr = levy_flight(nests[index],gen_cost,alpha,beta,p_min,p_max)
    # print("array: ",arr)
    new_nests = copy.deepcopy(selected_nests)
    # print("new_nests : ",new_nests)
    for k in range (1000):
        for i in range (itr):
            for j in range(len(new_nests)):
                alpha = calculate_alpha(i,itr,a,b)
                gen_cost=cost_gen(c1,c2,c0,j,new_nests,n_gen)
                # print(gen_cost)
                new_powers=levy_flight(new_nests[j],gen_cost,alpha,beta,p_min,p_max)
                # print(new_powers)
                power = 0
                flag = 1
                for k in range (len(new_powers)):
                    if(new_powers[k] < p_min[k] or new_powers[k] > p_max[k]):
                        # print("new_power of k: ",new_powers[k], " ", k)
                        flag = 0
                        break
                    power += new_powers[k]
                # print("",power)
                if(flag and power > demand):
                    # print("",power)
                    for k in range(n_gen):
                        new_nests[j][k]=new_powers[k]
                        # print(nests[j])
        # print(new_nests)
        # print("SELECTED_NEST : ",selected_nests)
        # print("NEW_NESTS",new_nests)
        total_nests = new_nests + selected_nests
        # print("total_nests : ",total_nests)
        total_cost = []
        for i in range (len(total_nests)):
            total_cost.append([sum(cost_gen(c1,c2,c0,i,total_nests,n_gen)),i])
        total_cost.sort()
        # print("total_costs : ",total_cost)
        selected_nests.clear()
        new_nests.clear()
        for i in range (num):
            selected_nests.append(total_nests[total_cost[i][1]])
        # print("SELECTED_NESTS : ",selected_nests)

    final_cost = []
    for i in range (len(selected_nests)):
        final_cost.append([sum(cost_gen(c1,c2,c0,i,selected_nests,n_gen)),i])
    final_cost.sort()

    optimal_cost = final_cost[0][0]
    optimal_nest = selected_nests[final_cost[0][1]]

    sol = [optimal_cost,optimal_nest]
    return sol
    print("OPTIMAL_COST : ",final_cost[0][0])
    print("NEST WITH OPTIMAL COST : ",selected_nests[final_cost[0][1]])

    # costs = objective_function(nests,c1,c2,c0,n_gen,n,pg_min,pg_max)
    # print("costs  : ",costs)
    # mn = min_cost(costs)
    # print("MINIMUM_COST : ",mn)
    # index=mn[0]
    # cost_min=mn[1]
    # print("BEST SOLUTION : ",cost_min)
    # print("NEST : ",nests[index])
    # gen_cost=cost_gen(c1,c2,c0,index,nests,n_gen)
    # print("gen_cost : ",gen_cost)
