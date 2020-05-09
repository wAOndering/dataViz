
'''
Rumbaugh lab
Test on data vizualization and code writing
email: tvaissie@scripps.edu
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
sns.set()
sns.set_style("ticks")
 #allow to have interactive mode on revert bakc with plt.ioff()
plt.ion()

# test of data vizulization based on latest graph
# # https://github.com/RainCloudPlots/
# # https://github.com/jorvlan/open-visualizations

# notes regarding ploting behavior check matplotlib backend
# plt.get_backend()



##########################################################################
# Functions
##########################################################################

### could be integrated into class ...

def randomDataCreation(Ngp=2, N=10, Nsub=20):

    """Function to create a random data frame in pandas that will create a data frame
    with mock up data for experimentation on viz

    Parameters:
        Ngp (int): simulated number of group
        N (int): simulated number of subject per group
        Nsub (int): simulated number of observation per subjectN
    """

    # set random seed to replicate the same random number
    np.random.seed(22)
    # form the group and data creation based on the most granular and build up
    # create all the granular data
    Ntotal=Ngp*N*Nsub
    data = np.random.randint(0,50,size=(Ntotal,))
    np.random.shuffle(data)

    # create the category for the N
    subN=list(range(0,N))
    subPerGroup=list(np.repeat(subN, [Ngp], axis=0))*Nsub

    # create the category for the group
    subGroup=list(range(0,Ngp))*N*Nsub

    # merge the date in a long format
    df = pd.DataFrame({'genotype': subGroup,
                        'subject': subPerGroup,
                        'value': data})
    df.genotype=df.genotype.astype(str) 
    return df

def myPalette(colnumber=9, coldivergence=3):

    """Function that returns an hexadecimal list 

    Parameters:
        colnumber (int): simulated number of group
        N (int): simulated number of subject per group

    """
    # color palette for plotting

    colcenter=int(colnumber/2)
    myPal=sns.diverging_palette(240, 10, n=colnumber).as_hex()
    # ## to plot the full palette that was generated see comments below to uncomment
    # sns.palplot(myPal)
    # plt.show(block=False)
    # subset the palette to the 2 color of interest
    myPal=[myPal[colcenter-coldivergence], myPal[colcenter+coldivergence]]

    return myPal

def paramsForCustomPlot(myPal, data, variableLabel='genotype', subjectLabel='subject', valueLabel='value'):
    """Function to create the parametters for ploting the variable, value, subject setup manually create a dictionary for the parameter to be reused for ploting see
    
    Parameters:
        data (DataFrame): dataframe with the data
        myPal (list): list of hexadecimal RGB value should be at least the length of the variableLable
        variableLabel (str): name of the variable of interest, header of the variable column
        subjectLabel (str): name of the subject of interest, header of the subject column
        valueLabel (str): name of the subject of interest, 

    """


    dfSummary=df.groupby(['genotype','subject']).mean()
    dfSummary.reset_index(inplace=True)



    params = dict(  data=dfSummary,
                    x=str(variableLabel),
                    y=str(valueLabel),
                    hue=str(variableLabel),
                    palette=list(myPal))

    paramsNest = dict(  data=df,
                    x=str(variableLabel),
                    y=str(valueLabel),
                    hue=str(variableLabel),
                    palette=list(myPal))

    return params, paramsNest

def customPlot(params, paramsNest, dirName='C:/Users/Windows/Desktop/MAINDATA_OUTPUT'):
    """Function to create save the plot to determine directior
    
    Parameters:
        params (dict): set of parameters for plotting main data
        paramsNest (dict): set of parameters for plotting main data (subNesting level)
        dirName(str): string to determine the directory
    """

    # create the frame for the figure
    os.makedirs(dirName,exist_ok=True)

    # the figure size correspond to the size of a plot in inches
    f, ax = plt.subplots(figsize=(7, 7))

    ## add if the study was longitudinal / repeated measures
    castdf=pd.pivot_table(df, values='value', index=['subject'], columns=['genotype'])
    for i in castdf.index:
        ax.plot([0,1], castdf.loc[i,[0,1]], linestyle='-', color = 'gray', alpha = .3)

    # fill the figure with appropiate seaborn plot
    # sns.boxplot(dodge = 10, width = 0.2, fliersize = 2, **params)
    sns.violinplot(split = True, inner = 'quartile', width=0.6, cut=1, **paramsNest)
    sns.stripplot(jitter=0.08, dodge=True, edgecolor='white', size=4, linewidth=1, **paramsNest)

    # control the figure parameter with matplotlib control
    # this order enable to have transparency of the distribution violin plot
    plt.setp(ax.collections, alpha=.2)


    # the point plot enable to plot the mean and the standard error 
    # to have the "sd" or 95 percent confidence interval 
    # for sem ci=68
    sns.pointplot(ci=68, scale=1.2, dodge= -0.1, errwidth=4, **params)
    sns.pointplot(ci=95, dodge= -0.1, errwidth=2, **params)
    # plot the median could be done with the commented line below however this would be redundant 
    # since the median is already ploted in the violin plot
    # sns.pointplot(ci=None, dodge= -0.2, markers='X',estimator=np.median, **params)
    sns.stripplot(jitter=0.08, dodge=True, edgecolor='white', size=8, linewidth=1, **params)

    # label plot legend and properties
    ax.legend_.remove()
    sns.despine() 

    ax.set_ylabel(params.get('y'), fontsize=30)
    ax.tick_params(axis="y", labelsize=20)
    # ax.set_ylim([-5,5])

    ax.set_xlabel(params.get('x'), fontsize=30)
    ax.tick_params(axis="x", labelsize=20, pad=10) # could also use: ax.xaxis.labelpad = 10 // plt.xlabel("", labelpad=10) // or change globally rcParams['xtick.major.pad']='8'
    plt.tight_layout()

    plt.show(block=False)


    # property to export the plot 
    # best output and import into illustrator are svg 
    return plt.savefig(dirName+"/testPlot.svg"),     plt.show(block=False)

##########################################################################
# data generation
##########################################################################

# create the dataset
df=randomDataCreation(2,10,20)

# obtain the color palette of interest
myPal=myPalette()

# create dictionary of parameteres to be used for ploting
params, paramsNest = paramsForCustomPlot(myPal, df)

customPlot(params,paramsNest)


# ax.set_adjustable('datalim')
# ax.set_aspect(0.05) #can be useful to change the aspect of the graph
