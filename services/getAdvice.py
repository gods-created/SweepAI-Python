from config import FILE_WITH_ADVICES

from os.path import exists
from pandas import read_csv, to_numeric, errors
from random import choice

def getAdviceService(score_in_percent: float) -> str:
    if not exists(FILE_WITH_ADVICES):
        raise FileNotFoundError('File with advices doesn\'t exist')

    if not FILE_WITH_ADVICES.endswith('.csv'):
        raise TypeError('File with advices has invalid format')

    try:
        df = read_csv(filepath_or_buffer=FILE_WITH_ADVICES)

    except errors.ParserError as e:
        raise ValueError(e)

    if df.empty:
        raise ValueError('File with advices is empty')

    required_columns = {'SCORE', 'ADVICE'}

    if not required_columns.issubset(df.columns):
        raise ValueError('File with advices must contain SCORE and ADVICE columns')

    df['SCORE'] = to_numeric(df['SCORE'], errors='coerce')
    df['ADVICE'] = df['ADVICE'].astype('string').str.strip()

    values = [
        (score, advice) for score, advice in zip(df['SCORE'], df['ADVICE'])
    ]

    if score_in_percent < 50:
        target_score = 0
    elif score_in_percent < 90:
        target_score = 50
    elif score_in_percent < 100:
        target_score = 90
    else:
        target_score = 100

    validated_values = [
        value for value in values if value[0] == target_score
    ]

    rand_pair = choice(validated_values)

    return rand_pair[1]