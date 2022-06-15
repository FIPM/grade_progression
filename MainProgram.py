from flask import Flask, render_template, request, session
from os import environ
from dotenv import load_dotenv

import pandas as pd
import os
# plots
import plotly
import plotly.graph_objs as go
# import plotly.figure_factory as ff
import plotly.express as px
import json

from scripts.import_data import df_Navbar, df_Content, db_fig1, db_fig2, db_fig3, db_fig4
load_dotenv('.env')


# creating app
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY'] 


# home
@app.route('/', methods=["GET", "POST"])
def Home():

    # language
    if session.get("Language",None)==None:
        Language=df_Navbar.columns[2]
    else:
        Language=session.get("Language")
                    
    if request.method == "POST":
        Language = request.form.get("LanguageSelected",df_Navbar.columns[2])
    
    # Navbar
    languages_to_drop = set(list(df_Navbar.columns[2:])).difference(set([Language]))
    menu = df_Navbar.drop(columns=languages_to_drop)
    names = list(menu.columns)
    names[-1]='Language'
    menu.columns = names
    navOptionsMenu=menu.groupby('Menu').agg(lambda x: x.to_list()).to_dict('records')  
    
    # Content
    menu = df_Content.drop(columns=languages_to_drop)
    names = list(menu.columns)
    names[-1]='Language'
    menu.columns = names
    menu.set_index('Keys', inplace=True)
    ContentMenu = menu.to_dict('dict')['Language']
    
    # Figure 1
    # plotting
    data = [go.Scatter(x=db_fig1['Grade'].values,y=100*db_fig1[x].values,name=x) for x in ['2015 National','2016 National','2015 Public Schools','2016 Public Schools','2015 Private Schools','2016 Private Schools']]
    layout = go.Layout(title="Figure 1: Cohort of First Grade Students in 2015 and 2016",
                    xaxis=dict(title="Last Grade Reached",
                                tickfont=dict(size=14,
                                            color='rgb(107, 107, 107)'),
                                tickangle=-45),
                    yaxis=dict(title="Student Grade Progression (%)",
                                titlefont=dict(size=16,
                                                color='rgb(107, 107, 107)'),
                                tickfont=dict(size=14,
                                            color='rgb(107, 107, 107)')),
                    )
    fig = go.Figure(data=data, layout=layout)
    graphJSON_Fig1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    # plotting fig 2
    data = [go.Scatter(x=db_fig2['Grade'].values,y=100*db_fig2[x].values,name=x) for x in ['2011 Public Schools','2015 Public Schools','2016 Public Schools']]
    layout = go.Layout(title='Figure 2: Cohort of First Grade Students in 2011, 2015, 2016<br>(Normalized to 1 in Third Grade)',
                    xaxis=dict(title='Last Grade Reached',
                                tickfont=dict(size=14,
                                                color='rgb(107, 107, 107)'),
                                tickangle=-45),
                    yaxis=dict(title='Student Grade Progression (%)',
                                titlefont=dict(size=16,
                                                color='rgb(107, 107, 107)'),
                                tickfont=dict(size=14,
                                                color='rgb(107, 107, 107)')),
                        )
    fig2 = go.Figure(data=data, layout=layout)
    graphJSON_Fig2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Figure 3
    fig3 = px.scatter(
        db_fig3, x='measure_M_std', y='measure_L_std',
        marginal_x='histogram', marginal_y='histogram',
        color='Last Grade Observed'
    )
    fig3.update_traces(histnorm='probability', selector={'type':'histogram'})
    fig3.update_layout(
        xaxis_title='Math',
        yaxis_title="Reading",
        title_text=" Figure 3: Third Grade Students' Performace in Guatemala in 2014"
    )
    to_hide=db_fig3['Last Grade Observed'].unique()
    to_hide=to_hide[1:-1]
    fig3.for_each_trace(lambda trace: trace.update(visible="legendonly") 
                   if trace.name in to_hide else ())
    graphJSON_Fig3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Figure 4
    data=[
        go.Bar(x=db_fig4[db_fig4['LastGrade']==g]["Index Name"],y=db_fig4[db_fig4['LastGrade']==g]["Index"],name='Attending Grade >='+str(g))
        for g in db_fig4['LastGrade'].unique()
    ]
    layout = go.Layout(title_text='Figure 4: Model Performace for Third Grade Students Progression in Guatemala',
                    xaxis_title='Metrics',
                    yaxis_title='Percentage'
                    )
    fig4 = go.Figure(data=data, layout=layout)
    graphJSON_Fig4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)


    
    
    
    navOptions=navOptionsMenu 
    Content=ContentMenu 
    
    
    session["Language"]=Language
                               
    return render_template('Home.html', 
                           navOptions=navOptions,  
                           Content=Content,                          
                           ButtonPressed = Language,
                           ActiveLink='/',
                           graphJSONFig1=graphJSON_Fig1,
                           graphJSONFig2=graphJSON_Fig2,
                           graphJSONFig4=graphJSON_Fig3,
                           graphJSONFig5=graphJSON_Fig4,                           
                           )
    

if __name__=='__main__':
    #app.run(debug=True)
    app.run(debug=True,host='localhost')
