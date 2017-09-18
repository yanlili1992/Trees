from math import log
import operator
#import treePlotter
#import pickle
import math

def createDataSet():
    dataSet = [[1,1,'yes'],
               [1,1,'yes'],
               [1,0,'no'],
               [0,1,'no'],
               [0,1,'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet,labels

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)#Data的大小N,N行
    labelCount = {}#字典存储 不同类别的个数
    for featVec in dataSet:
        currentLabel = featVec[-1]#每行的最后一个是类别
        if currentLabel not in labelCount.keys():
            labelCount[currentLabel] = 0
        labelCount[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCount:
        prob = float(labelCount[key])/numEntries
        shannonEnt -= prob*math.log(prob,2)
    return shannonEnt
    
def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1: ])
            retDataSet.append(reducedFeatVec)
    return retDataSet
    
def chooseBestFeatureToSplit(dataSet):
    #列数 = len(dataSet[0])
    #行数 = len(dataSet)
    numFeatures = len(dataSet[0]) - 1#最后一列是标签
    baseEntropy = calcShannonEnt(dataSet)#所有数据的信息熵
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):#遍历不同的属性
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:#在第i个属性里，遍历第i个属性所有不同的属性值
            subDataSet = splitDataSet(dataSet,i,value)#划分数据
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob*calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
        return bestFeature
        
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    classCount = sorted(classCount.items(),key=operator.itemgetter(),reverse=True)
    return classCount[0][0]#返回的是字典第一个元素的key,即 类别标签

def createTree(dataSet,labels):
    #myTree是一个字典，key是属性值，val是类别或者是另一个字典
    #如果val是类别标签，则该子节点就是叶子节点
    #如果val是另一个字典，则该节点是一个判断节点
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):#类别完全相同，停止划分
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]#某属性的所有值
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree
        
