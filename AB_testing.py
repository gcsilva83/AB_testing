import streamlit as st
from PIL import Image
import numpy as np
from scipy.stats import norm
# from streamlit_pdf_report import add_report_to_sidebar

st.set_page_config(
    page_title="A/B Testing Calculator",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="collapsed",
)



# Add your logo here
logo = Image.open("sticker.png")
st.sidebar.image(logo, use_column_width=True)

st.sidebar.title("A/B Testing Calculator Info")
st.sidebar.write("This app calculates the sample size required for an A/B test and displays the confidence levels for rejecting the null hypothesis and accepting the alternative hypothesis. You can input the experiment details, the expected percent change, and the alpha and beta values. The sample size is calculated using the effect size and the alpha and beta values. The confidence levels are calculated using the alpha and beta values and the power of the test.")

st.title("A/B Testing Calculator")

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #8C8984 ;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    "## This is the sidebar"


#################################################################################
import math
from scipy.stats import norm

def num_subjects(alpha, power_level, p, delta):
    if p > 0.5:
        p = 1.0 - p
    
    t_alpha2 = norm.ppf(1.0-alpha/2)
    t_beta = norm.ppf(power_level)

    sd1 = math.sqrt(2 * p * (1.0 - p))
    sd2 = math.sqrt(p * (1.0 - p) + (p + delta) * (1.0 - p - delta))

    return (t_alpha2 * sd1 + t_beta * sd2) * (t_alpha2 * sd1 + t_beta * sd2) / (delta * delta)
#################################################################################

# Input form for experiment details
exp_name = st.sidebar.text_input("Enter experiment name:")
h0 = st.sidebar.text_input("Enter null hypothesis:")
h1 = st.sidebar.text_input("Enter alternative hypothesis:")


# Input form for alpha and beta values
p_c = st.sidebar.slider("Select the Baseline Conversion Rate:", min_value=0.01, max_value=0.5, value=0.1, step=0.01)
#percent_change = st.sidebar.number_input("Enter expected percent change (%):")
percent_change = st.sidebar.slider("Enter expected percent change (%):", min_value=1.0, max_value=20.0, value=1.0, step=0.5)
alpha = st.sidebar.slider("Select alpha value:", min_value=0.01, max_value=0.5, value=0.05, step=0.01)
beta = st.sidebar.slider("Select beta value:", min_value=0.01, max_value=0.5, value=0.2, step=0.01)


# Calculate sample size
z_alpha = norm.ppf(1 - alpha/2)
z_beta = norm.ppf(1 - beta)
sd_pool = np.sqrt(2)
p0 = 0.5
p1 = (100 + percent_change) / 100 * p0
effect_size = abs(p1 - p0) / sd_pool
n = ((z_alpha + z_beta) ** 2 * (p0 * (1 - p0) + p1 * (1 - p1))) / effect_size ** 2

# n_1= num_subjects(alpha,1- beta, p_c, percent_change)
pc = percent_change/100
n= num_subjects(alpha,1-beta,p_c,pc)
v5 = int(np.ceil(n))
v5 = "{:,.0f}".format(v5)

# Calculate confidence levels
power = 1 - beta
cl_alpha = 1 - alpha
cl_beta = 1 - power

#######

# Define the variables
max_width = 1400
padding_top = 0.8
padding_right = 0.8
padding_left = 0.8
padding_bottom = 0.8
COLOR = "#333333"
BACKGROUND_COLOR = "#F0F2F6"

# Use the variables in the st.markdown code snippet
st.markdown(
    f"""
    <style>
        .reportview-container .main .block-container {{
            max-width: {max_width}px;
            padding-top: {padding_top}rem;
            padding-right: {padding_right}rem;
            padding-left: {padding_left}rem;
            padding-bottom: {padding_bottom}rem;
        }}
        .reportview-container .main {{
            color: {COLOR};
            background-color: {BACKGROUND_COLOR};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)
# Display results

st.write("## Interpretation")
st.write("The **null hypothesis** states that there is no statistically significant difference between the control group and the experimental group. The **alternative hypothesis** states that there is a statistically significant difference between the two groups.")
st.write(f"The **expected percent change** is the anticipated difference between the two groups, expressed as a percentage.")
st.write("The **alpha value** is the level of significance, or the probability of rejecting the null hypothesis when it is actually true. A common value for alpha is 0.05.")
st.write("The **beta value** is the probability of accepting the null hypothesis when it is actually false. The complement of beta is the **power**, which is the probability of rejecting the null hypothesis when it is actually false.")
st.write("The **sample size** is the number of participants needed in each group to achieve the desired level of statistical power.")
st.write("The **confidence level (alpha)** is the probability of correctly rejecting the null hypothesis when it is actually false. A common value for alpha is 0.05, which corresponds to a 95% confidence level.")
st.write("The **confidence level (beta)** is the probability of failing to reject the null hypothesis when it is actually false. A common value for beta is 0.2, which corresponds to an 80% power level.")
st.write(f"**Alternative hypothesis:** {h1}")
st.write(f"**Expected percent change:** {percent_change}%")
st.write(f"**Alpha value:** {alpha}")
st.write(f"**Beta value:** {beta}")

st.write("##  Sample Size for this Experiment is:")
st.metric(label="## Sample Size for this Experiment is:",
          value=v5,delta="samples",label_visibility="collapsed") 
