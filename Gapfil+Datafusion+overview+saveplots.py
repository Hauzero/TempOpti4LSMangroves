#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 02:59:45 2018

@author: leon
"""

    ### LOAD PACKAGES ###

from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import csv
from itertools import groupby

    ### DEFINE PATHS ###
    
user    = 'leon' #'hauserlt' 
pathall = '/media/' + user + '/FREECOM HDD/W-Documents/STI WORKS/Article w Binh/Raster/NgocHien_' 
output  = '/media/' + user + '/FREECOM HDD/W-Documents/STI WORKS/Article w Binh/Quickplot/'
log     = '/media/' + user + '/FREECOM HDD/W-Documents/STI WORKS/Article w Binh/log/' 
outgeo     = '/media/' + user + '/FREECOM HDD/W-Documents/STI WORKS/Article w Binh/Tiff_out/' 

yearlist = [ "2001-2002", "2003-2004", "2005-2006", "2007-2008", "2009-2010", "2011-2012", "2013", "2014", "2015", "2016", "2017" ] 



    ### LOAD LANDSAT 5, 7 and 8 ARCHIVES into 2 separate files LS 5+8 and LS 7+8 ###
shp5  = np.zeros((912, 1929,11)) 
shp7  = np.zeros((912, 1929,11))
for d, yr in enumerate(yearlist):
    if d <= 5:
        path = pathall + str(yr) + '_LS5_output.tif'
        data = gdal.Open(path)
        scn  = data.ReadAsArray()
        shp5[:,:,d] = scn
    if d >= 6:
        path = pathall + str(yr) + '_LS8_output.tif' 
        scn  = gdal.Open(path).ReadAsArray()
        shp5[:,:,d] = scn
#    plt.imshow(shp5[:,:,d])
#    plt.savefig((output + str(yr) + '.png' ))

for d, yr in enumerate(yearlist):
    if d <= 5:
        path = pathall + str(yr) + '_LS7_output.tif'
        data = gdal.Open(path)
        scn  = data.ReadAsArray()
        shp7[:,:,d] = scn
    if d >= 6:
        path = pathall + str(yr) + '_LS8_output.tif' 
        scn  = gdal.Open(path).ReadAsArray()
        shp7[:,:,d] = scn
#    plt.imshow(shp7[:,:,d])
#    plt.savefig((output + str(yr) + '.png' ))

mask = (shp7[:,:,1] == 0)
shp5_n = shp5.copy()
shp7_n = shp7.copy()

    ### FILL THE ZERO GAPS FOR LANDSAT 5 ###

col     = 0
row     = 0
counter = 0
weights = np.array([5,10,30,100,31,10,5])
counter = 0       
for row in range(912):
    print str(row*100/912), '%'
    for col in range(1929):
        if mask[row,col] == False:            
            pixel = shp5[row,col,:]
            before = pixel.tolist()
            if np.count_nonzero(pixel) >= ((np.shape(pixel)[0])/2):            
                for index, item in enumerate(pixel):
                    if (pixel[index] == 0) == True:
                        
                        spotted = int(index)            
                        spotmax = spotted+4
                        spotmin = spotted-3
                        pattern = pixel[spotmin:spotmax]
                        if spotmax == 14:
                            spotmax = 11 
                            zeroadded = [0,0,0]
                            pattern = np.append(pixel[spotmin:spotmax],zeroadded) 
                        if spotmax == 13:
                            spotmax = 11
                            zeroadded = [0,0]
                            pattern = np.append(pixel[spotmin:spotmax],zeroadded) 
                        if spotmax == 12:
                            spotmax = 11
                            zeroadded = [0]
                            pattern = np.append(pixel[spotmin:spotmax],zeroadded) 
                        if spotmin < -2:
                            spotmin = spotmin+3
                            zeroadded = [0,0,0]
                            pattern = np.append(zeroadded,pixel[spotmin:spotmax])                        
                        if spotmin < -1:
                            spotmin = spotmin+2
                            zeroadded = [0,0]
                            pattern = np.append(zeroadded,pixel[spotmin:spotmax])
                        if spotmin < 0:
                            spotmin = spotmin+1
                            zeroadded = [0]
                            pattern = np.append(zeroadded,pixel[spotmin:spotmax])                                                                                            
                        zeromask = pattern == 0
                        score = np.zeros(5)
                        for posr,ir in enumerate(range(1,6)):
                            for post in range(0,7):
                                if pattern[post] == ir:
                                    score[posr] = score[posr] + weights[post]
                        filler = (np.argmax(score) + 1)
                        pixel[spotted] = round(filler)
                        after = pixel.tolist()                
            shp5_n[row,col] = pixel

print "GAPS FILLED FOR L5"

    ### FILL THE ZERO GAPS FOR LANDSAT 7 ###

col     = 0
row     = 0
counter = 0
weights = np.array([5,10,30,100,31,10,5])
counter = 0       
for row in range(912):
    print str(row*100/912), '%'
    for col in range(1929):
        if mask[row,col] == False:            
            pixel = shp7[row,col,:]
            before = pixel.tolist()
            if np.count_nonzero(pixel) >= ((np.shape(pixel)[0])/2):            
                for index, item in enumerate(pixel):
                    if (pixel[index] == 0) == True:
                        
                        spotted = int(index)            
                        spotmax = spotted+4
                        spotmin = spotted-3
                        pattern = pixel[spotmin:spotmax]
                        if spotmax == 14:
                            spotmax = 11 
                            zeroadded = [0,0,0]
                            pattern = np.append(pixel[spotmin:spotmax],zeroadded) 
                        if spotmax == 13:
                            spotmax = 11
                            zeroadded = [0,0]
                            pattern = np.append(pixel[spotmin:spotmax],zeroadded) 
                        if spotmax == 12:
                            spotmax = 11
                            zeroadded = [0]
                            pattern = np.append(pixel[spotmin:spotmax],zeroadded) 
                        if spotmin < -2:
                            spotmin = spotmin+3
                            zeroadded = [0,0,0]
                            pattern = np.append(zeroadded,pixel[spotmin:spotmax])                        
                        if spotmin < -1:
                            spotmin = spotmin+2
                            zeroadded = [0,0]
                            pattern = np.append(zeroadded,pixel[spotmin:spotmax])
                        if spotmin < 0:
                            spotmin = spotmin+1
                            zeroadded = [0]
                            pattern = np.append(zeroadded,pixel[spotmin:spotmax])                                                                                            
                        zeromask = pattern == 0
                        score = np.zeros(5)
                        for posr,ir in enumerate(range(1,6)):
                            for post in range(0,7):
                                if pattern[post] == ir:
                                    score[posr] = score[posr] + weights[post]
                        filler = (np.argmax(score) + 1)
                        pixel[spotted] = round(filler)
                        after = pixel.tolist()                        
            shp7_n[row,col] = pixel

print "GAPS FILLED FOR L7"

overview = []

shp5  = np.zeros((912, 1929,11)) 
shp7  = np.zeros((912, 1929,11))
for d, yr in enumerate(yearlist):
    if d <= 5:
        path = pathall + str(yr) + '_LS5_output.tif'
        data = gdal.Open(path)
        scn  = data.ReadAsArray()
        shp5[:,:,d] = scn
    if d >= 6:
        path = pathall + str(yr) + '_LS8_output.tif' 
        scn  = gdal.Open(path).ReadAsArray()
        shp5[:,:,d] = scn
#    plt.imshow(shp5[:,:,d])
#    plt.savefig((output + str(yr) + '.png' ))

for d, yr in enumerate(yearlist):
    if d <= 5:
        path = pathall + str(yr) + '_LS7_output.tif'
        data = gdal.Open(path)
        scn  = data.ReadAsArray()
        shp7[:,:,d] = scn
    if d >= 6:
        path = pathall + str(yr) + '_LS8_output.tif' 
        scn  = gdal.Open(path).ReadAsArray()
        shp7[:,:,d] = scn

for d, yr in enumerate(yearlist):
    overview.append((yr, (np.unique(shp7[:,:,d], return_counts=True)[1][0] - np.unique(shp7_n[:,:,d], return_counts=True)[1][0]), 0))
            
col     = 0
row     = 0
counter = 0
weights = np.array([5,10,30,1,31,10,5])
counter = 0
mask = (shp7[:,:,1] == 0)
shp7_da = shp7_n.copy()

    ### COMBINE 
 
### FINDING 1 year SEQUENCES ####

for seq in range(3):
    for row in range(912):
    #    print str((row/912)*100), '%' 
        for col in range(1929):
            if mask[row,col] == False:            
                pixel5 = shp5_n[row,col,:]
                pixel7 = shp7_n[row,col,:]
        #            for index, item in enumerate(pixel):
                index1 = -1
                for index, (key, item) in enumerate(groupby(pixel7)):
                    item = list(item)
                    index1 = index1 + len(item)
                    if key == 4:
                        if len(item)== 1:
                            
                            if 9 > index1 > 0:
                                spotted = int(index1)            
                                spotmax = spotted+4
                                spotmin = spotted-3
                                before  = pixel7.tolist()
                                pattern7 = pixel7[spotmin:spotmax]
                                sc5 = 0
                                if spotmax == 14:
                                    spotmax = 11 
                                    zeroadded = [0,0,0]
                                    pattern7 = np.append(pixel7[spotmin:spotmax],zeroadded) 
                                if spotmax == 13:
                                    spotmax = 11
                                    zeroadded = [0,0]
                                    pattern7 = np.append(pixel7[spotmin:spotmax],zeroadded) 
                                if spotmax == 12:
                                    spotmax = 11
                                    zeroadded = [0]
                                    pattern7 = np.append(pixel7[spotmin:spotmax],zeroadded)
                                if spotmin < -2:
                                    spotmin = spotmin+3
                                    zeroadded = [0,0,0]
                                    pattern7 = np.append(zeroadded,pixel7[spotmin:spotmax])                        
                                if spotmin < -1:
                                    spotmin = spotmin+2
                                    zeroadded = [0,0]
                                    pattern7 = np.append(zeroadded,pixel7[spotmin:spotmax])
                                if spotmin < 0:
                                    spotmin = spotmin+1
                                    zeroadded = [0]
                                    pattern7 = np.append(zeroadded,pixel7[spotmin:spotmax])                                                                                            
                                zeromask = pattern7 == 0
                                score = np.zeros(5)
                                for posr,ir in enumerate(range(1,6)):
                                    for post in range(0,7):
                                        if pattern7[post] == ir:
                                            score[posr] = score[posr] + weights[post]
                                if  spotted <= 5:
                                    sc5 = int(pixel5[spotted]-1)
                                    sc5min = int(pixel5[spotted-1]-1)
                                    sc5max = int(pixel5[spotted+1]-1)
                                    score[sc5]  = score[sc5] + 40
                                    score[sc5min]  = score[sc5min] + 10
                                    score[sc5max]  = score[sc5max] + 10
                                score[3] = score[3]-6
                                filler = (np.argmax(score) + 1)
        #                            print "Yr: ", yearlist[spotted], "L7: ", pattern7, ", L5: ", [pixel5[spotted-1],pixel5[spotted],pixel5[spotted+1]], ", Fill: ",  filler, ", R/C:", row, col                            
                                pixel7[spotted] = round(filler)
                                counter = counter + 1
                                shp7_da[row,col,:] = pixel7
                                after = pixel7.tolist()

for seq in range(3):
    for row in range(912):
    #    print str((row/912)*100), '%' 
        for col in range(1929):
            if mask[row,col] == False:            
                pixel5 = shp5_n[row,col,:]
                pixel7 = shp7_n[row,col,:]
        #            for index, item in enumerate(pixel):
                index1 = -1
                for index, (key, item) in enumerate(groupby(pixel7)):
                    item = list(item)
                    index1 = index1 + len(item)
                    if key == 1:
                        if len(item)== 1:
                            
                            if 9 > index1 > 0:
                                spotted = int(index1)            
                                spotmax = spotted+4
                                spotmin = spotted-3
                                before  = pixel7.tolist()
                                pattern7 = pixel7[spotmin:spotmax]
                                sc5 = 0
                                if spotmax == 14:
                                    spotmax = 11 
                                    zeroadded = [0,0,0]
                                    pattern7 = np.append(pixel7[spotmin:spotmax],zeroadded) 
                                if spotmax == 13:
                                    spotmax = 11
                                    zeroadded = [0,0]
                                    pattern7 = np.append(pixel7[spotmin:spotmax],zeroadded) 
                                if spotmax == 12:
                                    spotmax = 11
                                    zeroadded = [0]
                                    pattern7 = np.append(pixel7[spotmin:spotmax],zeroadded)
                                if spotmin < -2:
                                    spotmin = spotmin+3
                                    zeroadded = [0,0,0]
                                    pattern7 = np.append(zeroadded,pixel7[spotmin:spotmax])                        
                                if spotmin < -1:
                                    spotmin = spotmin+2
                                    zeroadded = [0,0]
                                    pattern7 = np.append(zeroadded,pixel7[spotmin:spotmax])
                                if spotmin < 0:
                                    spotmin = spotmin+1
                                    zeroadded = [0]
                                    pattern7 = np.append(zeroadded,pixel7[spotmin:spotmax])                                                                                            
                                zeromask = pattern7 == 0
                                score = np.zeros(5)
                                for posr,ir in enumerate(range(1,6)):
                                    for post in range(0,7):
                                        if pattern7[post] == ir:
                                            score[posr] = score[posr] + weights[post]
                                if  spotted <= 5:
                                    sc5 = int(pixel5[spotted]-1)
                                    sc5min = int(pixel5[spotted-1]-1)
                                    sc5max = int(pixel5[spotted+1]-1)
                                    score[sc5]  = score[sc5] + 40
                                    score[sc5min]  = score[sc5min] + 10
                                    score[sc5max]  = score[sc5max] + 10
                                score[3] = score[3]-6
                                filler = (np.argmax(score) + 1)
        #                            print "Yr: ", yearlist[spotted], "L7: ", pattern7, ", L5: ", [pixel5[spotted-1],pixel5[spotted],pixel5[spotted+1]], ", Fill: ",  filler, ", R/C:", row, col                            
                                pixel7[spotted] = round(filler)
                                counter = counter + 1
                                shp7_da[row,col,:] = pixel7
                                after = pixel7.tolist()
                                
for d, yr in enumerate(yearlist):
    op = list(overview[d])
    op[2] = (np.unique(shp7_n[:,:,d], return_counts=True)[1][1] - np.unique(shp7_da[:,:,d], return_counts=True)[1][1]) + (np.unique(shp7_n[:,:,d], return_counts=True)[1][5] - np.unique(shp7_da[:,:,d], return_counts=True)[1][5])
    overview[d] = tuple(op)
    
combine = shp7_da == 5
shp7_da[combine] = 4

##SAVE TO QUICKPLOT AND TIFF
d = 0
yr = 0
for d, yr in enumerate(yearlist):
    plt.imshow(shp7_da[:,:,d])
    plt.savefig((output + str(yr) + '-datafuse.png' )) 
    filename = str(yr)
    if d <= 5:
        path = pathall + str(yr) + '_LS7_output.tif'
        data = gdal.Open(path)
        scn  = data.ReadAsArray()
    if d >= 6:
        path = pathall + str(yr) + '_LS8_output.tif' 
        data = gdal.Open(path)
        scn  = data.ReadAsArray()    
    [cols,rows] = scn.shape
    trans       = data.GetGeoTransform()
    proj        = data.GetProjection()
#    nodatav     = data.GetNoDataValue()
    outfile     = str(yr) + '-nogapsda7.tif'
    # Create the file, using the information from the original file
    outdriver = gdal.GetDriverByName('GTiff')
    outdata   = outdriver.Create(str(outgeo + outfile), rows, cols, 1, gdal.GDT_Float32)
    # Georeference the image
    outdata.SetGeoTransform(trans)
    # Write projection information
    outdata.SetProjection(proj)
    # Write the array to the file, which is the original array in this example
    outdata.GetRasterBand(1).WriteArray(shp7_da[:,:,d])
    outdata = 0 

with open(log + 'overview.txt', 'wb') as myfile:
    wr = csv.writer(myfile, delimiter="\n")
    wr.writerow(overview)
