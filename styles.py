# styles.py
import streamlit as st

def injetar_animacao_global():
    # Mantive a sua animação, pois ela é perfeita para uma entrada suave!
    st.markdown("""
        <style>
            @keyframes fadeInSuave { 
                0% { opacity: 0; transform: translateY(15px); } 
                100% { opacity: 1; transform: translateY(0); } 
            } 
            .block-container { 
                animation: fadeInSuave 0.8s ease-out !important; 
            }
        </style>
    """, unsafe_allow_html=True)

def injetar_css_login():
    st.markdown("""
        <style>
            /* Esconde elementos padrão do Streamlit */
            header { background: rgba(0,0,0,0) !important; } 
            .stDeployButton { display: none; } 
            [data-testid="InputInstructions"] { display: none !important; }

            /* Fundo Global Premium (Dark Gradient) */
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #090e17 0%, #000000 100%) !important;
                background-attachment: fixed !important;
            }

            /* EFEITO VIDRO (Glassmorphism) na Caixa de Login */
            [data-testid="stForm"] { 
                background: rgba(255, 255, 255, 0.03) !important; /* Quase transparente */
                backdrop-filter: blur(16px) !important; /* O desfoque mágico */
                -webkit-backdrop-filter: blur(16px) !important;
                padding: 40px !important; 
                border-radius: 20px !important; 
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6) !important; /* Sombra profunda */
                border: 1px solid rgba(255, 255, 255, 0.08) !important; /* Borda brilhante sutil */
                margin-top: 10vh !important; 
            } 

            /* Inputs Textuais Neons */
            [data-testid="stForm"] div[data-baseweb="input"] { 
                background-color: rgba(0, 0, 0, 0.2) !important; 
                border: 1px solid rgba(255, 255, 255, 0.1) !important; 
                border-radius: 8px !important; 
                transition: all 0.3s ease !important;
            } 
            [data-testid="stForm"] div[data-baseweb="input"]:focus-within { 
                border-color: #4fc3f7 !important; 
                box-shadow: 0 0 15px rgba(79, 195, 247, 0.4) !important; /* Brilho Neon Azul */
                background-color: rgba(79, 195, 247, 0.05) !important;
            } 
            [data-testid="stForm"] div[data-testid="stTextInput"] input { 
                color: white !important; 
                background-color: transparent !important; 
                padding: 12px !important; 
                outline: none !important; 
                border: none !important; 
                box-shadow: none !important; 
            } 
        </style>
    """, unsafe_allow_html=True)

def injetar_css_global():
    st.markdown("""
        <style>
            /* Esconde elementos padrão e aplica fundo em todo o app */
            header { background: rgba(0,0,0,0) !important; } 
            .stDeployButton { display: none; } 
            [data-testid="InputInstructions"] { display: none !important; }
            
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #090e17 0%, #000000 100%) !important;
                background-attachment: fixed !important;
            }

            /* Botão Principal Neon/Holográfico */
            .stButton > button[kind="primary"] { 
                background: linear-gradient(90deg, #4fc3f7 0%, #29b6f6 100%) !important; 
                color: #000000 !important; 
                border: none !important; 
                font-weight: 800 !important; 
                border-radius: 8px !important; 
                transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important; 
                box-shadow: 0 4px 15px rgba(79, 195, 247, 0.3) !important;
            } 
            .stButton > button[kind="primary"]:hover { 
                box-shadow: 0 0 25px rgba(79, 195, 247, 0.6) !important; 
                transform: translateY(-2px) scale(1.02) !important; 
            } 

            /* Cards dos Pallets (Efeito Vidro Leve) */
            .pallet-box { 
                position: relative; 
                overflow: visible; 
                transition: transform 0.3s ease, box-shadow 0.3s ease; 
                cursor: pointer; 
                border-radius: 12px;
            } 
            .pallet-box:hover { 
                transform: translateY(-6px); 
                box-shadow: 0 15px 25px rgba(0,0,0,0.5) !important; 
                z-index: 50; 
            } 

            /* Tooltip Holográfica (O grande salto de design) */
            .fefo-tooltip { 
                display: none; 
                position: absolute; 
                bottom: 110%; 
                left: 50%; 
                transform: translateX(-50%); 
                
                /* Efeito Vidro na Tooltip */
                background: rgba(20, 25, 35, 0.75); 
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                
                color: #fff; 
                padding: 20px; 
                border-radius: 12px; 
                width: 320px; 
                flex-direction: column; 
                justify-content: center; 
                align-items: flex-start; 
                z-index: 100; 
                box-shadow: 0 15px 35px rgba(0,0,0,0.8); 
                border: 1px solid rgba(255,255,255,0.1);
            } 
            .pallet-box:hover .fefo-tooltip { display: flex !important; } 

            /* Mini Pallets com Glow no Hover */
            .mini-pallet { 
                width: 60px; 
                height: 60px; 
                border-radius: 8px; 
                position: relative; 
                cursor: pointer; 
                border: 1px solid rgba(255,255,255,0.15); 
                transition: all 0.2s ease;
            } 
            .mini-pallet:hover { 
                border: 2px solid #4fc3f7; 
                box-shadow: 0 0 15px rgba(79, 195, 247, 0.5);
                transform: scale(1.15); 
                z-index: 50; 
            } 
            .mini-pallet .fefo-tooltip { bottom: 120%; } 
            .mini-pallet:hover .fefo-tooltip { display: flex !important; } 
        </style>
    """, unsafe_allow_html=True)