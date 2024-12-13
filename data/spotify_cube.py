import streamlit as st
import polars as pl
import data.constants as cst


def format_duration(seconds: int):
    days = int(seconds // (24 * 60 * 60))
    seconds_left = seconds % (24 * 60 * 60)
    hours = int(seconds_left // (60 * 60))
    seconds_left = int(seconds_left % (60 * 60))
    minutes = int(seconds_left // 60)
    seconds_left = int(seconds_left % 60)
    
    return f"{days:02d}j {hours:02d}h {minutes:02d}m {seconds_left:02d}s"
    
def rank_dataframe_over_duration(df: pl.DataFrame, grouped_by: list, period: str = None):
    agg_by = 'duration_seconds'
    sort_by = [agg_by] if period is None else [period, agg_by]
    
    result_df = (
        df
        .group_by(grouped_by)
        .agg(pl.col(agg_by).sum().alias(agg_by))
        .sort(sort_by, descending=[True for _ in sort_by])
        .with_columns(pl.col(agg_by).map_elements(format_duration, return_dtype=pl.String).alias(cst.MEASURE_DURATION_NAME))
        .with_columns((pl.col(agg_by) // 60).alias('duration_minutes'))
    )
    
    if period is None:
        result_df = result_df.with_row_index('Classement', offset=1)
    else:
        result_df = (
            result_df
            .group_by(period).head(cst.HEAD_TOP)
            .sort([period, cst.MEASURE_DURATION_NAME], descending=[True, True])
        )
        
    return result_df

def rank_dataframe_over_count(df: pl.DataFrame, grouped_by: list, period: str = None):
    agg_by = cst.MEASURE_COUNT_NAME
    sort_by = [agg_by] if period is None else [period, agg_by]
    
    result_df = (
        df
        .group_by(grouped_by)
        .agg(pl.count().alias(cst.MEASURE_COUNT_NAME))
        .sort(sort_by, descending=[True for _ in sort_by])
    )
    
    if period is None:
        result_df = result_df.with_row_index('Classement', offset=1)
    else:
        result_df = (
            result_df
            .group_by(period).head(cst.HEAD_TOP)
            .sort([period, cst.MEASURE_COUNT_NAME], descending=[True, True])
        )
        
    return result_df
            
            
class Cube:
    def __init__(self):
        pass
    
    def df(self) -> pl.DataFrame:
        return st.session_state.initial_dataframe
    
    def number_of_artists(self):
        return self.df().n_unique('Artiste')
    
    def number_of_titles(self):
        return self.df().n_unique('Titre')
    
    def duration(self):
        return format_duration(self.df().select('duration_seconds').sum().to_numpy()[0])
    
    def years(self):
        return sorted(self.df().unique('ANNEE')['ANNEE'].to_list(), reverse=True)
    
    def months(self):
        return sorted(self.df().unique('ANNEE_MOIS')['ANNEE_MOIS'].to_list(), reverse=True)
    
    def artists_ranking(self, over: str = cst.MEASURE_COUNT_NAME):
        grouped_by = ['Artiste']
        df = self.df()
        
        ranking_function = rank_dataframe_over_duration if over == cst.MEASURE_DURATION_NAME else rank_dataframe_over_count
            
        return ranking_function(df=df,
                                grouped_by=grouped_by)
        
    def titles_ranking(self, over: str = cst.MEASURE_COUNT_NAME):
        grouped_by = ['Artiste', 'Titre']
        df = self.df()
        
        ranking_function = rank_dataframe_over_duration if over == cst.MEASURE_DURATION_NAME else rank_dataframe_over_count
            
        return ranking_function(df=df,
                                grouped_by=grouped_by)
        
    def artists_ranking_by_year(self, years: list = None, over: str = cst.MEASURE_COUNT_NAME):
        if years is None:
            years = self.years()
            
        period = 'ANNEE'
        grouped_by = [period, 'Artiste']
        df = self.df().filter(pl.col(period).is_in(years))
        
        ranking_function = rank_dataframe_over_duration if over == cst.MEASURE_DURATION_NAME else rank_dataframe_over_count
            
        return ranking_function(df=df,
                                grouped_by=grouped_by,
                                period=period)
        
    def artists_ranking_by_month(self, months: list = None, over: str = cst.MEASURE_COUNT_NAME):
        if months is None:
            months = self.months()
            
        period = 'ANNEE_MOIS'
        grouped_by = [period, 'Artiste']
        df = self.df().filter(pl.col(period).is_in(months))
        
        ranking_function = rank_dataframe_over_duration if over == cst.MEASURE_DURATION_NAME else rank_dataframe_over_count
            
        return ranking_function(df=df,
                                grouped_by=grouped_by,
                                period=period)
        
    def titles_ranking_by_year(self, years: list = None, over: str = cst.MEASURE_COUNT_NAME):
        if years is None:
            years = self.years()
            
        period = 'ANNEE'
        grouped_by = [period, 'Artiste', 'Titre']
        df = self.df().filter(pl.col(period).is_in(years))
        
        ranking_function = rank_dataframe_over_duration if over == cst.MEASURE_DURATION_NAME else rank_dataframe_over_count
            
        return ranking_function(df=df,
                                grouped_by=grouped_by,
                                period=period)
        
    def titles_ranking_by_month(self, months: list = None, over: str = cst.MEASURE_COUNT_NAME):
        if months is None:
            months = self.months()
        
        period = 'ANNEE_MOIS'
        grouped_by = [period, 'Artiste', 'Titre']
        df = self.df().filter(pl.col(period).is_in(months))
        
        ranking_function = rank_dataframe_over_duration if over == cst.MEASURE_DURATION_NAME else rank_dataframe_over_count
            
        return ranking_function(df=df,
                                grouped_by=grouped_by,
                                period=period)