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

# Em styles.py (atualizando a função injetar_css_global)

def injetar_css_global():
    # Mantendo as configurações anteriores (fundo dark, botões neon azul)
    # e ADICIONANDO a estilização neon para a grade de pallets.
    st.markdown("""
        <style>
            /* --- CONFIGURAÇÕES BÁSICAS MANTIDAS --- */
            header { background: rgba(0,0,0,0) !important; } 
            .stDeployButton { display: none; } 
            [data-testid="InputInstructions"] { display: none !important; }
            
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #090e17 0%, #000000 100%) !important;
                background-attachment: fixed !important;
            }

            /* Botão Principal Neon Azul */
            .stButton > button[kind="primary"] { 
                background: linear-gradient(90deg, #4fc3f7 0%, #29b6f6 100%) !important; 
                color: #000000 !important; 
                font-weight: 800 !important; 
                border-radius: 8px !important; 
                transition: all 0.3s ease !important; 
                box-shadow: 0 4px 15px rgba(79, 195, 247, 0.3) !important;
                border: none !important;
            } 
            .stButton > button[kind="primary"]:hover { 
                box-shadow: 0 0 25px rgba(79, 195, 247, 0.6) !important; 
                transform: translateY(-2px) scale(1.02) !important; 
            } 

            /* Tooltip Holográfica */
            .fefo-tooltip { 
                display: none; position: absolute; bottom: 110%; left: 50%; transform: translateX(-50%); 
                background: rgba(20, 25, 35, 0.75); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
                color: #fff; padding: 20px; border-radius: 12px; width: 320px; flex-direction: column; 
                justify-content: center; align-items: flex-start; z-index: 100; 
                box-shadow: 0 15px 35px rgba(0,0,0,0.8); border: 1px solid rgba(255,255,255,0.1);
            } 

            /* --- NOVO ESTILO: GRADE DE PALLETS NEON (Target para image_4.png) --- */

            /* Classe base para todos os cards (Vazio ou Ocupado) */
            .pallet-card-custom {
                height: 120px !important;
                border-radius: 16px !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: center !important;
                align-items: center !important;
                text-align: center !important;
                padding: 15px !important;
                transition: transform 0.3s ease, box-shadow 0.3s ease !important;
                cursor: pointer;
                overflow: relative;
            }
            .pallet-card-custom:hover {
                transform: translateY(-5px) scale(1.03) !important;
            }
            /* Garantindo que os tooltips funcionem sobre os novos cards */
            .pallet-card-custom:hover .fefo-tooltip { display: flex !important; }


            /* --- ESTILO CARD VAZIO (Ex: A2-A6 na image_4.png) --- */
            /* Usamos Glassmorphism discreto para os vazios */
            .pallet-card-empty {
                background: rgba(255, 255, 255, 0.04) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                backdrop-filter: blur(4px);
            }
            .pallet-card-empty p { 
                color: #5c6bc0 !important; /* Texto azulado discreto em vez de cinza escuro */
                margin: 0; 
                font-weight: bold; 
                font-size: 24px !important;
                opacity: 0.7;
            }
            .pallet-card-empty small { 
                color: #3f51b5 !important; 
                opacity: 0.8;
                font-weight: bold;
                letter-spacing: 2px;
            }


            /* --- ESTILO CARD OCUPADO NEON (Ex: A1 na image_4.png) --- */
            .pallet-card-occupied-neon {
                /* Fundo escuro transparente para contrastar o glow */
                background: rgba(0, 0, 0, 0.3) !important; 
                backdrop-filter: blur(2px);
                
                /* A borda neon verde-limão saturada (#39ff14) */
                border: 3px solid #39ff14 !important;
                
                /* O SEGREDO DO NEON: Múltiplas camadas de sombra externa (GLOW) */
                box-shadow: 0 0 10px rgba(57, 255, 20, 0.9),  /* Sombra forte e verde perto */
                            0 0 25px rgba(57, 255, 20, 0.6),  /* Sombra média e verde difundida */
                            0 0 45px rgba(57, 255, 20, 0.3),  /* Sombra longe e fraca */
                            inset 0 0 10px rgba(57, 255, 20, 0.15) !important; /* Brilho interno sutil */
            }

            /* Estilização Neon para os textos dentro do card ocupado */
            .pallet-card-occupied-neon h3 { /* ID do Pallet: A1 */
                color: white !important;
                margin: 0;
                font-size: 32px !important;
                font-weight: 800 !important;
                /* Text Shadow para as letras brilharem */
                text-shadow: 0 0 8px rgba(255, 255, 255, 0.8), 0 0 15px #39ff14 !important;
            }
            
            .pallet-card-occupied-neon p { /* Nome do Produto: Melancia */
                color: white !important;
                margin: 5px 0 !important;
                font-weight: bold !important;
                font-size: 16px !important;
                text-shadow: 0 0 5px #39ff14 !important;
            }
            
            .pallet-card-occupied-neon small { /* Quantidade: 1/1 */
                color: #000000 !important; /* Texto preto para contrastar a 'pílula' de fundo */
                background: #39ff14; /* Fundo verde neon sólido como uma pílula */
                padding: 2px 8px !important;
                border-radius: 10px !important;
                font-weight: 800;
                box-shadow: 0 0 8px #39ff14 !important;
            }
        </style>
    """, unsafe_allow_html=True)