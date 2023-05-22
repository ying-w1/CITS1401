def main(csvfile, adultID, Option):
    
    # Clean up input parameters to align with the code - ensure capitalisation/lower case and correct type (String)
    adultID = str(adultID.capitalize())
    Option = str(Option.lower())
    csvfile = str(csvfile)

    # Process the input document into a new list rawData before cleanng up rawData into the final list data_list
    # This is done so every index of the final list is a single tuple
    rawData,data_list = [],[]
    with open(csvfile, "r") as filein: 
        for line in filein:
            linelist = line.split(",")
            rawData.append(linelist[0])
            rawData.append(linelist[1].upper())
            rawData.append(linelist[2])
            rawData.append(linelist[3])
            LDis = linelist[4]
            rawData.append(LDis[:-1])
    
    inc = 5
    for i in range(len(rawData)):
        data_list.append(rawData[inc:inc+5])
        inc += 5
    
    
    # Convert distance into integer and Gdis and Ldis into floats
    datalen = int(len(data_list)/5-1)
    
    for i in range(datalen):
        data_list[i][2] = int(data_list[i][2])
        data_list[i][3] = float(data_list[i][3])
        data_list[i][4] = float(data_list[i][4])
        
    data_list = [ele for ele in data_list if ele != []]
    
    data_list.sort()

    # If distance in the datafile is less than or equal to 0 then we are replacing the distance with 50
    for i in range(datalen):
        if data_list[i][3] <= 0:
            data_list[i][3] = 50
        if data_list[i][4] <= 0:
            data_list[i][4] = 50
    # Set up repetitive variables - expressions and adultIDs in the datafile
    # Assumption: these are the only expressions in every data file and in this order 
    expressions = ["Neutral", "Angry", "Disgust", "Happy"]

    # Create a list of all the adultIDs (no duplicates)
    uniqueAdultID = []
    allAdID = []
    for i in range(datalen):
        allAdID.append(data_list[i][0])
    [uniqueAdultID.append(x) for x in allAdID if x not in uniqueAdultID]
    
    # The following are functions when the option entered into the parameter is 'stat'
    def option_statOP1(adultID,dist):
        # Interate through the data_list and find the first index where the adultID appears for a given distance
        def find_index():
            adIndex = 0
            for i in range(datalen):
                if data_list[i][0] == adultID and data_list[i][2] == dist:
                    adIndex = i
            return adIndex
        
        # Return the minimum and maximum Gdis and Ldis for the each of the distances for the adultID we are interested in.
        # This will serve as a starting point to find the min and max of each distance
        minGDI = data_list[find_index()][3]
        maxGDI = data_list[find_index()][3]
        minLDI = data_list[find_index()][4]
        maxLDI = data_list[find_index()][4]
        
        # Iterate through the list and find the min and max of GDIS and LDIS for a given distance
        # Then add the mins and max into the list 'result'
        for i in range(datalen):
            if data_list[i][0] == adultID and data_list[i][2] == dist and data_list[i][3] < minGDI:
                minGDI = data_list[i][3]
            if data_list[i][0] == adultID and data_list[i][2] == dist and (data_list[i][3] > maxGDI):
                maxGDI = data_list[i][3]
            if data_list[i][0] == adultID and data_list[i][2] == dist and data_list[i][4] < minLDI:
                minLDI = data_list[i][4]
            if data_list[i][0] == adultID and data_list[i][2] == dist and (data_list[i][4] > maxLDI):
                maxLDI = data_list[i][4]
        
        result = []
        result.append(round(minGDI,4))
        result.append(round(maxGDI,4))
        result.append(round(minLDI,4))
        result.append(round(maxLDI,4))
        return result
    
    def option_statOP2(adultID, exp):
        # For the adultID and each expression of the adultID, deduct the GDIS from the LDis to find the difference
        # Append the result to a the list 'result'
        result = []
        diff = 0
        for i in range(datalen):
            if data_list[i][0] == adultID and data_list[i][1] == exp:
                diff = round(data_list[i][3] - data_list[i][4],4)
                result.append(diff)
        return result
    
    def option_statOP3(adultID, dist):
        
        geoSum = 0
        average = 0
        for i in range(datalen):
            if data_list[i][0] == adultID and data_list[i][2] == dist:
                geoSum += data_list[i][3]
        
        average = round(geoSum/len(expressions),4)
        return average
    
    def option_statOP4(adultID, dist):
        eucSum = 0
        sumData = 0
        dataMean = 0
        
        for i in range(datalen):
            if data_list[i][0] == adultID and data_list[i][2] == dist:
                sumData += data_list[i][4]
        dataMean = sumData/len(expressions)
        
        for i in range(datalen):
            if data_list[i][0] == adultID and data_list[i][2] == dist:
                eucSum += (data_list[i][4] - dataMean)**2
                
        result = round(((eucSum/len(expressions))**0.5),4)
        return result        
    
    # The following are functions when the option entered into the parameter is 'FR'
    # Produce a list of the GDIS for a given adultID
    def find_gdis(adultID, exp):
        gdis = []
        for i in range(datalen):
            if data_list[i][0] == adultID and data_list[i][1] == exp:
                gdis.append(data_list[i][3])
        return gdis
    
    # Calculate the cosine and returns a list with the cosine similarity value 
    def calc_cosine():
        testGDIS = ""
        refGDIS = find_gdis(adultID, "Neutral") # gdis of the referenace face (adultID in parameter)
        list = []
        
        # Calculate cosine value between refGDIS and other expression of the same reference adultID
        # Appends the ID of the adult we are calculating and the cosine value into the list 'list'
        for exp in expressions:
            if exp != "Neutral":
                testGDIS = find_gdis(adultID, exp)
                list.append(adultID)
                top,bottom1,bottom2,cosine = 0,0,0,0
                for i in range(8):
                    top += testGDIS[i]*refGDIS[i]
                    bottom1 += testGDIS[i]*testGDIS[i]
                    bottom2 += refGDIS[i]*refGDIS[i]
                cosine = round(top/((bottom1**0.5)*(bottom2**0.5)),4)
                list.append(cosine)        
        
        # Calculate cosine value between refGDIS and other adults of the 'Neutral' expressions
        # Appends the ID of the adult we are calculating and the cosine value into the list 'list'
        for adult in uniqueAdultID:
            if adult != adultID:
                testGDIS = find_gdis(adult, "Neutral")
                list.append(adult)
                top,bottom1,bottom2,cosine = 0,0,0,0
                for i in range(8):
                    top += testGDIS[i]*refGDIS[i]
                    bottom1 += testGDIS[i]*testGDIS[i]
                    bottom2 += refGDIS[i]*refGDIS[i]
                cosine = round(top/((bottom1**0.5)*(bottom2**0.5)),4)
                list.append(cosine)
            
        return list    
    
    # If the 'Option' entered the parameter is 'stat' the functions option_statOP1 to option_statOP4 will be executed 
    if Option == "stats":
        OP1, OP2, OP3, OP4 = [], [], [], []
        for i in range(1,9):
            OP1.append(option_statOP1(adultID, i))
            OP3.append(option_statOP3(adultID, i))
            OP4.append(option_statOP4(adultID, i))
        for exp in expressions:    
            OP2.append(option_statOP2(adultID, exp))
    
        return OP1, OP2, OP3, OP4
    # If the 'Option' entered the parameter is 'FR' the function calc_cosine() will be executed
    # The calc_cosine() provides a list as such: [AdultID, cosine value] for the various adult IDs and expressions
    # Only the [cosine value] if this list will be extracted into cosineList[] then using max() to find the largest casine value i.e greatest similarity to the reference adult
    # Indexing is used to return the adultID to the corrresponding max() cosine value
    elif Option == "fr":
        cosineList = []
        maxSimilarity = 0
        ID = ""
        inc = 1
        
        while inc < len(calc_cosine()):
            cosineList.append(calc_cosine()[inc])
            inc += 2
            
        maxSimilarity = max(cosineList)
        index1 = calc_cosine().index(maxSimilarity)
        index2 = index1 - 1
        ID = calc_cosine()[index2]
        
        return ID, maxSimilarity
        
