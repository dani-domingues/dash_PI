from dash import Dash, html, dcc, Output, Input
import plotly.express as px 
import pandas as pd             
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.io as pio


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# definindo aplicativo do flask
app = Dash(__name__, title='Tráfego Urbano')                         

df_2022 = pd.read_csv("/Users/danieladomingues/Documents/dash_PI/dashboards/assets/bd_transito_2022.csv", sep=",")

#Criar variaveis dia da semana para organizar Data Frame
dias_semana_ordem = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']


# Agrupar por dia da semana e região e calcular a soma do tamanho
df1 = pd.Categorical(df_2022['Dia da Semana'], categories=dias_semana_ordem, ordered=True)
df_grouped3 = round(df_2022.groupby(['Dia da Semana', 'Regiao'], sort=False)['Tamanho'].mean().reset_index(),2)

# Gerar gráfico de pizza comparando região com tamanho do congestionamento
figGraficoCongestionamentoMesRegiao = go.Figure()
figGraficoCongestionamentoMesRegiao.add_trace(go.Pie(labels=df_grouped3['Regiao'],values=df_grouped3['Tamanho'], hole=.65))
figGraficoCongestionamentoMesRegiao.update_layout(
    title='Comparação de Congestionamento por Mês e Região',
    xaxis_title='Mês',
    yaxis_title='Congestionamento (em metros)',
    barmode='group',
    autosize=False,
    width=495,
    height=500,
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Define a cor de fundo do gráfico como transparente
    paper_bgcolor='#252a48',  # Define a cor de fundo do papel como '#252a48'
    legend=dict(
        x=1.02,
        y=0.98,
        bgcolor='rgba(255, 255, 255, 0.1)',
        bordercolor='#252a48',
        borderwidth=2,
        font=dict(
            color='#fff' # Define a cor do texto da legenda como branco
        )
    ),
        title_font=dict(
        color='#fff'  # Define a cor do título do gráfico como branco
    ),
    xaxis=dict(
        tickfont=dict(
            color='#fff'  # Define a cor dos números e meses no eixo X como branco
        ),
        title_font=dict(
            color='#fff'  # Define a cor do título do eixo X como branco
        )
    ),
    yaxis=dict(
        tickfont=dict(
            color='#fff'  # Define a cor dos números no eixo Y como branco
        ),
        title_font=dict(
            color='#fff'  # Define a cor do título do eixo Y como branco
        )
    )
    )

#Agrupando por local e tirando a média de congestionamento
df_grouped_local1 = df_2022.groupby(['Local'], sort=False)['Tamanho'].mean()
df_grouped_local1.sort_values(ascending=False, inplace=True)
df_grouped_local = df_grouped_local1.reset_index()
#Mostrando indicador de via com maior média de congestionamento
figIndicadorZonaMaoirMediaCongestionamento = go.Figure()
figIndicadorZonaMaoirMediaCongestionamento.add_trace(go.Indicator(
    mode='number+delta',
    title={
        "text": f"<br><br><span style='font-size:350%; color:#fff; text-align:center; margin-top:50px'>{df_grouped_local['Local'].iloc[0]}</span> </br></br><br><span style='font-size:175%; color:#fff; text-align:center;'>Via com maior média de congestionamento</br>"
    },
    value=round(df_grouped_local['Tamanho'].iloc[0], 0),
    number={"suffix": " metros"},
    delta={'valueformat': '.1%', 'reference': df_grouped_local['Tamanho'].mean()},
    number_font={"size": 23, "color": "#fff"}  # Ajuste o tamanho e a cor do número do indicador aqui
))
figIndicadorZonaMaoirMediaCongestionamento.update_layout(
    paper_bgcolor='#252a48',  # Define a cor de fundo do papel como '#252a48'
    font=dict(color='#fff'),  # Define a cor do texto do gráfico como branco
    height=160,
    width=239,
    # ... outras configurações de layout ...
)

