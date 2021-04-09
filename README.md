# streaming_RFM_segmentation

Visit the web app directly at this address: https://share.streamlit.io/bbelescot/streaming_rfm_segmentation/main/app.py

To try RFM segmentation on your own data, please make a .csv file respecting these rules and upload the file in the last section of the [web app](https://share.streamlit.io/bbelescot/streaming_rfm_segmentation/main/app.py):
- headers should be the followings: `r_value, f_value, m_value'
- the size of the file should not overpass 200MB and the number of lines should be between at least a hundreds (to have something to work with) to tens of thousands max
- seperator should be a comma
- for reference, look at the .csv file provided in the repository as an example


To run the Streamlit webapp "app.py" locally: 

- Clone this directory: `git clone XXXXXXX`
- Install Streamlit and requirements `pip install streamlit` etc
- Move into the directory: `cd XXXX`
- Launch streamlit locally using: `streamlit run app.py`, a localhost page should open on your browser with the app running

