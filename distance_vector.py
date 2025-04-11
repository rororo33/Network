#!/usr/bin/env python3
# Distance Vector 알고리즘 시뮬레이션

import pandas as pd
from tabulate import tabulate

# 네트워크 토폴로지 정의
nodes = ['X', 'Y', 'Z']
n = len(nodes)

# 초기 거리 행렬 (무한대로 초기화)
inf = float('inf')
distances = {
    'X': {'X': 0, 'Y': 4, 'Z': 50},
    'Y': {'X': 4, 'Y': 0, 'Z': 1},
    'Z': {'X': 50, 'Z': 0, 'Y': 1}
}

# 초기 라우팅 테이블 (다음 홉)
next_hop = {
    'X': {'X': '-', 'Y': 'Y', 'Z': 'Z'},
    'Y': {'X': 'X', 'Y': '-', 'Z': 'Z'},
    'Z': {'X': 'X', 'Z': '-', 'Y': 'Y'}
}

# Distance Vector 알고리즘 시뮬레이션
def simulate_distance_vector():
    iterations = []
    
    # 초기 상태 저장
    initial_state = {
        'iteration': 0,
        'tables': {
            node: {dest: distances[node][dest] for dest in nodes} 
            for node in nodes
        },
        'next_hops': {
            node: {dest: next_hop[node][dest] for dest in nodes}
            for node in nodes
        }
    }
    iterations.append(initial_state)
    
    # 알고리즘 반복
    iteration = 1
    changes = True
    
    while changes and iteration <= 10:  # 최대 10회 반복 (무한 루프 방지)
        changes = False
        current_state = {
            'iteration': iteration,
            'tables': {
                node: {dest: distances[node][dest] for dest in nodes}
                for node in nodes
            },
            'next_hops': {
                node: {dest: next_hop[node][dest] for dest in nodes}
                for node in nodes
            },
            'updates': []
        }
        
        # 각 노드에 대해
        for node in nodes:
            # 이웃 노드들에 대해
            for neighbor in nodes:
                if node != neighbor and distances[node][neighbor] != inf:
                    # 이웃 노드를 통한 다른 노드로의 경로 확인
                    for dest in nodes:
                        if dest != node:
                            new_dist = distances[node][neighbor] + distances[neighbor][dest]
                            if new_dist < distances[node][dest]:
                                # 더 짧은 경로 발견
                                old_dist = distances[node][dest]
                                distances[node][dest] = new_dist
                                next_hop[node][dest] = next_hop[node][neighbor]
                                changes = True
                                
                                # 업데이트 기록
                                update = {
                                    'node': node,
                                    'destination': dest,
                                    'old_distance': old_dist,
                                    'new_distance': new_dist,
                                    'via': neighbor
                                }
                                current_state['updates'].append(update)
        
        # 현재 상태 저장
        if changes:
            iterations.append(current_state)
        
        iteration += 1
    
    return iterations

# 결과 출력 함수
def print_iterations(iterations):
    result = []
    
    for state in iterations:
        iteration = state['iteration']
        result.append(f"\n## 반복 {iteration}\n")
        
        # 각 노드의 라우팅 테이블 출력
        for node in nodes:
            table_data = []
            for dest in nodes:
                dist = state['tables'][node][dest]
                next_h = state['next_hops'][node][dest]
                if dist == float('inf'):
                    dist_str = "∞"
                else:
                    dist_str = str(dist)
                table_data.append([dest, dist_str, next_h])
            
            result.append(f"\n### 노드 {node}의 라우팅 테이블:\n")
            table = tabulate(table_data, headers=["목적지", "거리", "다음 홉"], tablefmt="grid")
            result.append(table)
        
        # 업데이트 정보 출력 (초기 상태 제외)
        if iteration > 0 and 'updates' in state and state['updates']:
            result.append("\n### 이번 반복에서의 업데이트:\n")
            for update in state['updates']:
                old_dist = "∞" if update['old_distance'] == float('inf') else str(update['old_distance'])
                result.append(f"노드 {update['node']}가 목적지 {update['destination']}까지의 거리를 {old_dist}에서 {update['new_distance']}로 업데이트 (노드 {update['via']}를 통해)")
    
    return "\n".join(result)

# 시간 순서별 테이블 생성
def generate_time_sequence_tables():
    iterations = simulate_distance_vector()
    return print_iterations(iterations)

# 메인 함수
def main():
    result = generate_time_sequence_tables()
    with open('/home/ubuntu/distance_vector_analysis/results.md', 'w') as f:
        f.write("# Distance Vector 알고리즘 시뮬레이션 결과\n\n")
        f.write("## 네트워크 토폴로지\n")
        f.write("- 노드: X, Y, Z\n")
        f.write("- 링크: X-Y (비용: 4), Y-Z (비용: 1), X-Z (비용: 50)\n\n")
        f.write("## 시간 순서별 라우팅 테이블 변화\n")
        f.write(result)

if __name__ == "__main__":
    main()
