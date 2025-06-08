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
    font-family: 'Nunito', sans-serif;
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
    font-family: 'Nunito', sans-serif;
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
