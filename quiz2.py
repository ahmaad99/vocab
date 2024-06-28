import streamlit as st
import pandas as pd
import ast
import random
import numpy as np
from pathlib import Path


directory_path = Path('word_list/')
file_names = [f.name for f in directory_path.iterdir() if f.is_file()]
option_tuple = tuple(file_names)
option = st.selectbox(
    'Select an option:',
    option_tuple
)
str = f"word_list/{option}"
df = pd.read_csv(str)
up_bound = st.number_input(
    f"Enter an upper bound between 0 and {len(df['word'])}:", step=1, format="%d")
down_bound = st.number_input(
    f"Enter a lower bound between 0 and {len(df['word'])}:", step=1, format="%d")
df = df[down_bound:up_bound]

st.write(df)

if 'execute' not in st.session_state:
    st.session_state.execute = False


if not st.session_state.execute:
    if st.button('Execute'):
        st.session_state.execute = True

if st.session_state.execute:



    def make_temp_list(df):

        df = df

        # Example array
        arr = [i for i in range(len(df['word']))]  # An array with 100 elements

        # Length of the array
        n = len(arr)

        # Generate 30 distinct random numbers in the range [0, len(arr))
        random_numbers = random.sample(range(n), 30)

        return random_numbers

    # Initialize session state variables
    if 'question_index' not in st.session_state:
        st.session_state.question_index = 0
        st.session_state.answers = []
        st.session_state.random_numbers = make_temp_list(df)
        st.session_state.answer_index = 0
        st.session_state.correct_answers = []
        st.session_state.sentence_seq = []

    # Start From here

    def show_question():

        list_seq = st.session_state.random_numbers
        arr = ['sentence1', 'sentence2', 'sentence3', 'sentence4', 'sentence5']
        st.session_state.sentence_seq.append(
            arr[random.randint(0, len(arr)-1)])

        st.write(
            f"Question {st.session_state.question_index + 1}/{30}")
        st.write(
            f"{df[st.session_state.sentence_seq[st.session_state.question_index]].iloc[list_seq[st.session_state.question_index]]}.".replace(df['word'].iloc[list_seq[st.session_state.question_index]], "_________"))

        list_a = ast.literal_eval(
            df['option_result'].iloc[list_seq[st.session_state.question_index]])
        answer = st.radio("Select an option:", list_a[:5],
                          index=0, key=f"q{st.session_state.question_index}")

        return list_a.index(answer), list_a[-1]

    # Function to calculate the score

    def calculate_score_wrong_answer():

        score = sum([1 for i in range(30)
                    if st.session_state.answers[i] == st.session_state.correct_answers[i]])
        return score

    # Display the current question or the final score
    if st.session_state.question_index < 30:
        user_answer_index, correct_answer_ind = show_question()

        if st.button("Next"):
            st.session_state.answers.append(user_answer_index)
            st.session_state.correct_answers.append(correct_answer_ind)
            st.session_state.question_index += 1
            st.experimental_rerun()
    else:
        df3 = pd.read_csv('data/vocabulary.csv')

        arr = list(df3['Word'])

        score = calculate_score_wrong_answer()

        st.write(
            f"You've completed the quiz! Your score is {score}/{30}.")
        st.write("Your answers were:")
        for i in range(30):

            st.write(
                f"Q{i+1}: {df[st.session_state.sentence_seq[i]].iloc[st.session_state.random_numbers[i]]}")

            list_a = ast.literal_eval(
                df['option_result'].iloc[st.session_state.random_numbers[i]])
            st.write(
                f"Your answer: {list_a[st.session_state.answers[i]]}")
            st.write(
                f"Correct answer: {list_a[st.session_state.correct_answers[i]]}")
            
            if list_a[st.session_state.correct_answers[i]] in list(df3['Word']):
                ind = arr.index(list_a[st.session_state.correct_answers[i]])
                string = f"Meaning: {df3.loc[ind, 'Definition']}"
            else:
                string = "Not in Vocabulary list....use chatgpt"
            st.write(string)

        wrong_num = list(filter(lambda x: x not in st.session_state.correct_answers,
                                st.session_state.random_numbers))
