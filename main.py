import streamlit as st
from streamlit_option_menu import option_menu
import base64
from login import init_login, require_login, get_current_user, is_logged_in

def display_home():
    # 主标题
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #2c3e50; font-size: 3.8rem; font-weight: 800; margin-bottom: 0.5rem;">
            🧸 欢迎来到心灵港湾
        </h1>
        <p style="color: #1a5276; font-size: 1.9rem; font-weight: 400; font-family: 'Times New Roman', serif; font-style: italic; letter-spacing: 0.5px;">
            "A warm and safe space for depression education and support"
        </p>
        <div style="height: 4px; width: 120px; background: linear-gradient(90deg, #8E6E8E, #B5A0B5, #D9C8D9, #B5A0B5, #8E6E8E); margin: 0.8rem auto 0; border-radius: 4px;"></div>
    </div>
    """, unsafe_allow_html=True)
    # 左右两列布局
    col_left, col_mid, col_right = st.columns([10, 0.3, 10], gap="small")

    with col_left:
        # 温暖的文字区域（无框，楷体）
        st.markdown("""
        <div style="margin: 0;">
            <h4 style="color: #1a5276; font-family: 'KaiTi', '楷体', 'STKaiti'; margin-bottom: 0.8rem;">📖 引言</h4>
            <p style="font-size: 1.2rem; line-height: 1.8; color: #1a5276; text-align: justify; font-family: 'KaiTi', '楷体', 'STKaiti', serif; margin-bottom: 1rem;">
                欢迎来到心灵港湾。在这里，你可以放下所有的防备与伪装。  
                无论您是抑郁症患者还是最近过得不开心，都欢迎来这里倾诉自我，找到解决方法。你的感受值得被听见，你的痛苦值得被看见。
            </p>
            <p style="font-size: 1.2rem; line-height: 1.8; color: #1a5276; text-align: justify; font-family: 'KaiTi', '楷体', 'STKaiti', serif; margin-bottom: 1rem;">
                如果心情生病了，那就先当个植物。吃吃喝喝、好好睡觉、晒晒太阳。
            </p>
            <p style="font-size: 1.2rem; line-height: 1.8; color: #1a5276; text-align: justify; font-family: 'KaiTi', '楷体', 'STKaiti', serif;">
                无论您何时来到网站，请记住这里都有一盏灯为你亮着，有一双手愿意伸向你。也欢迎您将这份温暖传递下去!
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_mid:
        # 淡淡的深蓝色垂直分割线
        st.markdown("""
        <div style="height: 100%; border-left: 1.5px solid #c5d9e8; margin-top: 0.5rem;"></div>
        """, unsafe_allow_html=True)

    with col_right:
        # 网站功能详细介绍（简洁标题）
        st.markdown("""
        <h3 style="color: #1a5276; text-align: center; font-family: 'KaiTi', '楷体', 'STKaiti';margin-bottom: 0.3rem;">🌱 这里有什么？</h3>
        """, unsafe_allow_html=True)

        features = [
            {"icon": "📚", "title": "抑郁症科普", "desc": "了解症状、成因与科学的治疗方法"},
            {"icon": "🧪", "title": "自评工具", "desc": "使用专业量表，了解自身情绪状态"},
            {"icon": "🌳", "title": "心灵树洞", "desc": "尽情分享心事，或给予他人温暖鼓励"},
        ]

        for f in features:
            st.markdown(f"""
            <div style="display: flex; align-items: flex-start; margin-bottom: 1.3rem; padding: 0.4rem 0.2rem; border-bottom: 1px solid #e0f0f5;">
                <div style="font-size: 2rem; margin-right: 0.8rem;">{f['icon']}</div>
                <div>
                    <div style="font-weight: 700; color: #2c3e50; font-size: 1rem;">{f['title']}</div>
                    <div style="color: #5d6d7e; font-size: 1rem;">{f['desc']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; font-family: 'KaiTi', '楷体', 'STKaiti';margin: 1rem 0 0.5rem 0;">
        <h4 style="color: #1a5276;">📋 轻松三步，开启自我关怀之旅</h4>
    </div>
    """, unsafe_allow_html=True)

    col_step1, col_step2, col_step3 = st.columns(3)
    with col_step1:
        st.markdown("""
        <div style="background-color: #FFF8dd; padding: 1rem; border-radius: 12px; border-left: 4px solid #f9a825;">
            <div style="font-weight: 700; color: #5A97D0; font-size: 1.1rem;">📖 探索知识</div>
            <div style="color: #4e342e; margin-top: 0.3rem; font-size: 0.9rem;">从左侧「知识科普」开始，了解抑郁症</div>
        </div>
        """, unsafe_allow_html=True)
    with col_step2:
        st.markdown("""
        <div style="background-color: #FFF8dd; padding: 1rem; border-radius: 12px; border-left: 4px solid #f9a825;">
            <div style="font-weight: 700; color: #5A97D0; font-size: 1.1rem;">🔍 自我评估</div>
            <div style="color: #4e342e; margin-top: 0.3rem; font-size: 0.9rem;">使用「自评工具」初步了解当前状态</div>
        </div>
        """, unsafe_allow_html=True)
    with col_step3:
        st.markdown("""
        <div style="background-color: #FFF8dd; padding: 1rem; border-radius: 12px; border-left: 4px solid #f9a825;">
            <div style="font-weight: 700; color: #5A97D0; font-size: 1.1rem;">🤝 寻求支持</div>
            <div style="color: #4e342e; margin-top: 0.3rem; font-size: 0.9rem;">通过「心灵树洞」获取支持</div>
        </div>
        """, unsafe_allow_html=True)

    # 紧急提醒
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #fff3e0; border-left: 5px solid #e67e22; padding: 1rem 1.5rem; border-radius: 16px; margin-top: 1rem;">
        <div style="font-weight: 800; color: #e67e22;">⚠️ 重要提醒</div>
        <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #2c3e50;">
            本网站提供科普与心理支持，<strong>不能替代专业医疗诊断或治疗</strong>。<br>
            若处于危机中，请立即拨打 <strong style="color: #e67e22;">心理援助热线：12356</strong> 或当地危机干预热线。
        </p>
    </div>
    """, unsafe_allow_html=True)

    if __name__ == "__main__":
        display_home()
if __name__ == "__main__":
    display_home()