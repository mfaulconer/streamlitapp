import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

## streamlit
st.title('My Name App')

## data
df = pd.read_csv('all_names.csv')
df['total_births'] = df.groupby(['year', 'sex'])['n'].transform('sum')
df['prop'] = df['n'] / df['total_births']

#create tabs for streamlit
tab1, tab2, tab3 = st.tabs(['Overall', 'By Name', 'By Year'])

with tab1:
    st.write('Here is stuff about all the data')
    births_by_sex = df.groupby(['year', 'sex'])['n'].sum().unstack().fillna(0)
    births_by_sex['Total'] = births_by_sex['F'] + births_by_sex['M']
    births_by_sex['Male Ratio'] = births_by_sex['M'] / births_by_sex['Total']
    births_by_sex['Female Ratio'] = births_by_sex['F'] / births_by_sex['Total']

    fig1, ax = plt.subplots(figsize=(10, 4))
    ax.plot(births_by_sex.index, births_by_sex['Male Ratio'], label='Male')
    ax.plot(births_by_sex.index, births_by_sex['Female Ratio'], label='Female')
    ax.set_title('Gender Ratio Over Time')
    ax.set_ylabel('Proportion')
    ax.set_xlabel('Year')
    ax.legend()
    plt.show()

    st.pyplot(fig1)

with tab2:
    st.write('Name')
    ## choose 1 name
    noi = st.text_input('Enter a name')
    #soi = st.radio('Choose the sex to plot', ['M', 'F'])
    plot_female = st.checkbox('Plot female line')
    plot_male = st.checkbox('Plot male line')
    name_df = df[(df['name'] == noi)] #& (df['sex'] == soi)]

    ## plot chosen name
    fig2 = plt.figure(figsize=(15,8))
    if plot_female:
        sns.lineplot(data=name_df[name_df['sex'] == 'F'], x='year', y='prop', label='Female')
    if plot_male:
        sns.lineplot(data=name_df[name_df['sex'] == 'M'], x='year', y='prop', label='Male')
    plt.title(f'Plot of {noi}')
    plt.xlabel('year')
    plt.ylabel('count')
    plt.show()

    st.pyplot(fig2)

with tab3:
    st.write('By Year')
    year_of_interest = int(st.text_input('Enter a Year'))
    top_names = df[df['year'] == year_of_interest]
    top_female = top_names[top_names['sex'] == 'F'].nlargest(10, 'n')


    fig3 = plt.figure(figsize=(15,8))
    sns.barplot(data=top_female, x='n', y='name')
    plt.title(f"Top 10 Female Names in {year_of_interest}")
    plt.xlabel('Count')
    plt.ylabel('Name')
    plt.tight_layout()
    plt.show()

    st.pyplot(fig3)



