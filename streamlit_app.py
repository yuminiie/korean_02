import streamlit as st
import numpy as np

# --- 1. 앱 페이지 설정 및 상태 관리 ---
def setup_page():
    st.set_page_config(
        page_title="OX 빙고 게임",
        layout="centered"
    )
    st.title("OX 빙고 게임 🎮")
    st.markdown("---")

    # 세션 상태 초기화
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
        st.session_state.turn = 0  # 턴 카운트: 0, 1, 2, ...
        st.session_state.board = np.full((4, 4), '', dtype=object)  # 빈 보드
        st.session_state.game_over = False
        st.session_state.winner = None

# --- 2. 게임 시작 화면 ---
def start_screen():
    st.info("홀수 번째 턴은 'O', 짝수 번째 턴은 'X'로 표시됩니다.")
    st.markdown("아래 버튼을 눌러 게임을 시작하세요.")
    if st.button("게임 시작", key="start_button"):
        st.session_state.game_started = True
        st.session_state.turn = 0
        st.session_state.board = np.full((4, 4), '', dtype=object)
        st.session_state.game_over = False
        st.session_state.winner = None
        st.rerun()

# --- 3. 빙고 판정 로직 ---
def check_win(board):
    # 가로, 세로, 대각선 승리 조건 확인
    
    # 가로 & 세로 검사
    for i in range(4):
        # 가로
        if board[i, 0] != '' and np.all(board[i, :] == board[i, 0]):
            return board[i, 0]
        # 세로
        if board[0, i] != '' and np.all(board[:, i] == board[0, i]):
            return board[0, i]

    # 대각선 검사
    # 왼쪽 위 -> 오른쪽 아래
    if board[0, 0] != '' and np.all(np.diag(board) == board[0, 0]):
        return board[0, 0]
    # 오른쪽 위 -> 왼쪽 아래
    if board[0, 3] != '' and np.all(np.diag(np.fliplr(board)) == board[0, 3]):
        return board[0, 3]

    # 승리자가 없는 경우 None 반환
    return None

# --- 4. 게임 화면 및 턴 진행 로직 ---
def game_screen():
    # 현재 턴 플레이어 결정 ('O' 또는 'X')
    current_player = 'O' if st.session_state.turn % 2 == 0 else 'X'
    
    if st.session_state.game_over:
        if st.session_state.winner:
            st.balloons()
            st.success(f"🎉 {st.session_state.winner} 승리!")
        else:
            st.warning("🤝 무승부!")
        
        if st.button("다시 시작", key="restart_button"):
            st.session_state.game_started = False
            st.rerun()
        return

    st.subheader(f"➡️ 현재 턴: {current_player}")
    st.caption(f"총 턴 수: {st.session_state.turn}")
    
    # 빙고 보드 생성 (4x4 그리드)
    for i in range(4):
        cols = st.columns(4)
        for j in range(4):
            with cols[j]:
                # 이미 선택된 칸은 비활성화
                if st.session_state.board[i, j] != '':
                    st.button(f"**{st.session_state.board[i, j]}**", key=f"btn_{i}-{j}", disabled=True)
                else:
                    # 클릭 가능한 버튼
                    if st.button(" ", key=f"btn_{i}-{j}"):
                        st.session_state.board[i, j] = current_player
                        st.session_state.turn += 1
                        
                        # 승리자 확인
                        winner = check_win(st.session_state.board)
                        if winner:
                            st.session_state.game_over = True
                            st.session_state.winner = winner
                        # 모든 칸이 채워졌는지 확인 (무승부)
                        elif st.session_state.turn == 16:
                            st.session_state.game_over = True
                            st.session_state.winner = None
                        
                        st.rerun()

# --- 5. 메인 함수 (앱의 진입점) ---
def main():
    setup_page()
    
    if st.session_state.game_started:
        game_screen()
    else:
        start_screen()

if __name__ == "__main__":
    main()