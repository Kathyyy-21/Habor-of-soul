import streamlit as st
import sqlite3
from datetime import datetime


def init_treehole_in_user_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            likes INTEGER DEFAULT 0,
            user_name TEXT NOT NULL,
            is_public INTEGER DEFAULT 1
        )
    ''')

    try:
        cursor.execute("ALTER TABLE posts ADD COLUMN is_public INTEGER DEFAULT 1")
    except:
        pass

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_name TEXT NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_name TEXT NOT NULL,
            UNIQUE(post_id, user_name)
        )
    ''')

    conn.commit()
    conn.close()


def get_db():
    return sqlite3.connect("users.db")


def display_treehole():
    if not st.session_state.get("logged_in", False):
        st.warning("🔒 请先登录再进入心灵树洞")
        return

    current_user = st.session_state.get("current_user", "未知用户")
    init_treehole_in_user_db()

    st.markdown("""
    <style>
        .treehole-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 6px solid #4CAF50;
            transition: all 0.3s;
        }
        .treehole-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }
        .private-tag {
            background-color: #ffecb3;
            color: #ff6d00;
            padding: 2px 8px;
            border-radius: 8px;
            font-size: 0.8em;
            font-weight: bold;
        }
        .public-tag {
            background-color: #e8f5e9;
            color: #2e7d32;
            padding: 2px 8px;
            border-radius: 8px;
            font-size: 0.8em;
            font-weight: bold;
        }
        .reply-card {
            background: white;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.8rem 0;
            border-left: 4px solid #2196F3;
        }
        .post-meta {
            color: #666;
            font-size: 0.9em;
            margin-top: 0.8rem;
            padding-top: 0.8rem;
            border-top: 1px solid rgba(0,0,0,0.1);
        }
        .left-panel {
            background: linear-gradient(180deg, #f7f9fc 0%, #eef2f7 100%);
            padding: 20px;
            border-radius: 18px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }
        .stButton>button {
            border-radius: 10px;
            height: 3.1em;
            font-weight: 500;
        }
        .edit-area {
            background: #fff9e6;
            padding: 14px;
            border-radius: 10px;
            margin: 10px 0;
            border: 1px solid #ffd700;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center; color:#4CAF50'>🌳 心灵树洞</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center'>欢迎你，{current_user}</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    # ====================== 左侧发布 ======================
    with col1:
        st.markdown("### ✏️ 发布心事")

        with st.form("post_form", clear_on_submit=True):
            content = st.text_area("分享你的心情...", height=160, max_chars=1000)
            privacy = st.radio("帖子权限", ["公开（所有人可见）", "私密（仅自己可见）"], horizontal=True)
            is_public = 1 if privacy == "公开（所有人可见）" else 0
            submitted = st.form_submit_button("📤 发布", use_container_width=True)

            if submitted:
                if content.strip():
                    db = get_db()
                    db.execute("INSERT INTO posts (content, user_name, is_public) VALUES (?,?,?)",
                               (content.strip(), current_user, is_public))
                    db.commit()
                    db.close()
                    st.success("✅ 发布成功！")
                    st.rerun()
                else:
                    st.error("请输入内容")

        db = get_db()
        total_public = db.execute("SELECT COUNT(*) FROM posts WHERE is_public=1").fetchone()[0]
        my_total = db.execute("SELECT COUNT(*) FROM posts WHERE user_name=?", (current_user,)).fetchone()[0]
        total_replies = db.execute("SELECT COUNT(*) FROM replies").fetchone()[0]
        db.close()

        st.markdown("### 📊 统计")
        a, b, c = st.columns(3)
        a.metric("公开帖子", total_public)
        b.metric("我的帖子", my_total)
        c.metric("回复", total_replies)
        st.markdown('</div>', unsafe_allow_html=True)

    # ====================== 右侧 ======================
    with col2:
        tab_all, tab_mine = st.tabs(["🌐 全部公开帖子", "📁 我的帖子"])

        # -------------------------- 全部公开帖子（所有人） --------------------------
        with tab_all:
            st.markdown("### 🌐 全部公开帖子")
            st.caption("展示所有人的公开帖子")
            if st.button("🔄 刷新", key="ref_all"):
                st.rerun()

            db = get_db()
            posts = db.execute('''
                SELECT p.*,
                (SELECT COUNT(*) FROM replies WHERE post_id=p.id) AS reply_count
                FROM posts p
                WHERE p.is_public = 1
                ORDER BY p.created_at DESC
            ''').fetchall()
            db.close()

            if not posts:
                st.info("暂无公开帖子")

            for post in posts:
                post_id, content, created_at, likes, user_name, is_public, reply_count = post
                is_private = (is_public == 0)

                st.markdown(f"""
                <div class='treehole-card'>
                    <div style='font-size:1.1em; line-height:1.6'>{content}</div>
                    <div class='post-meta'>
                        <span class='public-tag'>公开</span> &nbsp;
                        👤 <b style='color:#4CAF50'>{user_name}</b><br>
                        📅 {datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S').strftime('%m-%d %H:%M')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # 点赞 + 回复
                c1, c2, _ = st.columns([1, 1, 5])
                with c1:
                    if st.button(f"❤️ {likes}", key=f"al_{post_id}"):
                        try:
                            db = get_db()
                            db.execute("INSERT INTO user_likes (post_id, user_name) VALUES (?,?)",
                                       (post_id, current_user))
                            db.execute("UPDATE posts SET likes = likes +1 WHERE id=?", (post_id,))
                            db.commit()
                            db.close()
                        except:
                            st.warning("已点赞")
                        st.rerun()
                with c2:
                    if st.button(f"💬 {reply_count}", key=f"ar_{post_id}"):
                        st.session_state.reply_target = post_id
                        st.rerun()

                # 回复框
                if st.session_state.get("reply_target") == post_id:
                    with st.form(f"arf{post_id}", clear_on_submit=True):
                        txt = st.text_area("你的回复")
                        s, c = st.columns([3, 1])
                        send = s.form_submit_button("发送")
                        cancel = c.form_submit_button("取消")
                        if send:
                            if txt:
                                db = get_db()
                                db.execute("INSERT INTO replies (post_id, content, user_name) VALUES (?,?,?)",
                                           (post_id, txt, current_user))
                                db.commit()
                                db.close()
                                st.success("回复成功")
                                st.session_state.reply_target = None
                                st.rerun()
                        if cancel:
                            st.session_state.reply_target = None
                            st.rerun()

                # 查看回复（修复版：用on_change回调）
                db = get_db()
                replies = db.execute("SELECT * FROM replies WHERE post_id=?", (post_id,)).fetchall()
                db.close()
                if replies:
                    # 初始化状态
                    show_key = f"ashow_{post_id}"
                    if show_key not in st.session_state:
                        st.session_state[show_key] = False

                    # 用checkbox代替按钮，彻底解决状态修改报错
                    st.checkbox(
                        f"📄 查看回复 ({len(replies)})",
                        value=st.session_state[show_key],
                        key=show_key
                    )

                    if st.session_state[show_key]:
                        for r in replies:
                            rid, _, rcont, rtime, ruser = r
                            st.markdown(f"""
                            <div class='reply-card'>
                                <div>{rcont}</div>
                                <div style='font-size:0.85em;color:#888'>👤 {ruser} • {datetime.strptime(rtime, '%Y-%m-%d %H:%M:%S').strftime('%m-%d %H:%M')}</div>
                            </div>
                            """, unsafe_allow_html=True)
                st.divider()

        # -------------------------- 我的帖子（可编辑删除） --------------------------
        with tab_mine:
            st.markdown("### 📁 我的帖子")
            st.caption("只有你自己能看见和管理")
            if st.button("🔄 刷新", key="ref_my"):
                st.rerun()

            db = get_db()
            my_posts = db.execute('''
                SELECT p.*,
                (SELECT COUNT(*) FROM replies WHERE post_id=p.id) AS reply_count
                FROM posts p
                WHERE p.user_name = ?
                ORDER BY p.created_at DESC
            ''', (current_user,)).fetchall()
            db.close()

            if not my_posts:
                st.info("你还没有发布帖子")

            for post in my_posts:
                post_id, content, created_at, likes, user_name, is_public, reply_count = post
                is_private = (is_public == 0)
                tag = '<span class="private-tag">私密</span>' if is_private else '<span class="public-tag">公开</span>'

                st.markdown(f"""
                <div class='treehole-card'>
                    <div style='font-size:1.1em; line-height:1.6'>{content}</div>
                    <div class='post-meta'>
                        {tag} &nbsp;
                        👤 <b style='color:#4CAF50'>{user_name}</b><br>
                        📅 {datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S').strftime('%m-%d %H:%M')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ====================== 只有我的帖子出现：编辑/删除 ======================
                with st.expander("✏️ 编辑 / 删除帖子"):
                    st.markdown('<div class="edit-area">', unsafe_allow_html=True)
                    new_content = st.text_area("修改内容", value=content, key=f"e{post_id}")
                    new_pub = st.radio("权限", ["公开", "私密"], index=0 if is_public else 1, horizontal=True,
                                       key=f"p{post_id}")
                    new_pub_val = 1 if new_pub == "公开" else 0
                    col_sv, col_del = st.columns(2)
                    with col_sv:
                        if st.button("💾 保存", key=f"sv{post_id}", use_container_width=True):
                            db = get_db()
                            db.execute("UPDATE posts SET content=?, is_public=? WHERE id=?",
                                       (new_content.strip(), new_pub_val, post_id))
                            db.commit()
                            db.close()
                            st.success("已保存")
                            st.rerun()
                    with col_del:
                        if st.button("🗑️ 删除", key=f"del{post_id}", use_container_width=True):
                            db = get_db()
                            db.execute("DELETE FROM posts WHERE id=?", (post_id,))
                            db.commit()
                            db.close()
                            st.warning("已删除")
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

                # 点赞 + 回复
                c1, c2, _ = st.columns([1, 1, 5])
                with c1:
                    if st.button(f"❤️ {likes}", key=f"ml_{post_id}"):
                        try:
                            db = get_db()
                            db.execute("INSERT INTO user_likes (post_id, user_name) VALUES (?,?)",
                                       (post_id, current_user))
                            db.execute("UPDATE posts SET likes = likes +1 WHERE id=?", (post_id,))
                            db.commit()
                            db.close()
                        except:
                            st.warning("已点赞")
                        st.rerun()
                with c2:
                    if st.button(f"💬 {reply_count}", key=f"mr_{post_id}"):
                        st.session_state.reply_target = post_id
                        st.rerun()

                if st.session_state.get("reply_target") == post_id:
                    with st.form(f"mrf{post_id}", clear_on_submit=True):
                        txt = st.text_area("你的回复")
                        s, c = st.columns([3, 1])
                        send = s.form_submit_button("发送")
                        cancel = c.form_submit_button("取消")
                        if send:
                            if txt:
                                db = get_db()
                                db.execute("INSERT INTO replies (post_id, content, user_name) VALUES (?,?,?)",
                                           (post_id, txt, current_user))
                                db.commit()
                                db.close()
                                st.success("回复成功")
                                st.session_state.reply_target = None
                                st.rerun()
                        if cancel:
                            st.session_state.reply_target = None
                            st.rerun()

                # 查看回复（修复版）
                db = get_db()
                replies = db.execute("SELECT * FROM replies WHERE post_id=?", (post_id,)).fetchall()
                db.close()
                if replies:
                    show_key = f"mshow_{post_id}"
                    if show_key not in st.session_state:
                        st.session_state[show_key] = False

                    st.checkbox(
                        f"📄 查看回复 ({len(replies)})",
                        value=st.session_state[show_key],
                        key=show_key
                    )

                    if st.session_state[show_key]:
                        for r in replies:
                            rid, _, rcont, rtime, ruser = r
                            st.markdown(f"""
                            <div class='reply-card'>
                                <div>{rcont}</div>
                                <div style='font-size:0.85em;color:#888'>👤 {ruser} • {datetime.strptime(rtime, '%Y-%m-%d %H:%M:%S').strftime('%m-%d %H:%M')}</div>
                            </div>
                            """, unsafe_allow_html=True)
                st.divider()


if __name__ == "__main__":
    st.set_page_config(page_title="心灵树洞", page_icon="🌳", layout="wide")
    display_treehole()