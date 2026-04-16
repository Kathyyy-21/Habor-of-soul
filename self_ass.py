import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from login import require_login, get_current_user, is_logged_in
import pytz


class SelfAssessment:
    def __init__(self):
        self.db_name = "users.db"
        self.init_database()

    def init_database(self):
        """初始化测评表（在已有的 user.db 里创建，不影响用户表）"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # 创建测评记录表（用 phone 关联用户）
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            total_score INTEGER NOT NULL,
            assessment_time TIMESTAMP NOT NULL,
            answers TEXT,
            FOREIGN KEY (phone) REFERENCES users(phone)
        )
        ''')

        conn.commit()
        conn.close()

    def get_beijing_time(self):
        """获取北京时间"""
        try:
            beijing_tz = pytz.timezone('Asia/Shanghai')
            return datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S')
        except:
            utc_now = datetime.utcnow()
            beijing_time = utc_now + timedelta(hours=8)
            return beijing_time.strftime('%Y-%m-%d %H:%M:%S')

    def save_assessment(self, phone, total_score, answers):
        """保存测评结果（使用手机号关联）"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            beijing_time = self.get_beijing_time()
            cursor.execute(
                "INSERT INTO assessments (phone, total_score, assessment_time, answers) VALUES (?, ?, ?, ?)",
                (phone, total_score, beijing_time, str(answers))
            )
            conn.commit()
            conn.close()
            return True, "测评结果保存成功！"
        except sqlite3.Error as e:
            return False, f"保存失败: {str(e)}"

    def get_user_assessments(self, phone):
        """获取当前手机号的测评历史"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, total_score, assessment_time, answers FROM assessments WHERE phone = ? ORDER BY assessment_time DESC",
                (phone,)
            )
            results = cursor.fetchall()
            conn.close()
            return results
        except sqlite3.Error as e:
            return []

    def delete_assessment(self, assessment_id, phone):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM assessments WHERE id = ? AND phone = ?",
                (assessment_id, phone)
            )
            if cursor.fetchone():
                cursor.execute("DELETE FROM assessments WHERE id = ?", (assessment_id,))
                conn.commit()
                conn.close()
                return True, f"记录 {assessment_id} 删除成功！"
            else:
                return False, "记录不存在或无权限删除"
        except sqlite3.Error as e:
            return False, f"删除失败: {str(e)}"


def display_self_assessment():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'show_delete_form' not in st.session_state:
        st.session_state.show_delete_form = False
    if 'delete_record_id' not in st.session_state:
        st.session_state.delete_record_id = None

    if not is_logged_in():
        st.warning("请先登录以使用自评工具")
        st.stop()

    current_user_phone = st.session_state.get('current_user_phone', None)
    current_user_nickname = get_current_user()
    assessment_system = SelfAssessment()

    st.set_page_config(
        page_title="心灵港湾 - 自评工具",
        page_icon="🧪",
        layout="wide"
    )

    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=ZCOOL+KuaiLe&family=Ma+Shan+Zheng&display=swap');

    .page-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        font-family: 'ZCOOL KuaiLe', cursive;
        font-size: 3.5rem !important;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        animation: fadeIn 1s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .assessment-section {
        margin: 1.5rem 0;
        animation: slideIn 0.5s ease-out;
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    .question-item {
        margin: 1.5rem 0;
        padding: 1rem 0;
        border-bottom: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }

    .question-item:hover {
        transform: translateX(5px);
        border-bottom-color: #667eea;
    }

    .question-title {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .warning-box {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.15), rgba(255, 235, 59, 0.15));
        border-left: 5px solid #ffc107;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.4); }
        50% { box-shadow: 0 0 0 10px rgba(255, 193, 7, 0); }
    }

    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: bounceIn 0.6s ease-out;
    }

    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.9); }
        50% { opacity: 1; transform: scale(1.02); }
        100% { opacity: 1; transform: scale(1); }
    }

    .history-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .history-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }

    /* 分数显示样式 —— 改成红色清晰版 */
    .score-display {
        font-family: 'Ma Shan Zheng', cursive;
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        color: #ff3333; /* 红色分数 */
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        animation: glow 2s ease-in-out infinite alternate;
    }

    .delete-confirm-box {
        background: linear-gradient(135deg, rgba(231, 76, 60, 0.1), rgba(231, 76, 60, 0.2));
        border: 2px solid #e74c3c;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        animation: shake 0.5s ease-in-out;
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        font-family: 'Noto Serif SC', serif;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }

    .stSelectbox > div > div {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        font-family: 'Noto Serif SC', serif;
    }

    .stAlert {
        border-radius: 10px;
        font-family: 'Noto Serif SC', serif;
    }

    .custom-hr {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, #667eea, transparent);
        margin: 2rem 0;
        animation: slideIn 1s ease-out;
    }

    .user-info {
        background: linear-gradient(135deg, #e8f4f8 0%, #d1e9f5 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        font-family: 'Noto Serif SC', serif;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div class="page-title">
            PHQ-9 抑郁症自评工具
        </div>
        <div style="font-family: 'Noto Serif SC', serif; color: #7f8c8d; font-size: 1rem;">
            用心倾听，科学评估
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📋 关于PHQ-9量表", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="font-family: 'KaiTi', serif; color: #003366; font-size: 15px;">
            <h4 style="color: #003366; font-family: 'KaiTi', serif;">✨ 什么是PHQ-9？</h4>
            PHQ-9（患者健康问卷-9）是一种国际上广泛使用的抑郁症筛查工具，简单快速，科学可靠。

            <h4 style="color: #003366; font-family: 'KaiTi', serif; margin-top: 1rem;">📊 评分标准：</h4>
            • <span style="color:#003366;">完全没有</span>：0分<br>
            • <span style="color:#003366;">有几天</span>：1分<br>
            • <span style="color:#003366;">一半以上的天数</span>：2分<br>
            • <span style="color:#003366;">几乎每天</span>：3分<br><br>
            <strong>总分：0–27分</strong>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="font-family: 'Noto Serif SC', serif; padding: 0.5rem;">
                <h4 style="color: #667eea;">🎯 分数解释：</h4>
                <div style="background: linear-gradient(135deg, #f5f7fa, #c3cfe2); padding: 1rem; border-radius: 10px;">
                    <p><span style="color: #2ecc71;">● 0-4分</span>：无抑郁症倾向</p>
                    <p><span style="color: #f39c12;">● 5-9分</span>：轻度抑郁症倾向</p>
                    <p><span style="color: #e67e22;">● 10-14分</span>：中度抑郁症倾向</p>
                    <p><span style="color: #e74c3c;">● 15-19分</span>：中重度抑郁症倾向</p>
                    <p><span style="color: #c0392b;">● 20-27分</span>：重度抑郁症倾向</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

    # ====================== 关键修改：显示自动登录的用户信息 ======================
    # 显示当前用户信息（自动读取）
    st.info(f"✅ 当前用户：{current_user_nickname}")

    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="assessment-section">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
            <span style="font-size: 1.8rem;">📝</span>
            <div>
                <h3 style="margin: 0; color: #667eea;">开始测评</h3>
                <p style="margin: 0.25rem 0 0 0; color: #7f8c8d;">请根据过去两周的情况，诚实地回答以下问题：</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    questions = [
        "1. 做事时提不起劲或没有兴趣",
        "2. 感到心情低落、沮丧或绝望",
        "3. 入睡困难、睡不安稳或睡眠过多",
        "4. 感觉疲倦或没有活力",
        "5. 食欲不振或吃太多",
        "6. 觉得自己很糟、很失败，或让自己、家人失望",
        "7. 难以集中注意力，例如阅读报纸或看电视时",
        "8. 行动或说话速度缓慢到别人已经觉察，或刚好相反：变得比平日更烦躁或坐立不安，动来动去",
        "9. 有不如死掉或用某种方式伤害自己的念头"
    ]

    options = {"0": "完全没有", "1": "有几天", "2": "一半以上的天数", "3": "几乎每天"}
    option_with_default = ["请选择..."] + list(options.values())

    answers = {}
    total_score = 0
    all_answered = True

    for i, question in enumerate(questions):
        with st.container():
            col_q, col_a = st.columns([3, 2])
            with col_q:
                colors = ["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe", "#00f2fe", "#43e97b", "#38f9d7",
                          "#fa709a"]
                st.markdown(f"""
                <div class="question-item">
                    <div class="question-title" style="color: {colors[i]};">
                        {question}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_a:
                answer_key = f"q{i + 1}"
                saved_answer = None
                if answer_key in st.session_state.answers:
                    saved_score = st.session_state.answers[answer_key]
                    saved_answer = options.get(str(saved_score), None)

                default_index = 0
                if saved_answer and saved_answer in option_with_default:
                    default_index = option_with_default.index(saved_answer)

                selected = st.selectbox(f"选择频率", option_with_default, index=default_index, key=f"select_{i}",
                                        label_visibility="collapsed")

                score = 0
                if selected != "请选择...":
                    for key, value in options.items():
                        if value == selected:
                            score = int(key)
                            break
                    answers[answer_key] = score
                    total_score += score

                    score_badge_color = {0: "#2ecc71", 1: "#f39c12", 2: "#e67e22", 3: "#e74c3c"}.get(score, "#95a5a6")
                    st.markdown(f"""
                    <div style="text-align: right; margin-top: 0.5rem;">
                        <span style="background: {score_badge_color}; color: white; padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                            得分：{score}分
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    answers[answer_key] = None
                    all_answered = False

    st.session_state.answers = answers
    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

    col_submit1, col_submit2, col_submit3 = st.columns([1, 2, 1])
    with col_submit2:
        submitted = st.button("📤 提交测评", use_container_width=True, type="primary")

    if submitted:
        unanswered = any(answer is None for answer in answers.values())
        if unanswered:
            st.error("⚠️ 请完成所有题目的选择后再提交")
        else:
            # 直接使用自动获取的手机号
            success, message = assessment_system.save_assessment(current_user_phone, total_score, answers)
            if success:
                st.balloons()
                st.success("✅ 测评结果已成功保存！")
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown('<h3 style="text-align: center; color: white;">📊 测评结果</h3>', unsafe_allow_html=True)
                st.markdown(f'<div class="score-display">{total_score}分</div>', unsafe_allow_html=True)

                if total_score <= 4:
                    st.success("**结果：无抑郁症倾向**")
                    st.info("💚 继续保持良好的心理状态！")
                elif total_score <= 9:
                    st.warning("**结果：您可能有轻度抑郁症倾向**")
                    st.info("💛 建议关注自己的情绪变化，适当进行放松和调节")
                elif total_score <= 14:
                    st.warning("**结果：您可能有中度抑郁症倾向**")
                    st.info("🧡 建议寻求专业心理咨询帮助")
                elif total_score <= 19:
                    st.error("**结果：您可能有中重度抑郁症倾向**")
                    st.info("❤️ 强烈建议尽快寻求专业医生的帮助")
                else:
                    st.error("**结果：您可能有重度抑郁症倾向**")
                    st.info("💔 请立即寻求专业医疗帮助，您不是一个人")

                st.markdown('</div>', unsafe_allow_html=True)

                with st.expander("📈 查看详细得分分布", expanded=False):
                    fig = go.Figure(data=[go.Bar(
                        x=list(range(1, 10)),
                        y=[answers[f"q{i}"] for i in range(1, 10)],
                        marker_color=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b',
                                      '#38f9d7', '#fa709a'],
                        text=[answers[f"q{i}"] for i in range(1, 10)],
                        textposition='auto',
                    )])
                    fig.update_layout(
                        title="各题目得分分布",
                        xaxis_title="题目编号",
                        yaxis_title="得分",
                        yaxis_range=[0, 3],
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Noto Serif SC", size=12),
                        title_font=dict(size=16, color="#667eea")
                    )
                    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
        <span style="font-size: 1.8rem;">📖</span>
        <div>
            <h3 style="margin: 0; color: #667eea;">历史测评记录</h3>
            <p style="margin: 0.25rem 0 0 0; color: #7f8c8d;">查看您的测评历程和变化趋势</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 查询我的历史记录", use_container_width=True):
        assessments = assessment_system.get_user_assessments(current_user_phone)
        if assessments:
            st.success(f"✨ 找到 {len(assessments)} 条测评记录")
            history_data = []
            for idx, assessment in enumerate(assessments, 1):
                assessment_id, score, time_str, answers_str = assessment
                history_data.append({"序号": idx, "记录ID": assessment_id, "总分": score, "测评时间": time_str})
            df_history = pd.DataFrame(history_data)

            st.dataframe(
                df_history[["序号", "总分", "测评时间"]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "序号": st.column_config.NumberColumn("序号", width="small"),
                    "总分": st.column_config.NumberColumn("总分", width="small"),
                    "测评时间": st.column_config.DatetimeColumn("测评时间", width="medium")
                }
            )

            if len(assessments) > 1:
                col_chart1, col_chart2 = st.columns(2)
                with col_chart1:
                    fig_trend = go.Figure()
                    fig_trend.add_trace(go.Scatter(
                        x=df_history["测评时间"],
                        y=df_history["总分"],
                        mode='lines+markers',
                        line=dict(color='#667eea', width=3),
                        marker=dict(size=10, color='#764ba2')
                    ))
                    fig_trend.update_layout(
                        title="📈 测评分数趋势",
                        xaxis_title="测评时间",
                        yaxis_title="总分",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Noto Serif SC", size=12)
                    )
                    st.plotly_chart(fig_trend, use_container_width=True)

                with col_chart2:
                    level_counts = {
                        "无抑郁": len(df_history[df_history["总分"] <= 4]),
                        "轻度": len(df_history[(df_history["总分"] >= 5) & (df_history["总分"] <= 9)]),
                        "中度": len(df_history[(df_history["总分"] >= 10) & (df_history["总分"] <= 14)]),
                        "中重度": len(df_history[(df_history["总分"] >= 15) & (df_history["总分"] <= 19)]),
                        "重度": len(df_history[df_history["总分"] >= 20])
                    }
                    fig_pie = go.Figure(data=[go.Pie(
                        labels=list(level_counts.keys()),
                        values=list(level_counts.values()),
                        marker_colors=['#2ecc71', '#f39c12', '#e67e22', '#e74c3c', '#c0392b']
                    )])
                    fig_pie.update_layout(title="📊 测评结果分布", font=dict(family="Noto Serif SC", size=12))
                    st.plotly_chart(fig_pie, use_container_width=True)


if __name__ == "__main__":
    display_self_assessment()