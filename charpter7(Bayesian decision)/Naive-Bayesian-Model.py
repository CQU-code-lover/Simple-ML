#朴素贝叶斯
#by 大白菜
#2019/10/24

import math
import numpy

class NbmException(Exception):
    def __init__(self,erro_str):
        self.erro_value=erro_str

class NaiveBayesianModel():
    def __init__(self,data_list,label_list=None,last_item_is_label_flag=True,debug=False):
        self.e_data=data_list
        self.data_length = len(self.e_data)
        self.property_length=None
        self.label_list=label_list
        self.last_item_is_label_flag=last_item_is_label_flag
        self.debug_flag=debug
        self.discrete_list=[]    #离散型表
        self.init_data()
        self.unique_label_list=[]
        self.property_list=[]    #二维表 list[i]对应第i个属性的可能取值
        self.three_d_property=[]   #3维属性对应表 对应label_list中不同的分类情况
        self.have_model_flag=False
    def init_data(self):
        #检查训练集
        try:
            temp1=len(self.e_data[0])
        except:
            raise NbmException("不合法的训练集")
        self.property_length=len(temp1)
        for i in temp1:
            if type(i)=="str":
                self.discrete_list.append(True)
            else:
                self.discrete_list.append(False)
        for i in self.e_data:
            try:
                if len(i)!=self.property_length:
                    raise NbmException("不合法的训练集")
                else:
                    pass
            except:
                NbmException("不合法的训练集")
        #检查样本标签
        if self.last_item_is_label_flag and self.label_list==None:
            self.label_list=[]
            for i in self.e_data:
                self.label_list.append(i.pop())
            if len(self.e_data[0])==0:
                raise NbmException("训练集除去label后属性为空")
        elif (not self.last_item_is_label_flag) and self.label_list==None:
            raise NbmException("不将数据集最后一个作为label时 label_list必须输入")
        elif self.last_item_is_label_flag and self.label_list!=None:
            raise NbmException("不能同时将最后一位设为label且输入自定义label")
        else:
            pass
        if len(self.e_data)!=len(self.label_list):
            raise NbmException("label表长与 训练集长度不一致")

        #生成去重后的label_list-------->unique_label_list
        self.unique_label_list=self._get_unique_list(self.label_list)
        if self.debug_flag:
            print(self.e_data)
            print(self.label_list)
        print("数据集通过检查")
    def _get_unique_list(self,input_list):
        re_list=[]
        for i in input_list:
            if i not in re_list:
                re_list.append(i)
        return re_list

    def exercise_model(self):   #生成模型
        #填充property_list
        for i in self.property_length:
            inner_list=[]
            if self.discrete_list[i]==False:     #当为非离散的数据时
                self.property_list.append(None)
                continue
            for j in self.data_length:
                if self.e_data[j][i] not in inner_list:
                    inner_list.append(self.e_data[j][i])
                else:
                    pass
            self.property_list.append(inner_list)

        #填充3Dproperty   [i][j][k]   分为第i类时第j号数据为property_list[j][k]时的概率（或者叫比例）
        for i in self.unique_label_list:
            two_d_list=[]    #2D表
            data_item_index_list=[]
            for l_index in range(self.label_list):
                if self.label_list[l_index]==i:
                    data_item_index_list.append(l_index)    #e_data的第l_index号元素为此label
                else:
                    pass
            Dc_length=len(data_item_index_list)

            for j in self.property_length:
                if self.discrete_list[j]==True:
                    two_d_list.append(self._count_data_by_property(data_item_index_list,j)/Dc_length)
                else:
                    #存放离散参数的元组
                    two_d_list.append(self._get_N_args(data_item_index_list,j))
            self.three_d_property.append(two_d_list)

        self.have_model_flag=True
    def _get_N_args(self,view_list,i):#view_list:e_data视图的索引表  i:第i号属性
        dis_value_list=[]
        for j in view_list:
            data_item=self.e_data[j]
            dis_value_list.append(data_item[i])
        ave=sum(dis_value_list)/len(dis_value_list)
        arg1=ave
        arg2=0
        for i in input_list:
            arg2+=pow(i-ave,2)
        arg2=pow(arg2,1/2)
        return [arg1,arg2]
    def _count_data_by_property(self,view_list,i):  #view_list:e_data视图的索引表  i:第i号属性
        re_list=[]
        for j in self.property_list[i]:
            counter=0
            for k in view_list:
                if self.e_data[k][i]==j:
                    counter+=1
            re_list.append(counter)
        return re_list

    def _get_P_continuous(self,args_list,x):
        return (1/((pow(2*math.pi,1/2)*args_list[1])))*math.exp(-(pow(x-args_list[0],2)/(2*pow(args_list[1],2))))

    def work(self,properties): #properties是一个输入的属性序列
        if not self.have_model_flag:
            raise NbmException("没有训练好的模型,使用exercise_model训练一个模型或者使用load_model加载一个模型")
        if len(properties)!=self.property_length:
            raise NbmException("properties长度不正确")
        if type(properties)!="list":
            raise NbmException("properties必须是一个list")
        h=[]   #代价函数序列





