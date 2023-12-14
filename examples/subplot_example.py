import forestplot as fp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec



# fill in
df = pd.read_csv('test.csv')

headers = ['Header 1','Header 2','Header 3','Header 4','Header 5']
header_short = ['h1', 'h2', 'h3', 'h4', 'h5']

fig, axarr = plt.subplots(2, 3, figsize=(20,20), sharey=True)
fig.tight_layout(h_pad=2)

k = 0
for i in range(2):
    for j in range(3):
      col = header_short[k]
      ax = fp.forestplot(df, ax=axarr[i,j], estimate=col+'1', ll=col+'2', hl=col+'3', 
                         varlabel='label', 
                  ci_report=False,  
                  **{"marker": "D",  # set maker symbol as diamond
                     "markersize": 35,  # adjust marker size
                     "xlinestyle": (0, (10, 5)),  # long dash for x-reference line 
                     "xlinecolor": ".1",  # gray color for x-reference line
                     "xtick_size": 12,  # adjust x-ticker fontsize
                     "fontsize": 14,
                     }  )
      if j > 0:
         ax.axes.get_yaxis().set_visible(False)
      ax.set_xlim(-.09, .09)
      ax.set_title(headers[k])#, loc='left')
      k += 1
      if k >= 5:
         break

axarr[-1,-1].axis('off')

plt.savefig('test.png', bbox_inches='tight', dpi=300)
