# Core pkgs
import streamlit as st

# EDA pkgs
import pandas as pd
import numpy as np

# Data viz pkgs
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

matplotlib.use('Agg')

# ML pkgs
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC


def main():
    """Semi Auto ML app with Streamlit"""
    st.title("Semi Auto ML App")
    st.text("Using Streamlit ==0.52.1+")
    st.set_option('deprecation.showPyplotGlobalUse', False)

    activities = ["EDA", "Plot", "Model Building", "About"]

    choice = st.sidebar.selectbox("Select Activity", activities)

    if choice == "EDA":
        st.subheader("Exploratory Data Analysis")
        data = st.file_uploader("Upload Dataset", type=["csv", "txt"])
        if data is not None:
            df = pd.read_csv(data)
            st.dataframe(df.head())

            if st.checkbox("Show shape"):
                st.write(df.shape)

            if st.checkbox("Show Column"):
                all_columns = df.columns.to_list()
                st.write(all_columns)

            if st.checkbox("Show Columns to Show"):
                selected_columns = st.multiselect("Select Columns", all_columns)
                new_df = df[selected_columns]
                st.dataframe(new_df)

            if st.checkbox("Show Summary"):
                st.write(df.describe())

            if st.checkbox("Show Value Counts"):
                st.write(df.iloc[:, -1].value_counts())

            if st.checkbox("Correlation with Seaborn"):
                st.write(sns.heatmap(df.corr(), annot=True))
                st.pyplot()

            if st.checkbox("Pie Chart"):
                all_columns = df.columns.to_list()
                columns_to_plot = st.selectbox("Select 1 column", all_columns)
                pie_plot = df[columns_to_plot].value_counts().plot.pie(autopct='%1.1f')
                st.write(pie_plot)
                st.pyplot()

    elif choice == "Plot":
        st.subheader("Data Visualization")
        data = st.file_uploader("Upload Dataset", type=["csv", "txt"])
        if data is not None:
            df = pd.read_csv(data)
            st.dataframe(df.head())

        all_columns_names = df.columns.tolist()
        type_of_plot = st.selectbox("Select type of plot", ["area", "bar", "line", "hist", "box", "kde"])
        selected_columns_names = st.multiselect("Select Columns to plot", all_columns_names)

        if st.button("Generate Plot"):
            st.success("Generating Customizable plot of {} to {}".format(type_of_plot, selected_columns_names))

            # Plot by Streamlit
            if type_of_plot == 'area':
                cust_data = df[selected_columns_names]
                st.area_chart(cust_data)

            elif type_of_plot == 'bar':
                cust_data = df[selected_columns_names]
                st.bar_chart(cust_data)

            elif type_of_plot == 'line':
                cust_data = df[selected_columns_names]
                st.line_chart(cust_data)

            # Custom plot
            elif type_of_plot:
                cust_plot = df[selected_columns_names].plot(kind=type_of_plot)
                st.write(cust_plot)
                st.pyplot()


    elif choice == "Model Building":
        st.subheader("Building ML Model")
        data = st.file_uploader("Upload Dataset", type=["csv", "txt"])
        if data is not None:
            df = pd.read_csv(data)
            st.dataframe(df.head())

            # Model building
            X = df.iloc[:, 0:-1]
            Y = df.iloc[:, -1]
            seed = 7

            # Model
            models = []
            models.append(("LR", LogisticRegression()))
            models.append(("LDA", LinearDiscriminantAnalysis()))
            models.append(("KNN", KNeighborsClassifier()))
            models.append(('CART', DecisionTreeClassifier()))
            models.append(('NB', GaussianNB()))
            models.append(('SVM', SVC()))

            # evaluate each model in turn
            # List
            model_names = []
            model_mean = []
            model_std = []
            all_models = []
            scoring = 'accuracy'

            for name, model in models:
                kfold = model_selection.KFold(n_splits=10, random_state=seed, shuffle=True)
                cv_results = model_selection.cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
                model_names.append(name)
                model_mean.append(cv_results.mean())
                model_std.append(cv_results.std())

                accuracy_results = {"model name": name, "model accuracy": cv_results.mean(),
                                    "standard deviation": cv_results.std()}
                all_models.append(accuracy_results)

            if st.checkbox("Metrics as Table"):
                st.dataframe(pd.DataFrame(zip(model_names, model_mean, model_std),
                                          columns=["model name", "model accuracy", "standard deviation"]))

            # print(Y)

            if st.checkbox("Metrics as JSON"):
                st.json(all_models)

    elif choice == "About":
        st.subheader("About")
        st.text("reach out to me for suggestions, queries and feedback at rrrtechie@gmail.com")


if __name__ == '__main__':
    main()
