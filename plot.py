import requests
import pandas as pd
import altair as alt
from altair import datum
from bokeh.plotting import figure,show,save

def main():
    cases_json=requests.get('https://data.sccgov.org/resource/6cnm-gchg.json').json()
    #hos_json=requests.get('https://data.sccgov.org/resource/5xkz-6esm.json').json()
    cases_df=pd.DataFrame(cases_json)
    #hos_df=pd.DataFrame(hos_json)
    #df=pd.merge(cases_df,hos_df,on='date')
    #df=df.melt(id_vars=['date'],var_name='Type',value_name='Count')
    df=cases_df
    print(df)
    print(cases_df.head())
    scales = alt.selection_interval(bind='scales',encodings=['x'])
    brush = alt.selection(type='interval', encodings=['x'])

    base=alt.Chart(df).encode(
        alt.X('date:T',axis=alt.Axis(title=None)),
    )
    bar=base.mark_bar(color='purple').encode(
        alt.Y('new_cases:Q',axis=alt.Axis(title='New Cases')),
        tooltip='new_cases:Q',
    )
    line=base.mark_line(color='red').encode(
        alt.Y('total_cases:Q',
            axis=alt.Axis(title='Total cases')
        ),
        tooltip='total_cases:Q'
    )
    cases=alt.layer(bar,line).resolve_scale(
        y='independent'
    ).properties(
        width=700,
        height=300,
        title='Santa Clara'
    ).add_selection(
        scales
    )
    chart=cases
    chart.save('index.html')

if __name__=='__main__':
    main()
