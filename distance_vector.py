# 앞서 정의했던 함수들을 포함하여 전체 코드를 오류 없이 통합

import pandas as pd
from tabulate import tabulate

# 네트워크 토폴로지 정의
nodes = ['X', 'Y', 'Z']
inf = float('inf')
distances = {
    'X': {'X': 0, 'Y': 4, 'Z': 50},
    'Y': {'X': 4, 'Y': 0, 'Z': 1},
    'Z': {'X': 50, 'Z': 0, 'Y': 1}
}
next_hop = {
    'X': {'X': '-', 'Y': 'Y', 'Z': 'Z'},
    'Y': {'X': 'X', 'Y': '-', 'Z': 'Z'},
    'Z': {'X': 'X', 'Z': '-', 'Y': 'Y'}
}

def simulate_distance_vector():
    iterations = []
    initial_state = {
        'iteration': 0,
        'tables': {node: {dest: distances[node][dest] for dest in nodes} for node in nodes},
        'next_hops': {node: {dest: next_hop[node][dest] for dest in nodes} for node in nodes}
    }
    iterations.append(initial_state)
    iteration = 1
    changes = True
    while changes and iteration <= 10:
        changes = False
        current_state = {
            'iteration': iteration,
            'tables': {node: {dest: distances[node][dest] for dest in nodes} for node in nodes},
            'next_hops': {node: {dest: next_hop[node][dest] for dest in nodes} for node in nodes},
            'updates': []
        }
        for node in nodes:
            for neighbor in nodes:
                if node != neighbor and distances[node][neighbor] != inf:
                    for dest in nodes:
                        if dest != node:
                            new_dist = distances[node][neighbor] + distances[neighbor][dest]
                            if new_dist < distances[node][dest]:
                                old_dist = distances[node][dest]
                                distances[node][dest] = new_dist
                                next_hop[node][dest] = next_hop[node][neighbor]
                                changes = True
                                update = {
                                    'node': node,
                                    'destination': dest,
                                    'old_distance': old_dist,
                                    'new_distance': new_dist,
                                    'via': neighbor
                                }
                                current_state['updates'].append(update)
        if changes:
            iterations.append(current_state)
        iteration += 1
    return iterations

def generate_time_sequence_tables():
    iterations = simulate_distance_vector()
    return print_iterations(iterations)

def print_iterations(iterations):
    result = []
    for state in iterations:
        iteration = state['iteration']
        result.append(f"\n## 반복 {iteration}\n")
        for node in nodes:
            table_data = []
            for dest in nodes:
                dist = state['tables'][node][dest]
                next_h = state['next_hops'][node][dest]
                dist_str = "∞" if dist == float('inf') else str(dist)
                table_data.append([dest, dist_str, next_h])
            result.append(f"\n### 노드 {node}의 라우팅 테이블:\n")
            table = tabulate(table_data, headers=["목적지", "거리", "다음 홉"], tablefmt="grid")
            result.append(table)
        if iteration > 0 and 'updates' in state and state['updates']:
            result.append("\n### 이번 반복에서의 업데이트:\n")
            for update in state['updates']:
                old_dist = "∞" if update['old_distance'] == float('inf') else str(update['old_distance'])
                result.append(f"노드 {update['node']}가 목적지 {update['destination']}까지의 거리를 {old_dist}에서 {update['new_distance']}로 업데이트 (노드 {update['via']}를 통해)")
    return "\n".join(result)

def main():
    result = generate_time_sequence_tables()
    print("# Distance Vector 알고리즘 시뮬레이션 결과\n\n")
    print("## 네트워크 토폴로지\n")
    print("- 노드: X, Y, Z\n")
    print("- 링크: X-Y (비용: 4), Y-Z (비용: 1), X-Z (비용: 50)\n\n")
    print("## 시간 순서별 라우팅 테이블 변화\n")
    print(result)

main()
