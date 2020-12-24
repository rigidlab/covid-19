import argparse
import pandas as pd
import altair as alt
from altair import datum
from bokeh.plotting import figure,show,save

def main():
    parser=argparse.ArgumentParser(description='Plot COVID-19 Data')
    parser.add_argument('--cases',help='Cases CSV file',
        default='COVID-19_case_counts_by_date.csv')
    parser.add_argument('--hospitalizations',help='Hospitalizations CSV file',
        default='COVID-19_hospitalizations_by_date.csv')
    args=parser.parse_args()

    cases_df=pd.read_csv(args.cases)
    hos_df=pd.read_csv(args.hospitalizations)
    df=pd.merge(cases_df,hos_df,on='Date')
    df=df.melt(id_vars=['Date'],var_name='Type',value_name='Count')
    scales = alt.selection_interval(bind='scales',encodings=['x'])
    brush = alt.selection(type='interval', encodings=['x'])

    base=alt.Chart(df).encode(
        alt.X('Date:T',axis=alt.Axis(title=None)),
    )
    bar=base.mark_bar(color='purple').encode(
        alt.Y('Count:Q',axis=alt.Axis(title='New Cases')),
        tooltip='Count:Q',
    ).transform_filter(
        datum.Type=='New_cases'
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
        datum.Type=='Total_cases'
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
    chart.save('covid-19.html')

if __name__=='__main__':
    main()