#Agrupando por região e calculando a média de cada região
df_grouped_regiao1 = round(df_2022.groupby(['Regiao'], sort=False)['Tamanho'].mean(),2)
df_grouped_regiao1.sort_values(ascending=False, inplace=True)
df_grouped_regiao = df_grouped_regiao1.reset_index()
#Mostrando indicador da região com maior média de congestionamento
figIndicadorViaComMaoirMediaCongestionamento = go.Figure()
figIndicadorViaComMaoirMediaCongestionamento.add_trace(go.Indicator(mode='number+delta',
                            title = {"text": f"<br><span style='font-size:350%; color:#fff; text-align:center; margin-top:50px'>{df_grouped_regiao['Regiao'].iloc[0]}</span><br><br><br><span style='font-size:175%; color:#fff; text-align:center;'>Regiao com maior média de congestionamento</span>"},
                            value = round(df_grouped_regiao['Tamanho'].iloc[0],0),
                            number = {"suffix": " metros"},
                            delta = {'relative': True, 'valueformat': '.1%', 'reference': df_grouped_regiao['Tamanho'].mean()},
                            number_font={"size": 23, "color": "#fff"}  # Ajuste o tamanho e a cor do número do indicador aqui
                            )
)
figIndicadorViaComMaoirMediaCongestionamento.update_layout(
    paper_bgcolor='#252a48',  # Define a cor de fundo do papel como '#252a48'
    font=dict(color='#fff'),  # Define a cor do texto do gráfico como branco
    height=160,
    width=239,
    )

#Agrupando por dia da semana
df_grouped_dia_semana = round(df_2022.groupby(['Dia da Semana'], sort=False)['Tamanho'].mean(),2)
df_grouped_dia_semana.sort_values(ascending=False, inplace=True)
df_grouped_dia_semana = df_grouped_dia_semana.reset_index()
df_grouped_dia_semana.head()
figIndicadorDiaComMaiorMediaCongestionamento = go.Figure()
figIndicadorDiaComMaiorMediaCongestionamento.add_trace(go.Indicator(mode='number+delta',
                            title = {"text": f"<span style='font-size:350%; color:#fff; text-align:center;'>{df_grouped_dia_semana['Dia da Semana'].iloc[0]}</span><br><br><br><span style='font-size:175%; color:#fff; text-align:center;'> Dia com maior média de congestionamento</span>"},
                            value = round(df_grouped_dia_semana['Tamanho'].iloc[0],0),
                            number = {"suffix": " metros"},
                            delta = {'relative': True, 'valueformat': '.1%', 'reference': df_grouped_dia_semana['Tamanho'].mean()},
                            number_font={"size": 23, "color": "#fff"}  # Ajuste o tamanho e a cor do número do indicador aqui
                            )
)
figIndicadorDiaComMaiorMediaCongestionamento.update_layout(
    paper_bgcolor='#252a48',  # Define a cor de fundo do papel como '#252a48'
    font=dict(color='#fff'),  # Define a cor do texto do gráfico como branco
    height=160,
    width=239,
)

#AgrupandoMes MAior Media de Congestionamento
df_grouped_mes = round(df_2022.groupby(['Mes'], sort=False)['Tamanho'].mean(),2)
df_grouped_mes.sort_values(ascending=False, inplace=True)
df_grouped_mes = df_grouped_mes.reset_index()
df_grouped_mes.head()
figIndicadorMesMaiorMediaCongestionamento = go.Figure()
figIndicadorMesMaiorMediaCongestionamento .add_trace(go.Indicator(mode='number+delta',
                            title = {"text": f"<span style='font-size:350%; color:#fff; text-align:center;'>{df_grouped_mes['Mes'].iloc[0]}</span><br><br><br><span style='font-size:175%; color:#fff; text-align:center;'>Mês com maior média de congestionamento</span>"},
                            value = round(df_grouped_mes['Tamanho'].iloc[0],0),
                            number = {"suffix": " metros"},
                            delta = {'relative': True, 'valueformat': '.1%', 'reference': df_grouped_mes['Tamanho'].mean()},
                            number_font={"size": 23, "color": "#fff"}  # Ajuste o tamanho e a cor do número do indicador aqui
                            )
)
figIndicadorMesMaiorMediaCongestionamento .update_layout(
    paper_bgcolor='#252a48',  # Define a cor de fundo do papel como '#252a48'
    font=dict(color='#fff'),  # Define a cor do texto do gráfico como branco
    height=160,
    width=239,
    )

