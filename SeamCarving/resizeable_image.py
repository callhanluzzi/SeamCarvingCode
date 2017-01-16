# Callhan Luzzi
# Professor Daniels
# CSC 440
# November 11th, 2016

import imagematrix
import copy

class ResizeableImage(imagematrix.ImageMatrix):

    # energy  for each x,y in image
    energyLookup = {}
    # set lowest energy, will change after first loop of dfs
    lowestEng = 999999
    # lowest path for dfs
    lowestPath = []

    # depth first search function for naive approach 
    def dfs(self,i,j,diction,path,energy):
        # append i,j (x,y) to the path
        path.append((i,j))
        # if we have reached the bottom index
        if(j == self.height-1):
            # check to see if our current energy is less than the lowestEnergy
            if energy < self.lowestEng:
                # set lowestEnergy to energy
                self.lowestEng = energy
                # set lowestPath to path
                self.lowestPath = path
                return          
        else:
            # set the branches to the neighbors of i,j
            branches = diction[i,j]

            # for each neighbor in branches
            for q in branches:
                # add the energy from that branch to the total energy
                energy+=self.energyLookup[(i,j)]
                # recursively call dfs
                self.dfs(q[0],q[1],diction,copy.copy(path),energy)
        return
    
    def best_seam(self, dp=True):

        # set h and w to height and width
        h = self.height
        w = self.width

        # create a tempList to help append to energy table
        tempList = []
        energyTable = []
        
        memo = {}
        seam = []

        # for each x and y get the energy and add it to the energyTable array
        for g in range(0,h): 
            tempList = []
            k = 0
            for k in range(0,w):
                temp = self.energy(k,g)
                tempList.append(temp)
            energyTable.append(tempList)

        if(dp == False):
            # dictionary for all neighbors of each x and y
            neighbors = {}

            # for each x and y, add to the dict their 2, or 3 below neighbors
            for g in range(0,w): 
                k = 0
                for k in range(0,h):
                    temp = self.energy(g,k)
                    # if x is on left edge, only has two neighbors
                    if(g == 0):
                        neighbors[(g,k)] = ((g,k+1),(g+1,k+1))
                    # if x is on right edge, only has two neighbors
                    elif(g == w-1):
                        neighbors[(g,k)] = ((g-1,k+1),(g,k+1))
                    # if x is anywhere else, it has 3 below neighbors
                    else:
                        neighbors[(g,k)] = ((g-1,k+1),(g,k+1),(g+1,k+1))

                    # add the energy for x,y to the energyLookup table
                    self.energyLookup[(g,k)] = temp

            # for each i in the first row, call dfs
            for i in range(0,w):
                self.dfs(i,0,neighbors,[],0)

            # return the lowest path
            return(self.lowestPath)


        if(dp == True):

            # minimum x, y
            minXY = (0,0)

            # j in energy table represents y, for j in y
            for j in range(1,len(energyTable)):
                i = 0
                # i in energytable[0] is the list of energys x at row y
                for i in range(len(energyTable[0])):

                    # start with row 1, index 0. (1,0)
                    startNode = energyTable[j][i]
                    
                    # If we are at first pixel
                    if(i == 0):
                        above = energyTable[j-1][i]
                        aboveRight = energyTable[j-1][i+1]
                        # to ensure belowLeft cant be selected since a belowLeft does not exist for left most pixels
                        aboveLeft = 999999
                        
                    # If we are at last pixel           
                    elif(i == len(energyTable[0])-1):
                        # set above, aboveLeft, and aboveRight to the pixels in those locations relative to x,y
                        above = energyTable[j-1][i]
                        aboveLeft = energyTable[j-1][i-1]
                        # to ensure belowRight cant be selected since a belowRight does not exist for rigth most pixels
                        aboveRight = 999999

                    # If we are at any other pixel           
                    else:
                        above = energyTable[j-1][i]
                        aboveRight = energyTable[j-1][i+1]
                        aboveLeft = energyTable[j-1][i-1]

                    # if we select the above left pixel (it has lowest energy)
                    if(startNode + aboveLeft < startNode + aboveRight and startNode + aboveLeft < startNode + above):
                        # add the energy of the selected node to the totalenergy
                        energy = startNode + aboveLeft
                        # set in the memo table, the x, y we are at, the x and y we chose, and the total energy of the two
                        memo[(i,j)] = ((i-1,j-1),(energy))
                        
                    # if we select the above right pixel (it has lowest energy)
                    elif(startNode + aboveRight < startNode + above and startNode + aboveRight < startNode + aboveLeft):
                        energy = startNode + aboveRight
                        memo[(i,j)] = ((i+1,j-1),(energy))
                        
                    # if we select the directly above pixel (it has lowest energy)
                    else:   
                        energy = startNode + above
                        memo[(i,j)] = ((i,j-1),(energy))

                    # add into the table of energys, at row j, index i, the updated energy
                    energyTable[j][i] = energy


            # search through energytable for lowest seam
            for q in range(len(energyTable[0])):
                # set temp to 50000 if you are on the first index to ensure our eng of index is less than temp
                if(q == 0):
                    temp = 50000

                # grab the energy from the index starting at the bottom of the image
                eng = memo[q,h-1][1]

                # if eng < temp set finalEng to eng, update temp, update minXY
                if(eng < temp):
                    finalEng = eng
                    temp = finalEng
                    minXY = (q,h-1)
                    
            # add the first XY to our seam path
            seam.append(minXY)

            # append the remaining minXY's to our seam path
            for u in range(h-1):
                minXY = memo[minXY][0]
                seam.append(minXY)

        # reverse the seam so that it is in the correct order
        seam.reverse()
                       
        return seam


        

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())



    
