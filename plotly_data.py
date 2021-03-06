"""
Code for retrieving specific emotions from dictionary of emotions over a period of time and graphing
it with COVID data against time using plotly.

© Christina Lin and Victor Yao
"""
from datetime import datetime
from datetime import timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import emotion_data as ed
import tweet_data as td
import covid_data as cd


def get_emotion(start_date: datetime, end_date: datetime) -> dict:
    """Given a start and end date, returns a dictionary mapping each day to its emotional index.

    Preconditions:
        - to_datetime('2020-03-01') <= start_date < end_date < datetime.today()
    """
    num_days = (end_date - start_date).days
    data = td.retrieve_new_tweets(num_days + 1, start_date, False)
    tweet_data = ed.total_emotions(data, False)
    return tweet_data


def get_emotion_by_day(tweet_data: dict, chosen_emotion: str) -> list:
    """ Retrieves a single emotion's data across several days.

    Preconditions:
        - chosen_emotion != ''
    """
    emotion_by_day = []
    for date in tweet_data:
        emotion_by_day.append(tweet_data[date][chosen_emotion])
    return emotion_by_day


def get_date() -> (datetime, datetime, list):
    """ Retrieves the start and end date of saved emotion data in a tuple
    (start_date, end_date)
    """
    emotion_data = ed.pull_from_raw_data()
    start = td.to_datetime(min(emotion_data))
    end = td.to_datetime(max(emotion_data))

    return (start, end)


def get_emotion_from_file(chosen_emotion: str) -> list:
    """ Retrieves a single emotion's data from tweet_emotional_index.csv
        and returns (start_date, end_date, data)

    Preconditions:
        - chosen_emotion != ''
    """
    emotion_data = ed.pull_from_raw_data()
    emotion_by_day = []
    for date in emotion_data:
        emotion_by_day.append(emotion_data[date][chosen_emotion])
    return emotion_by_day


def get_desired_dates(start_date: datetime, end_date: datetime) -> list:
    """Return a set of dates in twint format from start_date to end_date.

    Preconditions:
        - to_datetime('2020-03-01') <= start_date < end_date < datetime.today()
    """
    desired_dates = []
    for n in range((end_date - start_date).days + 1):
        desired_dates.append(td.to_twint(start_date + timedelta(n)))
    return desired_dates


def get_covid_data(start_date: datetime, end_date: datetime, chosen_covid_data: str) -> list:
    """Returns a subset of COVID data given a start and end date.

    Preconditions:
        - to_datetime('2020-03-01') <= start_date < end_date < datetime.today()
        - chosen_covid_data != ''
    """
    covid_data = cd.process_data().set_index('header').to_dict()
    desired_dates = get_desired_dates(start_date, end_date)
    covid_data_by_day = []
    for date in desired_dates:
        covid_data_by_day.append(covid_data[date][chosen_covid_data])
    return covid_data_by_day


def draw_input_graph(start_date: datetime, end_date: datetime) -> None:
    """Plots COVID and emotional data from start_date to end_date.

    Preconditions:
        - to_datetime('2020-03-01') <= start_date < end_date < datetime.today()
    """
    emotions = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive',
                'sadness', 'surprise', 'trust']
    covid_data_types = list(cd.process_data().header)
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    dates = get_desired_dates(start_date, end_date)
    emote = get_emotion(start_date, end_date)

    # Emotion
    for emotion in emotions:
        emotion_data = get_emotion_by_day(emote, emotion)
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=emotion_data,
                name=f'{emotion.capitalize()}',
                line=dict(width=6),
                visible='legendonly'
            ),
            secondary_y=True,
        )

    # COVID
    for data_type in covid_data_types:
        covid_data = get_covid_data(start_date, end_date, data_type)
        fig.add_trace(
            go.Bar(
                x=dates,
                y=covid_data,
                name=f'{data_type}',
                visible='legendonly'
            ),
            secondary_y=False,
        )

    fig.update_layout(title_text='Sentimentality vs. COVID-19 Statistics', title_x=0.5)
    fig.update_xaxes(title_text='Day')
    fig.update_yaxes(title_text='Covid Statistic', secondary_y=False)
    fig.update_yaxes(title_text='Emotion', secondary_y=True)
    fig.show()


def draw_saved_graph() -> None:
    """Plots the COVID and emotional data from file.
    """
    emotions = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive',
                'sadness', 'surprise', 'trust']
    covid_data_types = list(cd.process_data().header)
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    start_date, end_date = get_date()
    dates = get_desired_dates(start_date, end_date)

# Emotion
    for emotion in emotions:
        emotion_data = get_emotion_from_file(emotion)
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=emotion_data,
                name=f'{emotion.capitalize()}',
                line=dict(width=6),
                visible='legendonly'
            ),
            secondary_y=True,
        )

# COVID

    for data_type in covid_data_types:
        covid_data = get_covid_data(start_date, end_date, data_type)
        fig.add_trace(
            go.Bar(
                x=dates,
                y=covid_data,
                name=f'{data_type}',
                visible='legendonly'
            ),
            secondary_y=False,
        )

    fig.update_layout(
        title_text='Sentimentality vs. COVID-19 Statistics'
    )

    fig.update_layout(title_text='Sentimentality vs. COVID-19 Statistics', title_x=0.5)
    fig.update_xaxes(title_text='Day')
    fig.update_yaxes(title_text='Covid Statistic', secondary_y=False)
    fig.update_yaxes(title_text='Emotion', secondary_y=True)
    fig.show()
