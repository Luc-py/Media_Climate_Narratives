from shiny import App, ui, render, reactive
import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# Load files
topics_df = pd.read_csv('csv_data/topic_data.csv',encoding='utf-8')

with open('txt_data\headers.txt',encoding='utf-8') as f:
    headers = f.read().split('\n')
with open('txt_data\paragraphs.txt',encoding='utf-8') as f:
    paragraphs = f.read().split('\n')


# UI
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h1('Graph Controls'),
        ui.input_select("y_selection", "Sort the y axis by:", 
                                        choices=["Topic Instances", "Article Sentiment", "Headline Sentiment"]),
        ui.input_select("data_selection", "What data do you want to see?", 
                                        choices=["Topic Instances", "Article Sentiment", "Headline Sentiment"]),
    ),
    ui.tags.style("""        
        h1 {
            font-family: Times New Roman;
            font-size: 24px;
            font-weight: bold;
        }
        h2 {
            font-family: Times New Roman;
            font-size: 14px;
            font-weight: bold;
        }
        p {
            font-family: Times New Roman;
            font-size: 14px;
            font-weight: normal;
        }
    """),

    ui.h1('Climate Narratives in the Media: an NLP Project'), # Title

    ui.h2(headers[0]),
    ui.p(paragraphs[0]),

    ui.output_plot('plot'),

    ui.h2(headers[1]),
    ui.p(paragraphs[1]),
    ui.p(''),

    ui.h2(headers[2]),
    ui.p(paragraphs[2]),
    ui.p(''),
    
    ui.h2(headers[3]),
    ui.p(paragraphs[3]),
    ui.p(''),

    ui.h2(headers[4]),
    ui.p(paragraphs[4]),
    ui.p(paragraphs[5]),
    ui.p(paragraphs[6]),
)


# Server
def server(input,output,session):
    @output
    @render.plot
    def plot():
        if input.y_selection() == 'Topic Instances':
            df = topics_df.sort_values('topic_count')
            ylabel = 'Topic in Order of Instances'
        elif input.y_selection() == 'Article Sentiment':
            df = topics_df.sort_values('article_sentiment')
            ylabel = 'Article Sentiment (top = most positive)'
        else:
            df = topics_df.sort_values('headline_sentiment')
            ylabel = 'Headline Sentiment (top = most positive)'

        if input.data_selection() == 'Topic Instances':
            values = df['topic_count']
            xlabel = 'Topic Instances Throughout all Articles'
        elif input.data_selection() == 'Article Sentiment':
            values = df['article_sentiment']
            xlabel = 'Sentiment Score'
        else:
            values = df['headline_sentiment']
            xlabel = 'Sentiment Score'            

        norm = mcolors.Normalize(vmin=values.min(), vmax=values.max())
        colors = cm.viridis_r(norm(values))

        fig, ax = plt.subplots()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.barh(df['topic_name'], values, color=colors)

        return fig

app = App(app_ui,server)

# cd 3_NLP\summative_2
# python -m shiny run app.py