# Agrupar por mês e região e calcular a soma do tamanho do congestionamento
df_grouped_mes = df_2022.groupby(['Mes', 'Regiao'], sort=False)['Tamanho'].sum().reset_index()
# Criar o gráfico de barras comparando cada região
figGraficoBarraComparacaoCongestionamentoMesRegiao = go.Figure(data=[
    go.Bar(name='LESTE', x=df_grouped_mes[df_grouped_mes['Regiao'] == 'LESTE']['Mes'], y=df_grouped_mes[df_grouped_mes['Regiao'] == 'LESTE']['Tamanho'], marker=dict(line=dict(width=0))),
    go.Bar(name='CENTRO', x=df_grouped_mes[df_grouped_mes['Regiao'] == 'CENTRO']['Mes'], y=df_grouped_mes[df_grouped_mes['Regiao'] == 'CENTRO']['Tamanho'],  marker=dict(line=dict(width=0))),
    go.Bar(name='NORTE', x=df_grouped_mes[df_grouped_mes['Regiao'] == 'NORTE']['Mes'], y=df_grouped_mes[df_grouped_mes['Regiao'] == 'NORTE']['Tamanho'],  marker=dict(line=dict(width=0))),
    go.Bar(name='OESTE', x=df_grouped_mes[df_grouped_mes['Regiao'] == 'OESTE']['Mes'], y=df_grouped_mes[df_grouped_mes['Regiao'] == 'OESTE']['Tamanho'],  marker=dict(line=dict(width=0))),
    go.Bar(name='SUL', x=df_grouped_mes[df_grouped_mes['Regiao'] == 'SUL']['Mes'], y=df_grouped_mes[df_grouped_mes['Regiao'] == 'SUL']['Tamanho'],  marker=dict(line=dict(width=0)))
])
# Atualizar o layout do gráfico
figGraficoBarraComparacaoCongestionamentoMesRegiao.update_layout(
    title='Comparação de Congestionamento por Mês e Região',
    xaxis_title='Mês',
    yaxis_title='Congestionamento (em metros)',
    barmode='group',
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Define a cor de fundo do gráfico como transparente
    paper_bgcolor='#252a48',  # Define a cor de fundo do papel como '#252a48'
    legend=dict(
        x=1.02,
        y=0.98,
        bgcolor='rgba(255, 255, 255, 0.1)',
        bordercolor='#252a48',
        borderwidth=2,
        font=dict(
            color='#fff' # Define a cor do texto da legenda como branco
        )
    ),
    title_font=dict(
        color='#fff'  # Define a cor do título do gráfico como branco
    ),
    xaxis=dict(
        tickfont=dict(
            color='#fff'  # Define a cor dos números e meses no eixo X como branco
        ),
        title_font=dict(
            color='#fff'  # Define a cor do título do eixo X como branco
        )
    ),
    yaxis=dict(
        tickfont=dict(
            color='#fff'  # Define a cor dos números no eixo Y como branco
        ),
        title_font=dict(
            color='#fff'  # Define a cor do título do eixo Y como branco
        )
    )
)

# Agrupar por mês e região e calcular a soma do tamanho
df_grouped = df_2022.groupby(['Mes', 'Regiao'], sort=False)['Tamanho'].sum().reset_index()
initial_region = 'LESTE'

# Criar o gráfico de barras
figGraficoBarrasHoriCongestionamentoMes = go.Figure(data=[
    go.Bar(name=initial_region, y=df_grouped[df_grouped['Regiao'] == initial_region]['Mes'], x=df_grouped[df_grouped['Regiao'] == initial_region]['Tamanho'], orientation='h'),
])

# Atualizar o layout do gráfico
figGraficoBarrasHoriCongestionamentoMes.update_layout(
    autosize=False,
    width=500,
    height=500,
    title='Comparação de Congestionamento por Mês e Região',
    xaxis_title='Mês',
    yaxis_title='Congestionamento (em metros)',
    barmode='group',
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Define the background color of the graph as transparent
    paper_bgcolor='#252a48',  # Define the background color of the paper as '#252a48'
    legend=dict(
        x=1.02,
        y=0.98,
        bgcolor='rgba(255, 255, 255, 0.1)',
        bordercolor='#252a48',
        borderwidth=2,
        font=dict(
            color='#fff' # Define the color of the legend text as white
        )
    ),
    xaxis=dict(
        tickfont=dict(
            color='#fff'  # Define a cor dos números no eixo X como branco
        ),
        title_font=dict(
            color='#fff'  # Define a cor do título do eixo X como branco
        )
    ),
    yaxis=dict(
        tickfont=dict(
            color='#fff'  # Define a cor dos números no eixo Y como branco
        ),
        title_font=dict(
            color='#fff'  # Define a cor do título do eixo Y como branco
        )
    )
)

