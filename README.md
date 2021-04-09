# streaming_RFM_segmentation

To run the Streamlit webapp "app.py": 

- First install Streamlit `pip install streamlit`
- Clone this directory: `git clone XXXXXXX`
- Move into the directory: `cd XXXX`
- Launch streamlit locally using: `streamlit run app.py`, a localhost page should open on your browser with the app running

To try RFM segmentation on your own data please, make a .csv file respecting these rules:
- headers should be the followings: `r_value, f_value, m_value'
- the size of the file should not overpass 200MB and the number of lines should be between at least a hundreds (to have something to work with) to tens of thousands max
- seperator should be a comma
- for reference, look at the .csv file provided in the repository as an example
