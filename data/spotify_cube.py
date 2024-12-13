import streamlit as st
import polars as pl

MEASURE_DURATION_NAME = "Durée d'écoute"
MEASURE_COUNT_NAME = 'Nombre de titres écoutés'
HEAD_TOP = 5

def format_duration(minutes: int):
    days = int(minutes // (24 * 60))
    mins_left = minutes % (24 * 60)
    hours = int(mins_left // 60)
    mins_left = int(mins_left % 60)
    
    return f"{days:02d}j {hours:02d}h {mins_left:02d}m"
    
def rank_dataframe_over_duration(df: pl.DataFrame, grouped_by: list, period: str = None):
    agg_by = 'duration_minutes'
    sort_by = [agg_by] if period is None else [period, agg_by]
    
    result_df = (
        df
        .group_by(grouped_by)
        .agg(pl.col(agg_by).sum().alias(agg_by))
        .sort(sort_by, descending=[True for _ in sort_by])
        .with_columns(pl.col(agg_by).map_elements(format_duration).alias(MEASURE_DURATION_NAME))
        .select(pl.exclude(agg_by))
    )
    
    if period is None:
        result_df = result_df.with_row_index('Classement', offset=1)
    else:
        result_df = (
            result_df
            .group_by(period).head(HEAD_TOP)
            .sort([period, MEASURE_DURATION_NAME], descending=[True, True])
        )
        
    return result_df

def rank_dataframe_over_count(df: pl.DataFrame, grouped_by: list, period: str = None):
    agg_by = MEASURE_COUNT_NAME
    sort_by = [agg_by] if period is None else [period, agg_by]
    
    result_df = (
        df
        .group_by(grouped_by)
        .agg(pl.count().alias(MEASURE_COUNT_NAME))
        .sort(sort_by, descending=[True for _ in sort_by])
    )
    
    if period is None:
        result_df = result_df.with_row_index('Classement', offset=1)
    else:
        result_df = (
            result_df
            .group_by(period).head(HEAD_TOP)
            .sort([period, MEASURE_COUNT_NAME], descending=[True, True])
        )
        
    return result_df
            
            
class Cube:
    def __init__(self):
        pass
    
    def df(self) -> pl.DataFrame:
        return st.session_state.initial_dataframe
    
    def number_of_artists(self):
        return self.df().n_unique('ARTISTE')
    
    def number_of_titles(self):
        return self.df().n_unique('TITRE')
    
    def duration(self):
        return format_duration(self.df().select('duration_minutes').sum().to_numpy()[0])
    
    def years(self):
        return sorted(self.df().unique('ANNEE')['ANNEE'].to_list(), reverse=True)
    
    def months(self):
        return sorted(self.df().unique('ANNEE_MOIS')['ANNEE_MOIS'].to_list(), reverse=True)
    
    def artists_ranking(self, over: str = MEASURE_COUNT_NAME):
        grouped_by = ['ARTISTE']
        df = self.df()
        
        ranking_function = rank_dataframe_over_duration if over == MEASURE_DURATION_NAME else rank_dataframe_over_count
            
        return ranking_function(df=df,
                                grouped_by=grouped_by)
        
    def titles_ranking(self, over: str = MEASURE_COUNT_NAME):
        grouped_by = ['ARTISTE', 'TITRE']
        df = self.df()
        
        ranking_function = rank_dataframe_over_duration if over == MEASURE_DURATION_NAME else rank_dataframe_over_count
            
        return ranking_function(df=df,
                                grouped_by=grouped_by)
        
    def artists_ranking_by_year(self, years: list = None, over: str = MEASURE_COUNT_NAME):
        if years is None:
            years = self.years()
            
        period = 'ANNEE'
        grouped_by = [period, 'ARTISTE']
        df = self.df().filter(pl.col(period).is_in(years))
        
        ranking_function = rank_dataframe_over_duration if over == MEASURE_DURATION_NAME else rank_dataframe_over_count
            
        return ranking_function(df=df,
                                grouped_by=grouped_by,
                                period=period)
        
    def artists_ranking_by_month(self, months: list = None, over: str = MEASURE_COUNT_NAME):
        if months is None:
            months = self.months()
            
        period = 'ANNEE_MOIS'
        grouped_by = [period, 'ARTISTE']
        df = self.df().filter(pl.col(period).is_in(months))
        
        ranking_function = rank_dataframe_over_duration if over == MEASURE_DURATION_NAME else rank_dataframe_over_count
            
        return ranking_function(df=df,
                                grouped_by=grouped_by,
                                period=period)
        
    def titles_ranking_by_year(self, years: list = None, over: str = MEASURE_COUNT_NAME):
        if years is None:
            years = self.years()
            
        period = 'ANNEE'
        grouped_by = [period, 'ARTISTE', 'TITRE']
        df = self.df().filter(pl.col(period).is_in(years))
        
        ranking_function = rank_dataframe_over_duration if over == MEASURE_DURATION_NAME else rank_dataframe_over_count
            
        return ranking_function(df=df,
                                grouped_by=grouped_by,
                                period=period)
        
    def titles_ranking_by_month(self, months: list = None, over: str = MEASURE_COUNT_NAME):
        if months is None:
            months = self.months()
        
        period = 'ANNEE_MOIS'
        grouped_by = [period, 'ARTISTE', 'TITRE']
        df = self.df().filter(pl.col(period).is_in(months))
        
        ranking_function = rank_dataframe_over_duration if over == MEASURE_DURATION_NAME else rank_dataframe_over_count
            
        return ranking_function(df=df,
                                grouped_by=grouped_by,
                                period=period)