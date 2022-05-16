import os
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from os.path import exists as file_exists

class VizManager:
    """
    a class that manages the extraction of charts from notebooks
    and deploying them on streamlit app.
    """

    def __init__(self) -> None:
        """
        set up.
        """
        # setting up directory paths.

        self.parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self.charts_dir = os.path.join(self.parent_dir, "charts")
        self.data_dir = os.path.join(self.parent_dir, "data")

        # checking if chart_tracker.csv file exists and importing it
        
        self.load_tracker()
        self.save_tracker()
            

    def save_tracker(self):
        """
        saving chart tracker dataframe.
        """
        self.chart_tracker_df.to_csv(self.tracker_file, index = False)

    def load_tracker(self):
        """
        loading saving chart tracker csv file
        """
        self.tracker_file = self.data_dir+"/chart_tracker.csv"

        if(file_exists(self.tracker_file) and os.stat(self.tracker_file).st_size != 0 ):
            self.chart_tracker_df = pd.read_csv(self.tracker_file)
        else:
            tracker_dict = { "chart_name": ["dummy"], "chart_desc": ["dummy desc"] }
            self.chart_tracker_df = pd.DataFrame(tracker_dict)
    
    
    def load_charts(self, st, chart_name):
        """
        loading charts from charts folder and descriptions from
        the tracking csv file.    
        """
        desc = self.chart_tracker_df[self.chart_tracker_df["chart_name"] == chart_name].iloc[1,2]

        st.subheader("Applications Data Usage")
        image = Image.open(self.charts_dir+"/"+chart_name)
        st.image(image, caption = desc)

    def save_charts(self, pltc, name, desc):
        """
        saves the charts in charts folder and 
        """
        self.load_tracker()

        pltc.savefig(self.charts_dir+"/"+name)
        self.chart_tracker_df.append
        row = {"chart_name":name, "chart_desc":desc}
        self.chart_tracker_df = self.chart_tracker_df[self.chart_tracker_df['chart_name'] != name]
        self.chart_tracker_df = self.chart_tracker_df.append(row, ignore_index = True)

        self.save_tracker()


    def plot_bar(self, df, col, title, save = False, name = None, desc = None):
        
        plt.bar(df[col[0]],df[col[1]])
        plt.title(title)
        plt.xlabel(col[0])
        plt.ylabel(col[1])
        plt.show()
        if (save):
            self.save_charts(plt, name, desc)

    
    def plot_pie(self, df, col, title, save=False, name = None, desc = None):
        """
        pie chart plotting function.
        """
        # Wedge properties
        wp = { 'linewidth' : 1, 'edgecolor' : "black" }

        # Creating autocpt arguments
        def func(pct, allvalues):
            absolute = int(pct / 100.*np.sum(allvalues))
            return "{:.1f}%\n({:d} g)".format(pct, absolute)
        
        fig, ax = plt.subplots(figsize =(10, 7))
        wedges, texts, autotexts = ax.pie(df[col[1]],
                                    autopct = lambda pct: func(pct, df[col[1]]),
                                    labels = df[col[0]].to_list(),
                                    startangle = 90,
                                    wedgeprops = wp,)

        plt.setp(autotexts, size = 8, weight ="bold")
        ax.set_title(title)
        if(save):
            self.save_charts(plt, name, desc)

    def plot_scatter(self):
        pass
