import streamlit as st

## CSS styling that will change the button width and 
## change the button hover animation
def style_buttons():
    st.markdown("""
<style>
div.stButton > button:first-child {
    border: 2px solid #0891B2;
    border-radius: 10px;
    padding: 0.5rem 2rem;
    transition: all 0.3s ease;
}
div.stButton > button:hover {
    background-color: #2B6CB0;
    border-color: #2B6CB0;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(8, 145, 178, 0.4);
}

div.stButton > button:active {
    transform: translateY(0px);
}
</style>
""", unsafe_allow_html=True)


## CSS code that will make the image
## drop on the screen 
def style_front_image():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Bungee&display=swap" rel="stylesheet">
    <style>
    .hero-container {
        position: relative;
        width: 100vw;
        height: 500px;
        margin-left: calc(-50vw + 50%);
        margin-right: calc(-50vw + 50%);
        overflow: hidden;
    }
    .full-hero-image {
        animation: slideUp 2s ease-out;
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }
    .hero-overlay {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        z-index: 2;
        animation: fadeIn 3s ease-in-out;
    }
    .hero-title {
        font-family: 'Bungee', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        color: white;
        text-shadow:
            3px 3px 0px rgba(0,0,0,0.8),
            -1px -1px 0px rgba(0,0,0,0.8),
            1px -1px 0px rgba(0,0,0,0.8),
            -1px 1px 0px rgba(0,0,0,0.8),
            0px 4px 8px rgba(0,0,0,0.6);
        margin-bottom: 1rem;
        letter-spacing: 1px;
    }
    .hero-subtitle {
        font-family: 'Bungee', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: white;
        text-shadow:
            2px 2px 0px rgba(0,0,0,0.8),
            -1px -1px 0px rgba(0,0,0,0.8),
            1px -1px 0px rgba(0,0,0,0.8),
            -1px 1px 0px rgba(0,0,0,0.8),
            0px 3px 6px rgba(0,0,0,0.5);
    }
    @keyframes slideUp {
        0% {
            transform: translateY(50px);
            opacity: 0;
        }
        100% {
            transform: translateY(0);
            opacity: 1;
        }
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    </style>
    
    <div class="hero-container">
        <img src="https://www.pocketwanderings.com/wp-content/uploads/2022/06/Dinant-Belgium.jpg" class="full-hero-image" alt="European Adventure">
        <div class="hero-overlay">
            <div class="hero-title">EuroTour</div>
            <div class="hero-subtitle">Smarter Travel, Stronger Insights, One Europe</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
##the boolean means if the text is going to be welcoming the user (in which the function will highlight their name)
def traveler_font(text, bool):
    if bool:
        st.markdown(f"""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
        .welcome-handwritten {{
            font-family: 'Poppins', sans-serif !important;
            font-size: 3rem !important;
            font-weight: 600 !important;
            color: #2c3e50 !important;
            text-align: center !important;
            margin: 0 !important;
            line-height: 1.2 !important;
            position: relative;
        }}
        .welcome-handwritten .name {{
            color: #e67e22 !important;
            font-weight: 700 !important;
        }}
        .stMarkdown h1 {{
            font-family: 'Poppins', sans-serif !important;
        }}
        </style>
        <h1 class="welcome-handwritten">
            Welcome Traveler, <span class="name">{text}</span>.
        </h1>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
        .welcome-handwritten {{
            font-family: 'Poppins', sans-serif !important;
            font-size: 3rem !important;
            font-weight: 600 !important;
            color: #2c3e50 !important;
            text-align: center !important;
            margin: 0 !important;
            line-height: 1.2 !important;
            position: relative;
        }}
        .welcome-handwritten .name {{
            color: #e67e22 !important;
            font-weight: 700 !important;
        }}
        .stMarkdown h1 {{
            font-family: 'Poppins', sans-serif !important;
        }}
        </style>
        <h1 class="welcome-handwritten">
            {text}
        </h1>
        """, unsafe_allow_html=True)
        
def collage_form(pic1, pic2, pic3, pic4, pic5, word1, word2, word3, word4, word5):
    st.markdown(f"""
<style>
.welcome-collage {{
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    grid-template-rows: 200px 200px;
    gap: 10px;
    border-radius: 15px;
    overflow: hidden;
    margin: 2rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}}

.collage-item {{
    background-size: cover;
    background-position: center;
    position: relative;
    transition: transform 0.3s ease;
}}

.collage-item:hover {{
    transform: scale(1.05);
    z-index: 2;
}}

.collage-main {{
    grid-row: 1 / 3;
    background-image: url({pic1});
}}

.collage-top-right {{
    background-image: url({pic2});
}}

.collage-bottom-right {{
    background-image: url({pic3});
}}
            
.collage-bottom {{
    background-image: url({pic4});
}}
            
.collage-bottom-left {{
    background-image: url({pic5});
}}

.image-overlay {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(transparent, rgba(0,0,0,0.7));
    color: white;
    padding: 1rem;
    font-weight: 600;
}}
</style>

<div class="welcome-collage">
    <div class="collage-item collage-main">
        <div class="image-overlay">{word1}</div>
    </div>
    <div class="collage-item collage-top-right">
        <div class="image-overlay">{word2}</div>
    </div>
    <div class="collage-item collage-bottom-right">
        <div class="image-overlay">{word3}</div>
    </div>
    <div class="collage-item collage-bottom">
        <div class="image-overlay">{word4}</div>
    </div>
    <div class="collage-item collage-bottom-left">
        <div class="image-overlay">{word5}</div>
    </div>
</div>
""", unsafe_allow_html=True)
    
def offical_font(text, bool):
    if bool:
        st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
    .official-hospitality {{
        font-family: 'Lato', sans-serif !important;
        font-size: 2.4rem !important;
        font-weight: 600 !important;
        color: #2a4365 !important;
        text-align: center !important;
        margin: 0 !important;
        line-height: 1.2 !important;
        position: relative !important;
        padding: 35px 0 50px 0 !important;
    }}
    
    .official-hospitality::before {{
        content: '' !important;
        position: absolute !important;
        top: 10px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100px !important;
        height: 4px !important;
        background: linear-gradient(90deg, #3182ce, #63b3ed) !important;
        border-radius: 2px !important;
    }}
    
    .official-hospitality .name {{
        color: #3182ce !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: 0.9em !important;
    }}
            
    .flag-accent {{
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1) !important;
        height: 6px !important;
        width: 150px !important;
        margin: 15px auto !important;
        border-radius: 3px !important;
    }}
    </style>
    
    <div class="official-hospitality">
        Welcome National Tourist Director, <span class="name">{text}</span>.
        <div class="flag-accent"></div>
    </div>
    """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
    .officials-hospitality {{
        font-family: 'Lato', sans-serif !important;
        font-size: 2.4rem !important;
        font-weight: 600 !important;
        color: #2a4365 !important;
        text-align: center !important;
        margin: 0 !important;
        line-height: 1.2 !important;
        position: relative !important;
        padding: 35px 0 50px 0 !important;
    }}
    
    
    .officials-hospitality .name {{
        color: #3182ce !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: 0.9em !important;
    }}
    </style>
    
    <div class="officials-hospitality">
        {text}
    </div>
    """, unsafe_allow_html=True)
        
