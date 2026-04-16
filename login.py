import streamlit as st
import sqlite3
import re
import hashlib

class LoginSystem:
    def __init__(self):
        self.db_name = "users.db"
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # 创建用户表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nickname TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        conn.commit()
        conn.close()

    def hash_password(self, password):
        """对密码进行哈希加密"""
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_phone(self, phone):
        """验证手机号格式"""
        pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(pattern, phone))

    def validate_password(self, password):
        """验证密码格式：至少6位，包含数字和字母"""
        if len(password) < 6:
            return False, "密码长度至少6位"
        if not re.search(r'\d', password):
            return False, "密码必须包含数字"
        if not re.search(r'[a-zA-Z]', password):
            return False, "密码必须包含字母"
        return True, ""

    def register_user(self, phone, password, nickname):
        """注册新用户"""
        if not self.validate_phone(phone):
            return False, "手机号格式不正确"

        valid, msg = self.validate_password(password)
        if not valid:
            return False, msg

        if not nickname or len(nickname.strip()) == 0:
            return False, "昵称不能为空"

        hashed_password = self.hash_password(password)

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT phone FROM users WHERE phone = ?", (phone,))
            if cursor.fetchone():
                return False, "该手机号已被注册"
            cursor.execute(
                "INSERT INTO users (phone, password, nickname) VALUES (?, ?, ?)",
                (phone, hashed_password, nickname.strip())
            )
            conn.commit()
            conn.close()
            return True, "注册成功！"
        except sqlite3.Error as e:
            return False, f"注册失败: {str(e)}"

    def login_user(self, phone, password):
        """用户登录"""
        if not self.validate_phone(phone):
            return False, "手机号格式不正确", None

        hashed_password = self.hash_password(password)

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT nickname FROM users WHERE phone = ? AND password = ?",
                (phone, hashed_password)
            )
            result = cursor.fetchone()
            conn.close()
            if result:
                return True, "登录成功！", result[0]
            else:
                return False, "手机号或密码错误", None
        except sqlite3.Error as e:
            return False, f"登录失败: {str(e)}", None

    def display_login_form(self):
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'current_user' not in st.session_state:
            st.session_state.current_user = None
        if 'current_user_phone' not in st.session_state:
            st.session_state.current_user_phone = None
        if 'show_register' not in st.session_state:
            st.session_state.show_register = False

        # 已登录直接返回
        if st.session_state.logged_in and st.session_state.current_user:
            return True

        # 顶部标题
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <div style="
                font-family: 'YouYuan';
                font-size: 72px;
                font-weight: bold;
                color: #E2A479;
                letter-spacing: 8px;
                line-height: 1.2;
                font-style: italic;
            ">
                欢迎来到心灵港湾
            </div>
            <div style="
                font-family: 'Times New Roman', serif;
                font-size: 40px;
                font-weight: bold;
                color: #82B6E8;
                letter-spacing: 4px;
                margin-top: 0.5rem;
                font-style: italic;
            ">
                Harbor of soul🚤
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_left, col_right = st.columns([1.2, 1])
        with col_left:
            pass
        with col_right:
            if not st.session_state.show_register:
                st.markdown("""
                <div style='text-align: center; margin-bottom: 20px;'>
                    <h1 style='color: #2C3E50; font-family: 'Times New Roman';font-weight: 500; margin-bottom: 5px;'>请登录您的账号</h1>
                    <p style='color: #7F8C8D; font-size: 16px;'>请使用您的账号信息安全登录</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('<div class="login-card">', unsafe_allow_html=True)
                with st.form("login_form"):
                    phone = st.text_input("📱 手机号", placeholder="请输入您的手机号")
                    password = st.text_input("🔑 密码", type="password", placeholder="请输入您的密码")
                    login_submitted = st.form_submit_button("登录", use_container_width=True)

                    if login_submitted:
                        if phone and password:
                            success, message, nickname = self.login_user(phone, password)
                            if success:
                                st.session_state.logged_in = True
                                st.session_state.current_user = nickname
                                st.session_state.current_user_phone = phone  # 保存手机号
                                st.success(f"✅ {message}")
                                st.rerun()
                            else:
                                st.error(f"❌ {message}")
                        else:
                            st.warning("⚠️ 请填写完整的登录信息")
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown(
                    '<div style="text-align:center; margin-top:1rem; color:#A88B70;">还没有账号？<a href="#" style="color:#E6A27B; text-decoration:none;">请先注册</a></div>',
                    unsafe_allow_html=True
                )
                if st.button("前往注册", key="go_register"):
                    st.session_state.show_register = True
                    st.rerun()

            else:
                st.markdown('<div class="login-card">', unsafe_allow_html=True)
                with st.form("register_form"):
                    phone = st.text_input("📱 手机号", placeholder="请输入11位手机号")
                    password = st.text_input("🔑 密码", type="password",
                                             placeholder="至少6位，包含数字和字母")
                    password_confirm = st.text_input("🔒 确认密码", type="password")
                    nickname = st.text_input("👤 昵称", placeholder="请输入您的昵称")
                    register_submitted = st.form_submit_button("完成注册", use_container_width=True)

                    if register_submitted:
                        if not all([phone, password, password_confirm, nickname]):
                            st.error("❌ 请填写所有必填项")
                        elif password != password_confirm:
                            st.error("❌ 两次输入的密码不一致")
                        else:
                            success, message = self.register_user(phone, password, nickname)
                            if success:
                                st.success(f"✅ {message}")
                                success_login, message_login, nickname_login = self.login_user(phone, password)
                                if success_login:
                                    st.session_state.logged_in = True
                                    st.session_state.current_user = nickname_login
                                    st.session_state.current_user_phone = phone  # 注册自动登录保存手机号
                                    st.session_state.show_register = False
                                    st.rerun()
                            else:
                                st.error(f"❌ {message}")
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown(
                    '<div style="text-align:center; margin-top:1rem; color:#A88B70;">已有账号？<a href="#" style="color:#E6A27B; text-decoration:none;">返回登录</a></div>',
                    unsafe_allow_html=True
                )
                if st.button("返回登录页面", key="go_login"):
                    st.session_state.show_register = False
                    st.rerun()

                with st.expander("📋 注册要求说明"):
                    st.markdown("""
                    ### 注册要求：
                    - 手机号必须是11位中国手机号
                    - 密码长度至少6位
                    - 密码必须包含数字和字母
                    - 昵称不能为空
                    - 昵称可以是中文、英文或数字
                    """)
        return False

    def require_login(self):
        """拦截未登录用户"""
        if not self.display_login_form():
            st.stop()

# 全局实例
login_system = LoginSystem()

def init_login():
    return login_system

def require_login():
    login_system.require_login()

def get_current_user():
    """获取当前登录昵称"""
    return st.session_state.get("current_user")

def get_current_user_phone():
    """获取当前登录手机号（给自评页面用）"""
    return st.session_state.get("current_user_phone")

def is_logged_in():
    """判断是否登录"""
    return st.session_state.get("logged_in", False)