#Gerar Data Frame com média agrupadas por mês e região
df_grouped2 = df_2022.groupby(['Mes', 'Regiao'], sort=False)['Tamanho'].mean().reset_index()
df_grouped2.head()
# Gerar gráfico de linha comparando região por mês
figGraficoLinhaComparacaoRegiaoMes = px.line(df_grouped2, x = "Mes", y = "Tamanho", color= "Regiao")
figGraficoLinhaComparacaoRegiaoMes.update_layout(
    autosize=False,
    width=1020,
    height=400,
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Define a cor de fundo do gráfico como transparente
    paper_bgcolor='#252a48',  # Define a cor de fundo do papel como '#252a48'
    legend=dict(
        x=1.02,
        y=0.98,
        bgcolor='rgba(255, 255, 255, 0.1)',
        bordercolor='#252a48',
        borderwidth=2,
        font=dict(
            color='#fff' # Define a cor do texto da legenda como branco
        )
    ),
        title_font=dict(
        color='#fff'  # Define a cor do título do gráfico como branco
    ),
    xaxis=dict(
        tickfont=dict(
            color='#fff'  # Define a cor dos números e meses no eixo X como branco
        ),
        title_font=dict(
            color='#fff'  # Define a cor do título do eixo X como branco
        )
    ),
    yaxis=dict(
        tickfont=dict(
            color='#fff'  # Define a cor dos números no eixo Y como branco
        ),
        title_font=dict(
            color='#fff'  # Define a cor do título do eixo Y como branco
        )
    )
    )

dias_semana_ordem = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
# Agrupar por dia da semana e região e calcular a soma do tamanho
df2 = pd.Categorical(df_2022['Dia da Semana'],categories=dias_semana_ordem, ordered=True)
df_grouped3 = df_2022.groupby(['Dia da Semana', 'Regiao'], sort=False)['Tamanho'].mean().reset_index()
df_grouped3.head()
# Criar o gráfico de barras
figGraficoBarraDiaSemana = go.Figure(data=[
    go.Bar(name='LESTE', x=df_grouped3[df_grouped3['Regiao'] == 'LESTE']['Dia da Semana'], y=df_grouped3[df_grouped3['Regiao'] == 'LESTE']['Tamanho'], marker=dict(line=dict(width=0))),
    go.Bar(name='CENTRO', x=df_grouped3[df_grouped3['Regiao'] == 'CENTRO']['Dia da Semana'], y=df_grouped3[df_grouped3['Regiao'] == 'CENTRO']['Tamanho'], marker=dict(line=dict(width=0))),
    go.Bar(name='NORTE', x=df_grouped3[df_grouped3['Regiao'] == 'NORTE']['Dia da Semana'], y=df_grouped3[df_grouped3['Regiao'] == 'NORTE']['Tamanho'], marker=dict(line=dict(width=0))),
    go.Bar(name='OESTE', x=df_grouped3[df_grouped3['Regiao'] == 'OESTE']['Dia da Semana'], y=df_grouped3[df_grouped3['Regiao'] == 'OESTE']['Tamanho'], marker=dict(line=dict(width=0))),
    go.Bar(name='SUL', x=df_grouped3[df_grouped3['Regiao'] == 'SUL']['Dia da Semana'], y=df_grouped3[df_grouped3['Regiao'] == 'SUL']['Tamanho'], marker=dict(line=dict(width=0)))
])
# Atualizar o layout do gráfico
figGraficoBarraDiaSemana.update_layout(
    autosize=False,
    width=1020,
    height=400,
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Define a cor de fundo do gráfico como transparente
    paper_bgcolor='#252a48',  # Define a cor de fundo do papel como '#252a48'
    legend=dict(
        x=1.02,
        y=0.98,
        bgcolor='rgba(255, 255, 255, 0.1)',
        bordercolor='#252a48',
        borderwidth=2,
        font=dict(
            color='#fff' # Define a cor do texto da legenda como branco
        )
    ),
        title_font=dict(
        color='#fff'  # Define a cor do título do gráfico como branco
    ),
    xaxis=dict(
        tickfont=dict(
            color='#fff'  # Define a cor dos números e meses no eixo X como branco
        ),
        title_font=dict(
            color='#fff'  # Define a cor do título do eixo X como branco
        )
    ),
    yaxis=dict(
        tickfont=dict(
            color='#fff'  # Define a cor dos números no eixo Y como branco
        ),
        title_font=dict(
            color='#fff'  # Define a cor do título do eixo Y como branco
        )
    )
    )

