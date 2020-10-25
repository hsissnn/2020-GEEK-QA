
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import xlrd
import ast

# 特征数量
character_count = 2


def train():
    print('-------------开始根据训练集特征向量训练模型-----------------')
    file = open("data/train_data_x.txt")
    line = file.readline()
    # 特征向量
    x = []
    # 对应特征向量的值
    y = []
    txt_len = character_count + 1
    while line:
        line = line.replace(' ', '')
        line = line.replace('[', '')
        line = line.replace(']', '')
        split_result = line.split(",")
        x1 = []
        index = 0
        for i in split_result:
            if index >= txt_len - 1:
                y.append(int(i))
            else:
                m = float(i)
                x1.append(m)
            index = index + 1
        x.append(x1)
        line = file.readline()

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.9)
    svc = train_SVC(x_train, y_train)
    file.close()
    print('-------------结束根据训练集特征向量训练模型-----------------')
    return svc


# x表示问题和答案的特征提取向量如 [[0.5, 0.2, 0.8], [0.9, 0.6, 0.1]]
# y表示最终的标签集合如 [1, 0]
def train_Logistic(x, y):
    classifier = LogisticRegression()
    classifier.fit(x, y)
    return classifier


def train_DecisionTreeClassifier(x, y):
    classifier = LogisticRegression()
    classifier.fit(x, y)
    return classifier


def train_SVC(x, y):
    classifier = SVC()
    classifier.fit(x, y)
    return classifier


def precess(classifier):
    print('-------------开始根据训练模型验证测试集数据-----------------')
    file = open("data/test_data_x.txt")
    txt_len = character_count + 3
    line = file.readline()
    work_book = xlrd.open_workbook("data/im_plus_data_test.xlsx")
    fw = open("data/result.txt", "a", encoding='utf-8')  # 利用追加模式,参数从w替换为a即可
    fw.seek(0)
    fw.truncate()
    table_number = work_book.sheets()[0]
    while line:
        line = line.replace(' ', '')
        line = line.replace('[', '')
        line = line.replace(']', '')
        split_result = line.split(",")
        x1 = []
        excel_row = 0
        answer_excel_index = 0
        question_excel_index = 0
        index = 0
        for i in split_result:
            if index == txt_len - 3:
                excel_row = int(i)
            elif index == txt_len - 2:
                answer_excel_index = int(i)
            elif index == txt_len - 1:
                question_excel_index = int(i)
            else:
                m = float(i)
                x1.append(m)
            index = index + 1
        line = file.readline()
        row = table_number.row_values(excel_row-1)
        jarray = ast.literal_eval(row[3])
        if classifier.predict([x1])[0] == 1:
            print("excel 第 " + str(excel_row) + "行 结果:")
            fw.write("excel 第 " + str(excel_row) + "行 结果:\n")
            qs = jarray[question_excel_index]['message']
            ans = jarray[answer_excel_index]['message']
            print("问题:" + qs)
            print("回答:" + ans)
            fw.write("问题:" + qs + "\n")
            fw.write("回答:" + ans + "\n")
    file.close()
    fw.close()
    print('-------------结束根据训练模型验证测试集数据-----------------')


if __name__ == '__main__':
    # cli = train();
    # precess(cli)
    f = open("../data/numbers.txt", "a")  # 利用追加模式,参数从w替换为a即可
    f.seek(0)
    f.truncate()
    f.write("abc\n")
    f.write("add\n")
    f.write("add")
    f.close()
# 如果一个问句, 是是否疑问句的话，去 重复词的影响
# 如果第一个问题在第一个回答中间有问题出现，那边去除距离的影响， 如果最后两个值分数一样，取近的那个
# 如果我们的第一个问题,没有被回答，而是第二个问题被回答了，那么应该取第二个问题的回答集合
# 如果一个
