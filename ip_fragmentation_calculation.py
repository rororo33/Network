#!/usr/bin/env python3

def calculate_ip_fragmentation(total_length, mtu):
    """
    IP 프래그먼테이션 계산
    
    Args:
        total_length: 원본 IP 패킷의 총 길이 (바이트)
        mtu: Maximum Transmission Unit (바이트)
    
    Returns:
        각 프래그먼트의 세부 정보 (length, ID, fragflag, offset)
    """
    # IP 헤더 크기 (기본 20바이트, 옵션 없음 가정)
    ip_header_size = 20
    
    # 각 프래그먼트에서 데이터가 차지할 수 있는 최대 크기
    # MTU에서 IP 헤더 크기를 뺀 값
    max_data_per_fragment = mtu - ip_header_size
    
    # 8의 배수로 데이터 크기 조정 (IP 프래그먼테이션 요구사항)
    max_data_per_fragment = (max_data_per_fragment // 8) * 8
    
    # 원본 데이터 크기 (IP 헤더 제외)
    original_data_size = total_length - ip_header_size
    
    # 필요한 프래그먼트 수 계산
    num_fragments = (original_data_size + max_data_per_fragment - 1) // max_data_per_fragment
    
    # 각 프래그먼트의 세부 정보 계산
    fragments = []
    remaining_data = original_data_size
    offset = 0
    
    # 임의의 ID 값 (실제로는 원본 패킷마다 고유한 값)
    id_value = 12345
    
    for i in range(num_fragments):
        # 마지막 프래그먼트인지 확인
        is_last_fragment = (i == num_fragments - 1)
        
        # 현재 프래그먼트의 데이터 크기
        data_size = min(max_data_per_fragment, remaining_data)
        
        # 프래그먼트의 총 길이 (IP 헤더 + 데이터)
        fragment_length = ip_header_size + data_size
        
        # 프래그먼트 플래그 (0: 마지막 프래그먼트, 1: 더 프래그먼트가 있음)
        frag_flag = 0 if is_last_fragment else 1
        
        # 프래그먼트 오프셋 (8바이트 단위)
        frag_offset = offset // 8
        
        fragments.append({
            'fragment_number': i + 1,
            'length': fragment_length,
            'id': id_value,
            'fragflag': frag_flag,
            'offset': frag_offset,
            'data_size': data_size
        })
        
        # 다음 프래그먼트를 위한 값 업데이트
        remaining_data -= data_size
        offset += data_size
    
    return fragments

def main():
    # 사용자 입력 값
    total_length = 4000  # 원본 패킷 크기 (바이트)
    mtu = 1500           # MTU 크기 (바이트)
    
    fragments = calculate_ip_fragmentation(total_length, mtu)
    
    # 결과 출력
    print(f"원본 패킷 크기: {total_length} 바이트")
    print(f"MTU: {mtu} 바이트")
    print(f"IP 헤더 크기: 20 바이트")
    print(f"프래그먼트 수: {len(fragments)}")
    print("\n각 프래그먼트 세부 정보:")
    
    for fragment in fragments:
        print(f"\n프래그먼트 #{fragment['fragment_number']}:")
        print(f"  Length: {fragment['length']} 바이트")
        print(f"  ID: {fragment['id']}")
        print(f"  Fragflag: {fragment['fragflag']} ({'더 프래그먼트 있음' if fragment['fragflag'] == 1 else '마지막 프래그먼트'})")
        print(f"  Offset: {fragment['offset']} (8바이트 단위, 실제 바이트 오프셋: {fragment['offset'] * 8})")
        print(f"  데이터 크기: {fragment['data_size']} 바이트")

if __name__ == "__main__":
    main()