# Caixa layout
app.layout = html.Div([ 
    
    html.Div(
        className="header",
        children=[
            html.H1('SISTEMA DE MONITORAMENTO DE TRAFEGO URBANO', className="header-logo"),
        ]
    ),

        html.Div(
        className="body-do-painel",
        children=[
            html.Img(
                src="./assets/utils/logo.png", alt="logo", className='logo'),
            # dcc.Dropdown(, 
            #     value='', 
            #     id='demo-dropdown',
            #     className='demo-dropdown'),
            html.H3(
                children='Selecione para filtrar:', className="body-do-painel-texto"),
            html.Div(style={"margin-bottom": "20px"}),  # Espaçamento entre os dropdowns

            #Dropdown seleção do ano
            html.Div(
                className="painel-lateral",
                children=[
                html.Label("Ano", className="titulo-dropdown"),
                dcc.Dropdown(
                    options=[
                        {"label": "2021", "value": "opcao1"},
                        {"label": "2022", "value": "opcao2"},
                    ],
                    style={'align-items': 'center', 'justify-content': 'center', 'width':'95%'},
                    searchable=False,
                    id='demo-dropdown',
                    placeholder="Selecione o ano",
                    className='lateral-dropdown'
                ),
                ],
            ),
            html.Div(style={"margin-bottom": "20px"}),  # Espaçamento entre os dropdowns

            #Dropdown seleção do ano
            html.Div(
                className="painel-lateral",
                id='base-dados-dropdown',
                children=[
                html.Label("Região", className="titulo-dropdown"),
                dcc.Dropdown(
                    options=[
                        {"label": "Todas as regioes", "value": "Todas as regioes"},
                        {"label": "Leste", "value": "LESTE"},
                        {"label": "Norte", "value": "NORTE"},
                        {"label": "Sul", "value": "SUL"},
                        {"label": "Oeste", "value": "OESTE"},
                    ],
                    placeholder="Selecione a Regiao",
                    style={'align-items': 'center', 'justify-content': 'center', 'width':'95%'},
                    searchable=False,
                    id='dropdown-regiao',
                    className='lateral-dropdown'
                )
                ],
            ),

        ]
    ),

    
    # INDICADORES
    html.Div(
    className="figIndicadorZonaMaoirMediaCongestionamento",
    children=[
        dcc.Graph(
            id='figIndicadorZonamMaoirMediaCongestionamento',
            figure=figIndicadorZonaMaoirMediaCongestionamento,
            style={
                'borderRadius': '10px',
                'border': '5px solid #252a48'
            }        
)
    ]
),
    html.Div(
    className="figIndicadorDiaComMaiorMediaCongestionamento",
    children=[
        dcc.Graph(
            id='IndicadorDiaComMaiorMediaCongestionamento',
            figure=figIndicadorDiaComMaiorMediaCongestionamento,
            style={
                'borderRadius': '10px',
                'border': '5px solid #252a48'
            }         
)
    ]
),
    html.Div(
    className="figIndicadorMesMaiorMediaCongestionamento",
    children=[
        dcc.Graph(
            id='figIndicadorMesMaiorMediaCongestionamento',
            figure=figIndicadorMesMaiorMediaCongestionamento,
            style={
                'borderRadius': '10px',
                'border': '5px solid #252a48'
            }          
)
    ]
),
    html.Div(
    className="figIndicadorViaComMaoirMediaCongestionamento",
    children=[
        dcc.Graph(
            id='figIndicadorViaComMaoirMediaCongestionamento',
            figure=figIndicadorViaComMaoirMediaCongestionamento,
            style={
                'borderRadius': '10px',
                'border': '5px solid #252a48'
            }         
)
    ]
),
    

    # GRAFICOS

    html.Div(
    className="figGraficoBarrasHoriCongestionamentoMes",
    children=[
        dcc.Graph(
            id='figGraficoBarrasHoriCongestionamentoMes',
            figure=figGraficoBarrasHoriCongestionamentoMes,  
            style={
                'borderRadius': '10px',
                'border': '5px solid #252a48'}    
)
    ]
),
    html.Div(
        className="figGraficoCongestionamentoMesRegiao",
        children=[
            dcc.Graph(
                id='figGraficoCongestionamentoMesRegiao',
                figure=figGraficoCongestionamentoMesRegiao,
                style={
                'borderRadius': '10px',
                'border': '5px solid #252a48'
            }            
                
    )
        ]
    ),
    html.Div(
    className="figGraficoBarraDiaSemana",
    children=[
        dcc.Graph(
            id='figGraficoBarraDiaSemana',
            figure=figGraficoBarraDiaSemana,
            style={
                'borderRadius': '10px',
                'border': '5px solid #252a48'
            }        
)
    ]
),
    html.Div(
    className="figGraficoBarraComparacaoCongestionamentoMesRegiao",
    children=[
        dcc.Graph(
            id='grafico_frutas',
            figure=figGraficoBarraComparacaoCongestionamentoMesRegiao,
            style={
                'borderRadius': '10px',
                'border': '5px solid #252a48'
            }        
)
    ]
),
    html.Div(
    className="figGraficoLinhaComparacaoRegiaoMes",
    children=[
        dcc.Graph(
            id='figGraficoLinhaComparacaoRegiaoMes',
            figure=figGraficoLinhaComparacaoRegiaoMes,
            style={
                'borderRadius': '10px',
                'border': '5px solid #252a48'
            }        
)
    ]
),



])



