import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_json('../dataset/2304201602/summarizer/2304201602.json')

grouped = df.groupby(['created_at']).size()

tweet_count = grouped.as_matrix()
timestamps = grouped.keys()

one_second = np.timedelta64(1, 's')
interval_start = timestamps[0]

batch_timestamps = np.zeros(1)
batch_tweet_count = np.zeros(1)
batch_range = np.zeros(1)

index, count = 0, 0

for time in timestamps:
	if ((time - interval_start) <= (40.0 * one_second)):
		count += tweet_count[index]
	else:
		batch_timestamps = np.append(batch_timestamps, interval_start)
		batch_tweet_count = np.append(batch_tweet_count, count)

		interval_start = timestamps[index]

		count = tweet_count[index]

	index += 1

df = pd.DataFrame()
df['x'] = pd.Series(batch_timestamps[1:])
df['x'] = df['x'].apply(lambda t: t.value // 10 ** 9)
df['y'] = pd.Series(batch_tweet_count[1:])

x = df['x'].as_matrix()
y = df['y'].as_matrix()

from scipy.interpolate import UnivariateSpline

s = UnivariateSpline(x, y, s=1)
xs = np.linspace(x[0], x[x.size-1], 6000)
ys = s(xs)

from scipy.signal import find_peaks_cwt, argrelextrema
markers = find_peaks_cwt(y, np.arange(1, 20))

maximas = argrelextrema(y, np.greater)

more_maximas = argrelextrema(y[maximas], np.greater)

z = (maximas[0])[more_maximas]

#df['created_at'] = df['created_at'].apply(lambda t: t.value // 10 ** 9)

plt.plot(x, y, '.-')
#plt.plot(x[maximas], y[maximas], 'ro')
plt.plot(x[z], y[z], 'go')
plt.plot(xs, ys)
plt.grid()
plt.show()
