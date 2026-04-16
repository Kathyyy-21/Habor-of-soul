import streamlit as st
def display_knowledge():

    st.set_page_config(
        page_title="心灵港湾 - 抑郁症知识科普",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 隐藏默认菜单和页脚
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # 添加自定义CSS
    st.markdown("""
    <style>
    /* 页面标题样式 */
    .main-title {
        color: #2c3e50;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid #f8bbd9;
        margin-bottom: 2rem;
    }

    /* 主版块标题 - 可点击展开 */
    .section-title {
        color: #3498db;
        font-size: 2rem !important;
        font-weight: 600;
        margin: 1.5rem 0 0.5rem 0;
        padding: 0.8rem 1rem;
        background: linear-gradient(135deg, rgba(52, 152, 219, 0.1), rgba(52, 152, 219, 0.05));
        border-radius: 8px;
        border-left: 5px solid #3498db;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .section-title:hover {
        background: linear-gradient(135deg, rgba(52, 152, 219, 0.15), rgba(52, 152, 219, 0.1));
        transform: translateX(5px);
    }

    /* 子版块标题 */
    .sub-section-title {
        color: #2c3e50;
        font-size: 1.6rem !important;
        font-weight: 600;
        margin: 1.5rem 0 0.8rem 0;
        padding-left: 0.8rem;
        border-left: 4px solid #f8bbd9;
    }

    /* 星级评分 */
    .star-rating {
        display: inline-block;
        margin-left: 10px;
    }

    .star {
        color: #f39c12;
        font-size: 1.2rem;
        margin-right: 2px;
    }

    /* 信息卡片 */
    .info-card {
        background: linear-gradient(135deg, #f8fafc, #ffffff);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #3498db;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
    }

    /* 治疗方法卡片 */
    .treatment-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease;
    }

    .treatment-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
s
    /* 误解列表样式 */
    .misconception-item {
        background: rgba(255, 245, 245, 0.8);
        border-left: 4px solid #e74c3c;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }

    /* 关键点强调 */
    .key-point {
        background: linear-gradient(135deg, rgba(52, 152, 219, 0.1), rgba(155, 89, 182, 0.1));
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid rgba(52, 152, 219, 0.2);
    }

    /* 标签样式 */
    .tag {
        display: inline-block;
        background: #e8f4fc;
        color: #2980b9;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.9rem;
        border: 1px solid rgba(52, 152, 219, 0.2);
    }

    /* 分隔线美化 */
    .divider {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #3498db, transparent);
        margin: 2rem 0;
    }

    /* 严重程度条 */
    .severity-bar {
        height: 10px;
        border-radius: 5px;
        margin: 5px 0 15px 0;
        background: linear-gradient(90deg, #2ecc71, #f1c40f, #e74c3c);
    }

    /* 类型卡片 */
    .type-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    /* 治疗标签 */
    .treatment-tag {
        display: inline-block;
        background: linear-gradient(135deg, #a8e6cf, #dcedc1);
        color: #2c3e50;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.9rem;
        border: 1px solid rgba(168, 230, 207, 0.5);
    }

    /* 折叠指示器 */
    .expand-indicator {
        float: right;
        font-size: 1.2rem;
        color: #3498db;
        transition: transform 0.3s ease;
    }

    .expanded .expand-indicator {
        transform: rotate(90deg);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">📚 抑郁症知识科普</h1>', unsafe_allow_html=True)

    # 页面介绍
    st.markdown("""
    <div style="text-align: center; padding: 1rem; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #546e7a;">
            🌈 <strong>了解是理解的第一步，理解是关怀的开始</strong>
        </p>
        <p style="color: #7f8c8d; font-style: italic;">
            点击下方各版块标题查看详细内容
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("### 💡 认识抑郁症|Understanding Depression", expanded=False):
        st.markdown('<div class="sub-section-title">📖 抑郁症的定义</div>', unsafe_allow_html=True)
        # 添加自定义CSS样式
        st.markdown("""
        <style>
            .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
                font-family: 'KaiTi', '楷体', 'STKaiti', serif !important;
            }

            /* 大标题深蓝色 */
            .stMarkdown h3 {
                color: #1a5276 !important;
                font-weight: 600;
                margin-top: 1rem;
            }

            /* 信息卡片样式 */
            .info-card {
                background: linear-gradient(135deg, #e8f4f8 0%, #d1e9f5 100%);
                padding: 1.2rem;
                border-radius: 15px;
                margin-bottom: 1rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                font-family: 'KaiTi', '楷体', 'STKaiti', serif;
            }

            .info-card h4 {
                color: #1a5276;
                margin-bottom: 0.5rem;
                font-weight: 600;
            }

            .info-card p {
                color: #2c3e50;
                line-height: 1.6;
            }

            /* 误解澄清卡片样式 */
            .misconception-item {
                background-color: #fef9e7;
                padding: 1rem 1.2rem;
                border-radius: 12px;
                margin-bottom: 1rem;
                border-left: 4px solid #e67e22;
                font-family: 'KaiTi', '楷体', 'STKaiti', serif;
            }

            .misconception-item h4 {
                color: #e67e22;
                margin-bottom: 0.5rem;
                font-size: 1rem;
            }

            .misconception-item p {
                color: #2c3e50;
                line-height: 1.6;
                margin: 0;
            }

            /* 子标题样式 */
            .sub-section-title {
                font-size: 1.6rem;
                font-weight: 600;
                color: #1a5276;
                margin: 1.5rem 0 1rem 0;
                padding-bottom: 0.3rem;
                border-bottom: 3px solid #5dade2;
                display: inline-block;
                font-family: 'KaiTi', '楷体', 'STKaiti', serif;
            }

            /* 标签页样式 */
            .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
                font-family: 'KaiTi', '楷体', 'STKaiti', serif !important;
                font-size: 1rem;
            }
        </style>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            <h3 style="color: #1a5276; font-family: 'KaiTi', '楷体', 'STKaiti', serif;">什么是抑郁症？</h3>

            <p style="font-family: 'KaiTi', '楷体', 'STKaiti', serif; font-size: 1rem; line-height: 1.8;">
            <strong>抑郁症</strong>是一种常见但严重的心境障碍，它不是简单的"心情不好"，而是一种需要专业干预的医学状况。
            </p>

            <h4 style="color: #1a5276; font-family: 'KaiTi', '楷体', 'STKaiti', serif; margin-top: 1rem;">核心特征：</h4>
            <ul style="font-family: 'KaiTi', '楷体', 'STKaiti', serif; line-height: 1.8;">
                <li><strong>持续性</strong>：症状持续至少两周以上</li>
                <li><strong>广泛性</strong>：影响生活的多个方面</li>
                <li><strong>功能性损害</strong>：明显影响日常生活和工作能力</li>
            </ul>

            <h4 style="color: #1a5276; font-family: 'KaiTi', '楷体', 'STKaiti', serif; margin-top: 1rem;">💭 正确认识</h4>
            <p style="font-family: 'KaiTi', '楷体', 'STKaiti', serif; line-height: 1.8;">
            患有抑郁症并不可耻，就像感冒发烧一样，需要及时关注和治疗。早期识别和干预对康复至关重要。
            </p>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="info-card">
                <h4>🌍 普遍性</h4>
                <p>全球约有3.4亿抑郁症患者，是最常见的精神障碍之一。</p>
            </div>

            <div class="info-card">
                <h4>💖 可治疗性</h4>
                <p>70-80%的患者通过规范治疗可获得明显改善。</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="sub-section-title">⚡ 核心症状</div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["情感症状", "生理症状", "认知行为症状"])

        with tab1:
            st.markdown("""
            <h4 style="color: #1a5276; font-family: 'KaiTi', '楷体', 'STKaiti', serif;">😔 情感与情绪症状</h4>
            <ul style="font-family: 'KaiTi', '楷体', 'STKaiti', serif; line-height: 1.8;">
                <li><strong>持续情绪低落</strong>：感到悲伤、空虚、绝望</li>
                <li><strong>兴趣丧失</strong>：对以往喜欢的活动失去兴趣</li>
                <li><strong>易怒烦躁</strong>：容易被小事激怒</li>
                <li><strong>情感麻木</strong>：感觉不到快乐或悲伤</li>
                <li><strong>无价值感</strong>：过度的自责、内疚</li>
            </ul>
            <p style="font-family: 'KaiTi', '楷体', 'STKaiti', serif; font-style: italic; color: #7f8c8d;">"感觉心里空荡荡的，对什么都提不起兴趣"</p>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("""
            <h4 style="color: #1a5276; font-family: 'KaiTi', '楷体', 'STKaiti', serif;">🏃 生理与躯体症状</h4>
            <ul style="font-family: 'KaiTi', '楷体', 'STKaiti', serif; line-height: 1.8;">
                <li><strong>睡眠障碍</strong>：失眠（难以入睡/早醒）或嗜睡</li>
                <li><strong>食欲改变</strong>：食欲减退或暴饮暴食</li>
                <li><strong>疲劳乏力</strong>：即使休息也无法缓解的疲劳</li>
                <li><strong>躯体疼痛</strong>：头痛、背痛、胃痛等</li>
            </ul>
            <p style="font-family: 'KaiTi', '楷体', 'STKaiti', serif; font-style: italic; color: #7f8c8d;">"身体像灌了铅一样沉重，总是感觉很累"</p>
            """, unsafe_allow_html=True)

        with tab3:
            st.markdown("""
            <h4 style="color: #1a5276; font-family: 'KaiTi', '楷体', 'STKaiti', serif;">🧠 认知与行为症状</h4>
            <ul style="font-family: 'KaiTi', '楷体', 'STKaiti', serif; line-height: 1.8;">
                <li><strong>注意力不集中</strong>：难以专注，记忆力下降</li>
                <li><strong>决策困难</strong>：即使小事也难以决定</li>
                <li><strong>思维迟缓</strong>：感觉思维变慢</li>
                <li><strong>消极思维</strong>：对未来悲观，看不到希望</li>
                <li><strong>行为退缩</strong>：回避社交，减少活动</li>
            </ul>
            <p style="font-family: 'KaiTi', '楷体', 'STKaiti', serif; font-style: italic; color: #7f8c8d;">"大脑好像生锈了，什么都想不清楚"</p>
            """, unsafe_allow_html=True)

        st.markdown('<div class="sub-section-title">❌ 常见误解与真相</div>', unsafe_allow_html=True)
        st.markdown("""
        <h4 style="color: #1a5276; font-family: 'KaiTi', '楷体', 'STKaiti', serif;">澄清误解，消除污名</h4>

        <div class="misconception-item">
            <h4>❌ 误解："抑郁症就是想太多"</h4>
            <p>✅ <strong>真相：</strong> 抑郁症有明确的生物化学基础，涉及大脑神经递质失衡，不是性格缺陷或意志力问题。</p>
        </div>

        <div class="misconception-item">
            <h4>❌ 误解："只要想开点就能好"</h4>
            <p>✅ <strong>真相：</strong> 抑郁症需要专业治疗，无法仅靠"振作起来"或"积极思考"来克服。</p>
        </div>

        <div class="misconception-item">
            <h4>❌ 误解："抑郁症患者都有自杀倾向"</h4>
            <p>✅ <strong>真相：</strong> 不是所有抑郁症患者都有自杀念头，但自杀风险确实增加，需要关注和防范。</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

    with st.expander("### 🔬 抑郁症类型|Types of Depression", expanded=False):
        st.markdown("""
        <div class="key-point">
        <h4>⭐ 严重程度说明</h4>
        <p>用<strong>★表示严重程度</strong>，★越多表示对生活功能影响越大（1-5星，5星最严重）</p>
        <p><em>注：实际诊断和严重程度评估需由专业医生进行</em></p>
        </div>
        """, unsafe_allow_html=True)

        # 创建星级函数
        def create_star_rating(level):
            """创建星级评分（1-5星）"""
            stars = "★" * level + "☆" * (5 - level)
            return f"{stars} ({level}/5)"

        # 抑郁症类型数据（包含案例）
        depression_types = [
            {
                "name": "重性抑郁障碍",
                "icon": "🔴",
                "desc": "最典型的抑郁症形式，症状严重且持续，明显影响日常生活。核心特征是至少持续2周的显著情绪低落、兴趣或愉悦感丧失，同时伴随多种附加症状。",
                "symptoms": ["持续情绪低落、兴趣丧失、体重显著变化、自杀念头"],
                "severity": 5,
                "prevalence": "约7%成年人",
                "treatment": "药物+心理治疗",
                "case": {
                    "name": "小林",
                    "age": 28,
                    "occupation": "互联网公司产品经理",
                    "story": "小林曾是团队里的'拼命三郎'，连续三年获得优秀员工。但从去年秋天开始，她发现自己再也提不起劲了。每天早上要花两个小时才能从床上爬起来，到了公司也无法集中注意力，曾经热爱的产品设计工作变得索然无味。她开始暴饮暴食，体重增加了15公斤。更可怕的是，她开始觉得'活着没有意义'，甚至偷偷搜索过自杀的方法。直到有一天，她在工位上突然崩溃大哭，被同事送到了医院，才被确诊为重度抑郁症。经过半年的药物治疗和心理咨询，小林慢慢找回了生活的勇气。她说：'最难的是承认自己生病了，但接受治疗是我做过最正确的决定。'"
                }
            },
            {
                "name": "持续性抑郁障碍",
                "icon": "🟡",
                "desc": "症状表现相对重性抑郁障碍更温和，但病程更长。持续时间至少2年，长期存在的轻度抑郁状态。",
                "symptoms": ["长期情绪低落、低能量、低自尊、绝望感"],
                "severity": 3,
                "prevalence": "约3%成年人",
                "treatment": "心理治疗为主",
                "case": {
                    "name": "阿杰",
                    "age": 35,
                    "occupation": "中学教师",
                    "story": "阿杰已经记不清自己'开心'是什么感觉了。从大学开始，他就一直处于一种淡淡的灰色情绪中。他可以正常上班、备课、讲课，但总觉得生活没有色彩。朋友们说他'性格内向'，家人觉得他'想太多'。他以为自己只是天生悲观，直到一次学校组织的心理健康讲座上，他才意识到自己可能生病了。心理医生告诉他，这是持续性抑郁障碍，也叫'高功能抑郁症'。阿杰开始接受认知行为治疗，学习识别和改变消极思维模式。'我现在知道，那种长期的低落不是我的错，而是一种可以治疗的疾病。'"
                }
            },
            {
                "name": "季节性情感障碍",
                "icon": "❄️",
                "desc": "特定季节（通常是冬季）出现的抑郁症状，与光照减少有关，春季或夏季症状会自行缓解。",
                "symptoms": ["季节性情绪低落、嗜睡、食欲增加（尤其嗜甜）、社交退缩"],
                "severity": 3,
                "prevalence": "约5%人群",
                "treatment": "光照疗法、心理治疗",
                "case": {
                    "name": "小雯",
                    "age": 26,
                    "occupation": "自由插画师",
                    "story": "小雯发现自己有一个奇怪的规律：每年11月到次年3月，她就像变了一个人。她会变得嗜睡，每天要睡12个小时以上；疯狂想吃甜食和碳水化合物；对画画完全失去兴趣，甚至连画笔都不想碰。但一到春天，她又会恢复活力，灵感迸发。这种情况持续了五年，她一直以为是自己'太矫情'。直到她去看了医生，才知道这是季节性情感障碍。医生建议她使用光照疗法，每天早晨照射30分钟特殊灯箱。'现在我明白了，这不是意志力的问题，而是我的大脑对光照的化学反应不同。'现在的小雯会在冬天提前做好准备，用光照疗法和规律作息度过难关。"
                }
            },
            {
                "name": "经前期烦躁障碍",
                "icon": "🌸",
                "desc": "属于与月经周期相关的抑郁障碍，症状在月经来潮前1-2周开始出现，月经来潮后迅速缓解",
                "symptoms": ["显著情绪波动、易怒/愤怒、情绪低落、焦虑紧张"],
                "severity": 3,
                "prevalence": "3-8%育龄女性",
                "treatment": "荷尔蒙治疗、药物",
                "case": {
                    "name": "小雅",
                    "age": 32,
                    "occupation": "律师事务所合伙人",
                    "story": "在同事眼中，小雅是雷厉风行的精英律师。但每个月有那么一周，她会变成一个'定时炸弹'——无缘无故对助理发火、在法庭上控制不住想哭、焦虑到失眠。她以为自己只是压力大，但当她发现自己在这个时期出现过自残念头时，她终于去看了医生。诊断结果是经前期烦躁障碍（PMDD）。'医生说这不是普通的经前综合征，而是一种真实的激素敏感性抑郁障碍。'通过调整避孕药和抗抑郁药物，小雅的症状得到了极大缓解。'我再也不用每个月'消失'一周了，这感觉真好。'"
                }
            },
            {
                "name": "破坏性心境失调障碍",
                "icon": "👦",
                "desc": "儿童和青少年中出现的严重、持续的易怒和频繁的情绪爆发",
                "symptoms": ["严重反复发脾气、持续易怒/愤怒、攻击性行为、功能损害"],
                "severity": 4,
                "prevalence": "2-5%儿童青少年",
                "treatment": "家庭治疗、行为治疗",
                "case": {
                    "name": "小浩",
                    "age": 10,
                    "occupation": "小学四年级学生",
                    "story": "小浩的妈妈已经记不清被老师叫去学校多少次了。这个男孩会在课堂上突然掀翻桌子，因为铅笔断了就尖叫20分钟，把同学推倒在地只因为对方看了他一眼。起初家人以为他只是'熊孩子'，但小浩自己也很难过：'我也不想这样，但我控制不住自己。'在儿童精神科医生的帮助下，小浩被诊断为破坏性心境失调障碍（DMDD）。通过家庭治疗、行为训练和情绪管理课程，小浩慢慢学会了识别自己的情绪预警信号。'现在生气的时候，我会深呼吸，告诉老师我需要去冷静角。'虽然进步缓慢，但小浩的妈妈看到了希望：'他不再是那个被所有人讨厌的孩子了。'"
                }
            },
        ]

        # 显示每种类型
        for i, dep_type in enumerate(depression_types, 1):
            stars = create_star_rating(dep_type['severity'])
            expander_title = f"{dep_type['icon']} **{dep_type['name']}** {stars}"

            with st.expander(expander_title, expanded=False):

                col1, col2 = st.columns([3, 2])

                with col1:
                    st.markdown(f"""
                    **📝 描述：** {dep_type['desc']}

                    **🩺 主要症状：**
                    """)
                    for symptom in dep_type['symptoms']:
                        st.markdown(f"- {symptom}")

                    st.markdown(f"""
                    **💊 主要治疗：** {dep_type['treatment']}
                    """)

                with col2:
                    # 严重程度可视化
                    st.markdown("**📊 严重程度：**")
                    severity_percent = (dep_type['severity'] / 5) * 100
                    st.markdown(f"""
                    <div class="severity-bar" style="width:{severity_percent}%; height:8px; background:linear-gradient(90deg,#e74c3c,#f39c12); border-radius:4px;"></div>
                    <br>
                    """, unsafe_allow_html=True)

                    # 患病率卡片
                    st.markdown(f"""
                    <div class="info-card" style="background:#f0f7ff; padding:0.8rem; border-radius:10px;">
                        <h4 style="margin:0 0 0.3rem 0;">📈 流行病学数据</h4>
                        <p style="margin:0;"><strong>患病率：</strong>{dep_type['prevalence']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # 案例分享部分
                case = dep_type['case']
                st.markdown("---")
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fdfbfb 0%, #f0f4f8 100%); 
                            padding: 1.2rem 1.5rem; 
                            border-radius: 16px; 
                            border-left: 5px solid #5dade2;
                            margin-top: 0.5rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="font-size: 1.8rem;">💭</span>
                        <h4 style="color: #1a5276; margin: 0 0 0 0.5rem;">真实案例分享 · {case['name']}（{case['age']}岁，{case['occupation']}）</h4>
                    </div>
                    <p style="font-family: 'KaiTi', '楷体', 'STKaiti', serif; 
                              font-size: 0.95rem; 
                              line-height: 1.8; 
                              color: #2c3e50; 
                              text-align: justify;
                              margin: 0;">
                        "{case['story']}"
                    </p>
                    <div style="margin-top: 0.8rem; text-align: right; font-size: 0.85rem; color: #7f8c8d; font-style: italic;">
                        —— 经本人同意匿名分享
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    with st.expander("### 🔍 成因与风险因素|Causes and risk factors", expanded=False):
        st.markdown("""
        <div class="key-point">
        <h4>🌐 生物-心理-社会模型</h4>
        <p>现代医学认为抑郁症是<strong>生物、心理、社会因素</strong>相互作用的结果。了解这些因素有助于消除自责，科学看待疾病。</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="sub-section-title">🧬 生物因素</div>', unsafe_allow_html=True)
            st.markdown("""
            ### 遗传因素
            - **家族史**：一级亲属患病风险增加2-3倍
            - **基因易感性**：多个基因相互作用

            ### 神经生物学
            - **神经递质失衡**：血清素、多巴胺、去甲肾上腺素
            - **大脑结构**：海马体、前额叶皮质变化
            - **神经内分泌**：下丘脑-垂体-肾上腺轴功能异常
            """)

        with col2:
            st.markdown('<div class="sub-section-title">💭 心理因素</div>', unsafe_allow_html=True)
            st.markdown("""
            ### 人格特质
            - **神经质**：情绪不稳定性
            - **完美主义**：过高自我要求，追求极致完美
            - **低自尊**：缺乏自我价值感

            ### 认知模式
            - **消极认知三联征**：对自我、世界、未来的负面看法
            - **反刍思维**：反复思考负面事件
            - **认知扭曲**：非黑即白、灾难化思维

            """)

        with col3:
            st.markdown('<div class="sub-section-title">🌍 环境因素</div>', unsafe_allow_html=True)
            st.markdown("""
            ### 生活事件
            - **重大丧失**：丧亲、失恋
            - **创伤经历**：虐待、灾难
            - **慢性压力**：学习、经济、关系压力

            ### 社会环境
            - **社会支持缺乏**：孤独、隔离
            - **歧视与污名**：心理健康污名化
            - **文化因素**：情感表达规范

            """)

    st.markdown("---")

    with st.expander("### 💊 治疗方法|Therapeutic method", expanded=False):

        # 治疗方法子版块
        st.markdown('<div class="sub-section-title">🧠 心理治疗</div>', unsafe_allow_html=True)
        st.markdown("""
        ### 主要心理治疗方法

        <div class="treatment-card">
            <h4>💡 认知行为疗法</h4>
            <p><strong>Cognitive Behavioral Therapy (CBT)</strong></p>
            <p><em>帮助识别和改变负面思维和行为模式</em></p>
            <p>✅ <strong>有效性：</strong> 高，特别适用于轻中度抑郁症</p>
            <p>⏱️ <strong>疗程：</strong> 通常12-20次会谈</p>
        </div>

        <div class="treatment-card">
            <h4>🤝 人际心理治疗</h4>
            <p><strong>Interpersonal Psychotherapy (IPT)</strong></p>
            <p><em>专注于改善人际关系和社交技能</em></p>
            <p>✅ <strong>有效性：</strong> 高，特别适用于人际问题相关的抑郁</p>
            <p>⏱️ <strong>疗程：</strong> 通常12-16次会谈</p>
        </div>

        """, unsafe_allow_html=True)

        st.markdown('<div class="sub-section-title">💊 药物治疗</div>', unsafe_allow_html=True)
        st.markdown("""
        ### 常用抗抑郁药物

        | 类别 | 代表药物 | 特点 | 常见副作用 |
        |------|----------|------|------------|
        | **SSRIs** | 氟西汀、舍曲林、帕罗西汀 | 一线选择，副作用相对较少 | 恶心、失眠、性功能障碍 |
        | **SNRIs** | 文拉法辛、度洛西汀 | 对疼痛症状也有改善 | 恶心、头晕、血压升高 |
        | **NaSSA** | 米氮平 | 改善睡眠和食欲 | 嗜睡、体重增加 |
        | **其他** | 安非他酮、阿戈美拉汀 | 对性功能影响小，改善睡眠 | 头痛、焦虑、恶心 |

        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sub-section-title">🌿 生活方式调整</div>', unsafe_allow_html=True)
        st.markdown("""
        ### 生活方式调整策略

        #### 🏃‍♂️ 身体活动
        - **规律运动**：每周3-5次，每次30分钟中等强度运动
        - **运动类型**：快走、跑步、游泳、瑜伽、太极
        - **益处**：促进内啡肽分泌，改善情绪和睡眠

        #### 🥗 饮食营养
        - **均衡饮食**：富含Omega-3（鱼类）、维生素B群、维生素D
        - **避免**：过量咖啡因、酒精、高糖加工食品
        - **建议**：地中海饮食模式

        #### 😴 睡眠管理
        - **规律作息**：固定时间起床和睡觉
        - **睡眠环境**：安静、黑暗、凉爽
        - **睡前习惯**：避免电子产品，建立放松程序

        #### 🤝 社会支持
        - **保持连接**：与支持性的人保持联系
        - **寻求支持**：考虑加入支持团体
        - **设定边界**：学会说"不"，保护自己的精力

        ### 🔖 实用生活贴士
        """)

        # 生活贴士标签
        tags = [
            "规律作息", "健康饮食", "适度运动", "社交活动",
            "放松练习", "培养爱好", "正念冥想", "感恩日记",
            "晒太阳", "减少屏幕时间", "亲近自然", "艺术创作",
            "宠物陪伴", "志愿服务", "学习新技能", "整理环境"
        ]

        # 分组显示标签
        cols = st.columns(4)
        for i, tag in enumerate(tags):
            with cols[i % 4]:
                st.markdown(f'<span class="treatment-tag">{tag}</span>', unsafe_allow_html=True)

    st.markdown("---")  # 添加分隔线
    # 单列显示文字内容
    st.markdown("### 🌈 给正在阅读的你")
    st.write("一些温暖的话语，希望能为你带来一丝慰藉")

    st.markdown("---")

    # 温馨引语
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #f8bbd9;">
        <p style="font-size: 1.2rem; font-style: italic; text-align: center; color: #2c3e50; margin: 0;">
            在人生最艰难的时刻，请记住：<br>
            黑暗过后必有黎明，风暴之后终将平静。
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**🌱 自我关怀小贴士**")
    st.caption("""
    🌸 愿每一个疲惫的心灵都能找到停泊的港湾，
    愿每一个生命的旅程都充满理解与关怀。
    """)

if __name__ == "__main__":
    display_knowledge()