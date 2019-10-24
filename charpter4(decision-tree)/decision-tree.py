#********************决策树***************************
#by 大白菜
#新建:2019/10/11
import math
import json

class DTreeException(Exception):
    def __init__(self,exception_str):
        self.exception_str=exception_str

class DTreeNode:
    def __init__(self,item_index_list,value_index_list,type,value,leaf_node_flag=False,result=None):
        self.value=value    #属性值
        self.type=type     #表示子节点分类按照的属性名索引
        self.children_dict = None   #表示子节点的属性值（key）对应的字节点对象（value）
        self.leaf_node_flag=leaf_node_flag  #是否是叶子节点
        self.item_index_list=item_index_list   #包含的样本的index
        self.value_index_list=value_index_list  #包含的样本的属性种类表index
        self.result=result    #当为叶子节点时设置的最终结果属性值 叶子节点为True时生效
    def reset_children_dict(self,c_dict):
        self.children_dict=c_dict
class DecisionTree:
    def __init__(self,e_data,
                 value_type=None,
                 P=None,                   #自定义的P集合
                 complete_value_flag=False,
                 cut_leaf_flag=None,
                 alog_type=0
                 ):
        self.head=None
        self.e_data=e_data   #训练集   二维列表
        self.complete_value_flag=complete_value_flag   #缺失值标志
        self.cut_leaf_flag=cut_leaf_flag  #None first last
        self.alog_type=alog_type #0---增益算法  1---增益率算法  2---基尼算法
        self.value_type=value_type    #属性名称
        self.P=P    #默认的P为None则从训练集中统计得出P集合
        #预处理数据：
        item_length = len(self.e_data[0])
        for i in range(1,len(self.e_data)):
            if len(self.e_data[i])!=item_length:
                raise DTreeException("训练集样本属性长度不一致 第一次发现在第"+str(i+1)+"项样本")
        if self.value_type==None:
            self.value_index_list=[]
            for i in range(item_length-1):  #不包括最后一项的分类集合
                self.value_index_list.append(i)
        if self.P==None:   #填充P集合
            self.P=[]
            for i in e_data:
                if i[-1] not in self.P:
                    self.P.append(i[-1])
        elif type(self.P)!="list":
            raise DTreeException("输入P集合必须是list类型")

    #初始化head节点
        item_index_list=[]
        value_index_list=[]
        for i in range(len(self.e_data)):
            item_index_list.append(i)
        for i in range(item_length-1):
            value_index_list.append(i)
        self.head=DTreeNode(item_index_list,value_index_list,None,None)
    def run(self):
        if self.alog_type==0:
            self._run_type0()
        elif self.alog_type==1:
            self._run_type1()
        elif self.alog_type==2:
            self._run_type2()
        elif self.alog_type==3:
            self._run_type3()
        else:
            raise DTreeException("不符合规范的算法选择")
    def _run_type0(self):#信息增益
        self._run0_helper(self.head)
    def _run0_helper(self,node):
        d_index_list=node.item_index_list
        v_index_list=node.value_index_list
        if d_index_list==[]:
            print("空数据index表")
            return 0
        common_type_flag=True
        temp1=self.e_data[d_index_list[0]][-1]
        for i in d_index_list:
            if self.e_data[i][-1]!=temp1:
                common_type_flag=False
                break
            else:
                temp1=self.e_data[i][-1]


        if common_type_flag:
            node.leaf_node_flag=True
            node.result=temp1
            print("相同种类"+str(temp1))
            return 0
        same_v_flag=True


        for i in v_index_list:
            temp2=self.e_data[0][i]
            for j in d_index_list:
                if self.e_data[j][i]!=temp2:
                    same_v_flag=False
                    break
                else:
                    temp2=self.e_data[j][i]
        if v_index_list==[] or same_v_flag:
            print("相同属性的数据或空的属性表")
            node.leaf_node_flag=True
            count_list=self.count(d_index_list)
            max_index=0
            for i in range(len(count_list)):
                if count_list[i]>count_list[max_index]:
                    max_index=i
            node.result=self.P[max_index]
            print("种类"+str(node.result))
            return 0
        #常规情况：
        print("普通情况")
        max_gain=0
        direct_v_index=0
        for v_index in v_index_list:
            temp3=self.gain(d_index_list,v_index)
            if temp3>max_gain:
                max_gain=temp3
                direct_v_index=v_index
        #生成分配节点的方案
        temp_dict={}
        for i in d_index_list:
            direct_value=self.e_data[i][direct_v_index]
            if direct_value not in temp_dict:
                temp_dict[direct_value]=[i]
            else:
                temp_dict[direct_value].append(i)
        #向node添加子节点表
        node_children_dict={}
        v_index_list.pop(direct_v_index)

        for i in temp_dict:
            # node必须传入参数：item_index_list,value_index_list,type,value
            node_children_dict[i]=DTreeNode(
                temp_dict[i],
                v_index_list,
                direct_v_index,
                i
            )
        node.reset_children_dict(node_children_dict)

        for i in node_children_dict:
            self._run0_helper(node_children_dict[i])

    def gain(self,d_index_list,v_index):   #按照v_index分划  ---kern_fun---
        temp_dict={}
        for i in d_index_list:
            direct_value=self.e_data[i][v_index]
            if direct_value not in temp_dict:
                temp_dict[direct_value]=[i]
            else:
                temp_dict[direct_value].append(i)

        #生成dict结构： v_index号属性属性值 ：含有此属性值的item索引
        D_length=len(d_index_list)
        sum1=0
        for i in temp_dict:
            Dv=temp_dict[i]
            Dv_length=len(Dv)
            sum1+=((Dv_length/D_length)*self.ent(Dv))
        return self.ent(d_index_list)-sum1

    def ent(self,d_index_list):  #纯度函数 ---kern_func---
        temp_dict={}
        temp_list=[]
        sum=0
        for i in d_index_list:
            if self.e_data[i][-1] not in temp_dict:
                temp_dict[self.e_data[i][-1]]=1
            else:
                temp_dict[self.e_data[i][-1]]+=1
        for k in temp_dict:
            temp_list.append(temp_dict[k])
        count_sum=0
        for m in temp_list:
            count_sum+=m
        for n in temp_list:
            rank_p=n/count_sum
            sum+=rank_p*math.log(rank_p,2)
        return -sum

    def count(self,d_index_list):
        result_list=[]
        p_lenth=len(self.P)

        for i in range(p_lenth):
            result_list.append(0)
        for k in d_index_list:
            for i in range(p_lenth):
                if self.P[i]==self.e_data[k][-1]:
                    result_list[i]+=1
        return result_list
    def _run_type1(self):#信息增益率
        pass
    def _run_type2(self):#基尼系数
        pass
    def _run_type3(self):#缺失+信息增益
        pass
    def _run_type4(self):#离散+信息增益
        pass
    def get_model(self):
        return self.head

    def reserve_model(self):
        pass

    def load_model(self):
        pass

    def last_cut_leaf(self):   #后修剪枝叶
        pass

    def work(self):
        pass

if __name__=="__main__":
    DecisionTree([[1,2,3],[1,2,3],[1,2,3],[1,4,4]]).run()