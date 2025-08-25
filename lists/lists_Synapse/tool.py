import glob


def write_name():
    # npz文件路径
    files = glob.glob(r'/Users/trids/project/SCUNet-PP/datasets/Synapse/train_npz/*.npz')
    # files = glob.glob(r'/content/datasets/Synapse/train_npz/*.npz')
    # txt文件路径
    # f = open(r'/content/drive/MyDrive/Deep Learning/SCUNet-plusplus/lists/lists_Synapse/train.txt', 'w')
    f = open(r'/Users/trids/project/SCUNet-PP/lists/lists_Synapse/train.txt', 'w')
    # f = open(r'/content/drive/MyDrive/Deep Learning/SCUNet-plusplus/lists/lists_Synapse/test.txt', 'w')
    for i in files:
        name = i.split('\\')[-1]
        name = name[:-4] + '\n'
        f.write(name)

    print("Finished!")


write_name()
