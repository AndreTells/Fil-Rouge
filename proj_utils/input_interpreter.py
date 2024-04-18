import pandas as pd
import math

def _calculate_customer_loads(route_id, customer_df):
    df_route1 = customer_df.loc[customer_df['ROUTE_ID'] == route_id] #Filters by route id first

    tab_limites = ['CUSTOMER_CODE','TOTAL_WEIGHT_KG','TOTAL_VOLUME_M3','CUSTOMER_DELIVERY_SERVICE_TIME_MIN']

    df_lim = df_route1[tab_limites].copy() #Table with the weight, volume and time spent with each delivery to each client
    
    lim_peso = df_lim['TOTAL_WEIGHT_KG'].tolist()
    lim_volume = df_lim['TOTAL_VOLUME_M3'].tolist()
    lim_time = df_lim['CUSTOMER_DELIVERY_SERVICE_TIME_MIN'].tolist()

    lista_limites = [(0,0)]+list(zip(lim_peso,lim_volume))
    return lista_limites

def _calculate_dist_adjacency_matrix(route_id, customer_df, deposit_df ):
    #Filters by route id first
    df_route = customer_df.loc[customer_df['ROUTE_ID'] == route_id]
    df_depot = deposit_df.loc[deposit_df['ROUTE_ID'] == route_id] 
    #Starts processing the data

    tab_dist = ['CUSTOMER_LATITUDE','CUSTOMER_LONGITUDE']
    tab_depot = ['DEPOT_LATITUDE','DEPOT_LONGITUDE']

    df_dist = df_route[tab_dist].copy()
    df_depot = df_depot[tab_depot].copy()

    df_dist.columns,df_depot.columns  = ['LATITUDE', 'LONGITUDE'],['LATITUDE', 'LONGITUDE']

    latitude_list = df_dist['LATITUDE'].tolist()
    latitude_list.append(df_depot['LATITUDE'].tolist()[0])

    longitude_list = df_dist['LONGITUDE'].tolist()
    longitude_list.append(df_depot['LONGITUDE'].tolist()[0])

    #Shifts 1 unit to the right so the depot will be the first on the list

    latitude_list = latitude_list[-1:] + latitude_list[:-1]
    longitude_list = longitude_list[-1:] + longitude_list[:-1]

    points = list(zip(latitude_list, longitude_list))
    #Finishes processing the data and creates a new dataframe

    new_df = pd.DataFrame({'LATITUDE': latitude_list, 'LONGITUDE': longitude_list})

    distance_matrix = []

    for i in range(len(latitude_list)):
        distance_matrix.append([])
        for j in range(len(longitude_list)):
            distance_matrix[i].append(math.sqrt((longitude_list[i] - longitude_list[j]) ** 2 +
                                        (latitude_list[i] - latitude_list[j]) ** 2))

    return distance_matrix, points

def _calculate_time_adjacency_matrix(route_id, customer_df, deposit_df, vel):
    #Filters by route id first
    df_route = customer_df.loc[customer_df['ROUTE_ID'] == route_id] 
    df_depot = deposit_df.loc[deposit_df['ROUTE_ID'] == route_id]
    #Starts processing the data

    tab_dist = ['CUSTOMER_LATITUDE','CUSTOMER_LONGITUDE']
    tab_depot = ['DEPOT_LATITUDE','DEPOT_LONGITUDE']

    df_dist = df_route[tab_dist].copy()
    df_depot = df_depot[tab_depot].copy()

    df_dist.columns,df_depot.columns  = ['LATITUDE', 'LONGITUDE'],['LATITUDE', 'LONGITUDE']

    latitude_list = df_dist['LATITUDE'].tolist()
    latitude_list.append(df_depot['LATITUDE'].tolist()[0])

    longitude_list = df_dist['LONGITUDE'].tolist()
    longitude_list.append(df_depot['LONGITUDE'].tolist()[0])

    #Shifts 1 unit to the right so the depot will be the first on the list

    latitude_list = latitude_list[-1:] + latitude_list[:-1]
    longitude_list = longitude_list[-1:] + longitude_list[:-1]

    #Finishes processing the data and creates a new dataframe
    points = list(zip(latitude_list, longitude_list))
    new_df = pd.DataFrame({'LATITUDE': latitude_list, 'LONGITUDE': longitude_list})

    temp_matrix = []

    for i in range(len(latitude_list)):
        temp_matrix.append([])
        for j in range(len(longitude_list)):
            aux = math.sqrt((longitude_list[i] - longitude_list[j]) ** 2 + (latitude_list[i] - latitude_list[j]) ** 2)
            temp_matrix[i].append(aux/vel)

    return temp_matrix, points

def format_input(route_id, customer_df, deposit_df):
    customer_loads = _calculate_customer_loads(route_id, customer_df)
    adjacency_matrix,points = _calculate_time_adjacency_matrix(route_id, customer_df, deposit_df, 1)
    return adjacency_matrix, customer_loads, points