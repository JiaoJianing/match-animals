#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom

rules = []

class Rule:
    def __init__(self):
        self.keys = []
        self.result = ''
        self.ignore = False,
        self.specific = False
        
def resetRules():
    for rule in rules:
        rule.ignore = False
        
def matchKeys(keys, features):
    for key in keys:
        # 一旦有key没匹配到 则认为此次匹配失败
        if (key not in features):
            return False
    return True 
        
def findMatchRule(features):
    for rule in rules:
        # 若之前已匹配到 则此次跳过
        if (rule.ignore == True):
            continue
        # 若features中包含此规则的result 则此次无需匹配 跳过
        if (rule.result in features):
            rule.ignore = True
            continue
        # 若该条规则的所有key都能在features中找到 则认为匹配成功
        matched = matchKeys(rule.keys, features)
        if (matched):
            rule.ignore = True
            printKeyResult(rule.keys, rule.result)
            return rule
    
    printKeyResult(features, 'No Match')
    return None

def matchFeatures(features):
    # 每次开始新的匹配前重置规则库状态
    resetRules()
    matchedRule = findMatchRule(features)
    while (matchedRule != None and matchedRule.specific != True):
        features.add(matchedRule.result)
        # 匹配到新的result 且不为specific 则将其添加到综合数据库
        newFeatureElement = InfoTree.createElement('feature')
        newTextElement = InfoTree.createTextNode(matchedRule.result)
        newFeatureElement.appendChild(newTextElement)
        infoElement.appendChild(newFeatureElement)
        # 继续匹配
        matchedRule = findMatchRule(features)

# 打印匹配信息
def printKeyResult(keys, result):
    printInfo = ''
    for key in keys:
        printInfo += ' ' + key
    printInfo += ' ==> '
    printInfo += result
    print(printInfo)

# 收集所有规则
RuleTree = xml.dom.minidom.parse("./rule_db.xml")
rulesCollection = RuleTree.documentElement
rulesElements = rulesCollection.getElementsByTagName("rule")
for ruleElement in rulesElements:
    keysElements = ruleElement.getElementsByTagName('key')
    rule = Rule()
    for keyElement in keysElements:
        rule.keys.append(keyElement.childNodes[0].data)
    resultElement = ruleElement.getElementsByTagName('result')[0]
    if (resultElement.hasAttribute('specific')):
        rule.specific = True
    rule.result = resultElement.childNodes[0].data
    rules.append(rule)

# 遍历综合数据库 根据features推断result
InfoTree = xml.dom.minidom.parse("./information_db.xml")
infoCollection = InfoTree.documentElement
infosElements = infoCollection.getElementsByTagName("information")
for infoElement in infosElements:
    # 收集该条信息的features
    features = set()
    featuresElements = infoElement.getElementsByTagName('feature')
    for featureElement in featuresElements:
        features.add(featureElement.childNodes[0].data)

    matchFeatures(features)

# 更新综合数据库
infoXmlFile = open('./information_db.xml', 'w', encoding='utf-8')
InfoTree.writexml(infoXmlFile, indent='', encoding = 'utf-8')
infoXmlFile.close()

featureString = input('请输入特征描述: ')
while (featureString != 'end'):
    featureList = featureString.split()
    featureSet = set()
    for feature in featureList:
        featureSet.add(feature)
    matchFeatures(featureSet)
    featureString = input('请输入特征描述: ')