def researcher_font(text, bool):
    if bool:
        st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
    .researcher-classic {{
        font-family: 'Playfair Display', serif !important;
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        color: #1a365d !important;
        text-align: center !important;
        margin: 0 !important;
        line-height: 1.2 !important;
        position: relative !important;
        padding: 20px 0 30px 0 !important;
    }}
    
    .researcher-classic .name {{
        color: #2b6cb0 !important;
        font-weight: 700 !important;
    }}
    
    .researcher-classic::after {{
        content: '' !important;
        position: absolute !important;
        bottom: 8px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 80px !important;
        height: 2px !important;
        background: linear-gradient(90deg, #2b6cb0, #4299e1) !important;
        border-radius: 1px !important;
    }}
    
    </style>
    
    <div class="researcher-classic">
        Welcome Researcher, <span class="name">{text}</span>.
    </div>
    """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
    .researchers-classic {{
        font-family: 'Playfair Display', serif !important;
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        color: #1a365d !important;
        text-align: center !important;
        margin: 0 !important;
        line-height: 1.2 !important;
        position: relative !important;
        padding: 20px 0 30px 0 !important;
    }}
    
    </style>
    
    <div class="researchers-classic">
        {text}
    </div>
    """, unsafe_allow_html=True)

def traveler_font_country(text):
    st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
    .welcome-handwritten {{
        font-family: 'Poppins', sans-serif !important;
        font-size: 3rem !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
        text-align: center !important;
        margin: 0 !important;
        line-height: 1.2 !important;
        position: relative;
    }}
    .welcome-handwritten .name {{
        color: #e67e22 !important;
        font-weight: 700 !important;
    }}
    .stMarkdown h1 {{
        font-family: 'Poppins', sans-serif !important;
    }}
    </style>
    <h1 class="welcome-handwritten">
        Best Tourist Attractions In <span class="name">{text}</span>.
    </h1>
    """, unsafe_allow_html=True)
        
def basic_font(text):
    st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
    .bubble-text {{
    font-family: 'Poppins', sans-serif;
    font-size: 3rem;
    font-weight: 600;
    color: 
    #C1D5C0;
    text-align: center;
    text-stroke:
    margin: 1rem 0;
    letter-spacing: 1px;
    }}
    </style>
    <div class="bubble-text">{text}</div>
    """, unsafe_allow_html=True)

def style_interactive_hero():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
    .hero-container {
        position: relative;
        text-align: center;
        padding: 3rem 1rem;
        background: linear-gradient(135deg, #C1D5C0 0%, rgba(193, 213, 192, 0.3) 100%);
        border-radius: 15px;
        margin: 1rem 0 2rem 0;
        overflow: hidden;
    }
    
    .hero-title-interactive {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #1C3334;
        margin-bottom: 1rem;
        animation: fadeInDown 1s ease-out;
    }
    
    .hero-subtitle-interactive {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 500;
        color: #0891B2;
        animation: fadeInUp 1s ease-out 0.5s both;
    }
    
    .floating-icon {
        position: absolute;
        font-size: 2rem;
        animation: float 3s ease-in-out infinite;
        opacity: 0.7;
    }
    
    .icon-1 { top: 20%; left: 10%; animation-delay: 0s; }
    .icon-2 { top: 30%; right: 15%; animation-delay: 1s; }
    .icon-3 { bottom: 25%; left: 15%; animation-delay: 2s; }
    .icon-4 { bottom: 35%; right: 10%; animation-delay: 0.5s; }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    @keyframes fadeInDown {
        0% { opacity: 0; transform: translateY(-30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .hero-container:hover .floating-icon {
        animation-duration: 1.5s;
    }
    </style>
    
    <div class="hero-container">
        <div class="floating-icon icon-1">🏰</div>
        <div class="floating-icon icon-2">✈️</div>
        <div class="floating-icon icon-3">🗺️</div>
        <div class="floating-icon icon-4">🎯</div>
        
        <div class="hero-title-interactive">
            Lost on where to travel in Europe?
        </div>
        <div class="hero-subtitle-interactive">
            🌟 No Worries! Input your preferences below! 🌟
        </div>
    </div>
    """, unsafe_allow_html=True)

