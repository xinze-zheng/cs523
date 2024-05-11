import sys, os, subprocess
from github import Github, Auth, Repository
import logging
logging.basicConfig(filename='contributor.log', encoding='utf-8', level=logging.DEBUG)

auth = Auth.Token("Your token") #Provide token to increase API rate limit
g = Github(auth=auth)

def parseRepoIdentifier(url: str) -> str:
    return url[url.rfind('/', 0, url.rfind('/')) + 1: ]

operator_list = []
system_list = []
operator_repo = []
system_repo = []
with open('operator_urls', 'r') as f:
    for line in f:
        identifier = parseRepoIdentifier(line.strip())
        print(identifier)
        repo = g.get_repo(identifier)
        operator_repo.append(repo)
        

with open('system_urls', 'r') as f:
    for line in f:
        if 'http' not in line:
            system_repo.append(None)
            continue

        identifier = parseRepoIdentifier(line.strip())
        print(identifier)
        repo = g.get_repo(identifier)
        system_repo.append(repo)
assert(len(operator_repo) == len(system_repo))
result = []
for i in range(len(operator_repo)):
    logging.debug(f'Process {i}')
    stat = []
    operator_con_set = set()
    repo = operator_repo[i]
    contributors = repo.get_contributors(anon=0) 
    for individual in contributors:
            operator_con_set.add(individual.email)
    print(f"len operator: {len(operator_con_set)}")
    stat.append(len(operator_con_set))
    operator_list.append(operator_con_set)
    if system_repo[i] is None:
        logging.debug(f'Not found at {i}')
        stat.append(0)
        stat.append(0)
        system_list.append(None)
        result.append(stat)
        continue
    
    system_con_set = set()
    repo = system_repo[i]
    contributors = repo.get_contributors(anon=0) 
    for individual in contributors:
            system_con_set.add(individual.email)
    print(f"len system: {len(system_con_set)}")
    stat.append(len(system_con_set))
    system_list.append(system_con_set)

    print("Find intersection")
    intersection_cnt = 0
    for item in operator_con_set:
        if item in system_con_set:
            logging.debug(f'Find intersection at {item}')
            intersection_cnt += 1
    print(f"inter: {intersection_cnt}")
    stat.append(intersection_cnt)
    print(stat)
    result.append(stat)
    logging.info(f'Currnet result {result}')







# for repo in operator_repo:
#     contributors = repo.get_contributors(anon=False)
#     con_set = []
#     for individual in contributors:
#         if individual.name != None or individual.email != None:
#             con_set.append((individual.name, individual.email))
#     print(con_set)
#     operator_list.append(con_set)

# for repo in system_repo:
#     contributors = repo.get_contributors(anon=False)
#     con_set = []
#     for individual in contributors:
#         if individual.name != None or individual.email != None:
#             con_set.append((individual.name, individual.email))
#     print(con_set)
#     system_list.append(con_set)
    
# with open('contrinutor_out.txt', 'w') as f:
#     f.write(operator_list)
#     f.write('\n')
#     f.write(system_list)

# for i in range(len(operator_list)):



