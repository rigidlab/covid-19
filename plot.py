import requests
import pandas as pd
import altair as alt
from altair import datum
from bokeh.plotting import figure,show,save

def main():
    cases_json=requests.get('https://data.sccgov.org/resource/6cnm-gchg.json').json()
    hos_json=requests.get('https://data.sccgov.org/resource/5xkz-6esm.json').json()
    cases_df=pd.DataFrame(cases_json)
    hos_df=pd.DataFrame(hos_json)
    print(cases_df.head())
    print(hos_df.head())
    df=pd.merge(cases_df,hos_df,on='date')
    df=df.melt(id_vars=['date'],var_name='Type',value_name='Count')
    scales = alt.selection_interval(bind='scales',encodings=['x'])
    brush = alt.selection(type='interval', encodings=['x'])

    base=alt.Chart(df).encode(
        alt.X('date:T',axis=alt.Axis(title=None)),
    )
    bar=base.mark_bar(color='purple').encode(
        alt.Y('Count:Q',axis=alt.Axis(title='New Cases')),
        tooltip='Count:Q',
    ).transform_filter(
        datum.Type=='new_cases'
    )

    bar2=base.mark_bar().encode(
        alt.Y('Count:Q',axis=alt.Axis(title='Hospitalizations')),
        color='Type'
    ).transform_filter(
        (datum.Type=='non_icu_covid')  | (datum.Type=='icu_covid')
    )
    line=base.mark_line(color='red').encode(
        alt.Y('Count:Q',
            axis=alt.Axis(title='Total cases')
        )
    ).transform_filter(
        datum.Type=='total_cases'
    )
    #chart=(bar+bar2).add_selection(scales)
    cases=alt.layer(bar,line).resolve_scale(
        y='independent'
    ).properties(
        width=700,
        height=300,
        title='Santa Clara'
    ).add_selection(
        scales,
    )
    hos=bar2.properties(
        width=700,
        height=300,
        title='Santa Clara'
    ).add_selection(
        scales,
    )

    chart=cases&hos
    chart.save('index.html')

if __name__=='__main__':
    main()
