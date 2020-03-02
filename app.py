import pandas as pd
import numpy as np
import plotly.graph_objects as do
import streamlit as st
import os

token_map= os.environ.get('MAPBOX_TOKEN')
style_map= os.environ.get('MAPBOX_STYLE')

@st.cache
def data_load():
	return pd.read_excel('Volcano Eruptions (mod).xlsx')

def main():
	data = data_load()
	
	st.title('Volcano Eruptions Around the World')
	st.markdown('Location of volcanoes with eruptions during the Holocene period (approximately the last 10,000 years).')
	
	option1 = st.selectbox('Select activity evidence', data['Activity Evidence'].unique())
	df = data.loc[data['Activity Evidence']==option1]
	
	st.markdown('*It is recommended to view the map in full screen for better interactivity. Click the control in the top right corner of the map to go full screen.*')

	midpoint = (np.average(data['latitude']), np.average(data['longitude']))
	map_token = token_map
	map_style = style_map

	vulcan_lat = list(df['latitude'])
	vulcan_lon = list(df['longitude'])
	vulcan_name = list(df['Volcano Name'])
	vulcan_type = list(df['Primary Volcano Type'])
	vulcan_country = list(df['Country'])
	vulcan_erup = list(df['Last Known Eruption'])

	hover_text = ['Name: ' + '{}'.format(x) + '<br>Type: ' + '{}'.format(y) + '<br>Country: ' + '{}'.format(z) + '<br>Last Eruption: ' + '{}'.format(v) for x,y,z,v in zip(vulcan_name,vulcan_type,vulcan_country,vulcan_erup)]
	
	plot = do.Figure()
	
	plot.add_trace(
		do.Scattermapbox(
        		lat=vulcan_lat,
        		lon=vulcan_lon,
       			mode='markers',
        		marker=do.scattermapbox.Marker(
            			size=10,
            			color='rgb(238, 45, 41)',
            			opacity=0.6
        			),
        		text= hover_text,
        		hoverinfo='text',
        		showlegend= False
    		)
	)
    	
	plot.update_layout(
    		mapbox= do.layout.Mapbox(
    			accesstoken= map_token,
    			center= do.layout.mapbox.Center(
    				lat= midpoint[0],
    				lon= midpoint[1]
    			),
    			zoom= 0.5,
    			style= map_style
    		),
		margin= do.layout.Margin(
    			l=0,
    			r=0,
    			t=0,
    			b=0
    		)
	)
	st.plotly_chart(plot,use_container_width=True)
	
	st.markdown('Data Source: Global Volcanism Program | Viz by: nvqa')


if __name__ == '__main__':
	main()
