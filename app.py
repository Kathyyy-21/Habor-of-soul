import streamlit as st
from streamlit_option_menu import option_menu
from login import init_login, get_current_user, is_logged_in
from main import display_home
import knowledge
import self_ass as self_module
import treehole as tree_module

st.markdown("""
<style>
    /* 隐藏顶部默认白条 */
    [data-testid="stHeader"] {
        background-color: transparent !important;
        height: 0px !important;
        visibility: hidden !important;
    }

    /* 隐藏侧边栏 */
    [data-testid="stSidebar"] {
        display: none !important;
    }

    /* 主内容顶格对齐 */
    .main .block-container {
        margin-top: 0rem !important;
        padding-top: 1rem !important;
    }

    /* 右上角用户信息样式 */
    .user-info {
        font-size: 16px;
        color: #663333;
        font-weight: 500;
        text-align: right;
        margin-bottom: 10px;
    }

    /* 文字链接样式 */
    .nav-link {
        color: #B86B77;
        font-size: 18px;
        font-weight: 500;
        text-decoration: none;
        padding: 10px 12px;
    }
    .nav-link:hover {
        color: #E2A479;
    }
</style>
""", unsafe_allow_html=True)


def set_simple_background(image_path, opacity=0.4):
    try:
        import base64
        with open(image_path, "rb") as f:
            img_data = f.read()
        b64_img = base64.b64encode(img_data).decode()

        st.markdown(f"""
            <style>
            .stApp {{
                background: 
                    linear-gradient(
                        rgba(255, 255, 255, {opacity}),
                        rgba(255, 255, 255, {opacity})
                    ),
                    url("data:image/jpg;base64,{b64_img}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .main .block-container {{
                background-color: rgba(255, 255, 255, 0.85);
                border-radius: 15px;
                padding: 2rem;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            }}
            </style>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"背景图片设置失败: {e}")


def main():
    # 页面配置必须放第一行
    st.set_page_config(
        page_title="心灵港湾",
        page_icon="💙",
        layout="wide",
    )

    login_system = init_login()
    set_simple_background("登陆界面图片.jpg", opacity=0.4)
    login_system.display_login_form()

    if not is_logged_in():
        return

    current_user = get_current_user()

    col_welcome, col_buttons = st.columns([3, 1])

    with col_welcome:
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; align-items: center;">
                <span style="color: #B86B77; font-size: 16px;">💕 欢迎，{current_user}！</span>
            </div>
        """, unsafe_allow_html=True)

    with col_buttons:
        # 退出和切换按钮放在同一行（使用水平布局）
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚪 切换账户", key="switch_btn", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.current_user = None
                st.query_params.clear()
                st.rerun()
        with col_btn2:
            if st.button("🔚 退出登录", key="logout_btn", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.current_user = None
                st.query_params.clear()
                st.rerun()

    # 减少顶部间距（移除了多余的空格和margin）
    st.markdown("""
    <style>
        /* 减少整个页面顶部的空白 */
        .main > div {
            padding-top: 0rem;
        }

        /* 减少block容器的上边距 */
        .block-container {
            padding-top: 1rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # 初始化 page 变量（解决报错！）
    if "page" not in st.session_state:
        st.session_state.page = "home"

    # 获取当前页面状态
    current_page = st.session_state.page

    # 文字导航（深蓝色，放大字体，减少与分割线的距离）
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # 为当前页面的按钮添加特殊样式类
        btn_home_type = "primary" if current_page == "home" else "secondary"
        if st.button("🏠 首页", use_container_width=True, type=btn_home_type, key="btn_home"):
            st.session_state.page = "home"
            st.rerun()
    with col2:
        btn_knowledge_type = "primary" if current_page == "knowledge" else "secondary"
        if st.button("📚 知识科普", use_container_width=True, type=btn_knowledge_type, key="btn_knowledge"):
            st.session_state.page = "knowledge"
            st.rerun()
    with col3:
        btn_self_type = "primary" if current_page == "self_ass" else "secondary"
        if st.button("🧪 自评工具", use_container_width=True, type=btn_self_type, key="btn_self"):
            st.session_state.page = "self_ass"
            st.rerun()
    with col4:
        btn_tree_type = "primary" if current_page == "treehole" else "secondary"
        if st.button("🌳 心灵树洞", use_container_width=True, type=btn_tree_type, key="btn_tree"):
            st.session_state.page = "treehole"
            st.rerun()

    st.markdown(f"""
    <style>
    /* 所有导航按钮的基础样式 */
    button[kind="secondary"] {{
        background: transparent !important;
        border: none !important;
        color: #000000 !important;
        font-size: 24px !important;
        font-weight: 600 !important;
        padding: 8px 0 !important;
        transition: all 0.3s ease !important;
    }}

    button[kind="secondary"]:hover {{
        color: #3B82F6 !important;
        background: transparent !important;
        transform: translateY(-2px) !important;
    }}

    /* 当前激活页面的按钮样式（淡粉色渐变） */
    button[kind="primary"] {{
        background: linear-gradient(135deg, #FFB6C1 0%, #FFC0CB 50%, #FFD1DC 100%) !important;
        border: none !important;
        color: white !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        padding: 8px 0 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(255, 182, 193, 0.4) !important;
        transition: all 0.3s ease !important;
    }}

    button[kind="primary"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 182, 193, 0.6) !important;
        background: linear-gradient(135deg, #FFC0CB 0%, #FFD1DC 50%, #FFE4E1 100%) !important;
    }}

    /* 退出和切换按钮样式 */
    button[key="switch_btn"], button[key="logout_btn"] {{
        background: transparent !important;
        border: 1px solid #B86B77 !important;
        color: #B86B77 !important;
        font-size: 14px !important;
        font-weight: normal !important;
        border-radius: 20px !important;
        padding: 4px 12px !important;
        transition: all 0.3s ease !important;
    }}

    button[key="switch_btn"]:hover, button[key="logout_btn"]:hover {{
        background: #B86B7710 !important;
        border-color: #E2A479 !important;
        color: #E2A479 !important;
        transform: translateY(-1px) !important;
    }}

    /* 缩小导航按钮和分割线之间的距离 */
    hr {{
        margin-top: 1px !important;
        margin-bottom: 5px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border: 1px solid #c4F4F2F;'>", unsafe_allow_html=True)

    if st.session_state.page == "home":
        set_simple_background("树洞背景.jpg", opacity=0.4)
        display_home()
    elif st.session_state.page == "knowledge":
        set_simple_background("蓝天背景.jpg", opacity=0.4)
        knowledge.display_knowledge()
    elif st.session_state.page == "self_ass":
        set_simple_background("蓝天背景.jpg", opacity=0.4)
        self_module.display_self_assessment()
    elif st.session_state.page == "treehole":
        set_simple_background("树洞背景.jpg", opacity=0.4)
        tree_module.display_treehole()


if __name__ == "__main__":
    main()