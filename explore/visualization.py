from order import ExploreOrder
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)
from utility.datafilepath import g_singletonDataFilePath
from weather import ExploreWeather
from traffic import ExploreTraffic
import numpy as np
import math
from poi import ExplorePoi


class visualizeData(ExploreOrder, ExploreWeather, ExploreTraffic, ExplorePoi):
    def __init__(self):
        ExploreOrder.__init__(self)
        self.gapdf = self.load_gapdf(g_singletonDataFilePath.getTrainDir())
#         self.gap_time_dict = self.gapdf.groupby('time_slotid')['gap'].sum().to_dict()
        self.weathdf = self.load_weatherdf(
            g_singletonDataFilePath.getTrainDir())
#         self.trafficdf = self.load_trafficdf(g_singletonDataFilePath.getTrainDir())
#         self.gapDict = self.loadGapDict(g_singletonDataFilePath.getTrainDir() + 'temp/gap.csv.dict.pickle')
        return

    def disp_gap_bytimeiid(self):
        gaps_mean = self.gapdf.groupby('time_id')['gap'].mean()
        gaps_mean.plot(kind='bar')
        plt.ylabel('Mean of gap')
        plt.title('Timeslot/Correlation')
        return

    def disp_gap_bydistrict(self):
        gaps_mean = self.gapdf.groupby('start_district_id')['gap'].mean()
        gaps_mean.plot(kind='bar')
        plt.ylabel('Mean of gap')
        plt.title('District/Gap Correlation')
#         for i in gaps_mean.index:
#             plt.plot([i,i], [0, gaps_mean[i]], 'k-')
#         plt.show()
        return

    def disp_gap_bydate(self):
        gaps_mean = self.gapdf.groupby('time_date')['gap'].mean()
        gaps_mean.plot(kind='bar')
        plt.ylabel('Mean of gap')
        plt.title('Date/Gap Correlation')
#         for i in gaps_mean.index:
#             plt.plot([i,i], [0, gaps_mean[i]], 'k-')
        plt.show()
        return

    def find_gap_by_timeslot(self, timeslot):
        try:
            return self.gap_time_dict[timeslot]
        except:
            return 0
        return

    def show_weather_bydate(self):
        self.weathdf['gap'] = self.weathdf['time_slotid'].apply(
            self.find_gap_by_timeslot)
        by_date = self.weathdf.groupby('time_date')
        size = len(by_date)
        col_len = row_len = math.ceil(math.sqrt(size))
        count = 1
        for name, group in by_date:
            ax = plt.subplot(row_len, col_len, count)
#             temp = np.empty(group['time_id'].shape[0])
#             temp.fill(2)

#             ax.plot(group['time_id'], group['gap']/group['gap'].max(), 'r', alpha=0.75)
#             ax.plot(group['time_id'], group['weather']/group['weather'].max())
            ax.bar(group['time_id'], group['weather'], width=1)
            ax.set_title(name)
            count = count + 1
#             plt.bar(group['time_id'], np.full(group['time_id'].shape[0], 5), width=1)

        plt.show()
        return

    def run(self):
        self.show_weather_bydate()

        return


if __name__ == "__main__":
    obj = visualizeData()
    obj.run()