# Defina a função de callback para atualizar o gráfico quando o valor do dropdown mudar
@app.callback(
    Output('figGraficoBarrasHoriCongestionamentoMes', 'figure'),
    [Input('dropdown-regiao', 'value')]
)
def update_graph(region):
    colors = {'LESTE': '#3b6be3', 'CENTRO': '#14cb96', 'NORTE': '#fca05a', 'OESTE': '#ee553b', 'SUL': '#7e6bf8'}
    
    if region == "Todas as regioes":
        fig = go.Figure(data=[
            go.Bar(name='LESTE', y=df_grouped[df_grouped['Regiao'] == 'LESTE']['Mes'], x=df_grouped[df_grouped['Regiao'] == 'LESTE']['Tamanho'], orientation='h', marker=dict(color=colors['LESTE'], line=dict(width=0))),
            go.Bar(name='CENTRO', y=df_grouped[df_grouped['Regiao'] == 'CENTRO']['Mes'], x=df_grouped[df_grouped['Regiao'] == 'CENTRO']['Tamanho'], orientation='h', marker=dict(color=colors['CENTRO'], line=dict(width=0))),
            go.Bar(name='NORTE', y=df_grouped[df_grouped['Regiao'] == 'NORTE']['Mes'], x=df_grouped[df_grouped['Regiao'] == 'NORTE']['Tamanho'], orientation='h', marker=dict(color=colors['NORTE'], line=dict(width=0))),
            go.Bar(name='OESTE', y=df_grouped[df_grouped['Regiao'] == 'OESTE']['Mes'], x=df_grouped[df_grouped['Regiao'] == 'OESTE']['Tamanho'], orientation='h', marker=dict(color=colors['OESTE'], line=dict(width=0))),
            go.Bar(name='SUL', y=df_grouped[df_grouped['Regiao'] == 'SUL']['Mes'], x=df_grouped[df_grouped['Regiao'] == 'SUL']['Tamanho'], orientation='h', marker=dict(color=colors['SUL'], line=dict(width=0)))
        ])
    else:
        filtered_data = df_grouped[df_grouped['Regiao'] == region]
        region_color = colors[region]
        fig = go.Figure(data=go.Bar(name=region, y=filtered_data['Mes'], x=filtered_data['Tamanho'], orientation='h', marker=dict(color=region_color, line=dict(width=0))))
    
    fig.update_layout(
        title=f'Tamanho por Região - {region}',
        xaxis_title='Congestionamento (em metros)',
        yaxis_title='Mês',
        barmode='group',
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Define the background color of the graph as transparent
        paper_bgcolor='#252a48',  # Define the background color of the paper as '#252a48'
        legend=dict(
            x=1.02,
            y=0.98,
            bgcolor='rgba(255, 255, 255, 0.1)',
            bordercolor='#252a48',
            borderwidth=2,
            font=dict(
                color='#fff' # Define a cor do texto da legenda como branco
            )
        ),
        title_font=dict(
            color='#fff'  # Define a cor do título do gráfico como branco
        ),
        xaxis=dict(
            tickfont=dict(
                color='#fff'  # Define a cor dos números no eixo X como branco
            ),
            title_font=dict(
                color='#fff'  # Define a cor do título do eixo X como branco
            )
        ),
        yaxis=dict(
            tickfont=dict(
                color='#fff'  # Define a cor dos números no eixo Y como branco
            ),
            title_font=dict(
                color='#fff'  # Define a cor do título do eixo Y como branco
            )
        )
    )
    
    return fig







# Colocar no ar
if __name__ == '__main__':
    app.run_server(debug=True)
